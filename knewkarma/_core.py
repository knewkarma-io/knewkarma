import re
from collections import Counter

import aiohttp

from ._api import Api, DATA_TIMEFRAME, SORT_CRITERION, DATA_LISTING, TIME_FORMAT
from ._parsers import (
    parse_comments,
    parse_subreddits,
    parse_subreddit_wiki_page,
    parse_posts,
    parse_users,
)

api = Api()


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, username: str, time_format: TIME_FORMAT = "datetime"):
        """
        Initialises a User instance for getting profile, posts and comments data from the specified user.

        :param username: Username of the user to get data from.
        :type username: str
        :param time_format: Determines the format of the output. Use "concise" for a human-readable
                        time difference, or "datetime" for a localized datetime string. Defaults to "datetime".
        :type time_format: Literal["concise", "datetime"]
        """
        self._username = username
        self._time_format = time_format

    async def profile(self, session: aiohttp.ClientSession) -> dict:
        """
        Returns a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A dictionary containing user profile data.
        :rtype: dict
        """
        raw_user: dict = await api.get_profile(
            profile_source=self._username, profile_type="user", session=session
        )
        user_profile: dict = parse_users(raw_user, time_format=self._time_format)

        return user_profile

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
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
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        raw_posts: list = await api.get_posts(
            posts_source=self._username,
            posts_type="user_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        user_posts: list[dict] = parse_posts(raw_posts, time_format=self._time_format)

        return user_posts

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
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
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a comment.
        :rtype: list[dict]
        """
        raw_comments: list = await api.get_posts(
            posts_source=self._username,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        user_comments: list[dict] = parse_comments(
            raw_comments, time_format=self._time_format
        )

        return user_comments

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
        raw_comments: list = await api.get_posts(
            posts_source=self._username,
            posts_type="user_overview",
            limit=limit,
            session=session,
        )
        user_overview: list[dict] = parse_comments(
            raw_comments, time_format=self._time_format
        )

        return user_overview

    async def search_posts(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
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
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        user_posts: list = await api.get_posts(
            posts_type="user_posts",
            posts_source=self._username,
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

        return parse_posts(found_posts, time_format=self._time_format)

    async def search_comments(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
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
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a comment.
        :rtype: list[dict]
        """
        user_comments: list = await api.get_posts(
            posts_source=self._username,
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

        return parse_comments(found_comments, time_format=self._time_format)

    async def moderated_subreddits(self, session: aiohttp.ClientSession) -> list[dict]:
        """
        Returns subreddits moderated by the user.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing preview data of a Community.
        :rtype: list[dict]
        """
        raw_preview_subreddits: dict = await api.get_data(
            endpoint=f"{api.base_reddit_endpoint}/user/{self._username}/moderated_subreddits.json",
            session=session,
        )
        preview_subreddits: list[dict] = parse_subreddits(
            raw_preview_subreddits.get("data"),
            is_preview=True,
            time_format=self._time_format,
        )

        return preview_subreddits

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
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
        :type timeframe: str
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: Dictionary of top n subreddits and their counts.
        :rtype: dict
        """
        posts = await api.get_posts(
            posts_type="user_posts",
            posts_source=self._username,
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


class Search:
    """Represents Readit search functionality and provides methods for getting search results from different entities"""

    def __init__(self, time_format: TIME_FORMAT = "datetime"):
        self._time_format = time_format

    async def users(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
    ) -> list[dict]:
        """
        Search users.

        :param query: Search query.
        :type query: str
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        search_users: list = await api.get_search_results(
            query=query, search_type="users", limit=limit, session=session
        )
        users_results: list[dict] = parse_users(
            search_users, time_format=self._time_format
        )

        return users_results

    async def subreddits(
        self, query: str, limit: int, session: aiohttp.ClientSession
    ) -> list[dict]:
        """
        Search subreddits.

        :param query: Search query.
        :type query: str
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        search_subreddits: list = await api.get_search_results(
            query=query, search_type="subreddits", limit=limit, session=session
        )
        subreddits_results: list[dict] = parse_subreddits(
            search_subreddits, time_format=self._time_format
        )

        return subreddits_results

    async def posts(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns posts.

        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        search_posts: list = await api.get_search_results(
            query=query,
            search_type="posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        posts_results: list[dict] = parse_posts(
            search_posts, time_format=self._time_format
        )

        return posts_results


class Subreddit:
    """Represents a Reddit Community (Subreddit) and provides methods for getting data from the specified subreddit."""

    def __init__(self, subreddit: str, time_format: TIME_FORMAT = "datetime"):
        """
        Initialises a RedditCommunity instance for getting profile and posts from the specified subreddit.

        :param subreddit: Name of the subreddit to get data from.
        :type subreddit: str
        :param time_format: Determines the format of the output. Use "concise" for a human-readable
                        time difference, or "datetime" for a localized datetime string. Defaults to "datetime".
        :type time_format: Literal["concise", "datetime"]
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
        raw_subreddit: dict = await api.get_profile(
            profile_type="subreddit",
            profile_source=self._subreddit,
            session=session,
        )
        subreddit_profile: dict = parse_subreddits(
            raw_subreddit, time_format=self._time_format
        )

        return subreddit_profile

    async def wiki_pages(self, session: aiohttp.ClientSession) -> list[str]:
        """
        Return a subreddit's wiki pages.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
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
        raw_page: dict = await api.get_data(
            endpoint=f"{api.subreddit_data_endpoint}/{self._subreddit}/wiki/{page}.json",
            session=session,
        )
        wiki_page: dict = parse_subreddit_wiki_page(
            wiki_page=raw_page, time_format=self._time_format
        )

        return wiki_page

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
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
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        raw_posts: list = await api.get_posts(
            posts_type="subreddit_posts",
            posts_source=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        subreddit_posts: list[dict] = parse_posts(
            raw_posts, time_format=self._time_format
        )

        return subreddit_posts

    async def search(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns posts that contain a specified keyword from a subreddit.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param keyword: Keyword to search for in posts.
        :type keyword: str
        :param limit: Maximum number of posts to search from.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        all_posts: list = await api.get_posts(
            posts_type="subreddit_posts",
            posts_source=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        found_posts: list = []
        pattern = re.compile(re.escape(keyword), re.IGNORECASE)
        for post in all_posts:
            post_data: dict = post.get("data")
            if pattern.search(post_data.get("title")) or pattern.search(
                post_data.get("selftext")
            ):
                found_posts.append(post)

        return parse_posts(found_posts, time_format=self._time_format)


class Subreddits:
    """Represents Reddit subreddits and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "datetime"):
        self._time_format = time_format

    async def all(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Return all subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a subreddit.
        :rtype: list[dict]

        Note
        ----
            *in Morphius' voice* "the only limitation you have at this point is the matrix's rate limit."
        """
        raw_subreddits: list = await api.get_subreddits(
            subreddits_type="all", limit=limit, session=session
        )
        all_subreddits: list[dict] = parse_subreddits(
            raw_subreddits, is_preview=True, time_format=self._time_format
        )

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
        raw_subreddits: list = await api.get_subreddits(
            subreddits_type="default", limit=limit, session=session
        )
        default_subreddits: list[dict] = parse_subreddits(
            raw_subreddits, is_preview=True, time_format=self._time_format
        )

        return default_subreddits

    async def new(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Return new subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a subreddit.
        :rtype: list[dict]
        """
        raw_subreddits: list = await api.get_subreddits(
            subreddits_type="new", limit=limit, session=session
        )
        new_subreddits: list[dict] = parse_subreddits(
            raw_subreddits, is_preview=True, time_format=self._time_format
        )

        return new_subreddits

    async def popular(self, limit: int, session: aiohttp.ClientSession) -> list[dict]:
        """
        Return popular subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing data about a subreddit.
        :rtype: list[dict]
        """
        raw_subreddits: list = await api.get_subreddits(
            subreddits_type="popular", limit=limit, session=session
        )
        popular_subreddits: list[dict] = parse_subreddits(
            raw_subreddits, is_preview=True, time_format=self._time_format
        )

        return popular_subreddits


class Post:
    """Represents a Reddit post and provides method(s) for getting data from the specified post."""

    def __init__(
        self, post_id: str, subreddit: str, time_format: TIME_FORMAT = "datetime"
    ):
        self._post_id = post_id
        self._subreddit = subreddit
        self._time_format = time_format

    async def profile(self, session: aiohttp.ClientSession) -> dict:
        post_data: dict = await api.get_data(
            endpoint=f"{api.base_reddit_endpoint}/r/{self._subreddit}/comments/{self._post_id}.json",
            session=session,
        )

        raw_post: dict = (
            post_data[0].get("data", {}).get("children", [])[0].get("data", {})
        )
        if raw_post:
            return parse_posts(data=raw_post, time_format=self._time_format)

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        post_data: dict = await api.get_data(
            endpoint=f"{api.base_reddit_endpoint}/r/{self._subreddit}/comments/"
            f"{self._post_id}.json?sort={sort}&limit={limit}",
            session=session,
        )

        raw_comments: list = post_data[1].get("data", {}).get("children", [])

        if raw_comments:
            return parse_comments(comments=raw_comments, time_format=self._time_format)


class Posts:
    """Represents Reddit posts and provides methods for getting posts from various sources."""

    def __init__(self, time_format: TIME_FORMAT = "datetime"):
        self._time_format = time_format

    async def listing(
        self,
        session: aiohttp.ClientSession,
        listings_name: DATA_LISTING,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns posts from a specified listing.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param listings_name: Listing to get posts from.
        :type listings_name: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        listing_posts: list = await api.get_posts(
            posts_type="listing_posts",
            posts_source=listings_name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        if listing_posts:
            return parse_posts(listing_posts, time_format=self._time_format)

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Returns new posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        raw_posts: list = await api.get_posts(
            posts_type="new_posts",
            limit=limit,
            sort=sort,
            session=session,
        )
        new_posts: list[dict] = parse_posts(raw_posts, time_format=self._time_format)

        return new_posts

    async def front_page(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Returns posts from the Reddit front-page.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        :return: A list of dictionaries, each containing data about a post.
        :rtype: list[dict]
        """
        raw_posts: list = await api.get_posts(
            posts_type="front_page_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        front_page_posts: list = parse_posts(raw_posts, time_format=self._time_format)

        return front_page_posts
