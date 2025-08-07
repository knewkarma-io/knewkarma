import typing as t

import requests
from praw.models import Submission, Subreddit, Redditor
from rich.status import Status

from .client import reddit


class Search:
    def __init__(self, query: str):
        self._query = query

    def posts(
        self,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
    ) -> t.List[Submission]:
        search_results = reddit.search(
            session=session,
            status=status,
            kind="posts",
            query=self._query,
            limit=limit,
        )

        return search_results

    def subreddits(
        self,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
    ) -> t.List[Subreddit]:
        search_results = reddit.search(
            session=session,
            status=status,
            kind="subreddits",
            query=self._query,
            limit=limit,
        )

        return search_results

    def users(
        self,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
    ) -> t.List[Redditor]:
        search_results = reddit.search(
            session=session,
            status=status,
            kind="users",
            query=self._query,
            limit=limit,
        )

        return search_results
