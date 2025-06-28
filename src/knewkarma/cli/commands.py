import functools
import typing as t

import rich_click as click

from karmakrate.handlers.auth_handler import AuthHandler
from karmakrate.konsole.logging import console
from karmakrate.runtime.calls import RuntimeCalls
from .main import run
from ..core.client import LISTINGS, SORT, TIME_FILTERS
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
        "--listing",
        default="top",
        show_default=True,
        type=click.Choice(t.get_args(LISTINGS)),
        help="Reddit Listings (I'm still working on a better description)",
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
        default="lucene",
        show_default=True,
        type=click.Choice(t.get_args(SORT)),
        help="Sort criterion",
    )
    @click.option(
        "-t",
        "--time-filter",
        default="all",
        show_default=True,
        type=click.Choice(t.get_args(TIME_FILTERS)),
        help="Filter data by time",
    )
    @click.pass_context
    @functools.wraps(func)
    def wrapper(
        ctx: click.Context,
        time_filter: TIME_FILTERS,
        sort: SORT,
        limit: int,
        export: str,
        listing: str,
        *args,
        **kwargs,
    ):
        ctx.ensure_object(dict)
        ctx.obj["time_filter"] = time_filter
        ctx.obj["sort"] = sort
        ctx.obj["limit"] = limit
        ctx.obj["export"] = export
        ctx.obj["listing"] = listing
        return ctx.invoke(func, *args, **kwargs)

    return wrapper


def help_callback(ctx: click.Context, _, value: bool):
    """
    Custom callback function for handling the '--help' option in Click commands.
    """

    if value and not ctx.resilient_parsing:
        click.echo(ctx.get_help())
        if RuntimeCalls.is_snap_package():
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


@cli.command(name="auth", help="Authenticate with Reddit")
@click.option("--client-id", help="Reddit API client id", type=str)
@click.option("--client-secret", help="Reddit API client secret", type=str)
def auth(client_id: t.Optional[str], client_secret: t.Optional[str]):
    AuthHandler.write(client_id=client_id, client_secret=client_secret)


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
    help="Use this command to get an individual post's data including its comments.",
)
@click.argument("id")
@click.option("--info", is_flag=True, help="Get post info (w/o comments)")
@click.option("--comments", is_flag=True, help="Get post comments")
@global_options
@click.pass_context
def post(ctx: click.Context, id: str, info: bool, comments: bool):
    export: str = ctx.obj["export"]

    r_post = Post(id=id)
    method_map: t.Dict = {
        "comments": lambda session, status, logger: r_post.comments(status=status),
        "info": lambda session, status, logger: r_post.info(status=status),
    }

    run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        info=info,
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

    time_filter: TIME_FILTERS = ctx.obj["time_filter"]
    sort: SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    method_map: t.Dict = {
        "best": lambda session, status, logger: Posts.best(
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "controversial": lambda session, status, logger: Posts.controversial(
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "front_page": lambda session, status, logger: Posts.front_page(
            limit=limit, status=status, logger=logger, session=session
        ),
        "new": lambda session, status, logger: Posts.new(
            limit=limit, status=status, logger=logger, session=session
        ),
        "top": lambda session, status, logger: Posts.top(
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "rising": lambda session, status, logger: Posts.rising(
            limit=limit, status=status, logger=logger, session=session
        ),
    }

    run(
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

    sort: SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    search = Search(
        query=query,
    )
    method_map: t.Dict = {
        "posts": lambda session, status, logger: search.posts(
            limit=limit, status=status, logger=logger, session=session
        ),
        "subreddits": lambda session, status, logger: search.subreddits(
            limit=limit, logger=logger, session=session, status=status
        ),
        "users": lambda session, status, logger: search.users(
            limit=limit, status=status, logger=logger, session=session
        ),
    }

    run(
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
@click.option("--comments", is_flag=True, help="Get comments")
@click.option(
    "--moderated",
    is_flag=True,
    help="Get moderated subreddits",
)
@click.option("--overview", is_flag=True, help="Get most recent comments")
@click.option("--posts", is_flag=True, help="Get posts")
@click.option("--profile", is_flag=True, help="Get profile")
@click.option(
    "--top-subreddits",
    type=int,
    help="Get top n subreddits",
)
@global_options
@click.pass_context
def user(
    ctx: click.Context,
    username: str,
    comments: bool,
    moderated: bool,
    overview: bool,
    posts: bool,
    profile: bool,
    top_subreddits: int,
):
    time_filter: TIME_FILTERS = ctx.obj["time_filter"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    listing: LISTINGS = ctx.obj["listing"]

    r_user = User(username=username)
    method_map: t.Dict = {
        "comments": lambda status, logger: r_user.comments(
            limit=limit, listing=listing, status=status, logger=logger
        ),
        "moderated": lambda status, logger: r_user.moderated(
            status=status, logger=logger
        ),
        "overview": lambda status, logger: r_user.overview(
            status=status, logger=logger
        ),
        "posts": lambda status, logger: r_user.posts(
            limit=limit, listing=listing, status=status, logger=logger
        ),
        "profile": lambda status, logger: r_user.profile(status=status, logger=logger),
        "top_subreddits": lambda status, logger: r_user.top_subreddits(
            top_n=top_subreddits, status=status, logger=logger
        ),
    }

    run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        comments=comments,
        moderated=moderated,
        overview=overview,
        posts=posts,
        profile=profile,
        top_subreddits=top_subreddits,
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
    time_filter: TIME_FILTERS = ctx.obj["time_filter"]
    limit: int = ctx.obj["limit"]

    method_map: t.Dict = {
        "all": lambda session, status, logger: Users.all(
            logger=logger,
            session=session,
            limit=limit,
            status=status,
        ),
        "new": lambda session, status, logger: Users.new(
            logger=logger,
            session=session,
            limit=limit,
            status=status,
        ),
        "popular": lambda session, status, logger: Users.popular(
            logger=logger,
            session=session,
            limit=limit,
            status=status,
        ),
    }

    run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        all=all,
        new=new,
        popular=popular,
    )


@cli.command(
    name="subreddit",
    help="Get data from a specified subreddit.",
)
@click.argument("display_name")
@click.option("--comments", is_flag=True, type=str, help="Get comments")
@click.option("--posts", is_flag=True, help="Get posts")
@click.option("--profile", is_flag=True, help="Get profile")
@click.option("--search", type=str, help="Search for posts that match a query")
@click.option("--wiki-pages", is_flag=True, help="Get wiki pages")
@global_options
@click.pass_context
def subreddit(
    ctx: click.Context,
    display_name: str,
    comments: bool,
    posts: bool,
    profile: bool,
    search: str,
    wiki_pages: bool,
):
    time_filter: TIME_FILTERS = ctx.obj["time_filter"]
    sort: SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]
    listing: LISTINGS = ctx.obj["listing"]

    r_subreddit = Subreddit(display_name=display_name)
    method_map = {
        "comments": lambda status, logger: r_subreddit.comments(
            limit=limit, status=status, logger=logger
        ),
        "posts": lambda status, logger: r_subreddit.posts(
            limit=limit, listing=listing, status=status, logger=logger
        ),
        "profile": lambda status, logger: r_subreddit.profile(
            status=status, logger=logger
        ),
        "search": lambda status, logger: r_subreddit.search(
            query=search,
            limit=limit,
            sort=sort,
            time_filter=time_filter,
            status=status,
            logger=logger,
        ),
        "wiki_pages": lambda status, logger: r_subreddit.wiki_pages(
            status=status, logger=logger
        ),
    }
    run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        comments=comments,
        profile=profile,
        posts=posts,
        search=search,
        wiki_pages=wiki_pages,
        listing=listing,
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

    run(
        ctx=ctx,
        method_map=method_map,
        export=export,
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
