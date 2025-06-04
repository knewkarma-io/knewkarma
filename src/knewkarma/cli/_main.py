import typing as t

import rich_click as click

from tools.logging import console
from tools.runtime import Runtime
from . import _exec, _shared
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


def help_callback(ctx: click.Context, _, value: bool):
    """
    Custom callback function for handling the '--help' option in Click commands.

    Additionally, if the application is running as a Snap package, the
    function will pause execution, prompting the user to press any key
    before continuing. This is useful for when the user clicks the Knew Karma icon in application menu.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param value: The value of the custom help option. If True, the help
            message is displayed and the command execution is halted.
    :type value: bool
    """

    if value and not ctx.resilient_parsing:
        click.echo(ctx.get_help())
        if Runtime.is_snap_package():
            click.pause()
        ctx.exit()


@click.group(
    help=f"""
{Project.summary}
    
    
{Project.description}""",
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
@_shared.global_options
@click.pass_context
def cli(
    ctx: click.Context,
):
    """
    Main CLI group for Knew Karma.
    """
    set_window_title()
    ctx.ensure_object(t.Dict)


@cli.command("license")
@click.option("--conditions", help="License terms and conditions.", is_flag=True)
@click.option("--warranty", help="License warranty.", is_flag=True)
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
    help="Use this command to get an individual post's data including its comments, "
    "provided the post's <id> and source <subreddit> are specified.",
)
@click.argument("id")
@click.argument("subreddit")
@click.option("--data", is_flag=True, help="Get post data")
@click.option("--comments", is_flag=True, help="Get post comments")
@_shared.global_options
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

    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    post_instance = Post(id=id, subreddit=subreddit)
    method_map: t.Dict = {
        "comments": lambda session, status, logger: post_instance.comments(
            limit=limit, sort=sort, status=status, logger=logger, session=session
        ),
        "data": lambda session, status, logger: post_instance.data(
            session=session, status=status
        ),
    }

    _exec.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        data=data,
        comments=comments,
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
@_shared.global_options
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

    posts_instance = Posts()
    method_map: t.Dict = {
        "best": lambda session, status, logger: posts_instance.best(
            timeframe=timeframe,
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "controversial": lambda session, status, logger: posts_instance.controversial(
            timeframe=timeframe,
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "front_page": lambda session, status, logger: posts_instance.front_page(
            limit=limit, sort=sort, status=status, logger=logger, session=session
        ),
        "new": lambda session, status, logger: posts_instance.new(
            limit=limit, sort=sort, status=status, logger=logger, session=session
        ),
        "popular": lambda session, status, logger: posts_instance.popular(
            timeframe=timeframe,
            limit=limit,
            status=status,
            logger=logger,
            session=session,
        ),
        "rising": lambda session, status, logger: posts_instance.rising(
            limit=limit, status=status, logger=logger, session=session
        ),
    }

    _exec.run(
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
    help="Use this command for search/discovery of users, subreddits, and posts.",
)
@click.argument("query")
@click.option("--posts", is_flag=True, help="Search posts")
@click.option("--subreddits", is_flag=True, help="Search subreddits")
@click.option("--users", is_flag=True, help="Search users")
@_shared.global_options
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

    search_instance = Search(
        query=query,
    )
    method_map: t.Dict = {
        "posts": lambda session, status, logger: search_instance.posts(
            sort=sort, limit=limit, status=status, logger=logger, session=session
        ),
        "subreddits": lambda session, status, logger: search_instance.subreddits(
            sort=sort, limit=limit, logger=logger, session=session, status=status
        ),
        "users": lambda session, status, logger: search_instance.users(
            sort=sort, limit=limit, status=status, logger=logger, session=session
        ),
    }

    _exec.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        posts=posts,
        subreddits=subreddits,
        users=users,
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
    "--top-subreddits",
    type=int,
    help="Get user's top n subreddits",
)
@click.option(
    "--is-username-available",
    is_flag=True,
    help="Check if the given username is available or taken.",
)
@_shared.global_options
@click.pass_context
def user(
    ctx: click.Context,
    username: str,
    comments: bool,
    moderated_subreddits: bool,
    overview: bool,
    posts: bool,
    profile: bool,
    top_subreddits: int,
    is_username_available: bool,
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
    :param top_subreddits: Number of top subreddits to retrieve.
    :type top_subreddits: int
    :param is_username_available: Flag to check if the given username is available of taken.
    :type is_username_available: bool
    """
    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    user_instance = User(
        name=username,
    )
    method_map: t.Dict = {
        "comments": lambda session, status, logger: user_instance.comments(
            session=session,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
        ),
        "moderated_subreddits": lambda session, status, logger: user_instance.moderated_subreddits(
            logger=logger, session=session, status=status
        ),
        "overview": lambda session, status, logger: user_instance.overview(
            limit=limit, logger=logger, session=session, status=status
        ),
        "posts": lambda session, status, logger: user_instance.posts(
            session=session,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
        ),
        "profile": lambda session, status: user_instance.profile(
            session=session, status=status
        ),
        "top_subreddits": lambda session, status, logger: user_instance.top_subreddits(
            session=session,
            top_n=top_subreddits,
            limit=limit,
            timeframe=timeframe,
            status=status,
            logger=logger,
        ),
        "is_username_available": lambda session, status, logger: user_instance.is_username_available(
            logger=logger, session=session, status=status
        ),
    }

    _exec.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        comments=comments,
        moderated_subreddits=moderated_subreddits,
        overview=overview,
        posts=posts,
        profile=profile,
        top_subreddits=top_subreddits,
        is_username_available=is_username_available,
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
@_shared.global_options
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

    users_instance = Users()
    method_map: t.Dict = {
        "all": lambda session, status, logger: users_instance.all(
            logger=logger,
            session=session,
            limit=limit,
            timeframe=timeframe,
            status=status,
        ),
        "new": lambda session, status, logger: users_instance.new(
            logger=logger,
            session=session,
            limit=limit,
            timeframe=timeframe,
            status=status,
        ),
        "popular": lambda session, status, logger: users_instance.popular(
            logger=logger,
            session=session,
            limit=limit,
            timeframe=timeframe,
            status=status,
        ),
    }

    _exec.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        all=all,
        new=new,
        popular=popular,
    )


@click.command(
    help="Use this command to get a subreddit's data, such as comments, posts, wiki-pages, wiki-page data, and more...",
)
@click.argument("subreddit_name")
@click.option("--search", type=str, help="Search for posts in a subreddit")
@click.option("--profile", is_flag=True, help="Get a subreddit's profile")
@click.option("--posts", is_flag=True, help="Get a subreddit's posts")
@click.option("--wikipage", type=str, help="Get a subreddit's specified wiki page data")
@click.option("--wikipages", is_flag=True, help="Get a subreddit's wiki pages")
@_shared.global_options
@click.pass_context
def subreddit(
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
    :param wikipages: Flag to get the subreddit's wiki pages.
    :type wikipages: bool
    """

    timeframe: reddit.TIMEFRAME = ctx.obj["timeframe"]
    sort: reddit.SORT = ctx.obj["sort"]
    limit: int = ctx.obj["limit"]
    export: str = ctx.obj["export"]

    subreddit_instance = Subreddit(
        name=subreddit_name,
    )
    method_map: t.Dict = {
        "posts": lambda session, status, logger=None: subreddit_instance.posts(
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
            session=session,
        ),
        "profile": lambda session, status: subreddit_instance.profile(
            status=status, session=session
        ),
        "search": lambda session, status, logger: subreddit_instance.search(
            query=search,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            logger=logger,
            session=session,
        ),
        "wikipages": lambda session, status, logger: subreddit_instance.wikipages(
            status=status, session=session
        ),
        "wikipage": lambda session, status, logger: subreddit_instance.wikipage(
            page_name=wikipage, status=status, session=session
        ),
    }
    _exec.run(
        ctx=ctx,
        method_map=method_map,
        export=export,
        profile=profile,
        posts=posts,
        wikipages=wikipages,
        wikipage=wikipage,
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
@_shared.global_options
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

    subreddits_instance = Subreddits()
    method_map: t.Dict = {
        "all": lambda session, status, logger: subreddits_instance.all(
            limit=limit,
            session=session,
            status=status,
            logger=logger,
        ),
        "default": lambda session, status, logger: subreddits_instance.default(
            limit=limit, session=session, status=status
        ),
        "new": lambda session, status, logger: subreddits_instance.new(
            limit=limit, logger=logger, session=session, status=status
        ),
        "popular": lambda session, status, logger: subreddits_instance.popular(
            limit=limit, logger=logger, session=session, status=status
        ),
    }

    _exec.run(
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
