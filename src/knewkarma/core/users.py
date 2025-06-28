import typing as t
from logging import Logger

import requests
from praw.models import Redditor
from rich.status import Status

from .client import reddit


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    @classmethod
    def new(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Redditor]:
        """
        Get new users.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session
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

        new_users = reddit.users(
            session=session,
            logger=logger,
            status=status,
            kind="new",
            limit=limit,
        )

        return new_users

    @classmethod
    def popular(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Redditor]:
        """
        Get popular users.

        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session
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

        popular_users = reddit.users(
            session=session,
            logger=logger,
            status=status,
            kind="popular",
            limit=limit,
        )

        return popular_users

    @classmethod
    def all(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Redditor]:
        """
        Get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: A `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing a user's data.
        :rtype: List[SimpleNamespace]
        """

        all_users = reddit.users(
            session=session,
            logger=logger,
            status=status,
            kind="all",
            limit=limit,
        )

        return all_users
