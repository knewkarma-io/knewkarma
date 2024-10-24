import asyncio
import os
from datetime import datetime
from typing import get_args, Union, Callable, Literal, List, Dict

import aiohttp
import rich_click as click
from rich.status import Status

from ._main import (
    reddit,
    Post,
    Posts,
    Search,
    Subreddit,
    Subreddits,
    User,
    Users,
)
from .meta.about import Project
from .meta.license import License
from .meta.version import Version
from .utils.general import General
from .utils.package import Package
from .utils.terminal import console, Message, Style

__all__ = ["start"]

package = Package(
    name=Project.package, version=Version, requester=reddit.connection.send_request
)


def help_callback(ctx: click.Context, option: click.Option, value: bool):
    """
    Custom callback function for handling the '--help' option in Click commands.

    Additionally, if the application is running as a Snap package, the
    function will pause execution, prompting the user to press any key
    before continuing. This is useful for when the user clicks the Knew Karma icon in application menu.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param option: The Click option that triggered this callback.
    :type option: click.Option
    :param value: The value of the custom help option. If True, the help
            message is displayed and the command execution is halted.
    :type value: bool
    """

    if value and not ctx.resilient_parsing:
        click.echo(ctx.get_help())
        if package.is_snap_package():
            click.pause()
        ctx.exit()


@click.command(
    name="license", help="Use this command to get licen[cs]e related information."
)
@click.option("-c", "--conditions", is_flag=True, help="Get licen[cs]e warranty.")
@click.option("-w", "--warranty", is_flag=True, help="Get licen[cs]e conditions.")
@click.pass_context
def license(ctx: click.Context, conditions: bool, warranty: bool):
    """
    Callback function for the `license` command.
    """
    if conditions:
        console.print(License.conditions, justify="center")
    elif warranty:
        console.print(License.warranty, justify="center")
    else:
        click.echo(ctx.command.get_usage(ctx=ctx))


@click.command(name="updates", help="Use this command to check for or install updates.")
@click.option("-c", "--check", is_flag=True, help="Check for updates.")
@click.option(
    "-i",
    "--install",
    is_flag=True,
    help="Install updates, if any are available [Non-Snap Packages only]",
)
@click.pass_context
def updates(ctx: click.Context, check: bool, install: bool):
    """
    Check for, or install updates if any are available.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param check: Option to check for updates.
    :type check: bool
    :param install: Option to install updates.
    :type install: bool
    """
    method_map = {
        "check": lambda session, status=None, message=None: package.check_updates(
            session=session, status=status
        ),
        "install": lambda session, status=None, message=None: package.check_updates(
            session=session, status=status, message=message, install_if_available=True
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=None,
            check=check,
            install=install,
        )
    )


@click.group(
    help=f"""
{Project.summary}
    
    
{Project.description}""",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option(
    "--export",
    type=str,
    help="A comma-separated list (no whitespaces) of file types to export the output to <supported: csv,html,json,xml>",
)
@click.option(
    "--limit",
    default=100,
    show_default=True,
    type=int,
    help=f"<bulk/semi-bulk> Maximum data output limit",
)
@click.option(
    "--sort",
    default="all",
    show_default=True,
    type=click.Choice(get_args(reddit.SORT)),
    help=f"<bulk/semi-bulk> Sort criterion",
)
@click.option(
    "--timeframe",
    default="all",
    show_default=True,
    type=click.Choice(get_args(reddit.TIMEFRAME)),
    help=f"<bulk/semi-bulk> Timeframe to get data from",
)
@click.option(
    "--time-format",
    default="locale",
    show_default=True,
    type=click.Choice(["concise", "locale"]),
    help=f"Determines the format of the output time",
)
@click.option(
    "-h",
    "--help",
    is_flag=True,
    expose_value=False,
    is_eager=True,
    callback=help_callback,
    help="Show this message and exit.",
)
@click.version_option(
    Version.full_version,
    "-v",
    "--version",
)
@click.pass_context
def cli(
    ctx: click.Context,
    timeframe: reddit.TIMEFRAME,
    sort: reddit.SORT,
    limit: int,
    time_format: str,
    export: List[General.EXPORT_FORMATS],
):
    """
    Main CLI group for Knew Karma.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param timeframe: Option to set the timeframe for the data.
    :type timeframe: Literal[str]
    :param sort: Option to set the sort criterion for the data.
    :type sort: Literal[str]
    :param limit: Option to set output data limit.
    :type limit: int
    :param time_format: Option to set the output's time format.
    :type time_format: Literal[str]
    :param export: Option to set data export file types.
    :type export: Literal[str]
    """

    ctx.ensure_object(Dict)
    ctx.obj["timeframe"] = timeframe
    ctx.obj["sort"] = sort
    ctx.obj["limit"] = limit
    ctx.obj["time_format"] = time_format
    ctx.obj["export"] = export


cli.add_command(cmd=license, name="license")
cli.add_command(cmd=updates, name="updates")


@cli.command(
    help="Use this command to get an individual post's data including its comments, "
    "provided the post's <id> and source <subreddit> are specified.",
)
@click.argument("id")
@click.argument("subreddit")
@click.option("--data", is_flag=True, help="Get post data")
@click.option("--comments", is_flag=True, help="Get post comments")
@click.pass_context
def post(ctx: click.Context, id: str, subreddit: str, data: bool, comments: bool):
    """
    Retrieve an individual post's data or comments.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param id: The ID of the post.
    :type id: str
    :param subreddit: The source subreddit of the post.
    :type subreddit: str
    :param data: Flag to get post data.
    :type data: bool
    :param comments: Flag to get post comments.
    :type comments: bool
    """

    sort: SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: reddit.TIME_FORMAT = ctx.obj["time_format"]

    post_instance = Post(id=id, subreddit=subreddit)
    method_map: Dict = {
        "comments": lambda session, status=None, message=None: post_instance.comments(
            limit=limit, sort=sort, status=status, message=message, session=session
        ),
        "data": lambda session, status=None, message=None: post_instance.data(
            session=session, status=status
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=export,
            data=data,
            comments=comments,
        )
    )


@cli.command(
    help="Use this command get best, controversial, front-page, new, popular, and/or rising posts.",
)
@click.option("--best", is_flag=True, help="Get posts from the best listing")
@click.option(
    "--controversial",
    is_flag=True,
    help="Get posts from the controversial listing",
)
@click.option(
    "--front-page",
    is_flag=True,
    help="Get posts from the reddit front-page",
)
@click.option("--new", is_flag=True, help="Get new posts")
@click.option(
    "--popular",
    is_flag=True,
    help="Get posts from the popular listing",
)
@click.option("--rising", is_flag=True, help="Get posts from the rising listing")
@click.pass_context
def posts(
    ctx: click.Context,
    best: bool,
    controversial: bool,
    front_page: bool,
    new: bool,
    popular: bool,
    rising: bool,
):
    """
    Retrieve various types of posts such as best, controversial, popular, new, and front-page.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param best: Flag to get posts from the best listing.
    :type best: bool
    :param controversial: Flag to get posts from the controversial listing.
    :type controversial: bool
    :param front_page: Flag to get posts from the reddit front-page.
    :type front_page: bool
    :param new: Flag to get new posts.
    :type new: bool
    :param popular: Flag to get posts from the popular listing.
    :type popular: bool
    :param rising: Flag to get posts from the rising listing.
    :type rising: bool
    """

    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: reddit.TIME_FORMAT = ctx.obj["time_format"]

    posts_instance = Posts()
    method_map: Dict = {
        "best": lambda session, status=None, message=None: posts_instance.best(
            timeframe=timeframe,
            limit=limit,
            status=status,
            message=message,
            session=session,
        ),
        "controversial": lambda session, status=None, message=None: posts_instance.controversial(
            timeframe=timeframe,
            limit=limit,
            status=status,
            message=message,
            session=session,
        ),
        "front_page": lambda session, status=None, message=None: posts_instance.front_page(
            limit=limit, sort=sort, status=status, message=message, session=session
        ),
        "new": lambda session, status=None, message=None: posts_instance.new(
            limit=limit, sort=sort, status=status, message=message, session=session
        ),
        "popular": lambda session, status=None, message=None: posts_instance.popular(
            timeframe=timeframe,
            limit=limit,
            status=status,
            message=message,
            session=session,
        ),
        "rising": lambda session, status=None, message=None: posts_instance.rising(
            limit=limit, status=status, message=message, session=session
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=export,
            best=best,
            controversial=controversial,
            front_page=front_page,
            new=new,
            popular=popular,
            rising=rising,
        )
    )


@cli.command(
    help="Use this command for search/discovery of users, subreddits, and posts.",
)
@click.argument("query")
@click.option("--posts", is_flag=True, help="Search posts")
@click.option("--subreddits", is_flag=True, help="Search subreddits")
@click.option("--users", is_flag=True, help="Search users")
@click.pass_context
def search(ctx: click.Context, query: str, posts: bool, subreddits: bool, users: bool):
    """
    Search for posts, subreddits, or users based on a query.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param query: The search query.
    :type query: str
    :param posts: Flag to search posts.
    :type posts: bool
    :param subreddits: Flag to search subreddits.
    :type subreddits: bool
    :param users: Flag to search users.
    :type users: bool
    """

    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: reddit.TIME_FORMAT = ctx.obj["time_format"]

    search_instance = Search(
        query=query,
    )
    method_map: Dict = {
        "posts": lambda session, status=None, message=None: search_instance.posts(
            sort=sort, limit=limit, status=status, message=message, session=session
        ),
        "subreddits": lambda session, status=None, message=None: search_instance.subreddits(
            sort=sort, limit=limit, session=session
        ),
        "users": lambda session, status=None, message=None: search_instance.users(
            sort=sort, limit=limit, status=status, message=message, session=session
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=export,
            posts=posts,
            subreddits=subreddits,
            users=users,
        )
    )


@cli.command(
    help="Use this command to get a subreddit's data, such as comments, posts, wiki-pages, wiki-page data, and more...",
)
@click.argument("subreddit_name")
@click.option(
    "--comments",
    is_flag=True,
    help="Get a subreddit's comments (beta)",
)
@click.option(
    "--comments-per-post",
    type=int,
    help="To be used when getting comments with `--comments`",
)
@click.option("--profile", is_flag=True, help="Get a subreddit's profile")
@click.option("--posts", is_flag=True, help="Get a subreddit's posts")
@click.option("--search-comments", type=str, help="Search comments in a subreddit")
@click.option("--search-post", type=str, help="Search posts in a subreddit")
@click.option(
    "--wiki-page", type=str, help="Get a subreddit's specified wiki page data"
)
@click.option("--wiki-pages", is_flag=True, help="Get a subreddit's wiki pages")
@click.pass_context
def subreddit(
    ctx: click.Context,
    subreddit_name: str,
    comments: bool,
    comments_per_post: int,
    posts: bool,
    profile: bool,
    search_comments: str,
    search_post: str,
    wiki_page: str,
    wiki_pages: bool,
):
    """
    Retrieve data about a specific subreddit including profile, comments, posts, and wiki pages.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param subreddit_name: The name of the subreddit.
    :type subreddit_name: str
    :param comments: Flag to get the subreddit's comments.
    :type comments: bool
    :param comments_per_post: Number of comments per post to retrieve.
    :type comments_per_post: int
    :param posts: Flag to get the subreddit's posts.
    :type posts: bool
    :param profile: Flag to get the subreddit's profile.
    :type profile: bool
    :param search_comments: Query to search comments in the subreddit.
    :type search_comments: str
    :param search_post: Query to search posts in the subreddit.
    :type search_post: str
    :param wiki_page: The name of the wiki page to retrieve.
    :type wiki_page: str
    :param wiki_pages: Flag to get the subreddit's wiki pages.
    :type wiki_pages: bool
    """

    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: reddit.TIME_FORMAT = ctx.obj["time_format"]

    subreddit_instance = Subreddit(
        name=subreddit_name,
    )
    method_map: Dict = {
        "comments": lambda session, status=None, message=None: subreddit_instance.comments(
            session=session,
            posts_limit=limit,
            comments_per_post=comments_per_post,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
        ),
        "posts": lambda session, status=None, message=None: subreddit_instance.posts(
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
            session=session,
        ),
        "profile": lambda session, status=None, message=None: subreddit_instance.profile(
            status=status, message=message, session=session
        ),
        "search_comments": lambda session, status=None, message=None: subreddit_instance.search_comments(
            query=search_comments,
            posts_limit=limit,
            comments_per_post=comments_per_post,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
            session=session,
        ),
        "search_post": lambda session, status=None, message=None: subreddit_instance.search_posts(
            query=search_post,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
            session=session,
        ),
        "wiki_pages": lambda session, status=None, message=None: subreddit_instance.wiki_pages(
            status=status, message=message, session=session
        ),
        "wiki_page": lambda session, status=None, message=None: subreddit_instance.wiki_page(
            page_name=wiki_page, status=status, message=message, session=session
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=export,
            profile=profile,
            comments=comments,
            comments_per_post=comments_per_post,
            posts=posts,
            search_comments=search_comments,
            search_post=search_post,
            wiki_pages=wiki_pages,
            wiki_page=wiki_page,
        )
    )


@cli.command(
    help="Use this command to get all, default, new, and/or popular subreddits.",
)
@click.option("--all", is_flag=True, help="Get all subreddits")
@click.option(
    "--default",
    is_flag=True,
    help="Get default subreddits",
)
@click.option(
    "--new",
    is_flag=True,
    help="Get new subreddits",
)
@click.option(
    "--popular",
    is_flag=True,
    help="Get popular subreddits",
)
@click.pass_context
def subreddits(ctx: click.Context, all: bool, default: bool, new: bool, popular: bool):
    """
    Retrieve various subreddits such as new, popular, default, and all subreddits.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param all: Flag to get all subreddits.
    :type all: bool
    :param default: Flag to get default subreddits.
    :type default: bool
    :param new: Flag to get new subreddits.
    :type new: bool
    :param popular: Flag to get popular subreddits.
    :type popular: bool
    """

    export: str = ctx.obj["export"]
    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    limit: int = ctx.obj["limit"]
    time_format: reddit.TIME_FORMAT = ctx.obj["time_format"]

    subreddits_instance = Subreddits()
    method_map: Dict = {
        "all": lambda session, status=None, message=None: subreddits_instance.all(
            limit=limit,
            session=session,
            status=status,
            message=message,
        ),
        "default": lambda session, status=None, message=None: subreddits_instance.default(
            limit=limit, session=session, status=status
        ),
        "new": lambda session, status=None, message=None: subreddits_instance.new(
            limit=limit, session=session, status=status
        ),
        "popular": lambda session, status=None, message=None: subreddits_instance.popular(
            limit=limit, session=session, status=status
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=export,
            timeframe=timeframe,
            all=all,
            default=default,
            new=new,
            popular=popular,
        )
    )


@cli.command(
    help="Use this command to get user data, such as profile, posts, "
    "comments, top subreddits, moderated subreddits, and more...",
)
@click.argument("username")
@click.option("--comments", is_flag=True, help="Get user's comments")
@click.option(
    "--moderated-subreddits",
    is_flag=True,
    help="Get user's moderated subreddits",
)
@click.option("--overview", is_flag=True, help="Get user's most recent comments")
@click.option("--posts", is_flag=True, help="Get user's posts")
@click.option("--profile", is_flag=True, help="Get user's profile")
@click.option(
    "--search-comments",
    type=str,
    help="Search user's comments that contains a specified query string",
)
@click.option(
    "--search-posts",
    type=str,
    help="Search user's posts that contains a specified query string",
)
@click.option(
    "--top-subreddits",
    type=int,
    help="Get user's top n subreddits",
)
@click.option(
    "--username-available",
    is_flag=True,
    help="Check if the given username is available or taken.",
)
@click.pass_context
def user(
    ctx: click.Context,
    username: str,
    comments: bool,
    moderated_subreddits: bool,
    overview: bool,
    posts: bool,
    profile: bool,
    search_comments: str,
    search_posts: str,
    top_subreddits: int,
    username_available: bool,
):
    """
    Retrieve data about a specific user including profile, posts, comments, and top subreddits.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param username: The username to retrieve data for.
    :type username: str
    :param comments: Flag to get user's comments.
    :type comments: bool
    :param moderated_subreddits: Flag to get user's moderated subreddits.
    :type moderated_subreddits: bool
    :param overview: Flag to get user's most recent comments.
    :type overview: bool
    :param posts: Flag to get user's posts.
    :type posts: bool
    :param profile: Flag to get user's profile.
    :type profile: bool
    :param search_comments: Query to search user's comments.
    :type search_comments: str
    :param search_posts: Query to search user's posts.
    :type search_posts: str
    :param top_subreddits: Number of top subreddits to retrieve.
    :type top_subreddits: int
    :param username_available: Flag to check if the given username is available of taken.
    :type username_available: bool
    """
    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: reddit.TIME_FORMAT = ctx.obj["time_format"]

    user_instance: User = User(
        name=username,
    )
    method_map: Dict = {
        "comments": lambda session, status=None, message=None: user_instance.comments(
            session=session,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
        ),
        "moderated_subreddits": lambda session, status=None, message=None: user_instance.moderated_subreddits(
            session=session, status=status
        ),
        "overview": lambda session, status=None, message=None: user_instance.overview(
            limit=limit, session=session, status=status
        ),
        "posts": lambda session, status=None, message=None: user_instance.posts(
            session=session,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
        ),
        "profile": lambda session, status=None, message=None: user_instance.profile(
            session=session, status=status
        ),
        "search_comments": lambda session, status=None, message=None: user_instance.search_comments(
            query=search_comments,
            limit=limit,
            session=session,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
        ),
        "search_posts": lambda session, status=None, message=None: user_instance.search_posts(
            query=search_posts,
            limit=limit,
            session=session,
            sort=sort,
            timeframe=timeframe,
            status=status,
            message=message,
        ),
        "top_subreddits": lambda session, status=None, message=None: user_instance.top_subreddits(
            session=session,
            top_n=top_subreddits,
            limit=limit,
            timeframe=timeframe,
            status=status,
            message=message,
        ),
        "username_available": lambda session, status=None, message=None: user_instance.username_available(
            session=session, status=status
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=export,
            comments=comments,
            moderated_subreddits=moderated_subreddits,
            overview=overview,
            posts=posts,
            profile=profile,
            search_comments=search_comments,
            search_posts=search_posts,
            top_subreddits=top_subreddits,
            username_available=username_available,
        )
    )


@cli.command(
    help="Use this command to get all, new, and/or popular users.",
)
@click.option("--all", is_flag=True, help="Get all users")
@click.option(
    "--new",
    is_flag=True,
    help="Get new users",
)
@click.option(
    "--popular",
    is_flag=True,
    help="Get popular users",
)
@click.pass_context
def users(ctx: click.Context, all: bool, new: bool, popular: bool):
    """
    Retrieve various users such as new, popular, and all users.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param all: Flag to get all users.
    :type all: bool
    :param new: Flag to get new users.
    :type new: bool
    :param popular: Flag to get popular users.
    :type popular: bool
    """

    export: str = ctx.obj["export"]
    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    limit: int = ctx.obj["limit"]
    time_format: reddit.TIME_FORMAT = ctx.obj["time_format"]

    users_instance = Users()
    method_map: Dict = {
        "all": lambda session, status=None, message=None: users_instance.all(
            session=session, limit=limit, timeframe=timeframe, status=status
        ),
        "new": lambda session, status=None, message=None: users_instance.new(
            session=session, limit=limit, timeframe=timeframe, status=status
        ),
        "popular": lambda session, status=None, message=None: users_instance.popular(
            session=session, limit=limit, timeframe=timeframe, status=status
        ),
    }

    asyncio.run(
        method_call_handler(
            ctx=ctx,
            method_map=method_map,
            export=export,
            all=all,
            new=new,
            popular=popular,
        )
    )


async def call_method(
    method: Callable,
    **kwargs: Union[str, click.Context, aiohttp.ClientSession, Status],
):
    """
    Calls a method with the provided arguments.

    :param method: A method to call.
    :type method: Callable
    :param session: A aiohttp.ClientSession to use for the method's requests.
    :type session: aiohttp.ClientSession
    :param status: An instance of `console.status` used to display animated status messages inside the method.
    :type status: Console.console.status
    :param kwargs: Additional keyword arguments for `export: str`, `argument: str` and `ctx: click.Context` .
    """

    session = kwargs.get("session")
    status = kwargs.get("status")
    message = kwargs.get("message")

    command: str = kwargs.get("ctx").command.name
    argument: str = kwargs.get("argument")

    response_data: Union[List, Dict, str, bool] = await method(
        session=session,
        status=status,
        message=Message,
    )
    if argument == "username_available" and (response_data, bool):
        if response_data:
            Message.ok("Username is available.")
        else:
            Message.warning("Username is already taken.")
    else:
        if response_data:
            dataframe = General.create_dataframe(data=response_data)
            console.print(dataframe)

            if kwargs.get("export"):

                exports_child_dir: str = os.path.join(
                    General.EXPORTS_PARENT_DIR,
                    "exports",
                    command,
                    argument,
                )

                General.pathfinder(
                    directories=[
                        os.path.join(exports_child_dir, extension)
                        for extension in ["csv", "html", "json", "xml"]
                    ],
                )

                export_to: List = kwargs.get("export").split(",")
                General.export_dataframe(
                    dataframe=dataframe,
                    filename=General.filename_timestamp(),
                    directory=exports_child_dir,
                    formats=export_to,
                )


async def method_call_handler(
    ctx: click.Context,
    method_map: Dict,
    export: str,
    **kwargs: Union[str, int, bool],
):
    """
    Handle the method calls based on the provided arguments.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param method_map: Dictionary mapping method names to their corresponding functions.
    :type method_map: Dict
    :param export: The export format.
    :type export: str
    :param kwargs: Additional keyword arguments.
    :type kwargs: Union[str, int, bool]
    """

    is_valid_arg: bool = False

    for argument, method in method_map.items():
        if kwargs.get(argument):
            is_valid_arg = True
            start_time: datetime = datetime.now()
            try:
                console.print(License.notice, justify="center")
                with Status(
                    status=f"Opening new client session",
                    spinner="dots",
                    spinner_style=Style.yellow.strip("[,]"),
                    console=console,
                ) as status:
                    async with aiohttp.ClientSession() as session:
                        Message.ok("New client session opened")
                        await reddit.infra_status(
                            session=session,
                            status=status,
                            message=Message,
                        )

                        await call_method(
                            method=method,
                            session=session,
                            status=status,
                            ctx=ctx,
                            export=export,
                            argument=argument,
                        )
            except aiohttp.ClientConnectionError as connection_error:
                Message.exception(
                    title="An HTTP error occurred", error=connection_error
                )
            except aiohttp.ClientResponseError as response_error:
                Message.exception(title="An API error occurred", error=response_error)
            finally:
                elapsed_time = datetime.now() - start_time
                Message.ok(
                    f"Session closed. {elapsed_time.total_seconds():.2f} seconds elapsed."
                )

    if not is_valid_arg:
        ctx.command.get_usage(ctx=ctx)


def start():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """

    console.set_window_title(f"{Project.name} {Version.release}")
    cli(obj={})


# -------------------------------- END ----------------------------------------- #
