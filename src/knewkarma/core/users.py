import typing as t

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
    ) -> t.List[Redditor]:
        new_users = reddit.users(
            session=session,
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
    ) -> t.List[Redditor]:
        popular_users = reddit.users(
            session=session,
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
    ) -> t.List[Redditor]:
        all_users = reddit.users(
            session=session,
            status=status,
            kind="all",
            limit=limit,
        )

        return all_users
