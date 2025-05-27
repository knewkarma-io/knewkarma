import typing as t
from logging import Logger

import aiohttp
from rich.status import Status

from engines.karmakaze.schemas import User
from .client import reddit


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    @staticmethod
    async def new(
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[User]:
        """
        Asynchronously get new users.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[User]:
        """
        Asynchronously get popular users.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[User]:
        """
        Asynchronously get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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
            logger=logger,
            status=status,
            kind="all",
            limit=limit,
            timeframe=timeframe,
        )

        return all_users
