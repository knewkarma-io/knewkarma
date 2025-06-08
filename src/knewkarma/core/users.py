import typing as t
from logging import Logger

import requests
from rich.status import Status

from engines.karmakaze.schemas import User
from .client import reddit


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    @classmethod
    def new(
        cls,
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[User]:
        """
        get new users.

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
            timeframe=timeframe,
        )

        return new_users

    @classmethod
    def popular(
        cls,
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[User]:
        """
        get popular users.

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
            timeframe=timeframe,
        )

        return popular_users

    @classmethod
    def all(
        cls,
        session: requests.Session,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[User]:
        """
        get all users.

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
            timeframe=timeframe,
        )

        return all_users
