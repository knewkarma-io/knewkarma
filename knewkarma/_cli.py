import argparse
import asyncio
import os
from datetime import datetime
from typing import get_args

import aiohttp
from rich.markdown import Markdown
from rich.tree import Tree
from rich_argparse import RichHelpFormatter

from . import Post, Posts, Search, Subreddit, Subreddits, User, Users
from .api import Api, SORT_CRITERION, TIMEFRAME
from .help import Help
from .tools.data_utils import create_dataframe, export_dataframe, show_exported_files
from .tools.general_utils import (
    console,
    pathfinder,
    print_banner,
)
from .tools.time_utils import filename_timestamp
from .version import Version


def args_parser() -> argparse.ArgumentParser:
    """
    Creates and configures an argument parser for the command line arguments.

    :return: A configured argparse.ArgumentParser object ready to parse the command line arguments.
    :rtype: argparse.ArgumentParser
    """
    main_parser = argparse.ArgumentParser(
        description=Markdown(Help.summary, style="argparse.text"),
        epilog=Markdown(Help.description),
        formatter_class=RichHelpFormatter,
    )
    subparsers = main_parser.add_subparsers(dest="module", help="module")
    main_parser.add_argument(
        "-t",
        "--timeframe",
        type=str,
        default="all",
        choices=list(get_args(TIMEFRAME)),
        help="([bold][green]bulk/semi-bulk[/][/]) timeframe to get data from (default: [green]%(default)s[/])",
    )
    main_parser.add_argument(
        "-s",
        "--sort",
        type=str,
        default="all",
        choices=list(get_args(SORT_CRITERION)),
        help="([bold][green]bulk/semi-bulk[/][/]) sort criterion (default: [green]%(default)s[/])",
    )
    main_parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=100,
        help="([bold][green]bulk/semi-bulk[/][/]) data output limit (default: [cyan]%(default)s[/])",
    )
    main_parser.add_argument(
        "--time-format",
        default="locale",
        help="determines the format of the output time (default: [green]%(default)s[/])",
        choices=["concise", "locale"],
    )
    main_parser.add_argument(
        "-e",
        "--export",
        type=str,
        help="a comma-separated list of file types to export the output to (supported: [green]csv,html,json,xml[/])",
    )
    main_parser.add_argument(
        "-v",
        "--version",
        version=Markdown(f"Knew Karma {Version.release} {Help.copyright}"),
        action="version",
    )

    post_parser = subparsers.add_parser(
        "post",
        help="post module ([bold][green]semi-bulk[/][/])",
        description=Markdown(
            "**Post Module**: *Pull an individual post's data*",
            style="argparse.text",
        ),
        epilog=Markdown(Help.examples["post"]),
        formatter_class=RichHelpFormatter,
    )

    post_parser.add_argument("id", help="post id", type=str)
    post_parser.add_argument("subreddit", help="post source subreddit", type=str)
    post_parser.add_argument("-d", "--data", help="get post data", action="store_true")
    post_parser.add_argument(
        "-c", "--comments", help="get post comments", action="store_true"
    )

    posts_parser = subparsers.add_parser(
        "posts",
        help="posts module ([bold][green]bulk[/][/])",
        description=Markdown(
            "**Posts**: *Pull posts from various sources.*", style="argparse.text"
        ),
        epilog=Markdown(Help.examples["posts"]),
        formatter_class=RichHelpFormatter,
    )
    posts_parser.add_argument(
        "-b",
        "--best",
        help="get posts from the [italic]best[/] listing",
        action="store_true",
    )
    posts_parser.add_argument(
        "-c",
        "--controversial",
        help="get posts from the [italic]controversial[/] listing",
        action="store_true",
    )
    posts_parser.add_argument(
        "-f",
        "--front-page",
        help="get posts from the reddit [italic]front-page[/]",
        action="store_true",
    )
    posts_parser.add_argument(
        "-n",
        "--new",
        help="get new posts",
        action="store_true",
    )
    posts_parser.add_argument(
        "-p",
        "--popular",
        help="get posts from the [italic]popular[/] listing",
        action="store_true",
    )
    posts_parser.add_argument(
        "-r",
        "--rising",
        help="get posts from the [italic]rising[/] listing",
        action="store_true",
    )

    search_parser = subparsers.add_parser(
        "search",
        help="search module ([bold][green]bulk[/][/])",
        description=Markdown(
            "**Search**: *Get search results from various sources.*",
            style="argparse.text",
        ),
        epilog=Markdown(Help.examples["search"]),
        formatter_class=RichHelpFormatter,
    )
    search_parser.add_argument("query", help="search query")
    search_parser.add_argument(
        "-p", "--posts", help="search posts", action="store_true"
    )
    search_parser.add_argument(
        "-s", "--subreddits", help="search subreddits", action="store_true"
    )
    search_parser.add_argument(
        "-u", "--users", help="search users", action="store_true"
    )

    subreddit_parser = subparsers.add_parser(
        "subreddit",
        help="subreddit module ([bold][green]semi-bulk[/][/])",
        description=Markdown(
            "**Subreddit**: *Pull a specified subreddit's data.*",
            style="argparse.text",
        ),
        epilog=Markdown(Help.examples["subreddit"]),
        formatter_class=RichHelpFormatter,
    )
    subreddit_parser.add_argument(
        "subreddit",
        help="subreddit name",
    )
    subreddit_parser.add_argument(
        "-p",
        "--profile",
        help="get a subreddit's profile",
        action="store_true",
    )
    subreddit_parser.add_argument(
        "-pp",
        "--posts",
        help="get a subreddit's posts",
        action="store_true",
    )
    subreddit_parser.add_argument(
        "-s",
        "--search",
        help="search posts in a subreddit",
        type=str,
    )

    subreddit_parser.add_argument(
        "-wp",
        "--wiki-page",
        dest="wiki_page",
        help="get a subreddit's specified wiki page data",
        metavar="WIKI_PAGE",
    )
    subreddit_parser.add_argument(
        "-wps",
        "--wiki-pages",
        dest="wiki_pages",
        help="get a subreddit's wiki pages",
        action="store_true",
    )

    subreddits_parser = subparsers.add_parser(
        "subreddits",
        help="subreddits module ([bold][green]bulk[/][/])",
        description=Markdown(
            "**Subreddits**: *Pull subreddits from various sources.*",
            style="argparse.text",
        ),
        epilog=Markdown(Help.examples["subreddits"]),
        formatter_class=RichHelpFormatter,
    )
    subreddits_parser.add_argument(
        "-a",
        "--all",
        help="get all subreddits",
        action="store_true",
    )
    subreddits_parser.add_argument(
        "-d",
        "--default",
        help="get default subreddits",
        action="store_true",
    )
    subreddits_parser.add_argument(
        "-n",
        "--new",
        help="get new subreddits",
        action="store_true",
    )
    subreddits_parser.add_argument(
        "-p",
        "--popular",
        help="get popular subreddits",
        action="store_true",
    )

    user_parser = subparsers.add_parser(
        "user",
        help="user module ([bold][green]semi-bulk[/][/])",
        description=Markdown(
            "**User**: *Pull a specified user's data.*", style="argparse.text"
        ),
        epilog=Markdown(Help.examples["user"]),
        formatter_class=RichHelpFormatter,
    )
    user_parser.add_argument("username", help="username")
    user_parser.add_argument(
        "-c",
        "--comments",
        help="get a user's comments",
        action="store_true",
    )
    user_parser.add_argument(
        "-mc",
        "--moderated-subreddits",
        dest="moderated_subreddits",
        help="get subreddits moderated by the user",
        action="store_true",
    )
    user_parser.add_argument(
        "-o",
        "--overview",
        help="get a user's most recent comment activity",
        action="store_true",
    )
    user_parser.add_argument(
        "-pp",
        "--posts",
        action="store_true",
        help="get a user's posts",
    )
    user_parser.add_argument(
        "-p",
        "--profile",
        help="get a user's profile",
        action="store_true",
    )
    user_parser.add_argument(
        "-sp",
        "--search-posts",
        dest="search_posts",
        help="get a user's posts that contain the specified keyword",
        type=str,
    )
    user_parser.add_argument(
        "-sc",
        "--search-comments",
        dest="search_comments",
        help="get a user's comments that contain the specified keyword",
        type=str,
    )

    user_parser.add_argument(
        "-tc",
        "--top-subreddits",
        dest="top_subreddits",
        metavar="TOP_N",
        type=int,
        help="get a user's top n subreddits based on subreddit frequency in n posts",
    )

    users_parser = subparsers.add_parser(
        "users",
        help="users module ([bold][green]bulk[/][/])",
        description=Markdown(
            "**Users**: *Pull users from various sources.*",
            style="argparse.text",
        ),
        epilog=Markdown(Help.examples["users"]),
        formatter_class=RichHelpFormatter,
    )
    users_parser.add_argument(
        "-a",
        "--all",
        help="get all users",
        action="store_true",
    )
    users_parser.add_argument(
        "-n",
        "--new",
        help="get new users",
        action="store_true",
    )
    users_parser.add_argument(
        "-p",
        "--popular",
        help="get popular users",
        action="store_true",
    )

    return main_parser


async def function_caller(args: argparse.Namespace, function_map: dict):
    """
    Calls command-line arguments' functions based on user-input.

    :param args: Argparse namespace object  containing parsed command-line arguments.
    :type args: argparse.Namespace
    :param function_map: Mapping of command-line commands to their respective functions
    :type function_map: dict
    """

    with console.status(
        "Establishing connection /w new session...", spinner="dots2"
    ) as status:
        async with aiohttp.ClientSession() as session:

            await Api().update_checker(session=session)

            mode_action = function_map.get(args.module)
            directory: str = ""
            for action, function in mode_action:
                arg_is_present: bool = False
                if getattr(args, action, False):
                    arg_is_present = True

                    if args.export:
                        output_dir: str = os.path.expanduser(
                            os.path.join("~", "knewkarma-output")
                        )
                        # Create path to main directory in which target data files will be exported
                        directory = os.path.join(output_dir, args.module, action)

                        # Create file directories for supported data file types
                        pathfinder(
                            directories=[
                                os.path.join(directory, "csv"),
                                os.path.join(directory, "html"),
                                os.path.join(directory, "json"),
                                os.path.join(directory, "xml"),
                            ]
                        )

                    function_data = await function(status=status, session=session)
                    if function_data:
                        dataframe = create_dataframe(data=function_data)

                        # Print the DataFrame, excluding the 'raw_data' column if it exists
                        console.log(dataframe)

                        if args.export:
                            export_dataframe(
                                dataframe=dataframe,
                                filename=filename_timestamp(),
                                directory=directory,
                                formats=args.export.split(","),
                            )

                            # Show exported files
                            tree = Tree(
                                f":open_file_folder: [bold]{directory}[/]",
                                guide_style="bold bright_blue",
                            )
                            show_exported_files(tree=tree, directory=directory)
                            console.log(tree)

                    break

            if not arg_is_present:
                console.log(
                    f"knewkarma [underline]{args.module}[/]: missing one or more expected argument(s)"
                )


def start():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """
    parser = args_parser()
    args = parser.parse_args()

    start_time: datetime = datetime.now()

    limit: int = args.limit
    sort = args.sort
    timeframe = args.timeframe
    time_format = args.time_format

    search_query = args.query if hasattr(args, "query") else None

    user = User(
        username=args.username if hasattr(args, "username") else None,
        time_format=time_format,
    )
    users = Users(time_format=time_format)
    search = Search(query=search_query, time_format=time_format)
    subreddit = Subreddit(
        subreddit=args.subreddit if hasattr(args, "subreddit") else None,
        time_format=time_format,
    )
    subreddits = Subreddits(time_format=time_format)
    post = Post(
        post_id=args.id if hasattr(args, "id") else None,
        post_subreddit=args.subreddit if hasattr(args, "subreddit") else None,
        time_format=time_format,
    )
    posts = Posts(time_format=time_format)

    function_map: dict = {
        "post": [
            ("data", lambda session, status=None: post.data(session=session)),
            (
                "comments",
                lambda session, status=None: post.comments(
                    limit=limit,
                    sort=sort,
                    status=status,
                    session=session,
                ),
            ),
        ],
        "posts": [
            (
                "best",
                lambda session, status=None: posts.best(
                    timeframe=timeframe,
                    limit=limit,
                    status=status,
                    session=session,
                ),
            ),
            (
                "controversial",
                lambda session, status=None: posts.controversial(
                    timeframe=timeframe,
                    limit=limit,
                    status=status,
                    session=session,
                ),
            ),
            (
                "front_page",
                lambda session, status=None: posts.front_page(
                    limit=limit, sort=sort, status=status, session=session
                ),
            ),
            (
                "new",
                lambda session, status=None: posts.new(
                    limit=limit, sort=sort, status=status, session=session
                ),
            ),
            (
                "popular",
                lambda session, status=None: posts.popular(
                    timeframe=timeframe,
                    limit=limit,
                    status=status,
                    session=session,
                ),
            ),
            (
                "rising",
                lambda session, status=None: posts.rising(
                    limit=limit,
                    status=status,
                    session=session,
                ),
            ),
        ],
        "search": [
            (
                "posts",
                lambda session, status=None: search.posts(
                    sort=sort,
                    limit=limit,
                    status=status,
                    session=session,
                ),
            ),
            (
                "subreddits",
                lambda session, status=None: search.subreddits(
                    sort=sort, limit=limit, session=session
                ),
            ),
            (
                "users",
                lambda session, status=None: search.users(
                    sort=sort, limit=limit, status=status, session=session
                ),
            ),
        ],
        "subreddit": [
            (
                "profile",
                lambda session, status=None: subreddit.profile(
                    status=status, session=session
                ),
            ),
            (
                "posts",
                lambda session, status=None: subreddit.posts(
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    status=status,
                    session=session,
                ),
            ),
            (
                "search",
                lambda session, status=None: subreddit.search(
                    query=args.search,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    status=status,
                    session=session,
                ),
            ),
            (
                "wiki_pages",
                lambda session, status=None: subreddit.wiki_pages(
                    status=status, session=session
                ),
            ),
            (
                "wiki_page",
                lambda session, status=None: subreddit.wiki_page(
                    page_name=args.wiki_page if hasattr(args, "wiki_page") else None,
                    status=status,
                    session=session,
                ),
            ),
        ],
        "subreddits": [
            (
                "all",
                lambda session, status=None: subreddits.all(
                    limit=limit, status=status, session=session
                ),
            ),
            (
                "default",
                lambda session, status=None: subreddits.default(
                    limit=limit, status=status, session=session
                ),
            ),
            (
                "new",
                lambda session, status=None: subreddits.new(
                    limit=limit, status=status, session=session
                ),
            ),
            (
                "popular",
                lambda session, status=None: subreddits.popular(
                    limit=limit, status=status, session=session
                ),
            ),
        ],
        "user": [
            (
                "profile",
                lambda session, status=None: user.profile(
                    status=status, session=session
                ),
            ),
            (
                "posts",
                lambda session, status=None: user.posts(
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    status=status,
                    session=session,
                ),
            ),
            (
                "comments",
                lambda session, status=None: user.comments(
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    status=status,
                    session=session,
                ),
            ),
            (
                "overview",
                lambda session, status=None: user.overview(
                    limit=limit, status=status, session=session
                ),
            ),
            (
                "moderated_subreddits",
                lambda session, status=None: user.moderated_subreddits(
                    status=status, session=session
                ),
            ),
            (
                "search_posts",
                lambda session, status=None: user.search_posts(
                    keyword=args.search_posts,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    status=status,
                    session=session,
                ),
            ),
            (
                "search_comments",
                lambda session, status=None: user.search_comments(
                    keyword=args.search_comments,
                    limit=limit,
                    sort=sort,
                    timeframe=timeframe,
                    status=status,
                    session=session,
                ),
            ),
            (
                "top_subreddits",
                lambda session, status=None: user.top_subreddits(
                    top_n=(
                        args.top_subreddits if hasattr(args, "top_subreddits") else None
                    ),
                    limit=limit,
                    timeframe=timeframe,
                    status=status,
                    session=session,
                ),
            ),
        ],
        "users": [
            (
                "all",
                lambda session, status=None: users.all(
                    limit=limit, status=status, session=session
                ),
            ),
            (
                "new",
                lambda session, status=None: users.new(
                    limit=limit, status=status, session=session
                ),
            ),
            (
                "popular",
                lambda session, status=None: users.popular(
                    limit=limit, status=status, session=session
                ),
            ),
        ],
    }

    if args.module:
        print_banner()
        try:
            start_time: datetime = datetime.now()
            asyncio.run(function_caller(args=args, function_map=function_map))
        except KeyboardInterrupt:
            console.log("[yellow]✘[/] User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            elapsed_time = datetime.now() - start_time
            console.log(
                f"[green]✔[/] DONE. {elapsed_time.total_seconds():.2f} seconds elapsed."
            )
    else:
        parser.print_usage()
