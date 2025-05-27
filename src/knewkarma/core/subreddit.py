import typing as t
from logging import Logger

import aiohttp
from rich.status import Status

from client import reddit
from engines.karmakaze.schemas import Post, WikiPage


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

    '''
    async def comments(
        self,
        session: aiohttp.ClientSession,
        posts_limit: int,
        comments_per_post: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[Comment]:
        """
        Asynchronously retrieves comments from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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
            logger=logger,
            status=status,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
        )
        all_comments: t.List = []
        for post in posts:
            post = Post(
                id=post.get("id"),
                subreddit=post.get("subreddit"),
            )
            post_comments = await post.comments(
                session=session,
                limit=comments_per_post,
                sort=sort,
                status=status,
            )

            all_comments.extend(post_comments)

        return all_comments
        '''

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[Post]:
        """
        Asynchronously retrieves posts from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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
        logger: t.Optional[Logger] = Logger,
        status: t.Optional[Status] = Status,
    ):
        """
        Asynchronously retrieves a subreddit's profile data.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A `SimpleNamespace` object containing the parsed subreddit profile data.
        :rtype: SimpleNamespace
        """

        subreddit_profile = await reddit.subreddit(
            session=session,
            logger=logger,
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
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[Post]:
        """
        Asynchronously get posts that contain the specified query string from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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
        status: t.Optional[Status] = Status,
    ) -> t.List[str]:
        """
        Asynchronously get a subreddit's wiki pages.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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
        )

        return pages.get("data")

    async def wikipage(
        self,
        page_name: str,
        session: aiohttp.ClientSession,
        status: t.Optional[Status] = Status,
    ) -> WikiPage:
        """
        Asynchronously get a subreddit's specified wiki page data.

        :param page_name: Wiki page to get data from.
        :type page_name: str
        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A `SimpleNamespace` object containing the parsed wiki page data.
        :rtype: SimpleNamespace
        """

        wiki_page = await reddit.wiki_page(
            session=session,
            status=status,
            name=page_name,
            subreddit=self._name,
        )

        return wiki_page
