import functools
import typing as t

import rich_click as click

from tools.log_config import console
from tools.runtime_ops import RuntimeOps
from . import command
from ..core.client import reddit
from ..core.post import Post
from ..core.posts import Posts
from ..core.search import Search
from ..core.subreddit import Subreddit
from ..core.subreddits import Subreddits
from ..core.user import User
from ..core.users import Users
from ..meta.about import Project
from ..meta.license import License
from ..meta.version import Version

__all__ = ["start"]


def set_window_title(text: t.Optional[str] = None):
    title = f"{Project.name} v{Version.release}"

    if text:
        title = f"{title} - {text}"

    console.set_window_title(title)


def global_options(func: t.Callable) -> t.Callable:
    """
    Decorator to add global CLI options like sort, timeframe, export, etc.,
    and inject them into ctx.obj for use within the command.
    """

    @click.option(
        "-e",
        "--export",
        type=str,
        help="A comma-separated list <w/o whitespaces> of file types to export the output to <supported: csv,html,json,xml>",
    )
    @click.option(
        "-l",
        "--limit",
        default=100,
        show_default=True,
        type=int,
        help="Maximum data output limit <max 100 if searching for users>",
    )
    @click.option(
        "-s",
        "--sort",
        default="all",
        show_default=True,
        type=click.Choice(t.get_args(reddit.SORT)),
        help="Sort criterion",
    )
    @click.option(
        "-t",
        "--timeframe",
        default="all",
        show_default=True,
        type=click.Choice(t.get_args(reddit.TIMEFRAME)),
        help="Timeframe to get data from",
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(
        ctx: click.Context,
        timeframe: reddit.TIMEFRAME,
        sort: reddit.SORT,
        limit: int,
        export: str,
        *args,
        **kwargs,
    ):
        ctx.ensure_object(dict)
        ctx.obj["timeframe"] = timeframe
        ctx.obj["sort"] = sort
        ctx.obj["limit"] = limit
        ctx.obj["export"] = export
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def help_callback(ctx: click.Context, _, value: bool):
    """
    Custom callback function for handling the '--help' option in Click commands.
    """

    if value and not ctx.resilient_parsing:
        click.echo(ctx.get_help())
        if RuntimeOps.is_snap_package():
            click.pause()
        ctx.exit()


@click.group(
    help=f"""
{Project.summary}\n\n\n{Project.description}""",
    context_settings=dict(help_option_names=["-h", "--help"]),
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
@global_options
@click.pass_context
def cli(
    ctx: click.Context,
):
    """
    Main CLI group for Knew Karma.
    """
    set_window_title()
    ctx.ensure_object(dict)


@cli.command("license")
@click.option("-c", "--conditions", help="License terms and conditions.", is_flag=True)
@click.option("-w", "--warranty", help="License warranty.", is_flag=True)
@click.pass_context
def licence(
    ctx: click.Context, conditions: t.Optional[bool], warranty: t.Optional[bool]
):
    """
    Show license information
    """
    set_window_title(
        "License Terms and Conditions"
        if conditions
        else "License Warranty" if warranty else None
    )
    if conditions:
        console.print(
            License.conditions,
            justify="center",
        )
    elif warranty:
        console.print(
            License.warranty,
            justify="center",
        )
    else:
        click.echo(ctx.get_help())


@cli.command(
    name="post",
    help="Use this command to get an individual post's data including its comments, "
    "provided the post's <id> and source <subreddit> are specified.",
)
@click.argument("_id", metavar="ID")
@click.argument("subreddit")
@click.option("--data", is_flag=True, help="Get post data")
@click.option("--comments", is_flag=True, help="Get post comments")
@global_options
@click.pass_context
def cmd_post(ctx: click.Context, _id: str, subreddit: str, data: bool, comments: bool):
    """
    Retrieve an individual post's data or comments.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param _id: The ID of the post.
    :type _id: str
    :param subreddit: The source subreddit of the post.
    :type subreddit: str
    :param data: Flag to get post data.
    :type data: bool
    :param comments: Flag to get post comments.
    :type comments: bool
    """

    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    post = Post(id=_id, subreddit=subreddit)
    method_map: t.Dict = {
        "comments": lambda session, status, logger: post.comments(
            limit=limit, sort=sort, status=status, logger=logger, session=session
        ),
        "data": lambda session, status, logger: post.data(
            session=session, status=status
        ),
    }

    command.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        data=data,
        comments=comments,
    )


@cli.command(
    name="posts",
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
    "--top",
    is_flag=True,
    help="Get posts from the top listing",
)
@click.option("--rising", is_flag=True, help="Get posts from the rising listing")
@global_options
@click.pass_context
def cmd_posts(
    ctx: click.Context,
    best: bool,
    controversial: bool,
    front_page: bool,
    new: bool,
    top: bool,
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
    param top: Flag to get posts from the top listing.
    :type top: bool
    :param rising: Flag to get posts from the rising listing.
    :type rising: bool
    """

    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    method_map: t.Dict = {
        "best": lambda session, status, logger: Posts.best(
            timeframe=timeframe,
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "controversial": lambda session, status, logger: Posts.controversial(
            timeframe=timeframe,
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "front_page": lambda session, status, logger: Posts.front_page(
            limit=limit, sort=sort, status=status, logger=logger, session=session
        ),
        "new": lambda session, status, logger: Posts.new(
            limit=limit, sort=sort, status=status, logger=logger, session=session
        ),
        "top": lambda session, status, logger: Posts.top(
            timeframe=timeframe,
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "rising": lambda session, status, logger: Posts.rising(
            limit=limit, status=status, logger=logger, session=session
        ),
    }

    command.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        best=best,
        controversial=controversial,
        front_page=front_page,
        new=new,
        top=top,
        rising=rising,
    )


@cli.command(
    name="search",
    help="Use this command for search/discovery of users, subreddits, and posts.",
)
@click.argument("query")
@click.option("--posts", is_flag=True, help="Search posts")
@click.option("--subreddits", is_flag=True, help="Search subreddits")
@click.option("--users", is_flag=True, help="Search users")
@global_options
@click.pass_context
def cmd_search(
    ctx: click.Context, query: str, posts: bool, subreddits: bool, users: bool
):
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

    search = Search(
        query=query,
    )
    method_map: t.Dict = {
        "posts": lambda session, status, logger: search.posts(
            sort=sort, limit=limit, status=status, logger=logger, session=session
        ),
        "subreddits": lambda session, status, logger: search.subreddits(
            sort=sort, limit=limit, logger=logger, session=session, status=status
        ),
        "users": lambda session, status, logger: search.users(
            sort=sort, limit=limit, status=status, logger=logger, session=session
        ),
    }

    command.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        posts=posts,
        subreddits=subreddits,
        users=users,
    )


@cli.command(
    name="user",
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
    "--top-subreddits",
    type=int,
    help="Get user's top n subreddits",
)
@click.option(
    "--does-user-exist",
    is_flag=True,
    help="Check if a user exists",
)
@click.option(
    "--search-posts",
    type=str,
    help="Search user posts that match a specified query string",
)
@click.option(
    "--search-comments",
    type=str,
    help="Search user comments that match a specified query string",
)
@global_options
@click.pass_context
def cmd_user(
    ctx: click.Context,
    username: str,
    comments: bool,
    moderated_subreddits: bool,
    search_comments: str,
    search_posts: str,
    overview: bool,
    posts: bool,
    profile: bool,
    top_subreddits: int,
    does_user_exist: bool,
):
    """
    Retrieve data about a specific user including profile, posts, comments, and top subreddits.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param username: The username to retrieve data for.
    :type username: str
    :param comments: Flag to get user's comments.
    :type comments: bool
    :param search_comments:
    :type search_comments: str
    :param search_posts:
    :type search_posts: str
    :param moderated_subreddits: Flag to get user's moderated subreddits.
    :type moderated_subreddits: bool
    :param overview: Flag to get user's most recent comments.
    :type overview: bool
    :param posts: Flag to get user's posts.
    :type posts: bool
    :param profile: Flag to get user's profile.
    :type profile: bool
    :param top_subreddits: Number of top subreddits to retrieve.
    :type top_subreddits: int
    :param does_user_exist: Flag to check if the given user exists.
    :type does_user_exist: bool
    """
    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    user = User(username=username)
    method_map: t.Dict = {
        "comments": lambda session, status, logger: user.comments(
            session=session,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
        ),
        "moderated_subreddits": lambda session, status, logger: user.moderated_subreddits(
            logger=logger, session=session, status=status
        ),
        "overview": lambda session, status, logger: user.overview(
            limit=limit, logger=logger, session=session, status=status
        ),
        "posts": lambda session, status, logger: user.posts(
            session=session,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
        ),
        "profile": lambda session, status: user.profile(session=session, status=status),
        "search_comments": lambda logger, status, session: user.search_comments(
            query=search_comments,
            limit=limit,
            logger=logger,
            status=status,
            session=session,
        ),
        "search_posts": lambda logger, status, session: user.search_posts(
            query=search_posts,
            limit=limit,
            logger=logger,
            status=status,
            session=session,
        ),
        "top_subreddits": lambda session, status, logger: user.top_subreddits(
            session=session,
            top_n=top_subreddits,
            limit=limit,
            timeframe=timeframe,
            status=status,
            logger=logger,
        ),
        "does_user_exist": lambda session, status, logger: user.does_user_exist(
            logger=logger, session=session, status=status
        ),
    }

    command.run(
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
        does_user_exist=does_user_exist,
    )


@cli.command(
    name="users",
    help="Use this command to get all, new, and/or popular users.",
)
@click.option("-a", "--all", "_all", is_flag=True, help="Get all users")
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
@global_options
@click.pass_context
def cmd_users(ctx: click.Context, _all: bool, new: bool, popular: bool):
    """
    Retrieve various users such as new, popular, and all users.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param _all: Flag to get all users.
    :type _all: bool
    :param new: Flag to get new users.
    :type new: bool
    :param popular: Flag to get popular users.
    :type popular: bool
    """

    export: str = ctx.obj["export"]
    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    limit: int = ctx.obj["limit"]

    method_map: t.Dict = {
        "all": lambda session, status, logger: Users.all(
            logger=logger,
            session=session,
            limit=limit,
            timeframe=timeframe,
            status=status,
        ),
        "new": lambda session, status, logger: Users.new(
            logger=logger,
            session=session,
            limit=limit,
            timeframe=timeframe,
            status=status,
        ),
        "popular": lambda session, status, logger: Users.popular(
            logger=logger,
            session=session,
            limit=limit,
            timeframe=timeframe,
            status=status,
        ),
    }

    command.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        all=all,
        new=new,
        popular=popular,
    )


@click.command(
    name="subreddit",
    help="Use this command to get a subreddit's data, such as comments, posts, wiki-pages, wiki-page data, and more...",
)
@click.argument("subreddit_name")
@click.option("-sr", "--search", type=str, help="Search for posts in a subreddit")
@click.option("-pf", "--profile", is_flag=True, help="Get a subreddit's profile")
@click.option("-ps", "--posts", is_flag=True, help="Get a subreddit's posts")
@click.option(
    "-wp", "--wikipage", type=str, help="Get a subreddit's specified wiki page data"
)
@click.option("-wps", "--wikipages", is_flag=True, help="Get a subreddit's wiki pages")
@global_options
@click.pass_context
def cmd_subreddit(
    ctx: click.Context,
    subreddit_name: str,
    posts: bool,
    profile: bool,
    wikipage: str,
    search: str,
    wikipages: bool,
):
    """
    Retrieve data about a specific subreddit including profile, comments, posts, and wiki pages.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param subreddit_name: The name of the subreddit.
    :type subreddit_name: str
    :param posts: Flag to get the subreddit's posts.
    :type posts: bool
    :param profile: Flag to get the subreddit's profile.
    :type profile: bool
    :param wikipage: The name of the wiki page to retrieve.
    :type wikipage: str
    :param search:
    :type search: str
    :param wikipages: Flag to get the subreddit's wiki pages.
    :type wikipages: bool
    """

    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    subreddit = Subreddit(
        name=subreddit_name,
    )
    method_map: t.Dict = {
        "posts": lambda session, status, logger=None: subreddit.posts(
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
            session=session,
        ),
        "profile": lambda session, status: subreddit.profile(
            status=status, session=session
        ),
        "search": lambda session, status, logger: subreddit.search(
            query=search,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
            session=session,
        ),
        "wikipages": lambda session, status, logger: subreddit.wikipages(
            status=status, session=session
        ),
        "wikipage": lambda session, status: subreddit.wikipage(
            page_name=wikipage, status=status, session=session
        ),
    }
    command.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        profile=profile,
        posts=posts,
        wikipages=wikipages,
        wikipage=wikipage,
    )


@cli.command(
    name="subreddits",
    help="Use this command to get all, default, new, and/or popular subreddits.",
)
@click.option("-a", "--all", "_all", is_flag=True, help="Get all subreddits")
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
@global_options
@click.pass_context
def cmd_subreddits(
    ctx: click.Context, _all: bool, default: bool, new: bool, popular: bool
):
    """
    Retrieve various subreddits such as new, popular, default, and all subreddits.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param _all: Flag to get all subreddits.
    :type _all: bool
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

    method_map: t.Dict = {
        "all": lambda session, status, logger: Subreddits.all(
            limit=limit,
            session=session,
            status=status,
            logger=logger,
        ),
        "default": lambda session, status, logger: Subreddits.default(
            limit=limit, session=session, status=status
        ),
        "new": lambda session, status, logger: Subreddits.new(
            limit=limit, logger=logger, session=session, status=status
        ),
        "popular": lambda session, status, logger: Subreddits.popular(
            limit=limit, logger=logger, session=session, status=status
        ),
    }

    command.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        timeframe=timeframe,
        all=all,
        default=default,
        new=new,
        popular=popular,
    )


def start():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """

    cli(obj={})


# -------------------------------- END ----------------------------------------- #
