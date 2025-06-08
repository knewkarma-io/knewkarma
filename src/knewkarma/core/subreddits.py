import typing as t
from logging import Logger

import requests
from rich.status import Status

from engines.karmakaze.schemas import Subreddit
from .client import reddit


class Subreddits:
    """Represents Reddit subreddits and provides methods for getting related data."""

    @classmethod
    def all(
        cls,
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Subreddit]:
        """
        get all subreddits.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get all subreddits.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Subreddit` objects, each containing subreddit data.
        :rtype: List[Subreddit]

        Note:
            Items will most likely be limited to 1000, per Reddit's public API policy.
        """

        all_subreddits = reddit.subreddits(
            session=session,
            logger=logger,
            status=status,
            kind="all",
            limit=limit,
            timeframe=timeframe,
        )

        return all_subreddits

    @classmethod
    def default(
        cls,
        limit: int,
        session: requests.Session,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Subreddit]:
        """
        get default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Subreddit` objects, each containing subreddit data.
        :rtype: List[Subreddit]
        """

        default_subreddits = reddit.subreddits(
            session=session,
            logger=logger,
            status=status,
            kind="default",
            timeframe="all",
            limit=limit,
        )

        return default_subreddits

    @classmethod
    def new(
        cls,
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Subreddit]:
        """
        get new subreddits.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Subreddit` objects, each containing subreddit data.
        :rtype: List[Subreddit]
        """
        new_subreddits = reddit.subreddits(
            session=session,
            logger=logger,
            status=status,
            kind="new",
            limit=limit,
            timeframe=timeframe,
        )

        return new_subreddits

    @classmethod
    def popular(
        cls,
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Subreddit]:
        """
        get popular subreddits.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Subreddit` objects, each containing subreddit data.
        :rtype: List[Subreddit]
        """

        popular_subreddits = reddit.subreddits(
            session=session,
            logger=logger,
            status=status,
            kind="popular",
            limit=limit,
            timeframe=timeframe,
        )

        return popular_subreddits
