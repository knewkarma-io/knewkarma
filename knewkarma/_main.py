import re
from collections import Counter
from typing import List, Dict

import requests
from rich.pretty import pprint

from .api import Api, SORT_CRITERION, TIMEFRAME, TIME_FORMAT
from .tools.general_utils import console
from .tools.parsing_utils import (
    parse_comments,
    parse_subreddits,
    parse_posts,
    parse_users,
    parse_wiki_page,
)

__all__ = ["Post", "Posts", "Search", "Subreddit", "Subreddits", "User", "Users"]

api = Api()


class Post:
    """Represents a Reddit post and provides method(s) for getting data from the specified post."""

    def __init__(
        self, post_id: str, post_subreddit: str, time_format: TIME_FORMAT = "locale"
    ):
        """
        Initialises the `Post()` instance for getting post's `data` and `comments`.

        :param post_id: ID of a post to get data from.
        :type post_id: str
        :param post_subreddit: Subreddit where the post was created.
        :type post_subreddit: str
        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._post_id = post_id
        self._post_subreddit = post_subreddit
        self._time_format = time_format
        self._status_template: str = (
            "Fetching {query_type} from post {post_id} in r/{post_subreddit}..."
        )

    def data(self, session: requests.Session, status: console.status = None) -> Dict:
        """
        Get a post's data (without comments)

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A dictionary containing a post's data.
        :rtype: dict

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Post
            >>> from pprint import pprint

            >>> def get_post_data():
            >>>    post = Post(post_id="13ptwzd", post_subreddit="AskReddit")
            >>>    with requests.Session() as request_session:
            >>>        data = post.data(session=request_session)
            >>>        pprint(data)


            >>> get_post_data()
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="data",
                    post_id=self._post_id,
                    post_subreddit=self._post_subreddit,
                )
            )

        post_data: dict = api.get_entity(
            post_id=self._post_id,
            post_subreddit=self._post_subreddit,
            entity_type="post",
            status=status,
            session=session,
        )

        if post_data:
            return parse_posts(
                data=post_data,
                time_format=self._time_format,
            )

    def comments(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a post's comments.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Post
            >>> from pprint import pprint

            >>> def get_post_comments(comments_limit, comments_sort):
            >>>    post = Post(post_id="13ptwzd", post_subreddit="AskReddit")
            >>>    with requests.Session() as request_session:
            >>>        comments = post.comments(limit=comments_limit, sort=comments_sort, session=request_session)
            >>>        pprint(comments)


            >>> get_post_comments(comments_limit=50, comments_sort="top")
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} comments",
                    post_id=self._post_id,
                    post_subreddit=self._post_subreddit,
                )
            )

        comments_data: List = api.get_posts(
            posts_type="post_comments",
            post_id=self._post_id,
            post_subreddit=self._post_subreddit,
            limit=limit,
            sort=sort,
            status=status,
            session=session,
        )

        if comments_data:
            return parse_comments(
                comments=comments_data,
                time_format=self._time_format,
            )


class Posts:
    """Represents Reddit posts and provides methods for getting posts from various sources."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Posts()` instance for getting `best`, `controversial`,
        `front-page`, `new`, `popular`, and `rising` posts.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._time_format = time_format
        self._status_template: str = "Fetching {limit} {listing} posts..."

    def best(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get best posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get best posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Posts
            >>> from pprint import pprint

            >>> def get_best_posts(posts_limit):
            >>>    posts = Posts()
            >>>    with requests.Session() as request_session:
            >>>        best = posts.best(limit=posts_limit, session=request_session)
            >>>        pprint(best)


            >>> get_best_posts(posts_limit=120)
        """
        if status:
            status.update(self._status_template.format(listing="best", limit=limit))

        best_posts: List = api.get_posts(
            posts_type="best",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if best_posts:
            return parse_posts(data=best_posts, time_format=self._time_format)

    def controversial(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get controversial posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get controversial posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Posts


            >>> def get_controversial_posts(posts_limit):
            >>>    posts = Posts()
            >>>    with requests.Session() as request_session:
            >>>        controversial = posts.controversial(limit=posts_limit, session=request_session)
            >>>        print(controversial)

            >>> get_controversial_posts(posts_limit=50)
        """
        if status:
            status.update(
                self._status_template.format(listing="controversial", limit=limit)
            )

        controversial_posts: List = api.get_posts(
            posts_type="controversial",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if controversial_posts:
            return parse_posts(data=controversial_posts, time_format=self._time_format)

    def front_page(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get posts from the Reddit front-page.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Posts
            >>> from pprint import pprint

            >>> def get_frontpage_posts(posts_limit):
            >>>    posts = Posts()
            >>>    with requests.Session() as request_session:
            >>>        frontpage = posts.front_page(limit=posts_limit, session=request_session)
            >>>        print(frontpage)


            >>> get_frontpage_posts(posts_limit=10)
        """
        if status:
            status.update(
                self._status_template.format(listing="front-page", limit=limit)
            )

        front_page_posts: List = api.get_posts(
            posts_type="front_page",
            limit=limit,
            sort=sort,
            status=status,
            session=session,
        )

        if front_page_posts:
            return parse_posts(data=front_page_posts, time_format=self._time_format)

    def new(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get new posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Posts
            >>> from pprint import pprint

            >>> def get_new_posts(posts_limit):
            >>>    posts = Posts()
            >>>    with requests.Session() as request_session:
            >>>        new = posts.new(limit=posts_limit, session=request_session)
            >>>        print(new)


            >>> get_new_posts(posts_limit=10)
        """
        if status:
            status.update(self._status_template.format(listing="new", limit=limit))

        new_posts: List = api.get_posts(
            posts_type="new",
            limit=limit,
            sort=sort,
            status=status,
            session=session,
        )

        if new_posts:
            return parse_posts(data=new_posts, time_format=self._time_format)

    def popular(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get popular posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Posts
            >>> from pprint import pprint

            >>> def get_popular_posts(posts_limit):
            >>>    posts = Posts()
            >>>    with requests.Session() as request_session:
            >>>        popular = posts.popular(limit=posts_limit, session=request_session)
            >>>        pprint(popular)


            >>> get_popular_posts(posts_limit=50)
        """
        if status:
            status.update(self._status_template.format(listing="popular", limit=limit))

        popular_posts: List = api.get_posts(
            posts_type="popular",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if popular_posts:
            return parse_posts(data=popular_posts, time_format=self._time_format)

    def rising(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get rising posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param timeframe: Timeframe from which to get rising posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Posts
            >>> from pprint import pprint

            >>> def get_rising_posts(posts_limit):
            >>>    posts = Posts()
            >>>    with requests.Session() as request_session:
            >>>        rising = posts.rising(limit=posts_limit, session=request_session)
            >>>        pprint(rising)


            >>> get_rising_posts(posts_limit=100)
        """
        if status:
            status.update(self._status_template.format(listing="rising", limit=limit))

        rising_posts: List = api.get_posts(
            posts_type="rising",
            timeframe=timeframe,
            limit=limit,
            status=status,
            session=session,
        )

        if rising_posts:
            return parse_posts(data=rising_posts, time_format=self._time_format)


class Search:
    """
    Represents the Readit search functionality and provides
    methods for getting search results from different entities
    """

    def __init__(self, query: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Search()` instance for searching `posts`, `subreddits` and `users`.

        :param query: Search query.
        :type query: str
        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._query = query
        self._time_format = time_format
        self._status_template: str = (
            "Searching for '{query}' in {limit} {query_type}..."
        )

    def posts(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Search posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Search
            >>> from pprint import pprint

            >>> def search_posts(query, results_limit):
            >>>    search = Search(query=query)
            >>>    with requests.Session() as request_session:
            >>>        posts = search.posts(limit=results_limit, session=request_session)
            >>>        pprint(posts)


            >>> search_posts(query="something in data science", results_limit=200)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="posts", limit=limit, query=self._query
                )
            )

        posts_results: List = api.search_entities(
            query=self._query,
            entity_type="posts",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )
        if posts_results:
            return parse_posts(data=posts_results, time_format=self._time_format)

    def subreddits(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Search subreddits.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Search
            >>> from pprint import pprint

            >>> def search_for_subreddits(query, results_limit):
            >>>    search = Search(query=query)
            >>>    with requests.Session() as request_session:
            >>>        subreddits = search.subreddits(limit=results_limit, session=request_session)
            >>>        pprint(subreddits)


            >>> search_for_subreddits(query="questions", results_limit=200)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="subreddits", limit=limit, query=self._query
                )
            )

        search_subreddits: List = api.search_entities(
            query=self._query,
            entity_type="subreddits",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )
        subreddits_results: List[Dict] = parse_subreddits(
            search_subreddits, time_format=self._time_format
        )

        return subreddits_results

    def users(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Search users.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing user data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Search
            >>> from pprint import pprint

            >>> def search_for_users(query, results_limit):
            >>>    search = Search(query=query)
            >>>    with requests.Session() as request_session:
            >>>        users = search.users(limit=results_limit, session=request_session)
            >>>        pprint(users)


            >>> search_for_users(query="john", results_limit=200)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="users", limit=limit, query=self._query
                )
            )

        search_users: List = api.search_entities(
            query=self._query,
            entity_type="users",
            sort=sort,
            limit=limit,
            status=status,
            session=session,
        )
        users_results: List[Dict] = parse_users(
            search_users, time_format=self._time_format
        )

        return users_results


class Subreddit:
    """Represents a Reddit Community (Subreddit) and provides methods for getting data from the specified subreddit."""

    def __init__(self, subreddit: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Subreddit()` instance for getting a subreddit's `profile`, `wiki pages`,
        `wiki page`, and `posts` data, as well as `searching for posts that contain a specified query`.

        :param subreddit: Name of the subreddit to get data from.
        :type subreddit: str
        :param time_format: Time format of the output data. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._subreddit = subreddit
        self._time_format = time_format
        self._status_template: str = (
            "Fetching {query_type} from subreddit r/{subreddit}..."
        )

    def comments(
        self,
        session: requests.Session,
        posts_limit: int,
        comments_per_post: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a subreddit's comments.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param posts_limit: Maximum number of posts to get comments from.
        :type posts_limit: int
        :param comments_per_post: Maximum number of comments to get from each post.
        :type comments_per_post: int
        :param sort: Sort criterion for the posts and comments.
        :type sort: str
        :param timeframe: Timeframe from which to get posts and comments.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of comments, each containing comment data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddit
            >>> import requests

            >>> def get_subreddit_comments(subreddit, posts_count, comments_p_post):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    with requests.Session() as request_session:
            >>>        comments = subreddit.comments(
            >>>                       posts_limit=posts_count,
            >>>                       comments_per_post=comments_p_post,
            >>>                       session=request_session
            >>>                   )
            >>>        pprint(comments)


            >>> get_subreddit_comments( subreddit="AskScience", posts_count=100, comments_p_post=20)
        """
        posts = self.posts(
            session=session,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
        )
        all_comments: List = []
        for post in posts:
            post = Post(
                post_id=post.get("id"),
                post_subreddit=post.get("subreddit"),
                time_format=self._time_format,
            )
            post_comments: List = post.comments(
                session=session, limit=comments_per_post, sort=sort, status=status
            )

            all_comments.extend(post_comments)

        return all_comments

    def posts(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a subreddit's posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddit
            >>> import requests

            >>> def get_subreddit_posts(subreddit, posts_limit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    with requests.Session() as request_session:
            >>>        posts = subreddit.posts(limit=posts_limit, session=request_session)
            >>>        pprint(posts)

            >>> get_subreddit_posts(posts_limit=500, subreddit="MachineLearning")
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} posts", subreddit=self._subreddit
                )
            )

        subreddit_posts: List = api.get_posts(
            posts_type="subreddit_posts",
            subreddit=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if subreddit_posts:
            return parse_posts(data=subreddit_posts, time_format=self._time_format)

    def profile(
        self,
        session: requests.Session,
        status: console.status = None,
    ) -> Dict:
        """
        Get a subreddit's profile data.

        :param session: aiohttp session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A dictionary containing subreddit profile data.
        :rtype: dict

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddit
            >>> from pprint import pprint

            >>> def get_subreddit_profile(subreddit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    with requests.Session() as request_session:
            >>>        profile = subreddit.profile(session=request_session)
            >>>        pprint(profile)


            >>> get_subreddit_profile(subreddit="MachineLearning")
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="profile data", subreddit=self._subreddit
                )
            )

        subreddit_profile: dict = api.get_entity(
            entity_type="subreddit",
            subreddit=self._subreddit,
            status=status,
            session=session,
        )
        if subreddit_profile:
            return parse_subreddits(
                data=subreddit_profile, time_format=self._time_format
            )

    def search_comments(
        self,
        session: requests.Session,
        query: str,
        posts_limit: int,
        comments_per_post: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get comments that contain the specified query string from a subreddit.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param query: Search query.
        :type query: str
        :param posts_limit: Maximum number of posts to get comments from.
        :type posts_limit: int
        :param comments_per_post: A maximum number of comments to get for each post.
        :type comments_per_post: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddit
            >>> from pprint import pprint

            >>> def search_subreddit_comments(search_query, subreddit, post_limit, comments_p_post):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    with requests.Session() as request_session:
            >>>        subreddit_comments = subreddit.search_comments(
            >>>            query=search_query,
            >>>            posts_limit=post_limit,
            >>>            comments_per_post=comments_p_post,
            >>>            session=request_session
            >>>        )
            >>>        pprint(subreddit_comments)


            >>> search_subreddit_comments(
            >>>     search_query="ML jobs",
            >>>     post_limit=100,
            >>>     comments_per_post=10,
            >>>     subreddit="MachineLearning"
            >>>   )
            >>> )
        """
        posts: List = self.posts(
            session=session,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
        )
        all_comments: List = []
        found_comments: List = []
        for post in posts:
            if status:
                status.update(f"Fetching comments from post {post.get('id')}...")

            post = Post(
                post_id=post.get("id"),
                post_subreddit=self._subreddit,
                time_format=self._time_format,
            )

            comments: List = post.comments(
                session=session, limit=comments_per_post, status=status
            )

            all_comments.extend(comments)

        pattern: str = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        for comment in all_comments:
            match: re.Match = regex.search(comment.get("body", ""))
            if match:
                found_comments.append(comment)

        if found_comments:
            return found_comments

    def search_posts(
        self,
        session: requests.Session,
        query: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get posts that contain the specified query string from a subreddit.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddit
            >>> from pprint import pprint

            >>> def search_subreddit_posts(search_query, subreddit, posts_limit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    with requests.Session() as request_session:
            >>>        posts = subreddit.search_posts(query=search_query, limit=posts_limit, session=request_session)
            >>>        pprint(posts)


            >>> search_subreddit_posts(
            >>>     search_query="ML jobs",
            >>>     posts_limit=100,
            >>>     subreddit="MachineLearning"
            >>>   )
            >>> )
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} posts with '{query}'",
                    subreddit=self._subreddit,
                )
            )
        found_posts: List = api.get_posts(
            posts_type="search_subreddit_posts",
            subreddit=self._subreddit,
            query=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if found_posts:
            return parse_posts(data=found_posts, time_format=self._time_format)

    def wiki_pages(
        self,
        session: requests.Session,
        status: console.status = None,
    ) -> list[str]:
        """
        Get a subreddit's wiki pages.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddit
            >>> from pprint import pprint

            >>> def get_subreddit_wiki_pages(subreddit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    with requests.Session() as request_session:
            >>>        wiki_pages = subreddit.wiki_pages(session=request_session)
            >>>        pprint(wiki_pages)


            >>> get_subreddit_wiki_pages(subreddit="MachineLearning")
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="wiki pages", subreddit=self._subreddit
                )
            )

        pages: dict = api.make_request(
            endpoint=f"{api.subreddit_endpoint}/{self._subreddit}/wiki/pages.json",
            session=session,
        )

        return pages.get("data")

    def wiki_page(
        self,
        page_name: str,
        session: requests.Session,
        status: console.status = None,
    ) -> Dict:
        """
        Get a subreddit's specified wiki page data.

        :param page_name: Wiki page to get data from.
        :type page_name: str
        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddit
            >>> from pprint import pprint

            >>> def get_subreddit_wiki_page(page, subreddit):
            >>>    subreddit = Subreddit(subreddit=subreddit)
            >>>    with requests.Session() as request_session:
            >>>        wiki_page_data = subreddit.wiki_page(page_name=page, session=request_session)
            >>>        pprint(wiki_page_data)


            >>> get_subreddit_wiki_page(page="rules", subreddit="MachineLearning")
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="wiki page data", subreddit=self._subreddit
                )
            )

        wiki_page: dict = api.get_entity(
            entity_type="wiki_page",
            page_name=page_name,
            subreddit=self._subreddit,
            status=status,
            session=session,
        )

        if wiki_page:
            return parse_wiki_page(wiki_page=wiki_page, time_format=self._time_format)


class Subreddits:
    """Represents Reddit subreddits and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Subreddits()` instance for getting `all`, `default`, `new` and `popular` subreddits.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._time_format = time_format
        self._status_template: str = "Fetching {limit} {subreddits_type} subreddits..."

    def all(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get all subreddits.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get all subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: List[Dict]

        Note:
            -*imitating Morphius' voice*- "the only limitation you have at this point is the matrix's rate-limit."

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddits
            >>> from pprint import pprint

            >>> def get_all_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    with requests.Session() as request_session:
            >>>        all_subs = subreddits.all(limit=subreddits_limit, session=request_session)
            >>>        pprint(all_subs)


            >>> get_all_subreddits(subreddits_limit=500)
        """
        if status:
            status.update(
                self._status_template.format(subreddits_type="all", limit=limit)
            )

        all_subreddits: List = api.get_subreddits(
            subreddits_type="all",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if all_subreddits:
            return parse_subreddits(data=all_subreddits, time_format=self._time_format)

    def default(
        self,
        limit: int,
        session: requests.Session,
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddits
            >>> import requests


            >>> def get_default_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    with requests.Session() as request_session:
            >>>        default_subs = subreddits.default(limit=subreddits_limit, session=request_session)
            >>>        pprint(default_subs)


            >>> get_default_subreddits(subreddits_limit=20)
        """
        if status:
            status.update(
                self._status_template.format(subreddits_type="default", limit=limit)
            )

        default_subreddits: List = api.get_subreddits(
            subreddits_type="default",
            timeframe="all",
            limit=limit,
            status=status,
            session=session,
        )
        if default_subreddits:
            return parse_subreddits(default_subreddits, time_format=self._time_format)

    def new(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get new subreddits.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddits
            >>> import requests


            >>> def get_new_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    with requests.Session() as request_session:
            >>>        new_subs = subreddits.new(limit=subreddits_limit, session=request_session)
            >>>        pprint(new_subs)


            >>> get_new_subreddits(subreddits_limit=50)
        """
        if status:
            status.update(
                self._status_template.format(subreddits_type="new", limit=limit)
            )

        new_subreddits: List = api.get_subreddits(
            subreddits_type="new",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if new_subreddits:
            return parse_subreddits(new_subreddits, time_format=self._time_format)

    def popular(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get popular subreddits.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Subreddits
            >>> import requests


            >>> def get_popular_subreddits(subreddits_limit):
            >>>    subreddits = Subreddits()
            >>>    with requests.Session() as request_session:
            >>>        popular_subs = subreddits.popular(limit=subreddits_limit, session=request_session)
            >>>        pprint(popular_subs)


            >>> get_popular_subreddits(subreddits_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(subreddits_type="popular", limit=limit)
            )

        popular_subreddits: List = api.get_subreddits(
            subreddits_type="popular",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        if popular_subreddits:
            return parse_subreddits(popular_subreddits, time_format=self._time_format)


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, username: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `User()` instance for getting a user's `profile`, `posts` and `comments` data.

        :param username: Username to get data from.
        :type username: str
        :param time_format: Time format of the output data. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._username = username
        self._time_format = time_format
        self._status_template: str = "Fetching {query_type} from user u/{username}..."

    def comments(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a user's comments.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which tyo get comments.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def get_user_comments(username, comments_limit):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        comments = user.comments(limit=comments_limit, session=request_session)
            >>>        pprint(comments)


            >>> get_user_comments(username="AutoModerator", comments_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} comments", username=self._username
                )
            )

        user_comments: List = api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if user_comments:
            return parse_comments(comments=user_comments, time_format=self._time_format)

    def moderated_subreddits(
        self,
        session: requests.Session,
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get subreddits moderated by user.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing subreddit data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def get_user_moderated_subreddits(username):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        moderated_subs = user.moderated_subreddits(session=request_session)
            >>>        pprint(moderated_subs)


            >>> get_user_moderated_subreddits(username="TheRealKSI")
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="moderated subreddits", username=self._username
                )
            )

        subreddits: dict = api.get_subreddits(
            subreddits_type="user_moderated",
            username=self._username,
            limit=0,
            status=status,
            session=session,
        )

        if subreddits:
            return parse_subreddits(
                subreddits.get("data"),
                time_format=self._time_format,
            )

    def overview(
        self,
        limit: int,
        session: requests.Session,
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing data about a recent comment.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def get_user_overview(username, comments_limit):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        comments = user.overview(limit=comments_limit, session=request_session)
            >>>        pprint(comments)


            >>> get_user_overview(username="AutoModerator", comments_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} recent comments", username=self._username
                )
            )

        user_overview: List = api.get_posts(
            username=self._username,
            posts_type="user_overview",
            limit=limit,
            status=status,
            session=session,
        )

        if user_overview:
            return parse_comments(user_overview, time_format=self._time_format)

    def posts(
        self,
        session: requests.Session,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a user's posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def get_user_posts(username, posts_limit):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        posts = user.posts(limit=posts_limit, session=request_session)
            >>>        pprint(posts)


            >>> get_user_posts(username="AutoModerator", posts_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} posts", username=self._username
                )
            )

        user_posts: List = api.get_posts(
            username=self._username,
            posts_type="user_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if user_posts:
            return parse_posts(user_posts, time_format=self._time_format)

    def profile(
        self,
        session: requests.Session,
        status: console.status = None,
    ) -> Dict:
        """
        Get a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A dictionary containing user profile data.
        :rtype: dict

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def get_user_profile(username):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        profile = user.profile(session=request_session)
            >>>        pprint(profile)


            >>> get_user_profile(username="AutoModerator")
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type="profile data", username=self._username
                )
            )

        user_profile: dict = api.get_entity(
            username=self._username, entity_type="user", status=status, session=session
        )

        if user_profile:
            return parse_users(data=user_profile, time_format=self._time_format)

    def search_posts(
        self,
        query: str,
        limit: int,
        session: requests.Session,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a user's posts that match with the specified search query.

        :param query: Search query.
        :type query: str
        :param session: A requests.Session to use for the request.
        :type session: requests.Session.
        :param limit: Maximum number of posts to search from.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def search_user_posts(username, search_query, posts_limit):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        posts = user.search_posts(query=search_query,
            >>>                                limit=posts_limit, session=request_session)
            >>>        pprint(posts)


            >>> search_user_posts(username="AutoModerator",
            >>>                             search_query="user has been banned", posts_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} posts for '{query}'", username=self._username
                )
            )

        pattern: str = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        user_posts: List = api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        found_posts: List = []

        for post in user_posts:
            post_data: dict = post.get("data")

            match: re.Match = regex.search(post_data.get("title", "")) or regex.search(
                post_data.get("selftext", "")
            )

            if match:
                found_posts.append(post)

        if found_posts:
            return parse_posts(found_posts, time_format=self._time_format)

    def search_comments(
        self,
        query: str,
        limit: int,
        session: requests.Session,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get a user's comments that contain the specified search query.

        :param query: Search query.
        :type query: str
        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :type session: requests.Session.
        :param limit: Maximum number of comments to search from.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which to get comments.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing comment data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def search_user_comments(username, search_query, comments_limit):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        comments = user.search_comments(query=search_query,
            >>>                                limit=comments_limit, session=request_session)
            >>>        pprint(comments)


            >>> search_user_comments(username="AutoModerator",
            >>>                            search_query="this action is automated", comments_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"{limit} comments for '{query}'",
                    username=self._username,
                )
            )

        pattern: str = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        user_comments: List = api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            status=status,
            session=session,
        )
        found_comments: List = []

        for comment in user_comments:
            match = regex.search(comment.get("data", {}).get("body", ""))
            if match:
                found_comments.append(comment)

        if found_comments:
            return parse_comments(found_comments, time_format=self._time_format)

    def top_subreddits(
        self,
        session: requests.Session,
        top_n: int,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[tuple]:
        """
        Get a user's top n subreddits based on subreddit frequency in n posts.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param top_n: Communities arranging number.
        :type top_n: int
        :param limit: Maximum number of posts to scrape.
        :type limit: int
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: Dictionary of top n subreddits and their ratio.
        :rtype: dict

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import User
            >>> import requests


            >>> def get_user_top_subreddits(username, top_number, subreddits_limit):
            >>>    user = User(username=username)
            >>>    with requests.Session() as request_session:
            >>>        top_subs = user.top_subreddits(top_n=top_number,
            >>>                             limit=subreddits_limit, session=request_session)
            >>>        pprint(top_subs)


            >>> get_user_top_subreddits(username="TheRealKSI",
            >>>                                     top_number=10, subreddits_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(
                    query_type=f"top {top_n}/{limit} subreddits",
                    username=self._username,
                )
            )

        posts = api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if posts:
            # Extract subreddit names
            subreddits = [post.get("data", {}).get("subreddit") for post in posts]

            # Count the occurrences of each subreddit
            subreddit_counts = Counter(subreddits)

            return subreddit_counts.most_common(top_n)


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Users()` instance for getting `new`, `popular` and `all` users.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """
        self._time_format = time_format
        self._status_template: str = "Fetching {limit} {query_type} users..."

    def new(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get new users.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of new users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Users
            >>> import requests


            >>> def get_new_users(users_limit):
            >>>    users = Users()
            >>>    with requests.Session() as request_session:
            >>>        new = users.new(limit=users_limit, session=request_session)
            >>>        pprint(new)


            >>> get_new_users(users_limit=500)
        """
        if status:
            status.update(self._status_template.format(query_type="new", limit=limit))

        new_users: List = api.get_users(
            users_type="new",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if new_users:
            return parse_users(new_users, time_format=self._time_format)

    def popular(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get popular users.

        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param limit: Maximum number of popular users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Users
            >>> import requests


            >>> def get_popular_users(users_limit):
            >>>    users = Users()
            >>>    with requests.Session() as request_session:
            >>>        popular = users.popular(limit=users_limit, session=request_session)
            >>>        pprint(popular)


            >>> get_popular_users(users_limit=100)
        """
        if status:
            status.update(
                self._status_template.format(query_type="popular", limit=limit)
            )

        popular_users: List = api.get_users(
            users_type="popular",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if popular_users:
            return parse_users(popular_users, time_format=self._time_format)

    def all(
        self,
        session: requests.Session,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> List[Dict]:
        """
        Get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: A requests.Session to use for the request.
        :type session: requests.Session
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal[str]
        :param status: An instance of `console.status` used to display animated status messages.
        :type: rich.console.Console.status
        :return: A list of dictionaries, each containing a user's data.
        :rtype: List[Dict]

        Usage::

            >>> from pprint import pprint
            >>> from knewkarma import Users
            >>> import requests


            >>> def get_all_users(users_limit):
            >>>    users = Users()
            >>>    with requests.Session() as request_session:
            >>>        all_users_data = users.all(limit=users_limit, session=request_session)
            >>>        pprint(all_users_data)


            >>> get_all_users(users_limit=1000))
        """
        if status:
            status.update(self._status_template.format(query_type="all", limit=limit))

        all_users: List = api.get_users(
            users_type="all",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        if all_users:
            return parse_users(all_users, time_format=self._time_format)


# -------------------------------- END ----------------------------------------- #
