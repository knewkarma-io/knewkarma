import typing as t
from logging import Logger

import requests
from rich.status import Status

from engines.karmakaze.schemas import Post, Subreddit, User
from knewkarma.config.client import reddit


class Search:
    """
    Represents the Reddit search functionality and provides methods for retrieving search results
    from different entities.
    """

    def __init__(self, query: str):
        """
        Initialises the `Search` instance for searching posts, subreddits, and users.

        :param query: The search query string.
        :type query: str
        """

        self._query = query

    def posts(
        self,
        session: requests.Session,
        limit: int,
        status: t.Optional[Status] = None,
        logger: t.Optional[Logger] = None,
    ) -> t.List[Post]:
        """
        Gets posts that match with the specified query.

        :param session: An `requests.Session` for making the HTTP request.
        :type session: requests.Session
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        search_results = reddit.search(
            session=session,
            logger=logger,
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
        logger: t.Optional[Logger] = None,
    ) -> t.List[Subreddit]:
        """
        Gets subreddits that match with the specified query.

        :param session: An `requests.Session` for making the HTTP request.
                :type session: requests.Session



        :param limit: Maximum number of subreddits to retrieve.
        :type limit: int
        :param sort: Sorting criterion for subreddits. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed subreddit data.
        :rtype: List[SimpleNamespace]
        """

        search_results = reddit.search(
            session=session,
            logger=logger,
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
        logger: t.Optional[Logger] = None,
    ) -> t.List[User]:
        """
        Gets users that match with the specified query.

        :param session: An `requests.Session` for making the HTTP request.
                :type session: requests.Session




        :param limit: Maximum number of users to retrieve.
        :type limit: int
        :param sort: Sorting criterion for users. Defaults to "all".
        :type sort: SORT, optional
        :param status: An optional `rich.status.Status` object for displaying status messages. Defaults to None.
        :type status: Optional[rich.status.Status]
        :param logger:
        :type logger: Logger
        :return: A list of `SimpleNamespace` objects, each containing parsed user data.
        :rtype: List[SimpleNamespace]
        """

        search_results = reddit.search(
            session=session,
            logger=logger,
            status=status,
            kind="users",
            query=self._query,
            limit=limit,
        )

        return search_results
