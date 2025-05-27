import typing as t
from collections import Counter
from logging import Logger

import aiohttp
from rich.status import Status

from engines.karmakaze.schemas import Comment, Subreddit, Post
from toolbox.render import Render
from .client import reddit

print(reddit.ENDPOINTS["username_available"])


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, name: str):
        """
        Initialises a `User()` instance for getting a user's `profile`, `posts` and `comments` data.

        :param name: Username to get data from.
        :type name: str
        """

        self.name = name

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Comment]:
        """
        Asynchronously get a user's comments.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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

        user_comments = await reddit.comments(
            session=session,
            logger=logger,
            status=status,
            kind="user",
            username=self.name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return user_comments

    async def moderated_subreddits(
        self,
        session: aiohttp.ClientSession,
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[Subreddit]:
        """
        Asynchronously get subreddits moderated by user.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession




        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        subreddits = await reddit.subreddits(
            session=session,
            logger=logger,
            status=status,
            kind="user_moderated",
            timeframe="all",
            username=self.name,
            limit=0,
        )

        return subreddits

    async def overview(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[Comment]:
        """
        Asynchronously get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession




        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing data about a recent comment.
        :rtype: List[SimpleNamespace]
        """

        user_overview = await reddit.comments(
            session=session,
            logger=logger,
            status=status,
            kind="user_overview",
            limit=limit,
            sort="all",
            timeframe="all",
            username=self.name,
        )

        return user_overview

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.List[Post]:
        """
        Asynchronously get a user's posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
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

        user_posts = await reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="user",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            username=self.name,
        )

        return user_posts

    async def profile(
        self,
        session: aiohttp.ClientSession,
        status: t.Optional[Status] = Status,
    ):
        """
        Asynchronously get a user's profile data.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A SimpleNamespace object containing user profile data.
        :rtype: SimpleNamespace
        """

        user_profile = await reddit.user(
            session=session,
            status=status,
            name=self.name,
        )

        return user_profile

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.Union[t.Dict[str, int], None]:
        """
        Asynchronously get a user's top n subreddits based on subreddit frequency in n posts and saves the analysis to a file.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




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

        posts = await reddit.posts(
            session=session,
            logger=logger,
            status=status,
            kind="user",
            limit=limit,
            sort="all",
            timeframe=timeframe,
            username=self.name,
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
                Render.bar_chart(
                    data=data,
                    title=f"top {top_n}/{limit} subreddits analysis",
                    x_label="Subreddits",
                    y_label="Frequency",
                )
            return data
        return None

    async def is_username_available(
        self,
        session: aiohttp.ClientSession,
        status: t.Optional[Status] = Status,
        logger: t.Optional[Logger] = Logger,
    ) -> t.Union[bool, None]:
        """
        Checks if the given username is available or taken.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
                :type session: aiohttp.ClientSession




        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: `True` if the given username is available. Otherwise, `False`.
        :rtype: bool
        """

        if status:
            status.update(f"Checking username availability: {self.name}")

        response: bool = await reddit.send_request(
            session=session,
            url=reddit.ENDPOINTS["username_available"],
            params={"user": self.name},
        )

        if status and logger:
            if bool(response) is True:
                logger.info(f"Username ({self.name}) is available")
            else:
                logger.warning(f"Username ({self.name}) is already taken")
        else:
            return response

        return None
