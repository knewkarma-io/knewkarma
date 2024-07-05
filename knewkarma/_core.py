import re
from collections import Counter

import aiohttp

from ._laundromat import (
    clean_comments,
    clean_subreddits,
    clean_subreddit_wiki_page,
    clean_posts,
    clean_users,
)
from ._utilities import TIME_FORMAT, get_status
from .api import Api, TIMEFRAME, SORT_CRITERION

api = Api()


class Post:
    """Represents a Reddit post and provides method(s) for getting data from the specified post."""

    def __init__(
        self, post_id: str, post_subreddit: str, time_format: TIME_FORMAT = "locale"
    ):
        self._post_id = post_id
        self._post_subreddit = post_subreddit
        self._time_format = time_format

    async def data(self, session: aiohttp.ClientSession) -> dict:
        """
        Returns a post's data (without comments)

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A dictionary containing a post's data.
        :rtype: dict
        """
        post_data: dict = await api.get_profile(
            post_id=self._post_id,
            post_subreddit=self._post_subreddit,
            profile_type="post",
            session=session,
        )

        if post_data:
            return clean_posts(
                data=post_data[0]
                .get("data", {})
                .get("children", [])[0]
                .get("data", {}),
                time_format=self._time_format,
            )

    async def comments(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Returns a post's comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param sort: Sort criterion for the comments.
        :return: A list of dictionaries, each containing information about a comment.
        :rtype: list[dict]
        """
        comments_data: list = await api.get_posts(
            posts_type="post_comments",
            post_id=self._post_id,
            post_subreddit=self._post_subreddit,
            limit=limit,
            sort=sort,
            session=session,
        )

        if comments_data:
            return clean_comments(
                comments=comments_data[1].get("data", {}).get("children", []),
                time_format=self._time_format,
            )


class Posts:
    """Represents Reddit posts and provides methods for getting posts from various sources."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        self._time_format = time_format

    async def best(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Returns best posts.

        :param limit: Maximum number of posts to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        best_posts: list = await api.get_posts(
            posts_type="best", limit=limit, session=session
        )

        if best_posts:
            return clean_posts(data=best_posts, time_format=self._time_format)

    async def controversial(
        self, limit: int, session: aiohttp.ClientSession
    ) -> list[dict]:
        """
        Returns controversial posts.

        :param limit: Maximum number of posts to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        controversial_posts: list = await api.get_posts(
            posts_type="controversial",
            limit=limit,
            session=session,
        )

        if controversial_posts:
            return clean_posts(data=controversial_posts, time_format=self._time_format)

    async def front_page(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Returns posts from the Reddit front-page.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        front_page_posts: list = await api.get_posts(
            posts_type="front_page",
            limit=limit,
            sort=sort,
            session=session,
        )

        if front_page_posts:
            return clean_posts(data=front_page_posts, time_format=self._time_format)

    async def new(
        self,
        limit: int,
        session: aiohttp.ClientSession,
    ) -> list[dict]:
        """
        Returns new posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        new_posts: list = await api.get_posts(
            posts_type="new",
            limit=limit,
            session=session,
        )

        if new_posts:
            return clean_posts(data=new_posts, time_format=self._time_format)

    async def popular(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Returns popular posts.

        :param limit: Maximum number of posts to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        popular_posts: list = await api.get_posts(
            posts_type="popular", limit=limit, session=session
        )

        if popular_posts:
            return clean_posts(data=popular_posts, time_format=self._time_format)

    async def rising(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Returns rising posts.

        :param limit: Maximum number of posts to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        rising_posts: list = await api.get_posts(
            posts_type="rising", limit=limit, session=session
        )

        if rising_posts:
            return clean_posts(data=rising_posts, time_format=self._time_format)


class Search:
    """Represents Readit search functionality and provides methods for getting search results from different entities"""

    def __init__(self, query: str, time_format: TIME_FORMAT = "locale"):
        self._query = query
        self._time_format = time_format

    async def posts(
        self,
        timeframe: TIMEFRAME,
        sort: SORT_CRITERION,
        limit: int,
        session: aiohttp.ClientSession,
    ) -> list[dict]:
        """
        Returns posts.

        :param timeframe: Timeframe from which to get results.
        :type timeframe: Literal[str]
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        posts_results: list = await api.get_search_results(
            query=self._query,
            search_type="posts",
            timeframe=timeframe,
            sort=sort,
            limit=limit,
            session=session,
        )
        if posts_results:
            return clean_posts(data=posts_results, time_format=self._time_format)

    async def subreddits(
        self,
        timeframe: TIMEFRAME,
        sort: SORT_CRITERION,
        limit: int,
        session: aiohttp.ClientSession,
    ) -> list[dict]:
        """
        Search subreddits.

        :param timeframe: Timeframe from which to get results.
        :type timeframe: Literal[str]
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        search_subreddits: list = await api.get_search_results(
            query=self._query,
            search_type="subreddits",
            timeframe=timeframe,
            sort=sort,
            limit=limit,
            session=session,
        )
        subreddits_results: list[dict] = clean_subreddits(
            search_subreddits, time_format=self._time_format
        )

        return subreddits_results

    async def users(
        self,
        timeframe: TIMEFRAME,
        sort: SORT_CRITERION,
        limit: int,
        session: aiohttp.ClientSession,
    ) -> list[dict]:
        """
        Search users.

        :param timeframe: Timeframe from which to get results.
        :type timeframe: Literal[str]
        :param sort: Sort criterion for the results.
        :type sort: Literal[str]
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        search_users: list = await api.get_search_results(
            query=self._query,
            search_type="users",
            timeframe=timeframe,
            sort=sort,
            limit=limit,
            session=session,
        )
        users_results: list[dict] = clean_users(
            search_users, time_format=self._time_format
        )

        return users_results


class Subreddit:
    """Represents a Reddit Community (Subreddit) and provides methods for getting data from the specified subreddit."""

    def __init__(self, subreddit: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a RedditCommunity instance for getting profile and posts from the specified subreddit.

        :param subreddit: Name of the subreddit to get data from.
        :type subreddit: str
        :param time_format: Determines the format of the output. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._subreddit = subreddit
        self._time_format = time_format

    async def profile(self, session: aiohttp.ClientSession) -> dict:
        """
        Returns a subreddit's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A dictionary containing subreddit profile data.
        :rtype: Community
        """
        subreddit_profile: dict = await api.get_profile(
            profile_type="subreddit",
            subreddit=self._subreddit,
            session=session,
        )
        if subreddit_profile:
            return clean_subreddits(
                data=subreddit_profile, time_format=self._time_format
            )

    async def wiki_pages(self, session: aiohttp.ClientSession) -> list[str]:
        """
        Return a subreddit's wiki pages.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        with get_status(
            status_message=f"Initialising [underline]single data[/] retrieval job..."
        ):
            pages: dict = await api.get_data(
                endpoint=f"{api.subreddit_data_endpoint}/{self._subreddit}/wiki/pages.json",
                session=session,
            )

            return pages.get("data")

    async def wiki_page(self, page: str, session: aiohttp.ClientSession) -> dict:
        """
        Return a subreddit's specified wiki page data.

        :param page: Wiki page to get data from.
        :type page: str
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        with get_status(
            status_message=f"Initialising [underline]single data[/] retrieval job..."
        ):
            wiki_page: dict = await api.get_data(
                endpoint=f"{api.subreddit_data_endpoint}/{self._subreddit}/wiki/{page}.json",
                session=session,
            )

            if wiki_page:
                return clean_subreddit_wiki_page(
                    wiki_page=wiki_page.get("data"), time_format=self._time_format
                )

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns a subreddit's posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        subreddit_posts: list = await api.get_posts(
            posts_type="subreddit_posts",
            subreddit=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if subreddit_posts:
            return clean_posts(data=subreddit_posts, time_format=self._time_format)

    async def search(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns posts that contain a specified keyword from a subreddit.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        found_posts: list = await api.get_posts(
            posts_type="search_subreddit_posts",
            subreddit=self._subreddit,
            query=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if found_posts:
            return clean_posts(data=found_posts, time_format=self._time_format)


class Subreddits:
    """Represents Reddit subreddits and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        self._time_format = time_format

    async def all(
        self, limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Return all subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get all subreddits.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a subreddit.
        :rtype: list[dict]

        Note
        ----
            *in Morphius' voice* "the only limitation you have at this point is the matrix's rate-limit."
        """
        all_subreddits: list = await api.get_subreddits(
            subreddits_type="all", limit=limit, timeframe=timeframe, session=session
        )
        if all_subreddits:
            return clean_subreddits(data=all_subreddits, time_format=self._time_format)

        return all_subreddits

    async def default(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Return default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a subreddit.
        :rtype: list[dict]
        """
        default_subreddits: list = await api.get_subreddits(
            subreddits_type="default", limit=limit, session=session
        )
        if default_subreddits:
            return clean_subreddits(default_subreddits, time_format=self._time_format)

    async def new(
        self, limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Return new subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a subreddit.
        :rtype: list[dict]
        """
        new_subreddits: list = await api.get_subreddits(
            subreddits_type="new", limit=limit, timeframe=timeframe, session=session
        )
        if new_subreddits:
            return clean_subreddits(new_subreddits, time_format=self._time_format)

    async def popular(
        self, limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Return popular subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a subreddit.
        :rtype: list[dict]
        """
        popular_subreddits: list = await api.get_subreddits(
            subreddits_type="popular", limit=limit, timeframe=timeframe, session=session
        )
        if popular_subreddits:
            return clean_subreddits(popular_subreddits, time_format=self._time_format)


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, username: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a User instance for getting profile, posts and comments data from the specified user.

        :param username: Username of the user to get data from.
        :type username: str
        :param time_format: Determines the format of the output. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """
        self._username = username
        self._time_format = time_format

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns a user's comments.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which tyo get comments.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a comment.
        :rtype: list[dict]
        """
        user_comments: list = await api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if user_comments:
            return clean_comments(comments=user_comments, time_format=self._time_format)

    async def moderated_subreddits(self, session: aiohttp.ClientSession) -> list[dict]:
        """
        Returns subreddits moderated by the user.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing preview data of a Community.
        :rtype: list[dict]
        """
        subreddits: dict = await api.get_data(
            endpoint=f"{api.base_reddit_endpoint}/user/{self._username}/moderated_subreddits.json",
            session=session,
        )
        if subreddits:
            return clean_subreddits(
                subreddits.get("data"),
                time_format=self._time_format,
            )

    async def overview(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Returns a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a recent comment.
        :rtype: list[dict]
        """
        user_overview: list = await api.get_posts(
            username=self._username,
            posts_type="user_overview",
            limit=limit,
            session=session,
        )
        if user_overview:
            return clean_comments(user_overview, time_format=self._time_format)

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns a user's posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        user_posts: list = await api.get_posts(
            username=self._username,
            posts_type="user_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        if user_posts:
            return clean_posts(user_posts, time_format=self._time_format)

    async def profile(self, session: aiohttp.ClientSession) -> dict:
        """
        Returns a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A dictionary containing user profile data.
        :rtype: dict
        """
        user_profile: dict = await api.get_profile(
            username=self._username, profile_type="user", session=session
        )
        if user_profile:
            return clean_users(data=user_profile, time_format=self._time_format)

    async def search_posts(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns a user's posts that contain the specified keywords.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param keyword: Keyword to search for in posts.
        :type keyword: str
        :param limit: Maximum number of posts to search from.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        user_posts: list = await api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        found_posts: list = []
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for post in user_posts:
            post_data: dict = post.get("data")
            if pattern.search(post_data.get("title")) or pattern.search(
                post_data.get("selftext")
            ):
                found_posts.append(post)
        if found_posts:
            return clean_posts(found_posts, time_format=self._time_format)

    async def search_comments(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns a user's comments that contain the specified keyword.

        :param session: Aiohttp session to use for the request.
        :param keyword: Keyword to search for in comments.
        :type keyword: str
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to search from.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which to get comments.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing data about a comment.
        :rtype: list[dict]
        """
        user_comments: list = await api.get_posts(
            username=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        found_comments: list = []
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for comment in user_comments:
            if pattern.search(comment.get("data").get("body")):
                found_comments.append(comment)

        if found_comments:
            return clean_comments(found_comments, time_format=self._time_format)

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
    ) -> list[tuple]:
        """
        Returns a user's top n subreddits based on subreddit frequency in n posts.

        :param top_n: Communities arranging number.
        :type top_n: int
        :param limit: Maximum number of posts to scrape.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: Dictionary of top n subreddits and their counts.
        :rtype: dict
        """
        posts = await api.get_posts(
            posts_type="user_posts",
            username=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if posts:
            # Extract subreddit names
            subreddits = [post.get("data", {}).get("subreddit") for post in posts]

            # Count the occurrences of each subreddit
            subreddit_counts = Counter(subreddits)

            return subreddit_counts.most_common(top_n)

        return []


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        self._time_format = time_format

    async def new(
        self, limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get new users.

        :param limit: Maximum number of new users to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get new posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        new_users: list = await api.get_users(
            users_type="new", limit=limit, timeframe=timeframe, session=session
        )
        if new_users:
            return clean_users(new_users, time_format=self._time_format)

    async def popular(
        self, limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get popular users.

        :param limit: Maximum number of popular users to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        popular_users: list = await api.get_users(
            users_type="popular",
            limit=limit,
            timeframe=timeframe,
            session=session,
        )
        if popular_users:
            return clean_users(popular_users, time_format=self._time_format)

    async def all(
        self, limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all"
    ) -> list[dict]:
        """
        Get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing a user's data.
        :rtype: list[dict]
        """
        all_users: list = await api.get_users(
            users_type="all", limit=limit, timeframe=timeframe, session=session
        )
        if all_users:
            return clean_users(all_users, time_format=self._time_format)
