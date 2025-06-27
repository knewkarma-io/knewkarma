import inspect
import os
import random
import typing as t
from datetime import datetime

import requests
import rich_click as click
from prawcore import exceptions
from rich.status import Status
from rich.syntax import Syntax

from tools import colours
from tools.io_handlers import DataFrameHandler, FileHandler
from tools.log_config import console
from tools.log_config import logger
from tools.rich_render import RichRender
from tools.runtime_ops import RuntimeOps
from ..meta.about import Project
from ..meta.version import Version

__all__ = ["run"]

THE_QUOTES: list = [
    "If you stare into the subreddit, the subreddit also stares back into you.",
    "*sigh* some people just want to watch the subreddit burn.",
    "I came here for memes and statistical insight. I’m all out of memes.",
    "You know, analysing Reddit is like herding cats... if the cats were arguing about pineapple on pizza.",
    "*sniffs* Hmmm this data smells like upvote farming.",
    "My code doesn't judge your karma. But I do.",
    "If it’s on r/conspiracy, it’s either the truth or a guy named Greg in his basement. Sometimes both.",
    "Behind every karma point, there’s a good chance someone was just looking for a little internet validation.",
    "My algorithm is 99.7% sure that this post is a cry for help.",
    "A subreddit is like a dumpster fire...",
    "The plural of anecdote is not data. Unless it's from r/AskReddit.",
    "This analysis was brought to you by caffeine, spite, and three deleted comments.",
    "I built this tool to understand Reddit, but now it understands me!",
    "When in doubt, blame the algorithm. That’s what I do.",
]
NORMAL_ERROR_PREFIX: str = f"{colours.RED}⚠{colours.RED_RESET}"
CRITICAL_ERROR_PREFIX: str = f"{colours.BOLD_RED}⚠{colours.BOLD_RED_RESET}"
WARNING_PREFIX: str = f"{colours.BOLD_YELLOW}⚠{colours.BOLD_YELLOW_RESET}"


def get_quote():
    syntax = Syntax(code=random.choice(THE_QUOTES), lexer="text")
    console.print(syntax)


def invoke_method(
    method: t.Callable,
    **kwargs: t.Union[str, click.Context, requests.Session, Status],
):
    """
    Invoke a method with the keyword arguments it accepts, and optionally export the result.

    :param method: The method to invoke.
    :type method: Callable
    :param kwargs: Keyword arguments that may include:
        - ``export`` (str): Comma-separated list of export formats (e.g., "csv,json").
        - ``status`` (Status): A Rich status indicator.
        - ``session`` (requests.Session): An HTTP session to use.
        - ``argument`` (str): The argument that triggered the method.
        - ``ctx`` (click.Context): The Click context object.
        - ``logger`` (logging.Logger): Optional logger.

    :raises ValueError: If the method cannot be called due to argument mismatch or invalid data.

    :return: None
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
    response_data: t.Union[t.List, t.Dict, str, bool, t.Any] = method(**accepted_kwargs)

    if response_data:
        RichRender.panels(data=response_data)
        if kwargs.get("export"):
            exports_child_dir: str = os.path.join(
                FileHandler.PARENT_DIR,
                "exports",
                command,
                argument,
            )

            FileHandler.pathfinder(
                directories=[
                    os.path.join(exports_child_dir, extension)
                    for extension in ["csv", "html", "json", "xml"]
                ],
            )

            export_to: t.List[str] = kwargs.get("export").split(",")
            dataframe = DataFrameHandler.build(data=response_data)
            DataFrameHandler.export(
                dataframe=dataframe,
                filename=FileHandler.time_to_filename(),
                directory=exports_child_dir,
                formats=export_to,
            )


def route_to_method(
    ctx: click.Context,
    method_map: t.Dict,
    export: str,
    **kwargs: t.Union[str, int, bool],
):
    """
    Routes CLI arguments to the appropriate method and delegates execution to `invoke_method`.

    :param ctx: The current Click context.
    :type ctx: click.Context
    :param method_map: A mapping of CLI argument names to their corresponding functions.
    :type method_map: Dict[str, Callable]
    :param export: Comma-separated string indicating desired export formats (e.g. "csv,html").
    :type export: str
    :param kwargs: Parsed CLI arguments (from `click`) that may contain trigger flags for each method.
    :type kwargs: Union[str, int, bool]

    Side Effects:
        - Prints status updates and errors to the console.
        - Displays a license notice.
        - Performs data export if applicable.
        - Logs execution details and exceptions.

    If no valid argument is provided, prints command usage help.
    """
    runtime = RuntimeOps(package_name=Project.package, version_cls=Version)

    is_valid_arg: bool = False

    for argument, method in method_map.items():
        if kwargs.get(argument):
            is_valid_arg = True
            start_time: datetime = datetime.now()
            try:
                runtime.clear_screen()
                console.print(
                    random.choice(THE_QUOTES),
                    justify="center",
                    style=f"{colours.BOLD_WHITE.strip('[,]')} on {colours.ORANGE_RED.strip('[,]')}",
                )
                with Status(
                    status=f"Starting",
                    console=console,
                ) as status:
                    with requests.Session() as session:
                        runtime.check_updates(session=session, status=status)
                        runtime.infra_status(
                            session=session,
                            status=status,
                            logger=logger,
                        )
                        status.update(f"Initialising {ctx.command.name} module...")

                    invoke_method(
                        method=method,
                        status=status,
                        logger=logger,
                        ctx=ctx,
                        export=export,
                        argument=argument,
                    )
            except exceptions.TooManyRequests as too_many_requests:
                logger.warning(
                    f"{WARNING_PREFIX} Woah! Chill out, dude: {too_many_requests}"
                )
            except exceptions.BadRequest as bad_request:
                logger.error(
                    f"{NORMAL_ERROR_PREFIX} A BadRequest error occurred: {bad_request}"
                )
            except exceptions.ServerError as server_error:
                logger.error(
                    f"{NORMAL_ERROR_PREFIX} A ServerError occurred: {server_error}"
                )
            except exceptions.RequestException as response_exception:
                logger.error(
                    f"{NORMAL_ERROR_PREFIX} A ResponseException error occurred: {response_exception}"
                )
            except exceptions.PrawcoreException as prawcore_exception:
                logger.critical(
                    f"{CRITICAL_ERROR_PREFIX} A PrawcoreException error: {prawcore_exception}"
                )
            except Exception as error:
                logger.critical(
                    f"{CRITICAL_ERROR_PREFIX} An unexpected error occurred: {error}"
                )
            finally:
                elapsed_time = datetime.now() - start_time
                console.print(
                    f"END. {elapsed_time.total_seconds():.2f} seconds elapsed.",
                    justify="center",
                    style=f"{colours.BOLD_WHITE.strip('[,]')} on {colours.ORANGE_RED.strip('[,]')}",
                )

    if not is_valid_arg:
        ctx.command.get_usage(ctx=ctx)


def run(
    ctx: click.Context,
    export: str,
    method_map: t.Dict[str, t.Callable],
    **kwargs: t.Any,
):
    """
    Entrypoint to execute a modular CLI command.

    :param ctx: The Click context for the current CLI invocation.
    :type ctx: click.Context
    :param export: Comma-separated string of export formats (e.g., "csv,json").
    :type export: str
    :param method_map: Dictionary mapping CLI argument names to callable functions.
    :type method_map: Dict[str, Callable]
    :param kwargs: Additional keyword arguments passed from Click options/arguments.
    :type kwargs: Any
    """
    route_to_method(
        ctx=ctx,
        method_map=method_map,
        export=export,
        **kwargs,
    )
