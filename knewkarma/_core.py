import re
from collections import Counter

import aiohttp

from .api import Api, TIMEFRAME, SORT_CRITERION
from .tools.cleaning_utils import (
    clean_comments,
    clean_subreddits,
    clean_subreddit_wiki_page,
    clean_posts,
    clean_users,
)
from .tools.general_utils import TIME_FORMAT, get_status

api = Api()


class Post:
    """Represents a Reddit post and provides method(s) for getting data from the specified post."""

    def __init__(
        self, post_id: str, post_subreddit: str, time_format: TIME_FORMAT = "locale"
    ):
        """
        Initialises the `Post()` instance for getting post's `data` and `comments`.

        :param post_id: ID of a post to get data from.
        :type post_id: str
        :param post_subreddit: Subreddit where the post was created.
        :type post_subreddit: str
        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._post_id = post_id
        self._post_subreddit = post_subreddit
        self._time_format = time_format

    async def data(self, session: aiohttp.ClientSession) -> dict:
        """
        Get a post's data (without comments)

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A dictionary containing a post's data.
        :rtype: dict

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Post


            >>> async def async_post_data():
            >>>    post = Post(post_id="13ptwzd", post_subreddit="AskReddit")
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        data = await post.data(session=request_session)
            >>>        print(data)


            >>> asyncio.run(async_post_data())
        """
        post_data: dict = await api.get_entity(
            post_id=self._post_id,
            post_subreddit=self._post_subreddit,
            entity_type="post",
            session=session,
        )

        if post_data:
            return clean_posts(
                data=post_data[0]
                .get("data", {})
                .get("children", [])[0]
                .get("data", {}),
                time_format=self._time_format,
            )

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Get a post's comments.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :return: A list of dictionaries, each containing comment data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Post


            >>> async def async_post_comments(comments_limit, comments_sort):
            >>>    post = Post(post_id="13ptwzd", post_subreddit="AskReddit")
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        comments = await post.comments(limit=comments_limit, sort=comments_sort, session=request_session)
            >>>        print(comments)


            >>> asyncio.run(async_post_comments(comments_limit=50, comments_sort="top"))
        """
        comments_data: list = await api.get_posts(
            posts_type="post_comments",
            post_id=self._post_id,
            post_subreddit=self._post_subreddit,
            limit=limit,
            sort=sort,
            session=session,
        )

        if comments_data:
            return clean_comments(
                comments=comments_data[1].get("data", {}).get("children", []),
                time_format=self._time_format,
            )


class Posts:
    """Represents Reddit posts and provides methods for getting posts from various sources."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Posts()` instance for getting `best`, `controversial`,
        `front-page`, `new`, `popular`, and `rising` posts.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._time_format = time_format

    async def best(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get best posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get best posts.
        :type timeframe: Literal[str]
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_best_posts(posts_timeframe, posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        best = await posts.best(timeframe=posts_timeframe, limit=posts_limit, session=request_session)
            >>>        print(best)


            >>> asyncio.run(async_best_posts(posts_timeframe="all", posts_limit=120))
        """
        best_posts: list = await api.get_posts(
            posts_type="best",
            timeframe=timeframe,
            limit=limit,
            session=session,
        )

        if best_posts:
            return clean_posts(data=best_posts, time_format=self._time_format)

    async def controversial(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get controversial posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get controversial posts.
        :type timeframe: Literal[str]
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_controversial_posts(posts_timeframe, posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        controversial = await posts.controversial(timeframe=posts_timeframe, limit=posts_limit,
            >>>                                                                       session=request_session)
            >>>        print(controversial)


            >>> asyncio.run(async_controversial_posts(posts_timeframe="year", posts_limit=50))
        """
        controversial_posts: list = await api.get_posts(
            posts_type="controversial",
            timeframe=timeframe,
            limit=limit,
            session=session,
        )

        if controversial_posts:
            return clean_posts(data=controversial_posts, time_format=self._time_format)

    async def front_page(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Get posts from the Reddit front-page.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_frontpage_posts(posts_sort, posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        frontpage = await posts.front_page(sort=posts_sort, limit=posts_limit, session=request_session)
            >>>        print(frontpage)


            >>> asyncio.run(async_frontpage_posts(posts_sort="hot", posts_limit=10))
        """
        front_page_posts: list = await api.get_posts(
            posts_type="front_page",
            limit=limit,
            sort=sort,
            session=session,
        )

        if front_page_posts:
            return clean_posts(data=front_page_posts, time_format=self._time_format)

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Get new posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_new_posts(posts_sort, posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        new = await posts.new(sort=posts_sort, limit=posts_limit, session=request_session)
            >>>        print(new)


            >>> asyncio.run(async_new_posts(posts_sort="hot", posts_limit=10))
        """
        new_posts: list = await api.get_posts(
            posts_type="new",
            limit=limit,
            sort=sort,
            session=session,
        )

        if new_posts:
            return clean_posts(data=new_posts, time_format=self._time_format)

    async def popular(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get popular posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        popular_posts: list = await api.get_posts(
            posts_type="popular",
            timeframe=timeframe,
            limit=limit,
            session=session,
        )

        if popular_posts:
            return clean_posts(data=popular_posts, time_format=self._time_format)

    async def rising(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get rising posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get rising posts.
        :type timeframe: Literal[str]
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        rising_posts: list = await api.get_posts(
            posts_type="rising",
            timeframe=timeframe,
            limit=limit,
            session=session,
        )

        if rising_posts:
            return clean_posts(data=rising_posts, time_format=self._time_format)


class Search:
    """
    Represents the Readit search functionality and provides
    methods for getting search results from different entities
    """

    def __init__(self, query: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Search()` instance for searching `posts`, `subreddits` and `users`.

        :param query: Search query.
        :type query: str
        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._query = query
        self._time_format = time_format

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Search posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        posts_results: list = await api.search_entities(
            query=self._query,
            entity_type="posts",
            sort=sort,
            limit=limit,
            session=session,
        )
        if posts_results:
            return clean_posts(data=posts_results, time_format=self._time_format)

    async def subreddits(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Search subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        search_subreddits: list = await api.search_entities(
            query=self._query,
            entity_type="subreddits",
            sort=sort,
            limit=limit,
            session=session,
        )
        subreddits_results: list[dict] = clean_subreddits(
            search_subreddits, time_format=self._time_format
        )

        return subreddits_results

    async def users(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Search users.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param limit: Maximum number of search results to return.
        :type limit: int
        :return: A list of dictionaries, each containing user data.
        :rtype: list[dict]
        """
        search_users: list = await api.search_entities(
            query=self._query,
            entity_type="users",
            sort=sort,
            limit=limit,
            session=session,
        )
        users_results: list[dict] = clean_users(
            search_users, time_format=self._time_format
        )

        return users_results


class Subreddit:
    """Represents a Reddit Community (Subreddit) and provides methods for getting data from the specified subreddit."""

    def __init__(self, subreddit: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Subreddit()` instance for getting a subreddit's `profile`, `wiki pages`,
        `wiki page`, and `posts` data, as well as `searching for posts that contain a specified keyword`.

        :param subreddit: Name of the subreddit to get data from.
        :type subreddit: str
        :param time_format: Time format of the output data. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._subreddit = subreddit
        self._time_format = time_format

    async def profile(self, session: aiohttp.ClientSession) -> dict:
        """
        Get a subreddit's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A dictionary containing subreddit profile data.
        :rtype: dict
        """
        subreddit_profile: dict = await api.get_entity(
            entity_type="subreddit",
            subreddit=self._subreddit,
            session=session,
        )
        if subreddit_profile:
            return clean_subreddits(
                data=subreddit_profile, time_format=self._time_format
            )

    async def wiki_pages(self, session: aiohttp.ClientSession) -> list[str]:
        """
        Return a subreddit's wiki pages.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        with get_status(
            status_message=f"Starting [underline]single data[/] retrieval process..."
        ):
            pages: dict = await api.send_request(
                endpoint=f"{api.subreddit_endpoint}/{self._subreddit}/wiki/pages.json",
                session=session,
            )

            return pages.get("data")

    async def wiki_page(self, page_name: str, session: aiohttp.ClientSession) -> dict:
        """
        Return a subreddit's specified wiki page data.

        :param page_name: Wiki page to get data from.
        :type page_name: str
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        wiki_page: dict = await api.get_entity(
            entity_type="wiki_page",
            page_name=page_name,
            subreddit=self._subreddit,
            session=session,
        )

        if wiki_page:
            return clean_subreddit_wiki_page(
                wiki_page=wiki_page, time_format=self._time_format
            )

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get a subreddit's posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        subreddit_posts: list = await api.get_posts(
            posts_type="subreddit_posts",
            subreddit=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if subreddit_posts:
            return clean_posts(data=subreddit_posts, time_format=self._time_format)

    async def search(
        self,
        session: aiohttp.ClientSession,
        query: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get posts that contain a specified keyword from a subreddit.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        found_posts: list = await api.get_posts(
            posts_type="search_subreddit_posts",
            subreddit=self._subreddit,
            query=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if found_posts:
            return clean_posts(data=found_posts, time_format=self._time_format)


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

    async def all(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Return all subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get all subreddits.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]

        Note:
            *in Morphius' voice* "the only limitation you have at this point is the matrix's rate-limit."
        """
        all_subreddits: list = await api.get_subreddits(
            subreddits_type="all", limit=limit, timeframe=timeframe, session=session
        )
        if all_subreddits:
            return clean_subreddits(data=all_subreddits, time_format=self._time_format)

    async def default(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Return default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        default_subreddits: list = await api.get_subreddits(
            subreddits_type="default", timeframe="all", limit=limit, session=session
        )
        if default_subreddits:
            return clean_subreddits(default_subreddits, time_format=self._time_format)

    async def new(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Return new subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        new_subreddits: list = await api.get_subreddits(
            subreddits_type="new", limit=limit, timeframe=timeframe, session=session
        )
        if new_subreddits:
            return clean_subreddits(new_subreddits, time_format=self._time_format)

    async def popular(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Return popular subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        popular_subreddits: list = await api.get_subreddits(
            subreddits_type="popular", limit=limit, timeframe=timeframe, session=session
        )
        if popular_subreddits:
            return clean_subreddits(popular_subreddits, time_format=self._time_format)


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, username: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `User()` instance for getting a user's `profile`, `posts` and `comments` data.

        :param username: Username to get data from.
        :type username: str
        :param time_format: Time format of the output data. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._username = username
        self._time_format = time_format

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get a user's comments.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which tyo get comments.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing comment data.
        :rtype: list[dict]
        """
        user_comments: list = await api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if user_comments:
            return clean_comments(comments=user_comments, time_format=self._time_format)

    async def moderated_subreddits(self, session: aiohttp.ClientSession) -> list[dict]:
        """
        Get subreddits moderated by user.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]
        """
        subreddits: dict = await api.get_subreddits(
            subreddits_type="user_moderated",
            username=self._username,
            session=session,
            limit=0,
        )
        if subreddits:
            return clean_subreddits(
                subreddits.get("data"),
                time_format=self._time_format,
            )

    async def overview(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a recent comment.
        :rtype: list[dict]
        """
        user_overview: list = await api.get_posts(
            username=self._username,
            posts_type="user_overview",
            limit=limit,
            session=session,
        )
        if user_overview:
            return clean_comments(user_overview, time_format=self._time_format)

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get a user's posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        user_posts: list = await api.get_posts(
            username=self._username,
            posts_type="user_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        if user_posts:
            return clean_posts(user_posts, time_format=self._time_format)

    async def profile(self, session: aiohttp.ClientSession) -> dict:
        """
        Get a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A dictionary containing user profile data.
        :rtype: dict
        """
        user_profile: dict = await api.get_entity(
            username=self._username, entity_type="user", session=session
        )
        if user_profile:
            return clean_users(data=user_profile, time_format=self._time_format)

    async def search_posts(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get a user's posts that contain the specified keywords.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param keyword: Keyword to search for in posts.
        :type keyword: str
        :param limit: Maximum number of posts to search from.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        user_posts: list = await api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        found_posts: list = []
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for post in user_posts:
            post_data: dict = post.get("data")
            if pattern.search(post_data.get("title")) or pattern.search(
                post_data.get("selftext")
            ):
                found_posts.append(post)
        if found_posts:
            return clean_posts(found_posts, time_format=self._time_format)

    async def search_comments(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Get a user's comments that contain the specified keyword.

        :param session: Aiohttp session to use for the request.
        :param keyword: Keyword to search for in comments.
        :type keyword: str
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to search from.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which to get comments.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing comment data.
        :rtype: list[dict]
        """
        user_comments: list = await api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        found_comments: list = []
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for comment in user_comments:
            if pattern.search(comment.get("data").get("body")):
                found_comments.append(comment)

        if found_comments:
            return clean_comments(found_comments, time_format=self._time_format)

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        timeframe: TIMEFRAME = "all",
    ) -> list[tuple]:
        """
        Get a user's top n subreddits based on subreddit frequency in n posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param top_n: Communities arranging number.
        :type top_n: int
        :param limit: Maximum number of posts to scrape.
        :type limit: int
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: Dictionary of top n subreddits and their ratio.
        :rtype: dict
        """
        posts = await api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            timeframe=timeframe,
            session=session,
        )

        if posts:
            # Extract subreddit names
            subreddits = [post.get("data", {}).get("subreddit") for post in posts]

            # Count the occurrences of each subreddit
            subreddit_counts = Counter(subreddits)

            return subreddit_counts.most_common(top_n)


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

    async def new(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get new users.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of new users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        new_users: list = await api.get_users(
            users_type="new", limit=limit, timeframe=timeframe, session=session
        )
        if new_users:
            return clean_users(new_users, time_format=self._time_format)

    async def popular(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get popular users.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of popular users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        popular_users: list = await api.get_users(
            users_type="popular",
            limit=limit,
            timeframe=timeframe,
            session=session,
        )
        if popular_users:
            return clean_users(popular_users, time_format=self._time_format)

    async def all(
        self, session: aiohttp.ClientSession, limit: int, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        all_users: list = await api.get_users(
            users_type="all", limit=limit, timeframe=timeframe, session=session
        )
        if all_users:
            return clean_users(all_users, time_format=self._time_format)
