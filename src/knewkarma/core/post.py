import typing as t
from logging import Logger

import requests
from rich.status import Status

from engines.karmakaze import schemas
from .client import reddit


class Post:
    """Represents a Reddit post and provides methods for fetching post data and comments."""

    def __init__(self, id: str, subreddit: str):
        """
        Initialises a `Post` instance to fetch the post's data and comments.

        :param id: The ID of the Reddit post to retrieve.
        :type id: str
        :param subreddit: The subreddit where the post was created.
        :type subreddit: str
        """

        self._id = id
        self._subreddit = subreddit

    def data(
        self,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ) -> schemas.Post:
        """
        Asynchronously retrieves data for a Reddit post, excluding comments.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session




        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :return: A `Post` object containing parsed post data.
        :rtype: Post
        """

        post_data = reddit.post(
            session=session,
            status=status,
            id=self._id,
            subreddit=self._subreddit,
        )

        return post_data

    def comments(
        self,
        session: requests.Session,
        limit: int,
        sort: reddit.SORT = "all",
        timeframe: reddit.TIMEFRAME = "all",
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[schemas.Comment]:
        """
        Asynchronously retrieves comments for a Reddit post.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session




        :param limit: Maximum number of comments to retrieve.
        :type limit: int
        :param sort: The sorting criterion for the comments. Defaults to "all".
        :type sort: SORT, optional
        :param timeframe:
        :type timeframe:
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `Comment` objects, each containing parsed comment data.
        :rtype: List[Comment]
        """

        comments_data = reddit.comments(
            session=session,
            logger=logger,
            status=status,
            kind="post",
            id=self._id,
            subreddit=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        return comments_data
