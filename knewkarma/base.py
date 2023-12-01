# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from dataclasses import dataclass
from typing import List

import aiohttp

from . import api
from ._coreutils import timestamp_to_utc


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@dataclass
class User:
    name: str
    id: str
    is_verified: bool
    has_verified_email: bool
    is_blocked: bool
    is_gold: bool
    is_mod: bool
    is_employee: bool
    hidden_from_bots: bool
    accepts_followers: bool
    comment_karma: int
    link_karma: int
    total_karma: int
    created_at: str
    subreddit: dict
    raw_data: dict


@dataclass
class Subreddit:
    name: str
    id: str
    description: str
    submit_text: str
    icon_img: str
    subreddit_type: str
    subscribers: int
    current_active_users: int
    is_nsfw: bool
    language: str
    created_at: str
    raw_data: dict


@dataclass
class Post:
    id: str
    thumbnail: str
    title: str
    text: str
    author: str
    subreddit: str
    subreddit_id: str
    subreddit_type: str
    upvotes: int
    upvote_ratio: float
    downvotes: int
    gilded: int
    is_nsfw: bool
    is_shareable: bool
    is_edited: bool
    comments: int
    hide_from_bots: bool
    score: float
    domain: str
    permalink: str
    is_locked: bool
    is_archived: bool
    created_at: str
    raw_post: dict


@dataclass
class Comment:
    id: str
    text: str
    author: str
    upvotes: int
    downvotes: int
    is_nsfw: bool
    is_edited: bool
    score: float
    hidden_score: bool
    gilded: int
    is_stickied: bool
    is_locked: bool
    is_archived: bool
    created_at: str
    subreddit: str
    subreddit_type: str
    post_id: str
    post_title: str
    author_is_premium: bool
    raw_data: dict


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditUser:
    # -------------------------------------------------------------- #

    def __init__(
        self,
        username: str,
        data_timeframe: str,
        data_sort: str,
        data_limit: int,
    ):
        self._username = username
        self._data_timeframe = data_timeframe
        self._data_sort = data_sort
        self._data_limit = data_limit

    # -------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> User:
        user_profile: dict = await api.get_profile(
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
            total_karma=user_profile.get("total_karma"),
            subreddit=user_profile.get("subreddit"),
            created_at=timestamp_to_utc(timestamp=user_profile.get("created")),
            raw_data=user_profile,
        )

    # -------------------------------------------------------------- #

    async def posts(self, session: aiohttp.ClientSession) -> List[Post]:
        user_posts: list = await api.get_posts(
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
        comments_list: list = []
        raw_comments: list = await api.get_posts(
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
    # -------------------------------------------------------------- #

    def __init__(
        self, subreddit: str, data_timeframe: str, data_sort: str, data_limit: int
    ):
        self._subreddit = subreddit
        self._data_timeframe = data_timeframe
        self._data_sort = data_sort
        self._data_limit = data_limit

    # -------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> Subreddit:
        subreddit_profile: dict = await api.get_profile(
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
        subreddit_posts: list = await api.get_posts(
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
    # -------------------------------------------------------------- #

    def __init__(
        self,
        timeframe: str,
        sort: str,
        limit: int,
    ):
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
        search_posts: list = await api.get_posts(
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
        listing_posts: list = await api.get_posts(
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
        front_page_posts: list = await api.get_posts(
            posts_type="front_page_posts",
            timeframe=self._timeframe,
            sort=self._sort,
            limit=self._limit,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=front_page_posts)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
