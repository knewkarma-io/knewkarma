import typing as t

from praw.models import Submission, Comment
from praw.models.reddit.subreddit import SubredditWiki
from rich.status import Status

from .client import reddit, TIME_FILTERS, SORT, LISTINGS


class Subreddit:
    def __init__(self, name: str):
        self._subreddit = reddit.subreddit(display_name=name)
        self._name = name

    def comments(
        self,
        limit: int = 100,
        # listing: LISTINGS = "top",
        status: t.Optional[Status] = None,
    ) -> t.List[Comment]:

        if isinstance(status, Status):
            status.update(
                f"Getting {limit} comments from {self._subreddit.display_name_prefixed}..."
            )
        comments = [
            comment.refresh() for comment in self._subreddit.comments(limit=limit)
        ]
        return comments

    def posts(
        self,
        listing: LISTINGS = "top",
        limit: int = 100,
        status: t.Optional[Status] = None,
    ) -> t.List[Submission]:
        if isinstance(status, Status):
            status.update(
                f"Getting {limit} {listing} posts from {self._subreddit.display_name_prefixed}..."
            )
        func = getattr(self._subreddit, listing)
        return list(func(limit=limit))

    def profile(self, status: t.Optional[Status] = None) -> "Subreddit":
        if isinstance(status, Status):
            status.update(f"Getting profile data from subreddit r/{self._name}...")

        return self._subreddit

    def search(
        self,
        query: str,
        limit: int,
        sort: SORT = "lucene",
        time_filter: TIME_FILTERS = "all",
        status: t.Optional[Status] = None,
    ) -> t.List[Submission]:

        if isinstance(status, Status):
            status.update(
                f"Searching for '{query}' in posts from {self._subreddit.display_name_prefixed}..."
            )
        results = self._subreddit.search(
            query=query,
            limit=limit,
            sort=sort,
            time_filter=time_filter,
        )

        return list(results)

    def wiki_pages(
        self,
        status: t.Optional[Status] = None,
    ) -> t.List[SubredditWiki]:
        if status:
            status.update(
                f"Getting wiki pages from {self._subreddit.display_name_prefixed}...",
            )

        pages = self._subreddit.wiki

        return list(pages)
