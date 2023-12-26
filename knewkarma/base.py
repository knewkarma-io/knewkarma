# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
from collections import Counter
from typing import List

import aiohttp

from ._meta import DATA_TIMEFRAME, DATA_SORT_CRITERION, POSTS_LISTINGS
from ._utils import unix_timestamp_to_utc
from .api import get_profile, get_posts, get_data, BASE_REDDIT_ENDPOINT
from .data import Comment, Community, PreviewCommunity, User, Post


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditUser:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    # ---------------------------------------------------------------- #

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

    # ---------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> User:
        """
        Returns a user's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A User object containing user profile data.
        :rtype: User
        """
        user_profile: dict = await get_profile(
            profile_type="user", profile_source=self._username, session=session
        )
        if "id" in user_profile:
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
                community=user_profile.get("subreddit"),
                created_at=unix_timestamp_to_utc(timestamp=user_profile.get("created")),
                raw_data=user_profile,
            )

    # ---------------------------------------------------------------- #

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

    # ---------------------------------------------------------------- #

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

        if raw_comments:
            for raw_comment in raw_comments:
                comment_data: dict = raw_comment.get("data")
                comments_list.append(
                    Comment(
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
                        community=comment_data.get("subreddit_name_prefixed"),
                        community_type=comment_data.get("subreddit_type"),
                        post_id=comment_data.get("link_id"),
                        post_title=comment_data.get("link_title"),
                        raw_data=comment_data,
                    )
                )

            return comments_list

    # ---------------------------------------------------------------- #

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
        communities: dict = await get_data(
            endpoint=f"{BASE_REDDIT_ENDPOINT}/user/{self._username}/moderated_subreddits.json",
            session=session,
        )

        if communities:
            communities_list: list = []
            for community in communities.get("data"):
                communities_list.append(
                    PreviewCommunity(
                        name=community.get("display_name"),
                        icon=community.get("community_icon").split("?")[0],
                        community_type=community.get("subreddit_type"),
                        subscribers=community.get("subscribers"),
                        whitelist_status=community.get("whitelist_status"),
                        url=community.get("url"),
                        created_at=unix_timestamp_to_utc(
                            timestamp=community.get("created")
                        ),
                        raw_data=community,
                    )
                )

            return communities_list

    # ---------------------------------------------------------------- #

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
            posts_type="user_posts",
            posts_source=self._username,
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


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditCommunity:
    """Represents a Reddit Community/Subreddit and provides methods for getting data from the specified community."""

    # ---------------------------------------------------------------- #

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

    # ---------------------------------------------------------------- #

    async def profile(self, session: aiohttp.ClientSession) -> Community:
        """
        Returns a community's profile data.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A community object containing community profile data.
        :rtype: Community
        """
        community: dict = await get_profile(
            profile_type="community",
            profile_source=self._community,
            session=session,
        )

        if "id" in community:
            return Community(
                name=community.get("display_name"),
                id=community.get("id"),
                description=community.get("public_description"),
                submit_text=community.get("submit_text"),
                icon=community.get("community_icon").split("?")[0],
                # icon_img=community.get("icon_img"),
                community_type=community.get("subreddit_type"),
                subscribers=community.get("subscribers"),
                current_active_users=community.get("accounts_active"),
                is_nsfw=community.get("over18"),
                language=community.get("lang"),
                whitelist_status=community.get("whitelist_status"),
                url=community.get("url"),
                created_at=unix_timestamp_to_utc(timestamp=community.get("created")),
                raw_data=community,
            )

    # ---------------------------------------------------------------- #

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
        community_posts: list = await get_posts(
            posts_type="community_posts",
            posts_source=self._community,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=community_posts)


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class RedditPosts:
    """Represents Reddit posts and provides method for getting posts from various sources."""

    @staticmethod
    def process_posts(raw_posts: list) -> List[Post]:
        if raw_posts:
            posts_list: list = []
            for raw_post in raw_posts:
                post_data = raw_post.get("data")
                posts_list.append(
                    Post(
                        title=post_data.get("title"),
                        thumbnail=post_data.get("thumbnail"),
                        id=post_data.get("id"),
                        body=post_data.get("selftext"),
                        author=post_data.get("author"),
                        community=post_data.get("subreddit"),
                        community_id=post_data.get("subreddit_id"),
                        community_type=post_data.get("subreddit_type"),
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
                        raw_data=post_data,
                    )
                )

            return posts_list

    # ---------------------------------------------------------------- #

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

    # ---------------------------------------------------------------- #

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

    # ---------------------------------------------------------------- #

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
        new_posts: list = await get_posts(
            posts_type="new_posts",
            limit=limit,
            sort=sort,
            session=session,
        )

        return RedditPosts.process_posts(raw_posts=new_posts)

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
