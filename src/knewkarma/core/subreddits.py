import typing as t

import requests
from praw.models import Subreddit
from rich.status import Status

from .client import reddit


class Subreddits:
    @classmethod
    def all(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
    ) -> t.List[Subreddit]:
        all_subreddits = reddit.subreddits(
            session=session,
            status=status,
            kind="all",
            limit=limit,
        )

        return all_subreddits

    @classmethod
    def default(
        cls,
        limit: int,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ) -> t.List[Subreddit]:
        default_subreddits = reddit.subreddits(
            session=session,
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
        status: t.Optional[Status] = None,
    ) -> t.List[Subreddit]:
        new_subreddits = reddit.subreddits(
            session=session,
            status=status,
            kind="new",
            limit=limit,
        )

        return new_subreddits

    @classmethod
    def popular(
        cls,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
    ) -> t.List[Subreddit]:
        popular_subreddits = reddit.subreddits(
            session=session,
            status=status,
            kind="popular",
            limit=limit,
        )

        return popular_subreddits
