from datetime import datetime, timezone, timedelta

import aiohttp
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from conftest import (
    TEST_USERNAME,
    TEST_SUBREDDIT,
    TEST_SUBREDDIT_ID,
    TEST_SUBREDDIT_CREATED_TIMESTAMP,
    TEST_USER_CREATED_TIMESTAMP,
    TEST_USER_ID,
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
async def test_search_posts():
    search_posts_query: str = "coronavirus"
    search_posts: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="posts",
        query=search_posts_query,
        limit=100,
    )

    assert isinstance(search_posts, list)
    assert len(search_posts) == 100
    for post_result in search_posts:
        post_data: dict = post_result.get("data")
        assert search_posts[0].get("kind") == "t3"
        assert (
            search_posts_query.lower() in post_data.get("selftext").lower()
            or post_data.get("title").lower()
        )


@pytest.mark.asyncio
async def test_search_subreddits():
    search_subreddits_query: str = "science"
    search_subreddits: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="subreddits",
        query=search_subreddits_query,
        limit=150,
    )

    assert isinstance(search_subreddits, list)
    assert len(search_subreddits) == 150
    for subreddit_result in search_subreddits:
        subreddit_data: dict = subreddit_result.get("data")
        assert search_subreddits[0].get("kind") == "t5"
        assert (
            search_subreddits_query.lower()
            in subreddit_data.get("public_description").lower()
            or subreddit_data.get("display_name").lower()
        )


@pytest.mark.asyncio
async def test_search_users():
    search_users_query: str = "john"
    search_users: list[dict] = await fetch_with_retry(
        api.get_search_results,
        search_type="users",
        query=search_users_query,
        limit=50,
    )

    assert isinstance(search_users, list)
    assert len(search_users) == 50

    for user_result in search_users:
        user_data: dict = user_result.get("data")
        assert search_users[0].get("kind") == "t2"
        assert (
            search_users_query.lower() in user_data.get("name").lower()
            or user_data.get("subreddit").get("display_name").lower()
        )


@pytest.mark.asyncio
async def test_search_posts_in_a_subreddit():
    search_query: str = "Rick and Morty"
    posts_subreddit: str = "AdultSwim"
    search_results = await fetch_with_retry(
        api.get_posts,
        posts_type="search_subreddit_posts",
        query=search_query,
        subreddit=posts_subreddit,
        limit=50,
    )

    assert isinstance(search_results, list)
    assert len(search_results) == 50
    for search_result in search_results:
        post_data: dict = search_result.get("data")
        assert post_data.get("subreddit") == posts_subreddit
        assert (
            search_query.lower() in post_data.get("title").lower()
            or post_data.get("selftext").lower()
        )


@pytest.mark.asyncio
async def test_get_user_and_subreddit_profiles():
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
async def test_get_user_and_subreddit_posts():
    user_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="user_posts",
        posts_source=TEST_USERNAME,
        limit=100,
    )

    assert isinstance(user_posts, list)
    assert len(user_posts) == 100
    for user_post in user_posts:
        post_data: dict = user_post.get("data")
        assert user_posts[0].get("kind") == "t3"
        assert post_data.get("author") == TEST_USERNAME

    # ----------------------------------------------------------------- #

    subreddit_posts: list = await fetch_with_retry(
        api.get_posts,
        posts_type="subreddit_posts",
        posts_source=TEST_SUBREDDIT,
        sort="top",
        limit=50,
    )

    assert isinstance(subreddit_posts, list)
    assert len(subreddit_posts) == 50

    for subreddit_post in subreddit_posts:
        post_data: dict = subreddit_post.get("data")
        assert subreddit_posts[0].get("kind") == "t3"
        assert post_data.get("subreddit") == TEST_SUBREDDIT


@pytest.mark.asyncio
async def test_get_new_posts():
    new_posts = await fetch_with_retry(
        api.get_posts,
        posts_type="new",
        limit=200,
    )

    now = datetime.now(timezone.utc)
    assert isinstance(new_posts, list)
    assert len(new_posts) == 200
    for new_post in new_posts:
        post_data: dict = new_post.get("data")
        created_timestamp = datetime.fromtimestamp(
            post_data.get("created"), timezone.utc
        )
        assert new_posts[0].get("kind") == "t3"
        assert (
            now - timedelta(days=1) < created_timestamp
        ), f"Post {post_data.get('id')} was not created recently."


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
    for new_user in new_users:
        user_data: dict = new_user.get("data")
        created_timestamp = datetime.fromtimestamp(
            user_data.get("created"), timezone.utc
        )
        assert (
            now - timedelta(days=7) < created_timestamp
        ), f"User {user_data.get('name')} was not created recently."


@pytest.mark.asyncio
async def test_get_new_subreddits():
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
        subreddit_data: dict = new_subreddit.get("data")
        created_timestamp = datetime.fromtimestamp(
            subreddit_data.get("created"), timezone.utc
        )
        assert (
            now - timedelta(days=1) < created_timestamp
        ), f"Subreddit {subreddit_data.get('display_name')} was not created recently."
