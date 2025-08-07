import typing as t

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
    ) -> t.List[Submission]:
        posts = reddit.posts(
            session=session,
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
    ) -> t.List[Submission]:
        posts = reddit.posts(
            session=session,
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
    ) -> t.List[Submission]:
        posts = reddit.posts(
            session=session,
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
    ) -> t.List[Submission]:

        posts = reddit.posts(
            session=session,
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
    ) -> t.List[Submission]:
        posts = reddit.posts(
            session=session,
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
    ) -> t.List[Submission]:
        posts = reddit.posts(
            session=session,
            status=status,
            kind="rising",
            limit=limit,
            sort="all",
        )

        return posts
