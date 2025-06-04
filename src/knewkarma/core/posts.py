import typing as t
from logging import Logger

import requests
from rich.status import Status

from engines.karmakaze.schemas import Post
from .client import reddit


class Posts:
    """Represents Reddit posts and provides methods for retrieving posts from various sources."""

    @staticmethod
    def best(
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Asynchronously retrieves the best posts.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session




        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Post` objects, each containing parsed post data.
        :rtype: List[Post]
        """

        best_posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="best",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return best_posts

    @staticmethod
    def controversial(
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Asynchronously retrieves the controversial posts.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session




        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Post` objects, each containing parsed post data.
        :rtype: List[Post]
        """

        controversial_posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="controversial",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return controversial_posts

    @staticmethod
    def front_page(
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        sort: reddit.SORT = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Asynchronously retrieves the front-page posts.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session




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
        :return: A list of `Post` objects, each containing parsed post data.
        :rtype: List[Post]
        """

        front_page_posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="front_page",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return front_page_posts

    @staticmethod
    def new(
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        sort: reddit.SORT = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Asynchronously retrieves the new posts.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session




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
        :return: A list of `Post` objects, each containing parsed post data.
        :rtype: List[Post]
        """

        new_posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="new",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return new_posts

    @staticmethod
    def popular(
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Asynchronously retrieves the popular posts.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session




        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Post` objects, each containing parsed post data.
        :rtype: List[Post]
        """
        popular_posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="popular",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return popular_posts

    @staticmethod
    def rising(
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Asynchronously retrieves the rising posts.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session




        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: reddit.TIMEFRAME, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Post` objects, each containing parsed post data.
        :rtype: List[Post]
        """

        rising_posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="rising",
            limit=limit,
            sort="all",
            timeframe=timeframe,
        )

        return rising_posts
