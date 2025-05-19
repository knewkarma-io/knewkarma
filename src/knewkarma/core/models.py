from collections import Counter
from logging import Logger
from platform import python_version, platform
from types import SimpleNamespace
from typing import Literal, Union, Optional, List

import aiohttp
from rich.status import Status

from engines import klaus
from toolbox.data_and_visualisation import DataAndVisualisation
from ..metadata.about import Project
from ..metadata.version import Version

__all__ = [
    "reddit",
    "Post",
    "Posts",
    "Search",
    "Subreddit",
    "Subreddits",
    "User",
    "Users",
]


reddit = klaus.RedditClient(
    user_agent=f"{Project.name.replace(' ', '-')}/{Version.release} "
    f"(Python {python_version} on {platform}; +{Project.documentation})"
)


class Post:
    """Represents a Reddit post and provides methods for fetching post data and comments."""

    def __init__(self, id: str, subreddit: str):
        """
        Initialises a `Post` instance to fetch the post's data and comments.

        :param id: The ID of the Reddit post to retrieve.
        :type id: str
        :param subreddit: The subreddit where the post was created.
        :type subreddit: str
        """

        self._id = id
        self._subreddit = subreddit

    async def data(
        self,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
    ) -> SimpleNamespace:
        """
        Asynchronously retrieves data for a Reddit post, excluding comments.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A `SimpleNamespace` object containing parsed post data.
        :rtype: SimpleNamespace
        """

        post_data = await reddit.post(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            status=status,
            id=self._id,
            subreddit=self._subreddit,
        )

        return post_data

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves comments for a Reddit post.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of comments to retrieve.
        :type limit: int
        :param sort: The sorting criterion for the comments. Defaults to "all".
        :type sort: SORT, optional
        :param timeframe:
        :type timeframe:
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed comment data.
        :rtype: List[SimpleNamespace]
        """

        comments_data = await reddit.comments(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="post",
            id=self._id,
            subreddit=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return comments_data


class Posts:
    """Represents Reddit posts and provides methods for retrieving posts from various sources."""

    @staticmethod
    async def best(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the best posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        best_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="best",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return best_posts

    @staticmethod
    async def controversial(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the controversial posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        controversial_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="controversial",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return controversial_posts

    @staticmethod
    async def front_page(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        sort: reddit.SORT = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the front-page posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        front_page_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="front_page",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return front_page_posts

    @staticmethod
    async def new(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        sort: reddit.SORT = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the new posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        new_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="new",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return new_posts

    @staticmethod
    async def popular(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the popular posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """
        popular_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="popular",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return popular_posts

    @staticmethod
    async def rising(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the rising posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        rising_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="rising",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return rising_posts


class Search:
    """
    Represents the Reddit search functionality and provides methods for retrieving search results
    from different entities.
    """

    def __init__(self, query: str):
        """
        Initialises the `Search` instance for searching posts, subreddits, and users.

        :param query: The search query string.
        :type query: str
        """

        self._query = query

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves posts that match with the specified query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession:param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await reddit.search(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="posts",
            query=self._query,
            sort=sort,
            limit=limit,
        )

        return search_results

    async def subreddits(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves subreddits that match with the specified query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession:param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of subreddits to retrieve.
        :type limit: int
        :param sort: Sorting criterion for subreddits. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed subreddit data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await reddit.search(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="subreddits",
            query=self._query,
            sort=sort,
            limit=limit,
        )

        return search_results

    async def users(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves users that match with the specified query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of users to retrieve.
        :type limit: int
        :param sort: Sorting criterion for users. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed user data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await reddit.search(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="users",
            query=self._query,
            sort=sort,
            limit=limit,
        )

        return search_results


class Subreddit:
    """Represents a Reddit community (subreddit) and provides methods for retrieving its data."""

    def __init__(self, name: str):
        """
        Initialises a `Subreddit` instance to get a subreddit's profile, wiki pages, and posts data,
        and to search for posts containing a specified query.

        :param name: The name of the subreddit to retrieve data from.
        :type name: str
        """

        self._name = name

    async def comments(
        self,
        session: aiohttp.ClientSession,
        posts_limit: int,
        comments_per_post: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves comments from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param posts_limit: Maximum number of posts to retrieve comments from.
        :type posts_limit: int
        :param comments_per_post: Maximum number of comments to retrieve per post.
        :type comments_per_post: int
        :param sort: Sorting criterion for the posts and comments. Defaults to "all".
        :type sort: SORT, optional
        :param timeframe: The timeframe from which to retrieve posts and comments. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed comment data.
        :rtype: List[SimpleNamespace]
        """

        posts = await self.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
        )
        all_comments: List = []
        for post in posts:
            post = Post(
                id=post.get("id"),
                subreddit=post.get("subreddit"),
            )
            post_comments = await post.comments(
                session=session,
                proxy=proxy,
                proxy_auth=proxy_auth,
                limit=comments_per_post,
                sort=sort,
                status=status,
            )

            all_comments.extend(post_comments)

        return all_comments

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves posts from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param sort: Sorting criterion for the posts. Defaults to "all".
        :type sort: SORT, optional
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        subreddit_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="subreddit",
            subreddit=self._name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return subreddit_posts

    async def profile(
        self,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
    ) -> SimpleNamespace:
        """
        Asynchronously retrieves a subreddit's profile data.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A `SimpleNamespace` object containing the parsed subreddit profile data.
        :rtype: SimpleNamespace
        """

        subreddit_profile = await reddit.subreddit(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            status=status,
            name=self._name,
        )

        return subreddit_profile

    async def search(
        self,
        session: aiohttp.ClientSession,
        query: str,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get posts that contain the specified query string from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing post data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="search_subreddit",
            subreddit=self._name,
            query=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return search_results

    async def wikipages(
        self,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
    ) -> List[str]:
        """
        Asynchronously get a subreddit's wiki pages.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A list of strings, each representing a wiki page.
        :rtype: List[str]
        """

        if status:
            status.update(
                f"Retrieving wiki pages from subreddit ({self._name})",
            )

        pages = await reddit.request_handler.send_request(
            endpoint=f"{reddit.api_endpoints.SUBREDDIT}/{self._name}/wiki/pages.json",
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
        )

        return pages.get("data")

    async def wikipage(
        self,
        page_name: str,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
    ) -> SimpleNamespace:
        """
        Asynchronously get a subreddit's specified wiki page data.

        :param page_name: Wiki page to get data from.
        :type page_name: str
        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A `SimpleNamespace` object containing the parsed wiki page data.
        :rtype: SimpleNamespace
        """

        wiki_page = await reddit.wiki_page(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            status=status,
            name=page_name,
            subreddit=self._name,
        )

        return wiki_page


class Subreddits:
    """Represents Reddit subreddits and provides methods for getting related data."""

    @staticmethod
    async def all(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get all subreddits.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get all subreddits.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]

        Note:
            Items will most likely be limited to 1000, per Reddit's API policy.
        """

        all_subreddits = await reddit.subreddits(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="all",
            limit=limit,
            timeframe=timeframe,
        )

        return all_subreddits

    @staticmethod
    async def default(
        limit: int,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        default_subreddits = await reddit.subreddits(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="default",
            timeframe="all",
            limit=limit,
        )

        return default_subreddits

    @staticmethod
    async def new(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get new subreddits.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """
        new_subreddits = await reddit.subreddits(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="new",
            limit=limit,
            timeframe=timeframe,
        )

        return new_subreddits

    @staticmethod
    async def popular(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get popular subreddits.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        popular_subreddits = await reddit.subreddits(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="popular",
            limit=limit,
            timeframe=timeframe,
        )

        return popular_subreddits


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, name: str):
        """
        Initialises a `User()` instance for getting a user's `profile`, `posts` and `comments` data.

        :param name: Username to get data from.
        :type name: str
        """

        self._name = name

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's comments.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which tyo get comments.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing comment data.
        :rtype: List[SimpleNamespace]
        """

        user_comments = await reddit.comments(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="user",
            username=self._name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return user_comments

    async def moderated_subreddits(
        self,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get subreddits moderated by user.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        subreddits = await reddit.subreddits(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="user_moderated",
            timeframe="all",
            username=self._name,
            limit=0,
        )

        return subreddits

    async def overview(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing data about a recent comment.
        :rtype: List[SimpleNamespace]
        """

        user_overview = await reddit.comments(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="user_overview",
            limit=limit,
            sort="all",
            timeframe="all",
            username=self._name,
        )

        return user_overview

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing post data.
        :rtype: List[SimpleNamespace]
        """

        user_posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="user",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            username=self._name,
        )

        return user_posts

    async def profile(
        self,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
    ) -> SimpleNamespace:
        """
        Asynchronously get a user's profile data.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A SimpleNamespace object containing user profile data.
        :rtype: SimpleNamespace
        """

        user_profile = await reddit.user(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            status=status,
            name=self._name,
        )

        return user_profile

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> Union[List[tuple[str, int]], None]:
        """
        Asynchronously get a user's top n subreddits based on subreddit frequency in n posts and saves the analysis to a file.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param top_n: Communities arranging number.
        :type top_n: int
        :param limit: Maximum number of posts to scrape.
        :type limit: int
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        """

        posts = await reddit.posts(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="user",
            limit=limit,
            sort="all",
            timeframe=timeframe,
            username=self._name,
        )

        if posts:
            # Extract subreddit names
            subreddits = [post.data.subreddit for post in posts]

            # Count the occurrences of each subreddit
            subreddit_counts: Counter = Counter(subreddits)

            # Get the most common subreddits
            top_subreddits: List[tuple[str, int]] = subreddit_counts.most_common(top_n)

            # Prepare data for plotting
            subreddit_names = [subreddit[0] for subreddit in top_subreddits]
            subreddit_frequencies = [subreddit[1] for subreddit in top_subreddits]

            DataAndVisualisation.plot_bar_chart(
                data=dict(zip(subreddit_names, subreddit_frequencies)),
                title=f"top {top_n}/{limit} subreddits analysis",
                x_label="Subreddits",
                y_label="Frequency",
            )

        return None

    async def username_available(
        self,
        session: aiohttp.ClientSession,
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> Union[bool, None]:
        """
        Checks if the given username is available or taken.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: `True` if the given username is available. Otherwise, `False`.
        :rtype: bool
        """

        if status:
            status.update(f"Checking username availability: {self._name}")

        response: bool = await reddit.request_handler.send_request(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            endpoint=reddit.api_endpoints.USERNAME_AVAILABLE,
            params={"user": self._name},
        )

        if status and logger:
            if response:
                logger.info(f"Username ({self._name}) is available")
            else:
                logger.warning(f"Username ({self._name}) is already taken")
        else:
            return response

        return None


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    @staticmethod
    async def new(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get new users.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of new users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing a user's data.
        :rtype: List[SimpleNamespace]
        """

        new_users = await reddit.users(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="new",
            limit=limit,
            timeframe=timeframe,
        )

        return new_users

    @staticmethod
    async def popular(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get popular users.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param limit: Maximum number of popular users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing a user's data.
        :rtype: List[SimpleNamespace]
        """

        popular_users = await reddit.users(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="popular",
            limit=limit,
            timeframe=timeframe,
        )

        return popular_users

    @staticmethod
    async def all(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        proxy: Optional[str] = None,
        proxy_auth: Optional[aiohttp.BasicAuth] = None,
        status: Optional[Status] = Status,
        logger: Optional[Logger] = Logger,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession
        :param proxy:
        :type proxy: str
        :param proxy_auth:
        :type proxy_auth: aiohttp.BasicAuth
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing a user's data.
        :rtype: List[SimpleNamespace]
        """

        all_users = await reddit.users(
            session=session,
            proxy=proxy,
            proxy_auth=proxy_auth,
            logger=logger,
            status=status,
            kind="all",
            limit=limit,
            timeframe=timeframe,
        )

        return all_users


# -------------------------------- END ----------------------------------------- #
