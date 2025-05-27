import asyncio
import inspect
import os
import typing as t
from datetime import datetime

import aiohttp
import rich_click as click
from rich.status import Status

from knewkarma.core.client import reddit
from toolbox import colours
from toolbox.data import Data
from toolbox.logging import console
from toolbox.render import Render
from toolbox.runtime import Runtime
from ..core.user import User
from ..core.users import Users
from ..metadata.about import Project
from ..metadata.license import License
from ..metadata.version import Version

__all__ = ["start"]


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


@click.command(
    name="license", help="Use this command to get licen[cs]e related information."
)
@click.option("-c", "--conditions", is_flag=True, help="Get licen[cs]e warranty.")
@click.option("-w", "--warranty", is_flag=True, help="Get licen[cs]e conditions.")
@click.pass_context
def _license(ctx: click.Context, conditions: bool, warranty: bool):
    """
    Callback function for the `license` command.
    """
    if conditions:
        console.print(License.conditions, justify="center")
    elif warranty:
        console.print(License.warranty, justify="center")
    else:
        click.echo(ctx.command.get_usage(ctx=ctx))


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
    help=f"<bulk/semi-bulk> Maximum data output limit (maximum is 100 if searching for users)",
)
@click.option(
    "--sort",
    default="all",
    show_default=True,
    type=click.Choice(t.get_args(reddit.SORT)),
    help=f"<bulk/semi-bulk> Sort criterion",
)
@click.option(
    "--timeframe",
    default="all",
    show_default=True,
    type=click.Choice(t.get_args(reddit.TIMEFRAME)),
    help=f"<bulk/semi-bulk> Timeframe to get data from",
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
    export: t.List[Data.EXPORT_FORMATS],
):
    """
    Main CLI group for Knew Karma.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param timeframe: Option to set the timeframe for the data.
    :type timeframe: t.Literal[str]
    :param sort: Option to set the sort criterion for the data.
    :type sort: t.Literal[str]
    :param limit: Option to set output data limit.
    :type limit: int
    :param export: Option to set data export file types.
    :type export: t.Literal[str]
    """

    ctx.ensure_object(t.Dict)
    ctx.obj["timeframe"] = timeframe
    ctx.obj["sort"] = sort
    ctx.obj["limit"] = limit

    ctx.obj["export"] = export


cli.add_command(cmd=_license, name="license")


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
            top_subreddits=top_subreddits,
            is_username_available=is_username_available,
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


async def method_caller(
    method: t.Callable,
    **kwargs: t.Union[str, click.Context, aiohttp.ClientSession, Status],
):
    """
    Calls a method with the provided arguments, filtering only those
    that are accepted by the method.

    :param method: A method to call.
    :type method: t.Callable
    :param kwargs: Additional keyword arguments such as:
        - export: str
        - status: rich.status.Status
        - session: aiohttp.ClientSession
        - argument: str
        - ctx: click.Context
        - logger: logging.Logger (optional)
    """

    session = kwargs.get("session")
    status = kwargs.get("status")
    ctx: click.Context = kwargs.get("ctx")
    command: str = ctx.command.name
    argument: str = kwargs.get("argument")

    # 🔍 Filter out only those kwargs that the method actually accepts
    sig = inspect.signature(method)
    accepted_kwargs = {
        key: value for key, value in kwargs.items() if key in sig.parameters
    }

    # 👇 Add direct assignment variables to the accepted args if needed
    if "session" in sig.parameters:
        accepted_kwargs["session"] = session
    if "status" in sig.parameters:
        accepted_kwargs["status"] = status
    if "logger" in sig.parameters:
        accepted_kwargs["logger"] = kwargs.get("logger")

    # 🧠 Actually call the method
    response_data: t.Union[t.List, t.Dict, str, bool, t.Any] = await method(
        **accepted_kwargs
    )

    if response_data:
        Render.show(data=response_data)

        if kwargs.get("export"):
            exports_child_dir: str = os.path.join(
                Data.EXPORTS_PARENT_DIR,
                "exports",
                command,
                argument,
            )

            Data.pathfinder(
                directories=[
                    os.path.join(exports_child_dir, extension)
                    for extension in ["csv", "html", "json", "xml"]
                ],
            )

            export_to: t.List[str] = kwargs.get("export").split(",")
            dataframe = Data.make_dataframe(data=response_data)
            Data.export_dataframe(
                dataframe=dataframe,
                filename=Data.filename_timestamp(),
                directory=exports_child_dir,
                formats=export_to,
            )


async def method_call_handler(
    ctx: click.Context,
    method_map: t.Dict,
    export: str,
    **kwargs: t.Union[str, int, bool],
):
    """
    Handle the method calls based on the provided arguments.

    :param ctx: The Click context object.
    :type ctx: click.Context
    :param method_map: t.Dictionary mapping method names to their corresponding functions.
    :type method_map: t.Dict
    :param export: The export format.
    :type export: str
    :param kwargs: Additional keyword arguments.
    :type kwargs: t.Union[str, int, bool]
    """

    from toolbox.logging import logger

    is_valid_arg: bool = False

    for argument, method in method_map.items():
        if kwargs.get(argument):
            is_valid_arg = True
            start_time: datetime = datetime.now()
            try:
                console.print(License.notice, justify="center")
                with Status(
                    status=f"Starting",
                    console=console,
                ) as status:
                    async with aiohttp.ClientSession() as session:
                        # logger.info(f"◉ Session opened.")
                        # await Runtime.check_updates(session=session, status=status)
                        await reddit.infra_status(
                            session=session,
                            status=status,
                            logger=logger,
                        )

                        await method_caller(
                            method=method,
                            session=session,
                            status=status,
                            logger=logger,
                            ctx=ctx,
                            export=export,
                            argument=argument,
                        )
            except aiohttp.ClientConnectionError as connection_error:
                logger.error(
                    f"[{colours.BOLD_RED}✘{colours.BOLD_RED_RESET}] A connection error occurred: {connection_error}"
                )
            except aiohttp.ClientResponseError as response_error:
                logger.error(
                    f"[{colours.BOLD_RED}✘{colours.BOLD_RED_RESET}] A response error occurred: {response_error}"
                )

            finally:
                elapsed_time = datetime.now() - start_time
                console.print(
                    f"{colours.ITALIC}END. {elapsed_time.total_seconds():.2f} seconds elapsed.{colours.RESET}",
                    justify="center",
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
