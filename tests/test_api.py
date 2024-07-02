from datetime import datetime, timedelta, timezone

import aiohttp
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from conftest import (
    TEST_USERNAME,
    TEST_USER_ID,
    TEST_USER_CREATED_TIMESTAMP,
    TEST_SUBREDDIT,
    TEST_SUBREDDIT_ID,
    TEST_SUBREDDIT_CREATED_TIMESTAMP,
)
from knewkarma.api import Api

api = Api()


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(15),
    retry=retry_if_exception_type(aiohttp.ClientError),
)
async def fetch_with_retry(fetch_func, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        return await fetch_func(*args, session=session, **kwargs)


@pytest.mark.asyncio
async def test_search():
    search_posts_query: str = "coronavirus"
    search_posts: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="posts",
        query=search_posts_query,
        limit=5,
    )

    assert isinstance(search_posts, list)
    assert len(search_posts) == 5
    for post_result in search_posts:
        selftext: str = post_result.get("data").get("selftext")
        title: str = post_result.get("data").get("title")
        assert search_posts_query in selftext.lower() or title.lower()

    search_subreddits_query: str = "Ask"
    search_subreddits: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="subreddits",
        query=search_subreddits_query,
        limit=13,
    )

    assert isinstance(search_subreddits, list)
    assert len(search_subreddits) == 13
    for subreddit_result in search_subreddits:
        assert (
            search_subreddits_query.lower()
            in subreddit_result.get("data").get("display_name").lower()
            or subreddit_result.get("data").get("submit_text").lower()
        )

    search_users_query: str = "john"
    search_users: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="users",
        query=search_users_query,
        limit=22,
    )

    assert isinstance(search_users, list)
    assert len(search_users) == 22

    for user_result in search_users:
        assert search_users_query in user_result.get("data").get("name").lower()


@pytest.mark.asyncio
async def test_get_profile():
    user_profile: dict = await fetch_with_retry(
        api.get_profile,
        profile_type="user",
        profile_source=TEST_USERNAME,
    )

    assert user_profile.get("id") == TEST_USER_ID
    assert user_profile.get("created") == TEST_USER_CREATED_TIMESTAMP

    subreddit_profile: dict = await fetch_with_retry(
        api.get_profile,
        profile_type="subreddit",
        profile_source=TEST_SUBREDDIT,
    )

    assert subreddit_profile.get("id") == TEST_SUBREDDIT_ID
    assert subreddit_profile.get("created") == TEST_SUBREDDIT_CREATED_TIMESTAMP


@pytest.mark.asyncio
async def test_get_subreddits():
    new_subreddits = await fetch_with_retry(
        api.get_subreddits,
        timeframe="day",
        subreddits_type="new",
        limit=200,
    )

    now = datetime.now(timezone.utc)
    assert isinstance(new_subreddits, list)
    assert len(new_subreddits) == 200
    for new_subreddit in new_subreddits:
        created_timestamp = datetime.fromtimestamp(
            new_subreddit.get("data").get("created"), timezone.utc
        )
        assert (
            now - timedelta(days=1) < created_timestamp
        ), f"Subreddit {new_subreddit.get('data').get('display_name')} was not created recently."

    popular_subreddits = await fetch_with_retry(
        api.get_subreddits,
        subreddits_type="popular",
        limit=200,
    )

    assert isinstance(popular_subreddits, list)
    assert len(new_subreddits) == 200
    for popular_subreddit in popular_subreddits:
        assert "display_name" in popular_subreddit.get("data")


@pytest.mark.asyncio
async def test_get_posts():
    user_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="user_posts",
        posts_source=TEST_USERNAME,
        sort="top",
        timeframe="year",
        limit=100,
    )

    assert isinstance(user_posts, list)
    assert len(user_posts) == 100
    for user_post in user_posts:
        assert user_post.get("data").get("author") == TEST_USERNAME

    subreddit_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="subreddit_posts",
        posts_source=TEST_SUBREDDIT,
        sort="top",
        timeframe="week",
        limit=200,
    )

    assert isinstance(subreddit_posts, list)
    assert len(subreddit_posts) == 200

    for post in subreddit_posts:
        assert post.get("data").get("subreddit") == TEST_SUBREDDIT

    listing_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="listing_posts",
        posts_source="best",
        sort="hot",
        timeframe="month",
        limit=10,
    )

    assert isinstance(listing_posts, list)
    assert len(listing_posts) == 10
    for listing_post in listing_posts:
        assert listing_post.get("data").get("subreddit") == "best"


@pytest.mark.asyncio
async def test_get_new_users():
    new_users: list[dict] = await fetch_with_retry(
        api.get_users,
        users_type="new",
        timeframe="week",
        limit=100,
    )

    assert isinstance(new_users, list)
    assert len(new_users) == 100

    now = datetime.now(timezone.utc)
    for user in new_users:
        created_timestamp = datetime.fromtimestamp(
            user.get("data").get("created"), timezone.utc
        )
        assert (
            now - timedelta(days=7) < created_timestamp
        ), f"User {user.get('data').get('name')} was not created recently."
