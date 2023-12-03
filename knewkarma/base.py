# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from typing import List

import aiohttp

from ._coreutils import timestamp_to_utc
from .api import get_profile, get_posts
from .data import User, Subreddit, Comment, Post


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditUser:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    # -------------------------------------------------------------- #

    def __init__(
        self,
        username: str,
        data_timeframe: str,
        data_sort: str,
        data_limit: int,
    ):
        """
        Initialises a RedditUser instance for getting profile, posts and comments data from the specified user.

        :param username: Username of the user to get data from.
        :param data_timeframe: The timeframe from which to get posts/comments
            (choices: 'all', 'hour', 'day', 'week', 'month', 'year').
        :param data_sort: Sort criterion for the retrieved posts/comments
            (choices: 'all', 'best', 'controversial', 'hot', 'new', 'rising', 'top').
        :param data_limit: The maximum number of user posts/comments to retrieve.
        """
        self._username = username
        self._data_timeframe = data_timeframe
        self._data_sort = data_sort
        self._data_limit = data_limit

    # -------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> User:
        """
        Gets a user's profile data.

        :param session: aiohttp session to use for the request.
        :return: A User object containing user profile data.
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
            created_at=timestamp_to_utc(timestamp=user_profile.get("created")),
            raw_data=user_profile,
        )

    # -------------------------------------------------------------- #

    async def posts(self, session: aiohttp.ClientSession) -> List[Post]:
        """
        Gets a user's posts.

        :param session: aiohttp session to use for the request.
        :return: A list of Post objects, each containing a post's data.
        """
        user_posts: list = await get_posts(
            posts_type="user_posts",
            posts_source=self._username,
            timeframe=self._data_timeframe,
            sort=self._data_sort,
            limit=self._data_limit,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=user_posts)

    # -------------------------------------------------------------- #

    async def comments(self, session: aiohttp.ClientSession) -> List[Comment]:
        """
        Gets a user's comments.

        :param session: aiohttp session to use for the request.
        :return:A list of Comment objects, each containing a comment's data.
        """
        comments_list: list = []
        raw_comments: list = await get_posts(
            posts_type="user_comments",
            posts_source=self._username,
            timeframe=self._data_timeframe,
            sort=self._data_sort,
            limit=self._data_limit,
            session=session,
        )

        for raw_comment in raw_comments:
            comment_data: dict = raw_comment.get("data")
            comment = Comment(
                id=comment_data.get("id"),
                text=comment_data.get("body"),
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
                created_at=timestamp_to_utc(timestamp=comment_data.get("created")),
                subreddit=comment_data.get("subreddit_name_prefixed"),
                subreddit_type=comment_data.get("subreddit_type"),
                post_id=comment_data.get("link_id"),
                post_title=comment_data.get("link_title"),
                raw_data=comment_data,
            )
            comments_list.append(comment)

        return comments_list


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditSub:
    """Represents a Subreddit and provides methods for getting data from the specified subreddit."""

    # -------------------------------------------------------------- #

    def __init__(
        self, subreddit: str, data_timeframe: str, data_sort: str, data_limit: int
    ):
        """
        Initialises a RedditSub instance for getting profile and posts from the specified subreddit.

        :param subreddit: Name of the subreddit to get data from.
        :param data_timeframe: The timeframe from which to get posts
            (choices: 'all', 'hour', 'day', 'week', 'month', 'year').
        :param data_sort: Sort criterion for the retrieved posts
            (choices: 'all', 'best', 'controversial', 'hot', 'new', 'rising', 'top').
        :param data_limit: The maximum number of subreddit posts to retrieve.
        """
        self._subreddit = subreddit
        self._data_timeframe = data_timeframe
        self._data_sort = data_sort
        self._data_limit = data_limit

    # -------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> Subreddit:
        """
        Gets a subreddit's profile data.

        :param session: aiohttp session to use for the request.
        :return: A Subreddit object containing subreddit profile data.
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
            created_at=timestamp_to_utc(timestamp=subreddit_profile.get("created")),
            raw_data=subreddit_profile,
        )

    # -------------------------------------------------------------- #

    async def posts(self, session: aiohttp.ClientSession) -> List[Post]:
        """
        Gets a subreddit's posts.

        :param session: aiohttp session to use for the request.
        :return: A list of Post objects, each containing a post's data.
        """
        subreddit_posts: list = await get_posts(
            posts_type="subreddit_posts",
            posts_source=self._subreddit,
            timeframe=self._data_timeframe,
            sort=self._data_sort,
            limit=self._data_limit,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=subreddit_posts)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditPosts:
    """Represents Reddit posts and provides method for getting posts from various sources."""

    # -------------------------------------------------------------- #

    def __init__(
        self,
        timeframe: str,
        sort: str,
        limit: int,
    ):
        """
        Initializes a RedditPosts instance for getting posts from various sources.

        :param timeframe: The timeframe from which to get posts
            (choices: 'all', 'hour', 'day', 'week', 'month', 'year').
        :param sort: Sort criterion for the retrieved posts
            (choices: 'all', 'best', 'controversial', 'hot', 'new', 'rising', 'top').
        :param limit: The maximum number of posts to retrieve.
        """
        self._timeframe = timeframe
        self._sort = sort
        self._limit = limit

    # -------------------------------------------------------------- #

    @staticmethod
    def process_posts(raw_posts: list) -> List[Post]:
        posts_list: list = []
        for raw_post in raw_posts:
            post_data = raw_post.get("data")
            post = Post(
                id=post_data.get("id"),
                thumbnail=post_data.get("thumbnail"),
                title=post_data.get("title"),
                text=post_data.get("selftext"),
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
                created_at=timestamp_to_utc(timestamp=post_data.get("created")),
                raw_post=post_data,
            )
            posts_list.append(post)

        return posts_list

    # -------------------------------------------------------------- #

    async def search(self, query: str, session: aiohttp.ClientSession) -> List[Post]:
        """
        Searches for posts on Reddit based on a search query.

        :param query: Search query.
        :param session: aiohttp session to use for the request.
        :return: A list of Post objects, each containing a post's data.
        """
        search_posts: list = await get_posts(
            posts_type="search_posts",
            posts_source=query,
            timeframe=self._timeframe,
            sort=self._sort,
            limit=self._limit,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=search_posts)

    # -------------------------------------------------------------- #

    async def listing(
        self, listings_name: str, session: aiohttp.ClientSession
    ) -> List[Post]:
        """
        Gets posts from a specified listing.

        :param listings_name: name of listing to get posts from
            (choices: 'all', 'best', 'controversial', 'popular', 'rising')
        :param session: aiohttp session to use for the request.
        :return: A list of Post objects, each containing a post's data.
        """
        listing_posts: list = await get_posts(
            posts_type="listing_posts",
            posts_source=listings_name,
            timeframe=self._timeframe,
            sort=self._sort,
            limit=self._limit,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=listing_posts)

    # -------------------------------------------------------------- #

    async def front_page(self, session: aiohttp.ClientSession) -> List[Post]:
        """
        Gets posts from the Reddit front-page.

        :param session: aiohttp session to use for the request.
        :return: A list of Post objects, each containing a post's data.
        """
        front_page_posts: list = await get_posts(
            posts_type="front_page_posts",
            timeframe=self._timeframe,
            sort=self._sort,
            limit=self._limit,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=front_page_posts)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
