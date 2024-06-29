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
    search_posts: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="posts",
        query="covid-19",
        limit=5,
    )

    assert isinstance(search_posts, list)
    assert len(search_posts) == 5
    assert (
        "covid-19" in search_posts[0].get("data").get("selftext").lower()
        or search_posts[0].get("data").get("title").lower()
    )

    search_subreddits: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="subreddits",
        query="ask",
        limit=13,
    )

    assert isinstance(search_subreddits, list)
    assert len(search_subreddits) == 13
    assert "ask" in search_subreddits[0].get("data").get("display_name").lower()

    search_users: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="users",
        query="john",
        limit=22,
    )

    assert isinstance(search_users, list)
    assert len(search_users) == 22
    assert "john" in search_users[1].get("data").get("name").lower()


@pytest.mark.asyncio
async def test_get_profile():
    user_profile: dict = await fetch_with_retry(
        api.get_profile,
        profile_type="user",
        profile_source=TEST_USERNAME,
    )

    assert user_profile.get("id") == TEST_USER_ID
    assert user_profile.get("created") == TEST_USER_CREATED_TIMESTAMP

    community_profile: dict = await fetch_with_retry(
        api.get_profile,
        profile_type="subreddit",
        profile_source=TEST_SUBREDDIT,
    )

    assert community_profile.get("id") == TEST_SUBREDDIT_ID
    assert community_profile.get("created") == TEST_SUBREDDIT_CREATED_TIMESTAMP


@pytest.mark.asyncio
async def test_get_subreddits():
    all_subreddits = await fetch_with_retry(
        api.get_subreddits,
        subreddits_type="all",
        limit=100,
    )

    assert isinstance(all_subreddits, list)
    assert "subreddit_type" in all_subreddits[0].get("data")
    assert len(all_subreddits) == 100

    default_subreddits = await fetch_with_retry(
        api.get_subreddits,
        subreddits_type="default",
        limit=150,
    )

    assert isinstance(default_subreddits, list)
    assert "community_icon" in default_subreddits[1].get("data")
    assert len(default_subreddits) == 150

    new_subreddits = await fetch_with_retry(
        api.get_subreddits,
        subreddits_type="new",
        limit=200,
    )

    assert isinstance(new_subreddits, list)
    assert "whitelist_status" in new_subreddits[3].get("data")
    assert len(new_subreddits) == 200

    popular_subreddits = await fetch_with_retry(
        api.get_subreddits,
        subreddits_type="popular",
        limit=200,
    )

    assert isinstance(popular_subreddits, list)
    assert "display_name" in popular_subreddits[3].get("data")
    assert len(new_subreddits) == 200


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
    assert user_posts[0].get("data").get("author") == TEST_USERNAME

    community_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="subreddit_posts",
        posts_source=TEST_SUBREDDIT,
        sort="top",
        timeframe="week",
        limit=200,
    )

    assert isinstance(community_posts, list)
    assert len(community_posts) == 200
    assert community_posts[0].get("data").get("subreddit") == TEST_SUBREDDIT

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
    assert listing_posts[0].get("data").get("subreddit") == "best"

    new_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="new_posts",
        limit=120,
    )

    assert isinstance(new_posts, list)
    assert len(new_posts) == 120

    front_page_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="front_page_posts",
        sort="top",
        timeframe="hour",
        limit=3,
    )

    assert isinstance(front_page_posts, list)
    assert len(front_page_posts) == 3
