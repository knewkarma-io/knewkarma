import typing as t
from logging import Logger

from praw.models import Submission, Comment
from praw.models.reddit.subreddit import SubredditWiki
from prawcore import exceptions
from rich.status import Status

from karmakrate.konsole import colours
from .client import reddit, TIME_FILTERS, SORT, LISTINGS


class Subreddit:
    def __init__(self, display_name: str):
        self._display_name = display_name
        self._subreddit = reddit.subreddit(display_name=display_name)

    def comments(
        self, limit: int, status: Status, logger: Logger
    ) -> t.Union[t.List[Comment], None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} comments from {self._subreddit.display_name_prefixed}..."
                )
            comments = [
                comment.refresh() for comment in self._subreddit.comments(limit=limit)
            ]
            return comments
        else:
            return None

    def posts(
        self, limit: int, status: Status, logger: Logger, listing: LISTINGS
    ) -> t.Union[t.List[Submission], None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} {listing} posts from {self._subreddit.display_name_prefixed}..."
                )
            func = getattr(self._subreddit, listing)
            return list(func(limit=limit))
        else:
            return None

    def profile(self, status: Status, logger: Logger) -> t.Union["Subreddit", None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(
                    f"Getting profile data from subreddit r/{self._display_name}..."
                )

            return self._subreddit
        else:
            return None

    def search(
        self,
        query: str,
        limit: int,
        status: Status,
        logger: Logger,
        sort: SORT,
        time_filter: TIME_FILTERS,
    ) -> t.Union[t.List[Submission], None]:
        if self.exists(status=status, logger=logger):
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
        else:
            return None

    def wiki_pages(
        self, status: Status, logger: Logger
    ) -> t.Union[t.List[SubredditWiki], None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(
                    f"Getting wiki pages from {self._subreddit.display_name_prefixed}...",
                )

            pages = self._subreddit.wiki

            return list(pages)
        else:
            return None

    def exists(self, status: Status, logger: Logger) -> bool:
        if isinstance(status, Status):
            status.update(f"Checking subreddit availability...")

        try:
            _ = self._subreddit.id
            verdict = True
        except exceptions.Redirect:
            verdict = False
        except exceptions.NotFound:
            verdict = False
        except exceptions.Forbidden:
            verdict = False

        if isinstance(logger, Logger):
            if verdict:
                logger.warning(
                    f"{colours.BOLD_GREEN}✔{colours.BOLD_GREEN_RESET} Subreddit exists"
                )

            elif not verdict:
                logger.info(
                    f"{colours.BOLD_YELLOW}✘{colours.BOLD_YELLOW_RESET} Subreddit does not exist"
                )
        return verdict
