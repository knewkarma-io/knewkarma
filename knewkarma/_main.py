import re
from collections import Counter

import aiohttp

from .api import Api, SORT_CRITERION, TIMEFRAME, TIME_FORMAT
from .tools.general_utils import console
from .tools.parsing_utils import (
    parse_comments,
    parse_subreddits,
    parse_posts,
    parse_users,
    parse_wiki_page,
)

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

    async def data(
        self, session: aiohttp.ClientSession, status: console.status = None
    ) -> dict:
        """
        Get a post's data (without comments)

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
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
            status=status,
            session=session,
        )

        if post_data:
            return parse_posts(
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
        status: console.status = None,
    ) -> list[dict]:
        """
        Get a post's comments.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
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
            status=status,
            session=session,
        )

        if comments_data:
            return parse_comments(
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
        status: console.status = None,
    ) -> list[dict]:
        """
        Get best posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get best posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_best_posts(posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        best = await posts.best(limit=posts_limit, session=request_session)
            >>>        print(best)


            >>> asyncio.run(async_best_posts(posts_limit=120))
        """
        best_posts: list = await api.get_posts(
            posts_type="best",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if best_posts:
            return parse_posts(data=best_posts, time_format=self._time_format)

    async def controversial(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get controversial posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get controversial posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_controversial_posts(posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        controversial = await posts.controversial(limit=posts_limit, session=request_session)
            >>>        print(controversial)

            >>> asyncio.run(async_controversial_posts(posts_limit=50))
        """
        controversial_posts: list = await api.get_posts(
            posts_type="controversial",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if controversial_posts:
            return parse_posts(data=controversial_posts, time_format=self._time_format)

    async def front_page(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get posts from the Reddit front-page.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_frontpage_posts(posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        frontpage = await posts.front_page(limit=posts_limit, session=request_session)
            >>>        print(frontpage)


            >>> asyncio.run(async_frontpage_posts(posts_limit=10))
        """
        front_page_posts: list = await api.get_posts(
            posts_type="front_page",
            limit=limit,
            sort=sort,
            status=status,
            session=session,
        )

        if front_page_posts:
            return parse_posts(data=front_page_posts, time_format=self._time_format)

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get new posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_new_posts(posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        new = await posts.new(limit=posts_limit, session=request_session)
            >>>        print(new)


            >>> asyncio.run(async_new_posts(posts_limit=10))
        """
        new_posts: list = await api.get_posts(
            posts_type="new",
            limit=limit,
            sort=sort,
            status=status,
            session=session,
        )

        if new_posts:
            return parse_posts(data=new_posts, time_format=self._time_format)

    async def popular(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get popular posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_popular_posts(posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        popular = await posts.popular(limit=posts_limit, session=request_session)
            >>>        print(popular)


            >>> asyncio.run(async_popular_posts(posts_limit=50))
        """
        popular_posts: list = await api.get_posts(
            posts_type="popular",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if popular_posts:
            return parse_posts(data=popular_posts, time_format=self._time_format)

    async def rising(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get rising posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get rising posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Posts


            >>> async def async_rising_posts(posts_limit):
            >>>    posts = Posts()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        rising = await posts.rising(limit=posts_limit, session=request_session)
            >>>        print(rising)


            >>> asyncio.run(async_rising_posts(posts_limit=100))
        """
        rising_posts: list = await api.get_posts(
            posts_type="rising",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if rising_posts:
            return parse_posts(data=rising_posts, time_format=self._time_format)


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
        status: console.status = None,
    ) -> list[dict]:
        """
        Search posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Search


            >>> async def async_search_posts(query, results_limit):
            >>>    search = Search(query=query)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        posts = await search.posts(limit=results_limit, session=request_session)
            >>>        print(posts)


            >>> asyncio.run(async_search_posts(query="something in data science", results_limit=200))
        """
        posts_results: list = await api.search_entities(
            query=self._query,
            entity_type="posts",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )
        if posts_results:
            return parse_posts(data=posts_results, time_format=self._time_format)

    async def subreddits(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Search subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Search


            >>> async def async_search_subreddits(query, results_limit):
            >>>    search = Search(query=query)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        subreddits = await search.subreddits(limit=results_limit, session=request_session)
            >>>        print(subreddits)


            >>> asyncio.run(async_search_subreddits(query="questions", results_limit=200))
        """
        search_subreddits: list = await api.search_entities(
            query=self._query,
            entity_type="subreddits",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )
        subreddits_results: list[dict] = parse_subreddits(
            search_subreddits, time_format=self._time_format
        )

        return subreddits_results

    async def users(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Search users.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing user data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Search


            >>> async def async_search_users(query, results_limit):
            >>>    search = Search(query=query)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        users = await search.users(limit=results_limit, session=request_session)
            >>>        print(users)


            >>> asyncio.run(async_search_users(query="john", results_limit=200))
        """
        search_users: list = await api.search_entities(
            query=self._query,
            entity_type="users",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )
        users_results: list[dict] = parse_users(
            search_users, time_format=self._time_format
        )

        return users_results


class Subreddit:
    """Represents a Reddit Community (Subreddit) and provides methods for getting data from the specified subreddit."""

    def __init__(self, subreddit: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Subreddit()` instance for getting a subreddit's `profile`, `wiki pages`,
        `wiki page`, and `posts` data, as well as `searching for posts that contain a specified query`.

        :param subreddit: Name of the subreddit to get data from.
        :type subreddit: str
        :param time_format: Time format of the output data. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._subreddit = subreddit
        self._time_format = time_format

    async def profile(
        self,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> dict:
        """
        Get a subreddit's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A dictionary containing subreddit profile data.
        :rtype: dict

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddit


            >>> async def async_subreddit_profile(subreddit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        profile = await subreddit.profile(session=request_session)
            >>>        print(profile)


            >>> asyncio.run(async_subreddit_profile(subreddit="MachineLearning"))
        """
        subreddit_profile: dict = await api.get_entity(
            entity_type="subreddit",
            subreddit=self._subreddit,
            status=status,
            session=session,
        )
        if subreddit_profile:
            return parse_subreddits(
                data=subreddit_profile, time_format=self._time_format
            )

    async def wiki_pages(
        self,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> list[str]:
        """
        Get a subreddit's wiki pages.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddit


            >>> async def async_subreddit_wiki_pages(subreddit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        wiki_pages = await subreddit.wiki_pages(session=request_session)
            >>>        print(wiki_pages)


            >>> asyncio.run(async_subreddit_wiki_pages(subreddit="MachineLearning"))
        """
        if status:
            status.update(f"Initialising single data retrieval job...")

        pages: dict = await api.make_request(
            endpoint=f"{api.subreddit_endpoint}/{self._subreddit}/wiki/pages.json",
            session=session,
        )

        return pages.get("data")

    async def wiki_page(
        self,
        page_name: str,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> dict:
        """
        Get a subreddit's specified wiki page data.

        :param page_name: Wiki page to get data from.
        :type page_name: str
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddit


            >>> async def async_subreddit_wiki_page(page, subreddit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        wiki_page_data = await subreddit.wiki_page(page_name=page, session=request_session)
            >>>        print(wiki_page_data)


            >>> asyncio.run(async_subreddit_wiki_page(page="rules", subreddit="MachineLearning"))
        """
        wiki_page: dict = await api.get_entity(
            entity_type="wiki_page",
            page_name=page_name,
            subreddit=self._subreddit,
            status=status,
            session=session,
        )

        if wiki_page:
            return parse_wiki_page(wiki_page=wiki_page, time_format=self._time_format)

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
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
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddit


            >>> async def async_subreddit_posts(subreddit, posts_limit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        posts = await subreddit.posts(limit=posts_limit, session=request_session)
            >>>        print(posts)


            >>> asyncio.run(async_subreddit_posts(posts_limit=500, subreddit="MachineLearning"))
        """
        subreddit_posts: list = await api.get_posts(
            posts_type="subreddit_posts",
            subreddit=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if subreddit_posts:
            return parse_posts(data=subreddit_posts, time_format=self._time_format)

    async def search(
        self,
        session: aiohttp.ClientSession,
        query: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get posts that match the specified query from a subreddit.

        :param session: Aiohttp session to use for the request.
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

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddit


            >>> async def async_search_subreddit_posts(search_query, subreddit, posts_limit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        posts = await subreddit.search(query=search_query, limit=posts_limit, session=request_session)
            >>>        print(posts)


            >>> asyncio.run(async_search_subreddit_posts(
            >>>     search_query="ML jobs",
            >>>     posts_limit=100,
            >>>     subreddit="MachineLearning"
            >>>   )
            >>> )
        """
        found_posts: list = await api.get_posts(
            posts_type="search_subreddit_posts",
            subreddit=self._subreddit,
            query=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if found_posts:
            return parse_posts(data=found_posts, time_format=self._time_format)


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
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get all subreddits.

        :param session: Aiohttp session to use for the request.
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

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddits


            >>> async def async_all_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        all_subs = await subreddits.all(limit=subreddits_limit, session=request_session)
            >>>        print(all_subs)


            >>> asyncio.run(async_all_subreddits(subreddits_limit=500))
        """
        all_subreddits: list = await api.get_subreddits(
            subreddits_type="all",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if all_subreddits:
            return parse_subreddits(data=all_subreddits, time_format=self._time_format)

    async def default(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> list[dict]:
        """
        Get default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddits


            >>> async def async_default_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        default_subs = await subreddits.default(limit=subreddits_limit, session=request_session)
            >>>        print(default_subs)


            >>> asyncio.run(async_default_subreddits(subreddits_limit=20))
        """
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
    ) -> list[dict]:
        """
        Get new subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddits


            >>> async def async_new_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        new_subs = await subreddits.new(limit=subreddits_limit, session=request_session)
            >>>        print(new_subs)


            >>> asyncio.run(async_new_subreddits(subreddits_limit=50))
        """
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
    ) -> list[dict]:
        """
        Get popular subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Subreddits


            >>> async def async_popular_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        popular_subs = await subreddits.popular(limit=subreddits_limit, session=request_session)
            >>>        print(popular_subs)


            >>> asyncio.run(async_popular_subreddits(subreddits_limit=100))
        """
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

    @staticmethod
    def _build_regex_pattern(text: str) -> re.Pattern:
        """
        Builds a regex pattern for word boundaries and OR conditions from a given text.
        Each word in the text will be matched as a whole word in a case-insensitive manner.

        :param text: The input text to create a regex pattern from.
        :type text: str
        :return: A compiled regex pattern that matches any of the words in the input text.
        :rtype: re.Pattern
        """
        words = text.split()

        # Create a regex pattern for word boundaries and OR conditions
        word_patterns = [f"\\b{re.escape(word)}\\b" for word in words]
        regex_pattern = "|".join(word_patterns)

        return re.compile(regex_pattern, re.IGNORECASE)

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
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
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_user_comments(username, comments_limit):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        comments = await user.comments(limit=comments_limit, session=request_session)
            >>>        print(comments)


            >>> asyncio.run(async_user_comments(username="AutoModerator", comments_limit=100))
        """
        user_comments: list = await api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if user_comments:
            return parse_comments(comments=user_comments, time_format=self._time_format)

    async def moderated_subreddits(
        self,
        session: aiohttp.ClientSession,
        status: console.status = None,
    ) -> list[dict]:
        """
        Get subreddits moderated by user.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_user_moderated_subreddits(username):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        moderated_subs = await user.moderated_subreddits(session=request_session)
            >>>        print(moderated_subs)


            >>> asyncio.run(async_user_moderated_subreddits(username="TheRealKSI"))
        """
        subreddits: dict = await api.get_subreddits(
            subreddits_type="user_moderated",
            username=self._username,
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
    ) -> list[dict]:
        """
        Get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing data about a recent comment.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_user_overview(username, comments_limit):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        comments = await user.overview(limit=comments_limit, session=request_session)
            >>>        print(comments)


            >>> asyncio.run(async_user_overview(username="AutoModerator", comments_limit=100))
        """
        user_overview: list = await api.get_posts(
            username=self._username,
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
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_user_posts(username, posts_limit):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        posts = await user.posts(limit=posts_limit, session=request_session)
            >>>        print(posts)


            >>> asyncio.run(async_user_posts(username="AutoModerator", posts_limit=100))
        """
        user_posts: list = await api.get_posts(
            username=self._username,
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
    ) -> dict:
        """
        Get a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A dictionary containing user profile data.
        :rtype: dict

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_user_profile(username):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        profile = await user.profile(session=request_session)
            >>>        print(profile)


            >>> asyncio.run(async_user_profile(username="AutoModerator"))
        """
        user_profile: dict = await api.get_entity(
            username=self._username, entity_type="user", status=status, session=session
        )
        if user_profile:
            return parse_users(data=user_profile, time_format=self._time_format)

    async def search_posts(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get a user's posts that match with the specified search query.

        :param query: Search query.
        :type query: str
        :param session: Aiohttp session to use for the request.
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

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_search_user_posts(username, search_query, posts_limit):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        posts = await user.search_posts(query=search_query,
            >>>                                limit=posts_limit, session=request_session)
            >>>        print(posts)


            >>> asyncio.run(async_search_user_posts(username="AutoModerator",
            >>>                             search_query="user has been banned", posts_limit=100))
        """
        user_posts: list = await api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        found_posts: list = []
        regex_pattern: re.Pattern = self._build_regex_pattern(text=query)

        for post in user_posts:
            post_data: dict = post.get("data")

            match = regex_pattern.search(
                post_data.get("title")
            ) or regex_pattern.search(post_data.get("selftext"))

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
    ) -> list[dict]:
        """
        Get a user's comments that contain the specified search query.

        :param query: Search query.
        :type query: str
        :param session: Aiohttp session to use for the request.
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

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_search_user_comments(username, search_query, comments_limit):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        comments = await user.search_comments(query=search_query,
            >>>                                limit=comments_limit, session=request_session)
            >>>        print(comments)


            >>> asyncio.run(async_search_user_comments(username="AutoModerator",
            >>>                            search_query="this action is automated", comments_limit=100))
        """
        user_comments: list = await api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        found_comments: list = []
        regex_pattern = self._build_regex_pattern(text=query)

        for comment in user_comments:
            match = regex_pattern.search(comment.get("data").get("body"))
            if match:
                found_comments.append(comment)

        if found_comments:
            return parse_comments(found_comments, time_format=self._time_format)

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
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
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: Dictionary of top n subreddits and their ratio.
        :rtype: dict

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import User


            >>> async def async_user_top_subreddits(username, top_number, subreddits_limit):
            >>>    user = User(username=username)
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        top_subs = await user.top_subreddits(top_n=top_number,
            >>>                             limit=subreddits_limit, session=request_session)
            >>>        print(top_subs)


            >>> asyncio.run(async_user_top_subreddits(username="TheRealKSI",
            >>>                                     top_number=10, subreddits_limit=100))
        """
        posts = await api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            timeframe=timeframe,
            status=status,
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
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Get new users.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of new users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Users


            >>> async def async_new_users(users_limit):
            >>>    users = Users()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        new = await users.new(limit=users_limit, session=request_session)
            >>>        print(new)


            >>> asyncio.run(async_new_users(users_limit=500))
        """
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
    ) -> list[dict]:
        """
        Get popular users.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of popular users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Users


            >>> async def async_popular_users(users_limit):
            >>>    users = Users()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        popular = await users.popular(limit=users_limit, session=request_session)
            >>>        print(popular)


            >>> asyncio.run(async_popular_users(users_limit=100))
        """
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
    ) -> list[dict]:
        """
        Get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]

        Usage::

            >>> import aiohttp
            >>> import asyncio
            >>> from knewkarma import Users


            >>> async def async_all_users(users_limit):
            >>>    users = Users()
            >>>    async with aiohttp.ClientSession() as request_session:
            >>>        all_users_data = await users.all(limit=users_limit, session=request_session)
            >>>        print(all_users_data)


            >>> asyncio.run(async_all_users(users_limit=1000))
        """
        all_users: list = await api.get_users(
            users_type="all",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if all_users:
            return parse_users(all_users, time_format=self._time_format)
