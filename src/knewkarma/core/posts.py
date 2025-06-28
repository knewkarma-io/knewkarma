import typing as t
from logging import Logger

import requests
from praw.models import Submission
from rich.status import Status

from .client import reddit


class Posts:
    """Represents Reddit posts and provides methods for retrieving posts from various sources."""

    @classmethod
    def best(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Submission]:
        """
        Gets best posts.

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

        posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="best",
            limit=limit,
            sort="all",
        )

        return posts

    @classmethod
    def controversial(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Submission]:
        """
        Gets controversial posts.

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

        posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="controversial",
            limit=limit,
            sort="all",
        )

        return posts

    @classmethod
    def front_page(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Submission]:
        """
        Gets front-page posts.

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

        posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="front_page",
            limit=limit,
        )

        return posts

    @classmethod
    def new(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Submission]:
        """
        Gets new posts.

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

        posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="new",
            limit=limit,
        )

        return posts

    @classmethod
    def top(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Submission]:
        """
        Gets top posts.

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

        posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="top",
            limit=limit,
            sort="all",
        )

        return posts

    @classmethod
    def rising(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Submission]:
        """
        Gets rising posts.

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

        posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="rising",
            limit=limit,
            sort="all",
        )

        return posts
