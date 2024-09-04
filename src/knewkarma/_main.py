import re
from collections import Counter
from types import SimpleNamespace
from typing import Literal, Union

import aiohttp

from .api import Api, SORT_CRITERION, TIMEFRAME, TIME_FORMAT
from .extras import plot_bar_chart, visualisation_deps_installed
from .tools.console import Colour
from .tools.general import console
from .tools.parsers import (
    parse_comments,
    parse_subreddits,
    parse_posts,
    parse_users,
    parse_wiki_page,
)

__all__ = [
    "Comment",
    "Post",
    "Posts",
    "Search",
    "Subreddit",
    "Subreddits",
    "User",
    "Users",
]

api = Api()
colour = Colour


class Comment:
    """Represents a Reddit comment and provides methods for interacting with it."""

    pass


class Post:
    """Represents a Reddit post and provides methods for fetching post data and comments."""

    def __init__(self, id: str, subreddit: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Post` instance to fetch the post's data and comments.

        :param id: The ID of the Reddit post to retrieve.
        :type id: str
        :param subreddit: The subreddit where the post was created.
        :type subreddit: str
        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """
        self._id = id
        self._subreddit = subreddit
        self._time_format = time_format
        self._status_template: str = (
            "Fetching {query_type} from post {post_id} in r/{post_subreddit}"
        )

    async def data(
        self, session: aiohttp.ClientSession, status: console.status = None
    ) -> SimpleNamespace:
        """
        Asynchronously retrieves data for a Reddit post, excluding comments.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A `SimpleNamespace` object containing parsed post data.
        :rtype: SimpleNamespace
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="data",
                    post_id=self._id,
                    post_subreddit=self._subreddit,
                )
            )

        post_data: dict = await api.get_entity(
            post_id=self._id,
            post_subreddit=self._subreddit,
            entity_type="post",
            status=status,
            session=session,
        )

        if post_data:
            return parse_posts(
                raw_posts=post_data,
                time_format=self._time_format,
            )

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves comments for a Reddit post.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of comments to retrieve.
        :type limit: int
        :param sort: The sorting criterion for the comments. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed comment data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} comments",
                    post_id=self._id,
                    post_subreddit=self._subreddit,
                )
            )

        comments_data: list = await api.get_posts(
            posts_type="post_comments",
            post_id=self._id,
            post_subreddit=self._subreddit,
            limit=limit,
            sort=sort,
            status=status,
            session=session,
        )

        if comments_data:
            return parse_comments(
                raw_comments=comments_data,
                time_format=self._time_format,
            )


class Posts:
    """Represents Reddit posts and provides methods for retrieving posts from various sources."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Posts` instance for retrieving posts such as 'best', 'controversial',
        'front-page', 'new', 'popular', and 'rising'.

        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """
        self._time_format = time_format
        self._status_template: str = "Fetching {limit} {listing} posts"

    async def best(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves the best posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    listing="best", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        best_posts: list = await api.get_posts(
            posts_type="best",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if best_posts:
            return parse_posts(raw_posts=best_posts, time_format=self._time_format)

    async def controversial(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves the controversial posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    listing="controversial", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        controversial_posts: list = await api.get_posts(
            posts_type="controversial",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if controversial_posts:
            return parse_posts(
                raw_posts=controversial_posts, time_format=self._time_format
            )

    async def front_page(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves the front-page posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    listing="front-page", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        front_page_posts: list = await api.get_posts(
            posts_type="front_page",
            limit=limit,
            timeframe=timeframe,
            sort=sort,
            status=status,
            session=session,
        )

        if front_page_posts:
            return parse_posts(
                raw_posts=front_page_posts, time_format=self._time_format
            )

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves the new posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    listing="new", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        new_posts: list = await api.get_posts(
            posts_type="new",
            limit=limit,
            timeframe=timeframe,
            sort=sort,
            status=status,
            session=session,
        )

        if new_posts:
            return parse_posts(raw_posts=new_posts, time_format=self._time_format)

    async def popular(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves the popular posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    listing="popular", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        popular_posts: list = await api.get_posts(
            posts_type="popular",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if popular_posts:
            return parse_posts(raw_posts=popular_posts, time_format=self._time_format)

    async def rising(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves the rising posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    listing="rising", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        rising_posts: list = await api.get_posts(
            posts_type="rising",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if rising_posts:
            return parse_posts(raw_posts=rising_posts, time_format=self._time_format)


class Search:
    """
    Represents the Reddit search functionality and provides methods for retrieving search results
    from different entities.
    """

    def __init__(self, query: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Search` instance for searching posts, subreddits, and users.

        :param query: The search query string.
        :type query: str
        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """
        self._query = query
        self._time_format = time_format
        self._status_template: str = "Searching for '{query}' in {limit} {query_type}"

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Searches for posts based on the query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param sort: Sorting criterion for the results. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="posts",
                    limit=f"{colour.cyan}{limit}{colour.reset}",
                    query=self._query,
                )
            )

        posts_results: list = await api.search_entities(
            query=self._query,
            entity_type="posts",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )
        if posts_results:
            return parse_posts(raw_posts=posts_results, time_format=self._time_format)

    async def subreddits(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Searches for subreddits based on the query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to retrieve.
        :type limit: int
        :param sort: Sorting criterion for the results. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed subreddit data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="subreddits",
                    limit=f"{colour.cyan}{limit}{colour.reset}",
                    query=self._query,
                )
            )

        search_subreddits: list = await api.search_entities(
            query=self._query,
            entity_type="subreddits",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )

        if search_subreddits:
            return parse_subreddits(
                raw_subreddits=search_subreddits, time_format=self._time_format
            )

    async def users(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Searches for users based on the query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of users to retrieve.
        :type limit: int
        :param sort: Sorting criterion for the results. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed user data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="users",
                    limit=f"{colour.cyan}{limit}{colour.reset}",
                    query=self._query,
                )
            )

        search_users: list[dict] = await api.search_entities(
            query=self._query,
            entity_type="users",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )

        if search_users:
            return parse_users(raw_users=search_users, time_format=self._time_format)


class Subreddit:
    """Represents a Reddit community (subreddit) and provides methods for retrieving its data."""

    def __init__(self, name: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Subreddit` instance to get a subreddit's profile, wiki pages, and posts data,
        and to search for posts containing a specified query.

        :param name: The name of the subreddit to retrieve data from.
        :type name: str
        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """
        self._name = name
        self._time_format = time_format
        self._status_template: str = (
            "Fetching {query_type} from subreddit r/{subreddit}"
        )

    async def comments(
        self,
        session: aiohttp.ClientSession,
        posts_limit: int,
        comments_per_post: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves comments from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param posts_limit: Maximum number of posts to retrieve comments from.
        :type posts_limit: int
        :param comments_per_post: Maximum number of comments to retrieve per post.
        :type comments_per_post: int
        :param sort: Sorting criterion for the posts and comments. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param timeframe: The timeframe from which to retrieve posts and comments. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed comment data.
        :rtype: list[SimpleNamespace]
        """
        posts = await self.posts(
            session=session,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
        )
        all_comments: list = []
        for post in posts:
            post = Post(
                id=post.get("id"),
                subreddit=post.get("subreddit"),
                time_format=self._time_format,
            )
            post_comments: list = await post.comments(
                session=session, limit=comments_per_post, sort=sort, status=status
            )

            all_comments.extend(post_comments)

        return all_comments

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously retrieves posts from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param sort: Sorting criterion for the posts. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: list[SimpleNamespace]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} posts",
                    subreddit=self._name,
                )
            )

        subreddit_posts: list = await api.get_posts(
            posts_type="subreddit_posts",
            subreddit=self._name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if subreddit_posts:
            return parse_posts(raw_posts=subreddit_posts, time_format=self._time_format)

    async def profile(
        self,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> SimpleNamespace:
        """
        Asynchronously retrieves a subreddit's profile data.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `console.status` object for displaying status messages.
        :type status: rich.console.Console.status, optional
        :return: A `SimpleNamespace` object containing the parsed subreddit profile data.
        :rtype: SimpleNamespace
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="profile data", subreddit=self._name
                )
            )

        subreddit_profile: dict = await api.get_entity(
            entity_type="subreddit",
            subreddit=self._name,
            status=status,
            session=session,
        )
        if subreddit_profile:
            return parse_subreddits(
                raw_subreddits=subreddit_profile, time_format=self._time_format
            )

    async def search_comments(
        self,
        session: aiohttp.ClientSession,
        query: str,
        posts_limit: int,
        comments_per_post: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get comments that contain the specified query string from a subreddit.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param query: Search query.
        :type query: str
        :param posts_limit: Maximum number of posts to get comments from.
        :type posts_limit: int
        :param comments_per_post: A maximum number of comments to get for each post.
        :type comments_per_post: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: list[dict]
        """
        posts: list = await self.posts(
            session=session,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
        )
        all_comments: list = []
        found_comments: list = []
        for post in posts:
            if status:
                status.update(f"Fetching comments from post {post.get('id')}")

            post = Post(
                id=post.get("id"),
                subreddit=self._name,
                time_format=self._time_format,
            )

            comments: list = await post.comments(
                session=session, limit=comments_per_post, status=status
            )

            all_comments.extend(comments)

        pattern: str = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        for comment in all_comments:
            match: re.Match = regex.search(comment.get("body", ""))
            if match:
                found_comments.append(comment)

        if found_comments:
            return found_comments

    async def search_posts(
        self,
        session: aiohttp.ClientSession,
        query: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get posts that contain the specified query string from a subreddit.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} posts with '{query}'",
                    subreddit=self._name,
                )
            )
        found_posts: list = await api.get_posts(
            posts_type="search_subreddit_posts",
            subreddit=self._name,
            query=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if found_posts:
            return parse_posts(raw_posts=found_posts, time_format=self._time_format)

    async def wiki_pages(
        self,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> list[str]:
        """
        Asynchronously get a subreddit's wiki pages.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="wiki pages", subreddit=self._name
                )
            )

        pages: dict = await api.make_request(
            endpoint=f"{api.subreddit_endpoint}/{self._name}/wiki/pages.json",
            session=session,
        )

        return pages.get("data")

    async def wiki_page(
        self,
        page_name: str,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> SimpleNamespace:
        """
        Asynchronously get a subreddit's specified wiki page data.

        :param page_name: Wiki page to get data from.
        :type page_name: str
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="wiki page data", subreddit=self._name
                )
            )

        wiki_page: dict = await api.get_entity(
            entity_type="wiki_page",
            page_name=page_name,
            subreddit=self._name,
            status=status,
            session=session,
        )

        if wiki_page:
            return parse_wiki_page(wiki_page=wiki_page, time_format=self._time_format)


class Subreddits:
    """Represents Reddit subreddits and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Subreddits()` instance for getting `all`, `default`, `new` and `popular` subreddits.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._time_format = time_format
        self._status_template: str = "Fetching {limit} {subreddits_type} subreddits"

    async def all(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get all subreddits.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get all subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]

        Note:
            -*imitating Morphius' voice*- "the only limitation you have at this point is the matrix's rate-limit."
        """
        if status:
            status.update(
                self._status_template.format(
                    subreddits_type="all", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        all_subreddits: list = await api.get_subreddits(
            subreddits_type="all",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if all_subreddits:
            return parse_subreddits(
                raw_subreddits=all_subreddits, time_format=self._time_format
            )

    async def default(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    subreddits_type="default",
                    limit=f"{colour.cyan}{limit}{colour.reset}",
                )
            )

        default_subreddits: list = await api.get_subreddits(
            subreddits_type="default",
            timeframe="all",
            limit=limit,
            status=status,
            session=session,
        )
        if default_subreddits:
            return parse_subreddits(default_subreddits, time_format=self._time_format)

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get new subreddits.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    subreddits_type="new", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        new_subreddits: list = await api.get_subreddits(
            subreddits_type="new",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if new_subreddits:
            return parse_subreddits(new_subreddits, time_format=self._time_format)

    async def popular(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get popular subreddits.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    subreddits_type="popular",
                    limit=f"{colour.cyan}{limit}{colour.reset}",
                )
            )

        popular_subreddits: list = await api.get_subreddits(
            subreddits_type="popular",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if popular_subreddits:
            return parse_subreddits(popular_subreddits, time_format=self._time_format)


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, name: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `User()` instance for getting a user's `profile`, `posts` and `comments` data.

        :param name: Username to get data from.
        :type name: str
        :param time_format: Time format of the output data. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._name = name
        self._time_format = time_format
        self._status_template: str = "Fetching {query_type} from user u/{username}"

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get a user's comments.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which tyo get comments.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} comments",
                    username=self._name,
                )
            )

        user_comments: list = await api.get_posts(
            username=self._name,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if user_comments:
            return parse_comments(
                raw_comments=user_comments, time_format=self._time_format
            )

    async def moderated_subreddits(
        self,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get subreddits moderated by user.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="moderated subreddits", username=self._name
                )
            )

        subreddits: dict = await api.get_subreddits(
            subreddits_type="user_moderated",
            username=self._name,
            limit=0,
            status=status,
            session=session,
        )

        if subreddits:
            return parse_subreddits(
                subreddits.get("data"),
                time_format=self._time_format,
            )

    async def overview(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing data about a recent comment.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} recent comments",
                    username=self._name,
                )
            )

        user_overview: list = await api.get_posts(
            username=self._name,
            posts_type="user_overview",
            limit=limit,
            status=status,
            session=session,
        )

        if user_overview:
            return parse_comments(user_overview, time_format=self._time_format)

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get a user's posts.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} posts",
                    username=self._name,
                )
            )

        user_posts: list = await api.get_posts(
            username=self._name,
            posts_type="user_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if user_posts:
            return parse_posts(user_posts, time_format=self._time_format)

    async def profile(
        self,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> SimpleNamespace:
        """
        Asynchronously get a user's profile data.

        :param session: A aiohttp.ClientSession session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A dictionary containing user profile data.
        :rtype: dict
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="profile data", username=self._name
                )
            )

        user_profile: dict = await api.get_entity(
            username=self._name, entity_type="user", status=status, session=session
        )

        if user_profile:
            return parse_users(raw_users=user_profile, time_format=self._time_format)

    async def search_posts(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get a user's posts that match with the specified search query.

        :param query: Search query.
        :type query: str
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to search from.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} posts for '{query}'",
                    username=self._name,
                )
            )

        pattern: str = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        user_posts: list = await api.get_posts(
            posts_type="user_posts",
            username=self._name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        found_posts: list = []

        for post in user_posts:
            post_data: dict = post.get("data")

            match: re.Match = regex.search(post_data.get("title", "")) or regex.search(
                post_data.get("selftext", "")
            )

            if match:
                found_posts.append(post)

        if found_posts:
            return parse_posts(found_posts, time_format=self._time_format)

    async def search_comments(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get a user's comments that contain the specified search query.

        :param query: Search query.
        :type query: str
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to search from.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which to get comments.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{colour.cyan}{limit}{colour.reset} comments for '{query}'",
                    username=self._name,
                )
            )

        pattern: str = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        user_comments: list = await api.get_posts(
            username=self._name,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        found_comments: list = []

        for comment in user_comments:
            match = regex.search(comment.get("data", {}).get("body", ""))
            if match:
                found_comments.append(comment)

        if found_comments:
            return parse_comments(found_comments, time_format=self._time_format)

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        filename: str = None,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> Union[list[tuple[str, int]], None]:
        """
        Asynchronously get a user's top n subreddits based on subreddit frequency in n posts and saves the analysis to a file.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param top_n: Communities arranging number.
        :type top_n: int
        :param limit: Maximum number of posts to scrape.
        :type limit: int
        :param filename: Filename to which the analysis will be saved.
        :type filename: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"top {colour.cyan}{top_n}{colour.reset}/{colour.cyan}{limit}{colour.reset} subreddits",
                    username=self._name,
                )
            )

        posts = await api.get_posts(
            posts_type="user_posts",
            username=self._name,
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if posts:
            # Extract subreddit names
            subreddits: list = [post.get("data", {}).get("subreddit") for post in posts]

            # Count the occurrences of each subreddit
            subreddit_counts: Counter = Counter(subreddits)

            # Get the most common subreddits
            top_subreddits: list[tuple[str, int]] = subreddit_counts.most_common(top_n)

            # Prepare data for plotting
            subreddit_names: list = [subreddit[0] for subreddit in top_subreddits]
            subreddit_frequencies: list = [subreddit[1] for subreddit in top_subreddits]

            if visualisation_deps_installed:
                plot_bar_chart(
                    data=dict(zip(subreddit_names, subreddit_frequencies)),
                    title=f"top {top_n}/{limit} subreddits analysis",
                    xlabel="Subreddits",
                    ylabel="Frequency",
                    figure_size=(top_n + 10, 5),
                    colours=["lightblue"] * top_n,
                    filename=f"{filename + '_' if filename else ''}top_{top_n}_of_{limit}_subreddits",
                )
            else:
                return top_subreddits


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Users()` instance for getting `new`, `popular` and `all` users.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._time_format = time_format
        self._status_template: str = "Fetching {limit} {query_type} users"

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get new users.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of new users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="new", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        new_users: list = await api.get_users(
            users_type="new",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if new_users:
            return parse_users(new_users, time_format=self._time_format)

    async def popular(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get popular users.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of popular users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="popular", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        popular_users: list = await api.get_users(
            users_type="popular",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if popular_users:
            return parse_users(popular_users, time_format=self._time_format)

    async def all(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[SimpleNamespace]:
        """
        Asynchronously get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="all", limit=f"{colour.cyan}{limit}{colour.reset}"
                )
            )

        all_users: list = await api.get_users(
            users_type="all",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if all_users:
            return parse_users(all_users, time_format=self._time_format)


# -------------------------------- END ----------------------------------------- #
