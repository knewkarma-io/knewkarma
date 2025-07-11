import typing as t

from praw.models import Submission, Comment
from praw.models.reddit.subreddit import SubredditWiki
from prawcore import exceptions
from rich.status import Status

from karmakrate.riches import rich_colours
from karmakrate.riches.rich_logging import console
from .client import reddit, TIME_FILTERS, SORT, LISTINGS
from .shared import is_empty_data


class Subreddit:
    def __init__(self, display_name: str):
        self._display_name = display_name
        self._subreddit = reddit.subreddit(display_name=display_name)

    def comments(
        self, limit: int, status: t.Optional[Status] = None
    ) -> t.Union[t.List[Comment], None]:
        """
        Retrieves a list of comments from the subreddit.

        :param limit: Maximum number of comments to retrieve.
        :type limit: int
        :param status: Optional status object for updating progress.
        :type status: t.Optional[Status]
        :return: List of comments from the subreddit, or None if the subreddit does not exist.
        :rtype: t.Union[t.List[Comment], None]
        """
        if self.exists(status=status):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} comments from {self._subreddit.display_name_prefixed}..."
                )
            comments = [
                comment.refresh() for comment in self._subreddit.comments(limit=limit)
            ]
            return is_empty_data(
                data=comments,
                message=f"No comments found in {self._subreddit.display_name_prefixed}.",
            )
        else:
            return None

    def posts(
        self, limit: int, listing: LISTINGS, status: t.Optional[Status] = None
    ) -> t.Union[t.List[Submission], None]:
        """
        Retrieves a list of posts from the subreddit based on the specified listing type.

        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param listing: Type of listing to retrieve (e.g., 'hot', 'new', 'top').
        :param status: Optional status object for updating progress.
        :type status: t.Optional[Status]
        :return: List of posts from the subreddit, or None if the subreddit does not exist.
        :rtype: t.Union[t.List[Submission], None]
        """
        if self.exists(status=status):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} {listing} posts from {self._subreddit.display_name_prefixed}..."
                )
            func = getattr(self._subreddit, listing)
            return is_empty_data(
                data=list(func(limit=limit)),
                message=f"No {listing} posts found in {self._subreddit.display_name_prefixed}.",
            )
        else:
            return None

    def profile(self, status: t.Optional[Status] = None) -> t.Union["Subreddit", None]:
        if self.exists(status=status):
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
        sort: SORT,
        time_filter: TIME_FILTERS,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[Submission], None]:
        """
        Searches for posts in the subreddit based on the provided query.

        :param query: Search query string.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sorting method for the search results.
        :type sort: SORT
        :param time_filter: Time filter for the search results.
        :type time_filter: TIME_FILTERS
        :param status: Optional status object for updating progress.
        :type status: t.Optional[Status]
        :return: List of posts matching the search query, or None if the subreddit does not exist.
        :rtype: t.Union[t.List[Submission], None]
        """
        if self.exists(status=status):
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

            return is_empty_data(
                data=list(results),
                message=f"No results found for '{query}' in {self._subreddit.display_name_prefixed}.",
            )
        else:
            return None

    def wiki_pages(
        self, status: t.Optional[Status] = None
    ) -> t.Union[t.List[SubredditWiki], None]:
        """
        Retrieves a list of wiki pages from the subreddit.

        :param status: Optional status object for updating progress.
        :type status: t.Optional[Status]
        :return: List of wiki pages from the subreddit, or None if the subreddit does not exist.
        :rtype: t.Union[t.List[SubredditWiki], None]
        """
        if self.exists(status=status):
            if isinstance(status, Status):
                status.update(
                    f"Getting wiki pages from {self._subreddit.display_name_prefixed}...",
                )

            pages = self._subreddit.wiki
            return is_empty_data(
                data=list(pages),
                message=f"No wiki pages found in {self._subreddit.display_name_prefixed}.",
            )
        else:
            return None

    def exists(self, status: t.Optional[Status] = None) -> bool:
        """
        Checks if the subreddit exists by attempting to access its ID.

        :param status: Optional status object for updating progress.
        :type status: t.Optional[Status]
        :return: True if the subreddit exists, False otherwise.
        :rtype: bool
        """
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

        if verdict:
            console.print(
                f"{rich_colours.BOLD_GREEN}✔{rich_colours.BOLD_GREEN_RESET} {self._display_name} is a real subreddit"
            )

        elif not verdict:
            console.print(
                f"{rich_colours.BOLD_YELLOW}✘{rich_colours.BOLD_YELLOW_RESET} {self._display_name} is not a real subreddit"
            )
        return verdict
