# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import aiohttp
import pytest

from conftest import (
    TEST_USERNAME,
    TEST_USER_ID,
    TEST_USER_CREATED_TIMESTAMP,
    TEST_COMMUNITY,
    TEST_COMMUNITY_ID,
    TEST_COMMUNITY_CREATED_TIMESTAMP,
)
from knewkarma.api import get_profile, get_posts


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@pytest.mark.asyncio
async def test_get_profile():
    async with aiohttp.ClientSession() as session:
        # ------------------------------------------------------------- #

        user_profile: dict = await get_profile(
            profile_type="user",
            profile_source=TEST_USERNAME,
            session=session,
        )

        assert user_profile.get("id") == TEST_USER_ID
        assert user_profile.get("created") == TEST_USER_CREATED_TIMESTAMP

        # ------------------------------------------------------------- #

        community_profile: dict = await get_profile(
            profile_type="community",
            profile_source=TEST_COMMUNITY,
            session=session,
        )

        assert community_profile.get("id") == TEST_COMMUNITY_ID
        assert community_profile.get("created") == TEST_COMMUNITY_CREATED_TIMESTAMP


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@pytest.mark.asyncio
async def test_get_posts():
    async with aiohttp.ClientSession() as session:
        # ------------------------------------------------------------- #

        user_posts: list = await get_posts(
            posts_type="user_posts",
            posts_source=TEST_USERNAME,
            sort="top",
            timeframe="year",
            limit=100,
            session=session,
        )

        assert isinstance(user_posts, list)
        assert len(user_posts) == 100
        assert user_posts[0].get("data").get("author") == TEST_USERNAME

        # ------------------------------------------------------------- #

        community_posts: list = await get_posts(
            posts_type="community_posts",
            posts_source=TEST_COMMUNITY,
            sort="top",
            timeframe="week",
            limit=200,
            session=session,
        )

        assert isinstance(community_posts, list)
        assert len(community_posts) == 200
        assert community_posts[0].get("data").get("subreddit") == TEST_COMMUNITY

        # ------------------------------------------------------------- #

        listing_posts: list = await get_posts(
            posts_type="listing_posts",
            posts_source="best",
            sort="hot",
            timeframe="month",
            limit=10,
            session=session,
        )

        assert isinstance(listing_posts, list)
        assert len(listing_posts) == 10
        assert listing_posts[0].get("data").get("subreddit") == "best"

        # ------------------------------------------------------------- #

        search_posts: list = await get_posts(
            posts_type="search_posts",
            posts_source="covid-19",
            sort="controversial",
            limit=5,
            session=session,
        )

        assert isinstance(search_posts, list)
        assert len(search_posts) == 5
        assert (
            "covid-19" in search_posts[0].get("data").get("selftext").lower()
            or search_posts[0].get("data").get("title").lower()
        )

        # ------------------------------------------------------------- #

        front_page_posts: list = await get_posts(
            posts_type="front_page_posts",
            sort="top",
            timeframe="hour",
            limit=3,
            session=session,
        )

        assert isinstance(front_page_posts, list)
        assert len(front_page_posts) == 3


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
