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
from .api import Api, SORT_CRITERION, TIMEFRAME, TIME_FORMAT
from .help import Help
from .tools.data_utils import create_dataframe, export_dataframe, show_exported_files
from .tools.general_utils import (
    console,
    pathfinder,
    print_banner,
)
from .tools.time_utils import filename_timestamp
from .version import Version


def parse_arguments() -> (
    tuple[argparse.ArgumentParser, argparse.ArgumentParser.parse_args]
):
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
        help="get a user's posts that match with the specified search query",
        type=str,
    )
    user_parser.add_argument(
        "-sc",
        "--search-comments",
        dest="search_comments",
        help="get a user's comments that match with the specified search query",
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

    return main_parser, main_parser.parse_args()


async def method_caller(arguments: argparse.Namespace, method_map: dict):
    """
    Calls command-line arguments' methods based on user-input.

    :param arguments: Argparse namespace object  containing parsed command-line arguments.
    :type arguments: argparse.Namespace
    :param method_map: Mapping of command-line commands to their respective methods
    :type method_map: dict
    """

    with console.status(
        "Establishing connection /w new session[yellow]...[/]", spinner="dots2"
    ) as status:
        async with aiohttp.ClientSession() as session:

            await Api().update_checker(session=session)

            module_action = method_map.get(arguments.module)
            directory: str = ""
            for action, method in module_action:
                arg_is_present: bool = False
                if getattr(arguments, action, False):
                    arg_is_present = True

                    if arguments.export:
                        output_dir: str = os.path.expanduser(
                            os.path.join("~", "knewkarma-output")
                        )
                        # Create path to main directory in which target data files will be exported
                        directory = os.path.join(output_dir, arguments.module, action)

                        # Create file directories for supported data file types
                        pathfinder(
                            directories=[
                                os.path.join(directory, "csv"),
                                os.path.join(directory, "html"),
                                os.path.join(directory, "json"),
                                os.path.join(directory, "xml"),
                            ]
                        )

                    method_data = await method(status=status, session=session)
                    if method_data:
                        dataframe = create_dataframe(data=method_data)
                        console.print(dataframe)

                        if arguments.export:
                            export_dataframe(
                                dataframe=dataframe,
                                filename=filename_timestamp(),
                                directory=directory,
                                formats=arguments.export.split(","),
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
                    f"knewkarma [underline]{arguments.module}[/]: missing one or more expected argument(s)"
                )


def start():
    """
    Main entrypoint for the Knew Karma command-line interface.
    """
    parser, arguments = parse_arguments()

    start_time: datetime = datetime.now()

    limit: int = arguments.limit
    sort: SORT_CRITERION = arguments.sort
    timeframe: TIMEFRAME = arguments.timeframe
    time_format: TIME_FORMAT = arguments.time_format
    search_query: str = arguments.query if hasattr(arguments, "query") else None

    user: User = User(
        username=arguments.username if hasattr(arguments, "username") else None,
        time_format=time_format,
    )
    users: Users = Users(time_format=time_format)
    search: Search = Search(query=search_query, time_format=time_format)
    subreddit: Subreddit = Subreddit(
        subreddit=arguments.subreddit if hasattr(arguments, "subreddit") else None,
        time_format=time_format,
    )
    subreddits: Subreddits = Subreddits(time_format=time_format)
    post: Post = Post(
        post_id=arguments.id if hasattr(arguments, "id") else None,
        post_subreddit=arguments.subreddit if hasattr(arguments, "subreddit") else None,
        time_format=time_format,
    )
    posts: Posts = Posts(time_format=time_format)

    method_map: dict = {
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
                    query=arguments.search,
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
                    page_name=(
                        arguments.wiki_page if hasattr(arguments, "wiki_page") else None
                    ),
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
                    query=arguments.search_posts,
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
                    query=arguments.search_comments,
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
                        arguments.top_subreddits
                        if hasattr(arguments, "top_subreddits")
                        else None
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

    if arguments.module:
        console.clear(home=False)
        print_banner()
        try:
            start_time: datetime = datetime.now()
            asyncio.run(method_caller(arguments=arguments, method_map=method_map))
        except KeyboardInterrupt:
            console.log("[yellow]✘[/] User interruption detected ([yellow]Ctrl+C[/])")
        finally:
            elapsed_time = datetime.now() - start_time
            console.print(
                f"[green]✔[/] DONE. {elapsed_time.total_seconds():.2f} seconds elapsed."
            )
    else:
        parser.print_usage()
