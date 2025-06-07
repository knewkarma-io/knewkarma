import functools
import typing as t

import rich_click as click

from ..core.client import reddit

__all__ = ["global_options"]


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
        **kwargs
    ):
        ctx.ensure_object(dict)
        ctx.obj["timeframe"] = timeframe
        ctx.obj["sort"] = sort
        ctx.obj["limit"] = limit
        ctx.obj["export"] = export
        return ctx.invoke(func, *args, **kwargs)

    return wrapper
