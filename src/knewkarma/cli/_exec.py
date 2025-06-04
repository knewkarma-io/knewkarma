import inspect
import os
import typing as t
from datetime import datetime

import click
import requests
from rich.status import Status

from tools import colours
from tools.io_assets import FileHandler, DataFrame
from tools.logging import console
from tools.render import Render
from ..core.client import reddit
from ..meta.license import License

__all__ = ["run"]


def _method_caller(
    method: t.Callable,
    **kwargs: t.Union[str, click.Context, requests.Session, Status],
):
    """
    Calls a method with the provided arguments, filtering only those
    that are accepted by the method.

    :param method: A method to call.
    :type method: t.Callable
    :param kwargs: Additional keyword arguments such as:
        - export: str
        - status: rich.status.Status
        - session: requests.Session
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
    response_data: t.Union[t.List, t.Dict, str, bool, t.Any] = method(**accepted_kwargs)

    if response_data:
        Render.show(data=response_data)
        if kwargs.get("export"):
            exports_child_dir: str = os.path.join(
                FileHandler.EXPORTS_PARENT_DIR,
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
            dataframe = DataFrame.build(data=response_data)
            DataFrame.export(
                dataframe=dataframe,
                filename=FileHandler.time_to_filename(),
                directory=exports_child_dir,
                formats=export_to,
            )


def _method_call_handler(
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

    from tools.logging import logger

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
                    with requests.Session() as session:
                        # logger.info(f"◉ Session opened.")
                        # Runtime.check_updates(session=session, status=status)
                        reddit.infra_status(
                            session=session,
                            status=status,
                            logger=logger,
                        )

                        _method_caller(
                            method=method,
                            session=session,
                            status=status,
                            logger=logger,
                            ctx=ctx,
                            export=export,
                            argument=argument,
                        )
            except requests.exceptions.ConnectionError as connection_error:
                logger.error(
                    f"{colours.BOLD_RED}⚠{colours.BOLD_RED_RESET} A connection error occurred: {connection_error}"
                )
            except requests.exceptions.HTTPError as response_error:
                logger.error(
                    f"{colours.BOLD_RED}⚠{colours.BOLD_RED_RESET} An HTTP error occurred: {response_error}"
                )
            finally:
                elapsed_time = datetime.now() - start_time
                console.print(
                    f"{colours.ITALIC}END... {elapsed_time.total_seconds():.2f} seconds elapsed{colours.RESET}",
                    justify="center",
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
    Wraps the call to method_call_handler.
    """
    _method_call_handler(
        ctx=ctx,
        method_map=method_map,
        export=export,
        **kwargs,
    )
