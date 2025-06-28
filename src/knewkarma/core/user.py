import typing as t
from collections import Counter

from praw.models import Submission, Redditor, Comment, Subreddit
from rich.status import Status

from karmakrate.riches import rich_colours
from karmakrate.riches.rich_logging import console
from karmakrate.riches.rich_render import Render
from .client import reddit, LISTINGS


class User:
    def __init__(self, username: str):
        self._redditor = reddit.redditor(name=username)
        self._username = username

    def comments(
        self,
        limit: int,
        listing: LISTINGS,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[Comment], None]:
        if self.exists(status=status):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} {listing} comments from u/{self._username}..."
                )

            func = getattr(self._redditor, listing)
            return list(func(limit=limit))

        else:
            return None

    def moderated(
        self, status: t.Optional[Status] = None
    ) -> t.Union[t.List[Subreddit], None]:
        if self.exists(status=status):
            if isinstance(status, Status):
                self.exists(status=status)

                status.update(
                    f"Getting moderated subreddits from u/{self._username}..."
                )
            return list(self._redditor.moderated())

        else:
            return None

    def overview(
        self,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[Comment], None]:
        if self.exists(status=status):
            if isinstance(status, Status):
                status.update(f"Getting recent comments from u/{self._username}...")

            return list(self._redditor.comments.new(limit=None))

        else:
            return None

    def posts(
        self,
        limit: t.Optional[int],
        listing: LISTINGS,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[Submission], None]:
        if self.exists(status=status):
            if isinstance(status, Status):
                status.update(
                    f"Getting {limit} {listing} posts from u/{self._username}..."
                )

            func = getattr(self._redditor.submissions, listing)
            return list(func(limit=limit))
        else:
            return None

    def profile(
        self,
        status: t.Optional[Status] = None,
    ) -> t.Union[Redditor, None]:
        if self.exists(status=status):
            if isinstance(status, Status):
                status.update(f"Getting profile info from u/{self._username}...")

            return self._redditor

        else:
            return None

    def top_subreddits(
        self,
        top_n: int,
        status: t.Optional[Status] = None,
    ):
        if self.exists(status=status):
            posts = self.posts(status=status, limit=None, listing="top")

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

                Render.bar_chart(
                    data=data,
                    title=f"top {top_n}/{len(posts)} subreddits analysis",
                    x_label="Subreddits",
                    y_label="Frequency",
                )

    def exists(
        self,
        status: t.Optional[Status] = None,
    ) -> bool:
        if isinstance(status, Status):
            status.update(f"Checking user availability...")

        verdict: bool = (
            True if not reddit.username_available(name=self._username) else False
        )

        if verdict:
            console.print(
                f"{rich_colours.BOLD_GREEN}✔{rich_colours.BOLD_GREEN_RESET} {self._username} is a real user"
            )

        elif not verdict:
            console.print(
                f"{rich_colours.BOLD_YELLOW}✘{rich_colours.BOLD_YELLOW_RESET} {self._username} is not a real user"
            )
        return verdict
