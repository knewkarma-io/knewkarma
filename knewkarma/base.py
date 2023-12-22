# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from typing import List

import aiohttp

from ._meta import DATA_TIMEFRAME, DATA_SORT_CRITERION, POSTS_LISTINGS
from ._utils import unix_timestamp_to_utc
from .api import get_profile, get_posts
from .data import User, Subreddit, Comment, Post


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditUser:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    # -------------------------------------------------------------- #

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

    # -------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> User:
        """
        Returns a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A User object containing user profile data.
        :rtype: User
        """
        user_profile: dict = await get_profile(
            profile_type="user_profile", profile_source=self._username, session=session
        )
        return User(
            name=user_profile.get("name"),
            id=user_profile.get("id"),
            is_verified=user_profile.get("verified"),
            has_verified_email=user_profile.get("has_verified_email"),
            is_gold=user_profile.get("is_gold"),
            is_mod=user_profile.get("is_mod"),
            is_employee=user_profile.get("is_employee"),
            is_blocked=user_profile.get("is_blocked"),
            hidden_from_bots=user_profile.get("hide_from_robots"),
            accepts_followers=user_profile.get("accept_followers"),
            comment_karma=user_profile.get("comment_karma"),
            link_karma=user_profile.get("link_karma"),
            awardee_karma=user_profile.get("awardee_karma"),
            total_karma=user_profile.get("total_karma"),
            subreddit=user_profile.get("subreddit"),
            created_at=unix_timestamp_to_utc(timestamp=user_profile.get("created")),
            raw_data=user_profile,
        )

    # -------------------------------------------------------------- #

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
        user_posts: list = await get_posts(
            posts_type="user_posts",
            posts_source=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=user_posts)

    # -------------------------------------------------------------- #

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
        comments_list: list = []
        raw_comments: list = await get_posts(
            posts_type="user_comments",
            posts_source=self._username,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        for comment_index, raw_comment in enumerate(raw_comments, start=1):
            comment_data: dict = raw_comment.get("data")
            comments_list.append(
                Comment(
                    index=comment_index,
                    body=comment_data.get("body"),
                    id=comment_data.get("id"),
                    author=comment_data.get("author"),
                    author_is_premium=comment_data.get("author_premium"),
                    upvotes=comment_data.get("ups"),
                    downvotes=comment_data.get("downs"),
                    is_nsfw=comment_data.get("over_18"),
                    is_edited=comment_data.get("edited"),
                    score=comment_data.get("score"),
                    hidden_score=comment_data.get("score_hidden"),
                    gilded=comment_data.get("gilded"),
                    is_stickied=comment_data.get("stickied"),
                    is_locked=comment_data.get("locked"),
                    is_archived=comment_data.get("archived"),
                    created_at=unix_timestamp_to_utc(
                        timestamp=comment_data.get("created")
                    ),
                    subreddit=comment_data.get("subreddit_name_prefixed"),
                    subreddit_type=comment_data.get("subreddit_type"),
                    post_id=comment_data.get("link_id"),
                    post_title=comment_data.get("link_title"),
                    raw_data=comment_data,
                )
            )

        return comments_list


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditSub:
    """Represents a Subreddit and provides methods for getting data from the specified subreddit."""

    # -------------------------------------------------------------- #

    def __init__(
        self,
        subreddit: str,
    ):
        """
        Initialises a RedditSub instance for getting profile and posts from the specified subreddit.

        :param subreddit: Name of the subreddit to get data from.
        :type subreddit: str
        """
        self._subreddit = subreddit

    # -------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> Subreddit:
        """
        Returns a subreddit's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A Subreddit object containing subreddit profile data.
        :rtype: Subreddit
        """
        subreddit_profile: dict = await get_profile(
            profile_type="subreddit_profile",
            profile_source=self._subreddit,
            session=session,
        )

        return Subreddit(
            name=subreddit_profile.get("display_name"),
            id=subreddit_profile.get("id"),
            description=subreddit_profile.get("public_description"),
            submit_text=subreddit_profile.get("submit_text"),
            icon_img=subreddit_profile.get("icon_img"),
            subreddit_type=subreddit_profile.get("subreddit_type"),
            subscribers=subreddit_profile.get("subscribers"),
            current_active_users=subreddit_profile.get("accounts_active"),
            is_nsfw=subreddit_profile.get("over18"),
            language=subreddit_profile.get("lang"),
            created_at=unix_timestamp_to_utc(
                timestamp=subreddit_profile.get("created")
            ),
            raw_data=subreddit_profile,
        )

    # -------------------------------------------------------------- #

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> List[Post]:
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
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        subreddit_posts: list = await get_posts(
            posts_type="subreddit_posts",
            posts_source=self._subreddit,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=subreddit_posts)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditPosts:
    """Represents Reddit posts and provides method for getting posts from various sources."""

    @staticmethod
    def process_posts(raw_posts: list) -> List[Post]:
        posts_list: list = []
        for post_index, raw_post in enumerate(raw_posts, start=1):
            post_data = raw_post.get("data")
            posts_list.append(
                Post(
                    index=post_index,
                    title=post_data.get("title"),
                    thumbnail=post_data.get("thumbnail"),
                    id=post_data.get("id"),
                    body=post_data.get("selftext"),
                    author=post_data.get("author"),
                    subreddit=post_data.get("subreddit"),
                    subreddit_id=post_data.get("subreddit_id"),
                    subreddit_type=post_data.get("subreddit_type"),
                    upvotes=post_data.get("ups"),
                    upvote_ratio=post_data.get("upvote_ratio"),
                    downvotes=post_data.get("downs"),
                    gilded=post_data.get("gilded"),
                    is_nsfw=post_data.get("over_18"),
                    is_shareable=post_data.get("is_reddit_media_domain"),
                    is_edited=post_data.get("edited"),
                    comments=post_data.get("num_comments"),
                    hide_from_bots=post_data.get("is_robot_indexable"),
                    score=post_data.get("score"),
                    domain=post_data.get("domain"),
                    permalink=post_data.get("permalink"),
                    is_locked=post_data.get("locked"),
                    is_archived=post_data.get("archived"),
                    created_at=unix_timestamp_to_utc(
                        timestamp=post_data.get("created")
                    ),
                    raw_post=post_data,
                )
            )

        return posts_list

    # -------------------------------------------------------------- #

    @staticmethod
    async def search(
        session: aiohttp.ClientSession,
        query: str,
        limit: int,
        sort: DATA_SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> List[Post]:
        """
        Returns posts that match a specified query..

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession.
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        :return: A list of Post objects, each containing data about a post.
        :rtype: list[Post]
        """
        search_posts: list = await get_posts(
            posts_type="search_posts",
            posts_source=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=search_posts)

    # -------------------------------------------------------------- #

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
            posts_type="listing_posts",
            posts_source=listings_name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=listing_posts)

    # -------------------------------------------------------------- #

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
        front_page_posts: list = await get_posts(
            posts_type="front_page_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=front_page_posts)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
