# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
import re
from collections import Counter
from typing import List

import aiohttp

from ._api import (
    get_communities,
    get_data,
    get_posts,
    get_profile,
    search,
    BASE_REDDIT_ENDPOINT,
    COMMUNITY_DATA_ENDPOINT,
)
from ._converters import (
    convert_comments,
    convert_communities,
    convert_community_wiki_page,
    convert_posts,
    convert_users,
)
from .data import Comment, Community, PreviewCommunity, User, Post, WikiPage
from .docs import DATA_TIMEFRAME, DATA_SORT_CRITERION, POSTS_LISTINGS


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditUser:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    # ------------------------------------------------------------------------------- #

    def __init__(
        self,
        username: str,
    ):
        """
        Initialises a RedditUser instance for getting profile, posts and comments data from the specified user.

        :param username: Username of the user to get data from.
        :type username: str
        """
        self._username = username

    # ------------------------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> User:
        """
        Returns a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A User object containing user profile data.
        :rtype: User
        """
        raw_user: dict = await get_profile(
            _from=self._username, _type="user", session=session
        )
        user_profile: User = convert_users(raw_user)

        return user_profile

    # ------------------------------------------------------------------------------- #

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[Post]:
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
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        raw_posts: list = await get_posts(
            _from=self._username,
            _type="user_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        user_posts: list[Post] = convert_posts(raw_posts)

        return user_posts

    # ------------------------------------------------------------------------------- #

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[Comment]:
        """
        Returns a user's comments.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which to get comments.
        :type timeframe: str
        :return: A list of Comment objects, each containing data about a comment.
        :rtype: list[Comment]
        """
        raw_comments: list = await get_posts(
            _from=self._username,
            _type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        user_comments: list[Comment] = convert_comments(raw_comments)

        return user_comments

    # ------------------------------------------------------------------------------- #

    async def overview(
        self, limit: int, session: aiohttp.ClientSession
    ) -> list[Comment]:
        """
        Returns a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of Comment objects, each containing data about a recent comment.
        :rtype: list[Comment]
        """
        raw_comments: list = await get_posts(
            _from=self._username,
            _type="user_overview",
            limit=limit,
            session=session,
        )
        user_overview: list[Comment] = convert_comments(raw_comments)

        return user_overview

    # ------------------------------------------------------------------------------- #

    async def search_posts(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[Post]:
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
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        user_posts: list = await get_posts(
            _type="user_posts",
            _from=self._username,
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

        return convert_posts(found_posts)

    # ------------------------------------------------------------------------------- #

    async def search_comments(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[Comment]:
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
        :return: A list of Comment objects, each containing data about a comment.
        :rtype: list[Comment]
        """
        user_comments: list = await get_posts(
            _from=self._username,
            _type="user_comments",
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

        return convert_comments(found_comments)

    # ------------------------------------------------------------------------------- #

    async def moderated_communities(
        self, session: aiohttp.ClientSession
    ) -> list[PreviewCommunity]:
        """
        Returns communities moderated by the user.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of PreviewCommunity objects, each containing preview data of a Community.
        :rtype: list[PreviewCommunity]
        """
        raw_preview_communities: dict = await get_data(
            endpoint=f"{BASE_REDDIT_ENDPOINT}/user/{self._username}/moderated_subreddits.json",
            session=session,
        )
        preview_communities: list[PreviewCommunity] = convert_communities(
            raw_preview_communities.get("data"), is_preview=True
        )

        return preview_communities

    # ------------------------------------------------------------------------------- #

    async def top_communities(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> dict:
        """
        Returns a user's top n communities based on community frequency in n posts.

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
        :return: Dictionary of top n communities and their counts.
        :rtype: dict
        """
        posts = await get_posts(
            _type="user_posts",
            _from=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        if posts:
            # Extract community names
            communities = [post.get("data", {}).get("subreddit") for post in posts]

            # Count the occurrences of each community
            community_counts = Counter(communities)

            # Get the top N communities
            most_active_communities = {
                f"top {top_n}": community_counts.most_common(top_n)
            }

            return most_active_communities

        return {}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditSearch:
    """Represents Readit search functionality and provides methods for getting search results from different entities"""

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def users(
        query: str, limit: int, session: aiohttp.ClientSession
    ) -> list[User]:
        """
        Search users.

        :param query: Search query.
        :type query: str
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        search_users: list = await search(
            query=query, _type="users", limit=limit, session=session
        )
        users_results: list[User] = convert_users(search_users)

        return users_results

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def communities(
        query: str, limit: int, session: aiohttp.ClientSession
    ) -> list[Community]:
        """
        Search communities.

        :param query: Search query.
        :type query: str
        :param limit: Maximum number of search results to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        search_communities: list = await search(
            query=query, _type="communities", limit=limit, session=session
        )
        communities_results: list[Community] = convert_communities(search_communities)

        return communities_results

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def posts(
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> List[Post]:
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
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        search_posts: list = await search(
            query=query,
            _type="posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        posts_results: list[Post] = convert_posts(search_posts)

        return posts_results


class RedditCommunity:
    """Represents a Reddit Community (Subreddit) and provides methods for getting data from the specified community."""

    # ------------------------------------------------------------------------------- #

    def __init__(
        self,
        community: str,
    ):
        """
        Initialises a RedditCommunity instance for getting profile and posts from the specified community.

        :param community: Name of the community to get data from.
        :type community: str
        """
        self._community = community

    # ------------------------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> Community:
        """
        Returns a community's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A community object containing community profile data.
        :rtype: Community
        """
        raw_community: dict = await get_profile(
            _type="community",
            _from=self._community,
            session=session,
        )
        community_profile: Community = convert_communities(raw_community)

        return community_profile

    async def wiki_pages(self, session: aiohttp.ClientSession) -> list[str]:
        """
        Return a community's wiki pages.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        pages: dict = await get_data(
            endpoint=f"{COMMUNITY_DATA_ENDPOINT}/{self._community}/wiki/pages.json",
            session=session,
        )

        return pages.get("data")

    # ------------------------------------------------------------------------------- #

    async def wiki_page(self, page: str, session: aiohttp.ClientSession) -> WikiPage:
        """
        Return a community's specified wiki page data.

        :param page: Wiki page to get data from.
        :type page: str
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of strings, each representing a wiki page.
        :rtype: list[str]
        """
        raw_page: dict = await get_data(
            endpoint=f"{COMMUNITY_DATA_ENDPOINT}/{self._community}/wiki/{page}.json",
            session=session,
        )
        wiki_page: WikiPage = convert_community_wiki_page(wiki_page=raw_page)

        return wiki_page

    # ------------------------------------------------------------------------------- #

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> List[Post]:
        """
        Returns a community's posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        raw_posts: list = await get_posts(
            _type="community",
            _from=self._community,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        community_posts: list[Post] = convert_posts(raw_posts)

        return community_posts

    # ------------------------------------------------------------------------------- #

    async def search(
        self,
        session: aiohttp.ClientSession,
        keyword: str,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[Post]:
        """
        Returns posts that contain a specified keyword from a community.

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
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        all_posts: list = await get_posts(
            _type="community",
            _from=self._community,
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

        return convert_posts(found_posts)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditCommunities:
    """Represents Reddit communities and provides methods for getting related data."""

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def all(limit: int, session: aiohttp.ClientSession) -> list[Community]:
        """
        Return all communities.

        :param limit: Maximum number of communities to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of community objects, each containing data about a community.
        :rtype: list[Community]

        Note
        ----
            *in morphius' voice* "the only limitation you have at this point is the matrix's rate limit."
        """
        raw_communities: list = await get_communities(
            _type="all", limit=limit, session=session
        )
        all_communities: list[Community] = convert_communities(raw_communities)

        return all_communities

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def default(limit: int, session: aiohttp.ClientSession) -> list[Community]:
        """
        Return default communities.

        :param limit: Maximum number of communities to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of community objects, each containing data about a community.
        :rtype: list[Community]
        """
        raw_communities: list = await get_communities(
            _type="default", limit=limit, session=session
        )
        default_communities: list[Community] = convert_communities(raw_communities)

        return default_communities

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def new(limit: int, session: aiohttp.ClientSession) -> list[Community]:
        """
        Return new communities.

        :param limit: Maximum number of communities to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of community objects, each containing data about a community.
        :rtype: list[Community]
        """
        raw_communities: list = await get_communities(
            _type="new", limit=limit, session=session
        )
        new_communities: list[Community] = convert_communities(raw_communities)

        return new_communities

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def popular(limit: int, session: aiohttp.ClientSession) -> list[Community]:
        """
        Return popular communities.

        :param limit: Maximum number of communities to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of community objects, each containing data about a community.
        :rtype: list[Community]
        """
        raw_communities: list = await get_communities(
            _type="popular", limit=limit, session=session
        )
        popular_communities: list[Community] = convert_communities(raw_communities)

        return popular_communities


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditPosts:
    """Represents Reddit posts and provides methods for getting posts from various sources."""

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def listing(
        session: aiohttp.ClientSession,
        listings_name: POSTS_LISTINGS,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> List[Post]:
        """
        Returns posts from a specified listing.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param listings_name: Listing to get posts from..
        :type listings_name: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        listing_posts: list = await get_posts(
            _type="listing",
            _from=listings_name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        if listing_posts:
            return convert_posts(listing_posts)

    # ------------------------------------------------------------------------------- #

    @staticmethod
    async def new(
        session: aiohttp.ClientSession,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
    ) -> List[Post]:
        """
        Returns new posts.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        raw_posts: list = await get_posts(
            _type="new",
            limit=limit,
            sort=sort,
            session=session,
        )
        new_posts: list[Post] = convert_posts(raw_posts)

        return new_posts

    @staticmethod
    async def front_page(
        session: aiohttp.ClientSession,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> List[Post]:
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
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        raw_posts: list = await get_posts(
            _type="front_page",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )
        front_page_posts: list[Post] = convert_posts(raw_posts)

        return front_page_posts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
