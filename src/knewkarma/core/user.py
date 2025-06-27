import typing as t
from collections import Counter
from logging import Logger

import requests
from rich.status import Status

from engines.karmakaze.schemas import Comment, Subreddit, Post
from tools import colours
from tools.rich_render import RichRender
from .client import reddit


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, username: str):
        """
        Initialises a `User()` instance for getting a user's `profile`, `posts` and `comments` data.

        :param username: Username to get data from.
        :type username: str
        """

        self.username = username

    def comments(
        self,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Comment]:
        """
        Get a user's comments.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which tyo get comments.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing comment data.
        :rtype: List[SimpleNamespace]
        """

        user_comments = reddit.comments(
            session=session,
            logger=logger,
            status=status,
            kind="user",
            username=self.username,
            limit=limit,
        )

        return user_comments

    def moderated_subreddits(
        self,
        session: requests.Session,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Subreddit]:
        """
        Get subreddits moderated by user.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        subreddits = reddit.subreddits(
            session=session,
            logger=logger,
            status=status,
            kind="user_moderated",
            timeframe="all",
            username=self.username,
            limit=0,
        )

        return subreddits

    def overview(
        self,
        limit: int,
        session: requests.Session,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Comment]:
        """
        Get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing data about a recent comment.
        :rtype: List[SimpleNamespace]
        """

        user_overview = reddit.comments(
            session=session,
            logger=logger,
            status=status,
            kind="u_overview",
            limit=limit,
            sort="all",
            timeframe="all",
            username=self.username,
        )

        return user_overview

    def posts(
        self,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Get a user's posts.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing post data.
        :rtype: List[SimpleNamespace]
        """

        user_posts = reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="user",
            limit=limit,
            username=self.username,
        )

        return user_posts

    def profile(
        self,
        session: requests.Session,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ):
        """
        Get a user's profile data.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger:
        :return: A SimpleNamespace object containing user profile data.
        :rtype: SimpleNamespace
        """

        user_profile = reddit.user(
            session=session,
            status=status,
            logger=logger,
            name=self.username,
        )

        return user_profile

    def search_comments(
        self,
        query: str,
        limit: int,
        session: requests.Session,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Comment]:
        """
        Search user comments that match the query string.
        """
        comments = self.comments(
            limit=limit,
            sort="all",
            timeframe="all",
            status=status,
            logger=logger,
            session=session,
        )

        results = []

        for comment in comments:
            if query in getattr(comment, "body"):
                results.append(comment)

        return results

    def search_posts(
        self,
        query: str,
        limit: int,
        session: requests.Session,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Search user posts that much the query string.
        """
        posts = self.posts(
            limit=limit,
            sort="all",
            timeframe="all",
            status=status,
            logger=logger,
            session=session,
        )

        results = []

        for post in posts:
            if query in getattr(post, "title") or getattr(post, "selftext"):
                results.append(post)

        return results

    def top_subreddits(
        self,
        session: requests.Session,
        top_n: int,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.Union[t.Dict[str, int], None]:
        """
        Get a user's top n subreddits based on subreddit frequency in n posts and saves the analysis to a file.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param top_n: Communities arranging number.
        :type top_n: int
        :param limit: Maximum number of posts to scrape.
        :type limit: int
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        """

        posts = self.posts(
            session=session,
            logger=logger,
            status=status,
            limit=limit,
            sort="all",
        )

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

            data: t.Dict[str, int] = dict(zip(subreddit_names, subreddit_frequencies))

            if logger or status:
                RichRender.bar_chart(
                    data=data,
                    title=f"top {top_n}/{limit} subreddits analysis",
                    x_label="Subreddits",
                    y_label="Frequency",
                )
            return data
        return None

    def does_user_exist(
        self,
        session: requests.Session,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.Union[bool, None]:
        """
        Checks if a specified user exists.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: `True` if the given username is available. Otherwise, `False`.
        :rtype: bool
        """

        if isinstance(status, Status):
            status.update(f"Checking user existence: {self.username}...")

        response: bool = reddit.send_request(
            url=reddit.ENDPOINTS["username_available"],
            session=session,
            params={"user": self.username},
            status=status,
            logger=logger,
        )

        if isinstance(logger, Logger):
            if bool(response) is True:
                logger.info(
                    f"[{self.username}] {colours.BOLD_YELLOW}User does not exist{colours.BOLD_YELLOW_RESET}"
                )
            else:
                logger.warning(
                    f"[{self.username}] {colours.BOLD_GREEN}User exists{colours.BOLD_GREEN_RESET}"
                )
        else:
            return response

        return None
