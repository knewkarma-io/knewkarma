import typing as t
from collections import Counter
from logging import Logger

from praw.models import Submission, Redditor
from rich.status import Status

from engines.karmakaze.schemas import Comment, Subreddit
from tools import colours
from tools.rich_render import RichRender
from ..config.client import reddit, LISTINGS


class User:
    def __init__(self, username: str):
        self._redditor = reddit.redditor(name=username)
        self._username = username

    def comments(
        self,
        limit: int,
        status: Status,
        logger: Logger,
        listing: LISTINGS,
    ) -> t.Union[t.List[Comment], None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} {listing} comments from u/{self._username}..."
                )

            func = getattr(self._redditor, listing)
            return list(func(limit=limit))

        else:
            return None

    def moderated(
        self, status: Status, logger: Logger
    ) -> t.Union[t.List[Subreddit], None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                self.exists(status=status, logger=logger)

                status.update(
                    f"Getting moderated subreddits from u/{self._username}..."
                )
            return list(self._redditor.moderated())

        else:
            return None

    def overview(
        self, status: Status, logger: Logger
    ) -> t.Union[t.List[Comment], None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(f"Getting recent comments from u/{self._username}...")

            return list(self._redditor.comments.new(limit=None))

        else:
            return None

    def posts(
        self,
        limit: t.Optional[int],
        status: Status,
        logger: Logger,
        listing: LISTINGS,
    ) -> t.Union[t.List[Submission], None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} {listing} posts from u/{self._username}..."
                )

            func = getattr(self._redditor.submissions, listing)
            return list(func(limit=limit))
        else:
            return None

    def profile(self, status: Status, logger: Logger) -> t.Union[Redditor, None]:
        if self.exists(status=status, logger=logger):
            if isinstance(status, Status):
                status.update(f"Getting profile info from u/{self._username}...")

            return self._redditor

        else:
            return None

    def top_subreddits(self, top_n: int, status: Status, logger: Logger):
        if self.exists(status=status, logger=logger):
            posts = self.posts(status=status, logger=logger, limit=None, listing="top")

            if posts:
                # Extract subreddit names
                subreddits = [post.data.subreddit for post in posts]

                # Count the occurrences of each subreddit
                subreddit_counts: t.Counter = Counter(subreddits)

                # Get the most common subreddits
                top_subreddits: t.List[tuple[str, int]] = subreddit_counts.most_common(
                    top_n
                )

                # Prepare data for plotting
                subreddit_names = [subreddit[0] for subreddit in top_subreddits]
                subreddit_frequencies = [subreddit[1] for subreddit in top_subreddits]

                data: t.Dict[str, int] = dict(
                    zip(subreddit_names, subreddit_frequencies)
                )

                RichRender.bar_chart(
                    data=data,
                    title=f"top {top_n}/{len(posts)} subreddits analysis",
                    x_label="Subreddits",
                    y_label="Frequency",
                )

    def exists(self, status: Status, logger: Logger) -> bool:
        if isinstance(status, Status):
            status.update(f"Checking user availability...")

        verdict: bool = (
            True if not reddit.username_available(name=self._username) else False
        )

        if isinstance(logger, Logger):
            if verdict:
                logger.warning(
                    f"{colours.BOLD_GREEN}✔{colours.BOLD_GREEN_RESET} Username exists"
                )

            elif not verdict:
                logger.info(
                    f"{colours.BOLD_YELLOW}✘{colours.BOLD_YELLOW_RESET} Username does not exist"
                )
        return verdict
