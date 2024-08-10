import os
from datetime import datetime
from typing import get_args, Union, Callable, Literal

import requests
import rich_click as click
from rich.text import Text

from . import Post, Posts, Search, Subreddit, Subreddits, User, Users
from .about import About
from .api import SORT_CRITERION, TIMEFRAME, TIME_FORMAT, Api
from .tools.data_utils import (
    create_dataframe,
    export_dataframe,
    EXPORT_FORMATS,
)
from .tools.general_utils import console, pathfinder, create_panel
from .tools.time_utils import filename_timestamp
from .version import Version

__all__ = ["start"]


@click.group(
    cls=click.RichGroup,
    help=f"""
{About.summary}


{About.description}""",
    context_settings=dict(help_option_names=["-h", "--help"]),
)
@click.option(
    "-e",
    "--export",
    type=str,
    help="A comma-separated list (without spaces) of file types to export the output to [supported: csv,html,json,xml]",
)
@click.option(
    "-l",
    "--limit",
    default=100,
    show_default=True,
    type=int,
    help=f"[bulk/semi-bulk] Maximum data output limit",
)
@click.option(
    "-s",
    "--sort",
    default="all",
    show_default=True,
    type=click.Choice(get_args(SORT_CRITERION)),
    help=f"[bulk/semi-bulk] Sort criterion",
)
@click.option(
    "-t",
    "--timeframe",
    default="all",
    show_default=True,
    type=click.Choice(get_args(TIMEFRAME)),
    help=f"[bulk/semi-bulk] Timeframe to get data from",
)
@click.option(
    "--time-format",
    default="locale",
    show_default=True,
    type=click.Choice(["concise", "locale"]),
    help=f"Determines the format of the output time",
)
@click.version_option(
    Version.release,
    "-v",
    "--version",
    message=About.copyright,
)
@click.pass_context
def cli(
        ctx: click.Context,
        timeframe: TIMEFRAME,
        sort: SORT_CRITERION,
        limit: int,
        time_format: str,
        export: list[EXPORT_FORMATS],
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
    ctx.ensure_object(dict)
    ctx.obj["timeframe"] = timeframe
    ctx.obj["sort"] = sort
    ctx.obj["limit"] = limit
    ctx.obj["time_format"] = time_format
    ctx.obj["export"] = export


@cli.command(
    help="Use this command to get an individual post's data including its comments, "
         "provided the post's `id` and source `subreddit` are specified.",
    cls=click.RichCommand,
)
@click.argument("id")
@click.argument("subreddit")
@click.option("-d", "--data", is_flag=True, help="Get post data")
@click.option("-c", "--comments", is_flag=True, help="Get post comments")
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
    sort: SORT_CRITERION = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: TIME_FORMAT = ctx.obj["time_format"]

    post_instance = Post(post_id=id, post_subreddit=subreddit, time_format=time_format)
    method_map: dict = {
        "comments": lambda session, status=None: post_instance.comments(
            limit=limit, sort=sort, status=status, session=session
        ),
        "data": lambda session, status=None: post_instance.data(
            session=session, status=status
        ),
    }

    handle_method_calls(
        ctx=ctx, method_map=method_map, export=export, data=data, comments=comments
    )


@cli.command(
    help="Use this command get best, controversial, popular, new and/or front-page posts.",
    cls=click.RichCommand,
)
@click.option("-b", "--best", is_flag=True, help="Get posts from the best listing")
@click.option(
    "-c",
    "--controversial",
    is_flag=True,
    help="Get posts from the controversial listing",
)
@click.option(
    "-f",
    "--front-page",
    is_flag=True,
    help="Get posts from the reddit front-page",
)
@click.option("-n", "--new", is_flag=True, help="Get new posts")
@click.option(
    "-p",
    "--popular",
    is_flag=True,
    help="Get posts from the popular listing",
)
@click.option("-r", "--rising", is_flag=True, help="Get posts from the rising listing")
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
    timeframe: TIMEFRAME = ctx.obj["timeframe"]
    sort: SORT_CRITERION = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: TIME_FORMAT = ctx.obj["time_format"]

    posts_instance = Posts(time_format=time_format)
    method_map: dict = {
        "best": lambda session, status=None: posts_instance.best(
            timeframe=timeframe, limit=limit, status=status, session=session
        ),
        "controversial": lambda session, status=None: posts_instance.controversial(
            timeframe=timeframe, limit=limit, status=status, session=session
        ),
        "front_page": lambda session, status=None: posts_instance.front_page(
            limit=limit, sort=sort, status=status, session=session
        ),
        "new": lambda session, status=None: posts_instance.new(
            limit=limit, sort=sort, status=status, session=session
        ),
        "popular": lambda session, status=None: posts_instance.popular(
            timeframe=timeframe, limit=limit, status=status, session=session
        ),
        "rising": lambda session, status=None: posts_instance.rising(
            limit=limit, status=status, session=session
        ),
    }

    handle_method_calls(
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


@cli.command(
    help="Use this command search/discovery of targets in users, subreddits, and posts.",
    cls=click.RichCommand,
)
@click.argument("query")
@click.option("-p", "--posts", is_flag=True, help="Search posts")
@click.option("-s", "--subreddits", is_flag=True, help="Search subreddits")
@click.option("-u", "--users", is_flag=True, help="Search users")
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
    sort: SORT_CRITERION = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: TIME_FORMAT = ctx.obj["time_format"]

    search_instance = Search(query=query, time_format=time_format)
    method_map: dict = {
        "posts": lambda session, status=None: search_instance.posts(
            sort=sort, limit=limit, status=status, session=session
        ),
        "subreddits": lambda session, status=None: search_instance.subreddits(
            sort=sort, limit=limit, session=session
        ),
        "users": lambda session, status=None: search_instance.users(
            sort=sort, limit=limit, status=status, session=session
        ),
    }

    handle_method_calls(
        ctx=ctx,
        method_map=method_map,
        export=export,
        posts=posts,
        subreddits=subreddits,
        users=users,
    )


@cli.command(
    help="Use this command to get a subreddit's data, such as comments, posts, wiki-pages, wiki-page data, and more...",
    cls=click.RichCommand,
)
@click.argument("subreddit_name")
@click.option(
    "-c",
    "--comments",
    is_flag=True,
    help="Get a subreddit's comments (beta)",
)
@click.option(
    "-cpp",
    "--comments-per-post",
    type=int,
    help="To be used when getting comments with `-c/--comments`",
)
@click.option("-p", "--profile", is_flag=True, help="Get a subreddit's profile")
@click.option("-pp", "--posts", is_flag=True, help="Get a subreddit's posts")
@click.option(
    "-sc", "--search-comments", type=str, help="Search comments in a subreddit"
)
@click.option("-sp", "--search-post", type=str, help="Search posts in a subreddit")
@click.option(
    "-wp", "--wiki-page", type=str, help="Get a subreddit's specified wiki page data"
)
@click.option("-wps", "--wiki-pages", is_flag=True, help="Get a subreddit's wiki pages")
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
    timeframe: TIMEFRAME = ctx.obj["timeframe"]
    sort: SORT_CRITERION = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: TIME_FORMAT = ctx.obj["time_format"]

    subreddit_instance = Subreddit(subreddit=subreddit_name, time_format=time_format)
    method_map: dict = {
        "comments": lambda session, status=None: subreddit_instance.comments(
            session=session,
            posts_limit=limit,
            comments_per_post=comments_per_post,
            sort=sort,
            timeframe=timeframe,
            status=status,
        ),
        "posts": lambda session, status=None: subreddit_instance.posts(
            limit=limit, sort=sort, timeframe=timeframe, status=status, session=session
        ),
        "profile": lambda session, status=None: subreddit_instance.profile(
            status=status, session=session
        ),
        "search_comments": lambda session, status=None: subreddit_instance.search_comments(
            query=search_comments,
            posts_limit=limit,
            comments_per_post=comments_per_post,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        ),
        "search_post": lambda session, status=None: subreddit_instance.search_posts(
            query=search_post,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        ),
        "wiki_pages": lambda session, status=None: subreddit_instance.wiki_pages(
            status=status, session=session
        ),
        "wiki_page": lambda session, status=None: subreddit_instance.wiki_page(
            page_name=wiki_page, status=status, session=session
        ),
    }

    handle_method_calls(
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


@cli.command(
    help="Use this command to get new, popular, default and/or all subreddits.",
    cls=click.RichCommand,
)
@click.option("-a", "--all", is_flag=True, help="Get all subreddits")
@click.option(
    "-d",
    "--default",
    is_flag=True,
    help="Get default subreddits",
)
@click.option(
    "-n",
    "--new",
    is_flag=True,
    help="Get new subreddits",
)
@click.option(
    "-p",
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
    timeframe: TIMEFRAME = ctx.obj["timeframe"]
    limit: int = ctx.obj["limit"]
    time_format: TIME_FORMAT = ctx.obj["time_format"]

    subreddits_instance = Subreddits(time_format=time_format)
    method_map: dict = {
        "all": lambda session, status=None: subreddits_instance.all(
            limit=limit,
            session=session,
            status=status,
        ),
        "default": lambda session, status=None: subreddits_instance.default(
            limit=limit, session=session, status=status
        ),
        "new": lambda session, status=None: subreddits_instance.new(
            limit=limit, session=session, status=status
        ),
        "popular": lambda session, status=None: subreddits_instance.popular(
            limit=limit, session=session, status=status
        ),
    }

    handle_method_calls(
        ctx=ctx,
        method_map=method_map,
        export=export,
        timeframe=timeframe,
        all=all,
        default=default,
        new=new,
        popular=popular,
    )


@cli.command(
    help="Use this command to get user data, such as profile, posts, "
         "comments, top subreddits, moderated subreddits, and more...",
    cls=click.RichCommand,
)
@click.argument("username")
@click.option("-c", "--comments", is_flag=True, help="Get user's comments")
@click.option(
    "-ms",
    "--moderated-subreddits",
    is_flag=True,
    help="Get user's moderated subreddits",
)
@click.option("-o", "--overview", is_flag=True, help="Get user's most recent comments")
@click.option("-ps", "--posts", is_flag=True, help="Get user's posts")
@click.option("-p", "--profile", is_flag=True, help="Get user's profile")
@click.option(
    "-sc",
    "--search-comments",
    type=str,
    help="Search user's comments that contains a specified query string",
)
@click.option(
    "-sp",
    "--search-posts",
    type=str,
    help="Search user's posts that contains a specified query string",
)
@click.option(
    "-ts",
    "--top-subreddits",
    type=int,
    help="Get user's top n subreddits",
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
    """
    timeframe: TIMEFRAME = ctx.obj["timeframe"]
    sort: SORT_CRITERION = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    time_format: TIME_FORMAT = ctx.obj["time_format"]

    user_instance: User = User(username=username, time_format=time_format)
    method_map: dict = {
        "comments": lambda session, status=None: user_instance.comments(
            session=session, limit=limit, sort=sort, timeframe=timeframe, status=status
        ),
        "moderated_subreddits": lambda session, status=None: user_instance.moderated_subreddits(
            session=session, status=status
        ),
        "overview": lambda session, status=None: user_instance.overview(
            limit=limit, session=session, status=status
        ),
        "posts": lambda session, status=None: user_instance.posts(
            session=session, limit=limit, sort=sort, timeframe=timeframe, status=status
        ),
        "profile": lambda session, status=None: user_instance.profile(
            session=session, status=status
        ),
        "search_comments": lambda session, status=None: user_instance.search_comments(
            query=search_comments,
            limit=limit,
            session=session,
            sort=sort,
            timeframe=timeframe,
            status=status,
        ),
        "search_posts": lambda session, status=None: user_instance.search_posts(
            query=search_posts,
            limit=limit,
            session=session,
            sort=sort,
            timeframe=timeframe,
            status=status,
        ),
        "top_subreddits": lambda session, status=None: user_instance.top_subreddits(
            session=session,
            top_n=top_subreddits,
            limit=limit,
            timeframe=timeframe,
            status=status,
        ),
    }

    handle_method_calls(
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
    )


@cli.command(
    help="Use this command to get new, popular, and/or all users.",
    cls=click.RichCommand,
)
@click.option("-a", "--all", is_flag=True, help="Get all users")
@click.option(
    "-n",
    "--new",
    is_flag=True,
    help="Get new users",
)
@click.option(
    "-p",
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
    timeframe: TIMEFRAME = ctx.obj["timeframe"]
    limit: int = ctx.obj["limit"]
    time_format: TIME_FORMAT = ctx.obj["time_format"]

    users_instance = Users(time_format=time_format)
    method_map: dict = {
        "all": lambda session, status=None: users_instance.all(
            session=session, limit=limit, timeframe=timeframe, status=status
        ),
        "new": lambda session, status=None: users_instance.new(
            session=session, limit=limit, timeframe=timeframe, status=status
        ),
        "popular": lambda session, status=None: users_instance.popular(
            session=session, limit=limit, timeframe=timeframe, status=status
        ),
    }

    handle_method_calls(
        ctx=ctx, method_map=method_map, export=export, all=all, new=new, popular=popular
    )


def call_method(
        method: Callable,
        session: requests.session,
        status: console.status,
        **kwargs: Union[str, click.Context],
):
    """
    Calls a method with the provided arguments.

    :param method: A method to call.
    :type method: Callable
    :param session: A requests.Session to use for the method's requests.
    :type session: requests.Session
    :param status: An instance of `console.status` used to display animated status messages inside the method.
    :type status: Console.console.status
    :param kwargs: Additional keyword arguments for `export: str`, `argument: str` and `ctx: click.Context` .
    """
    command: str = kwargs.get("ctx").command.name
    argument: str = kwargs.get("argument")

    response_data = method(session=session, status=status)
    if response_data:
        dataframe = create_dataframe(data=response_data)

        panel_title: str = (
            f"Showing [cyan]{len(response_data)}[/] {command} [italic]{argument}[/]"
            if isinstance(response_data, list)
            else f"Showing {command} [italic]{argument}[/]"
        )

        panel_title += f" — {About.name} [cyan]{Version.release}[/]"

        create_panel(
            title=panel_title,
            subtitle=f"[italic]Thank you, for using {About.name}![/] ❤️ ",
            content=Text(text=str(dataframe), style="dim"),
        )

        if kwargs.get("export"):
            output_parent_dir: str = os.path.expanduser(
                os.path.join("~", "knewkarma-data")
            )
            output_child_dir: str = os.path.join(
                output_parent_dir,
                command,
                argument,
            )

            pathfinder(
                directories=[
                    os.path.join(output_child_dir, extension)
                    for extension in ["csv", "html", "json", "xml"]
                ]
            )

            export_to_files: list = kwargs.get("export").split(",")
            export_dataframe(
                dataframe=dataframe,
                filename=filename_timestamp(),
                directory=output_child_dir,
                formats=export_to_files,
            )


def handle_method_calls(
        ctx: click.Context, method_map: dict, export: str, **kwargs: Union[str, int, bool]
):
    """
    Handle the method calls based on the provided arguments.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param method_map: Dictionary mapping method names to their corresponding functions.
    :type method_map: dict
    :param export: The export format.
    :type export: str
    :param kwargs: Additional keyword arguments.
    """
    is_valid_arg: bool = False
    for argument, method in method_map.items():
        if kwargs.get(argument):
            is_valid_arg = True
            start_time: datetime = datetime.now()
            try:
                with console.status(
                        "Establishing connection /w new session...", spinner="dots2"
                ) as status:
                    with requests.Session() as session:
                        Api().check_updates(session=session, status=status)
                        call_method(
                            method=method,
                            session=session,
                            status=status,
                            ctx=ctx,
                            export=export,
                            argument=argument,
                        )
            except KeyboardInterrupt:
                console.print("[[yellow]✘[/]] Process aborted /w CTRL+C.")
            finally:
                elapsed_time = datetime.now() - start_time
                console.print(
                    f"[[green]✔[/]] DONE. {elapsed_time.total_seconds():.2f}ms elapsed."
                )

    if not is_valid_arg:
        ctx.get_usage()


def start():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """
    cli(obj={})

# -------------------------------- END ----------------------------------------- #
