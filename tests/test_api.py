from datetime import timezone, datetime, timedelta
from typing import List, Dict

import aiohttp
import pytest
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from conftest import api, TEST_USERNAME, TEST_SUBREDDIT_2, TEST_SUBREDDIT_1


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(15),
    retry=retry_if_exception_type(aiohttp.ClientError),
)
async def fetch_with_retry(fetch_func, *args, **kwargs):
    async with aiohttp.ClientSession() as session:
        return await fetch_func(*args, session=session, **kwargs)


@pytest.mark.asyncio
async def test_username_availability():
    is_available: List[Dict] = await fetch_with_retry(
        api.send_request,
        endpoint=api.endpoint("username_available"),
        params={"user": TEST_USERNAME},
    )

    assert is_available is False


@pytest.mark.asyncio
async def test_search_for_posts():
    """Tests searching for posts that contain a query string from all over Reddit."""
    search_posts_query: str = "coronavirus"
    search_posts: List[Dict] = await fetch_with_retry(
        api.search_entities,
        kind="posts",
        query=search_posts_query,
        limit=100,
    )

    assert isinstance(search_posts, List)
    assert all(isinstance(post, Dict) for post in search_posts)
    assert len(search_posts) == 100
    for post_result in search_posts:
        assert (
            search_posts_query.lower() in post_result.get("selftext").lower()
            or post_result.get("title").lower()
        )


@pytest.mark.asyncio
async def test_search_for_posts_in_a_subreddit():
    """Tests searching for posts that match the search query from a subreddit."""
    search_query: str = "Rick and Morty"
    posts_subreddit: str = "AdultSwim"
    search_results = await fetch_with_retry(
        api.get_posts_or_comments,
        kind="search_from_a_subreddit",
        query=search_query,
        subreddit=posts_subreddit,
        limit=50,
    )

    assert isinstance(search_results, List)
    assert len(search_results) == 50
    assert all(isinstance(post, Dict) for post in search_results)
    for search_result in search_results:
        assert search_result.get("subreddit").lower() == posts_subreddit.lower()
        assert (
            search_result.get("title").lower()
            or search_result.get("selftext").lower() in search_query.split()
        )


@pytest.mark.asyncio
async def test_search_for_subreddits():
    """Tests searching for subreddits."""
    search_subreddits_query: str = "science"
    search_subreddits: List[Dict] = await fetch_with_retry(
        api.search_entities,
        kind="subreddits",
        query=search_subreddits_query,
        limit=100,
    )

    assert isinstance(search_subreddits, List)
    assert len(search_subreddits) == 100
    assert all(isinstance(subreddit, Dict) for subreddit in search_subreddits)
    for subreddit_result in search_subreddits:
        assert (
            search_subreddits_query.lower()
            in subreddit_result.get("public_description").lower()
            or subreddit_result.get("display_name").lower()
        )


@pytest.mark.asyncio
async def test_search_for_users():
    """Tests searching for users."""
    search_users_query: str = "justin"
    search_users: List[Dict] = await fetch_with_retry(
        api.search_entities,
        kind="users",
        query=search_users_query,
        limit=50,
    )

    assert isinstance(search_users, List)
    assert len(search_users) == 50
    assert all(isinstance(user, Dict) for user in search_users)

    for user_result in search_users:
        username = user_result.get("name")
        assert search_users_query.lower() in username.lower()


@pytest.mark.asyncio
async def test_get_user_and_subreddit_profiles():
    """Tests getting user and subreddit profiles."""
    user_profile: Dict = await fetch_with_retry(
        api.get_entity,
        kind="user",
        username=TEST_USERNAME,
    )

    assert isinstance(user_profile, Dict)
    assert user_profile.get("id") == "6l4z3"
    assert user_profile.get("created") == 1325741068

    subreddit_profile: Dict = await fetch_with_retry(
        api.get_entity,
        kind="subreddit",
        subreddit=TEST_SUBREDDIT_2,
    )

    assert subreddit_profile.get("id") == "2qh1i"
    assert subreddit_profile.get("created") == 1201233135


@pytest.mark.asyncio
async def test_get_posts_or_comments_from_a_subreddit():
    """Tests getting posts from a subreddit."""
    subreddit_posts: List = await fetch_with_retry(
        api.get_posts_or_comments,
        kind="posts_from_a_subreddit",
        subreddit=TEST_SUBREDDIT_1,
        limit=50,
    )

    assert isinstance(subreddit_posts, List)
    assert len(subreddit_posts) == 50
    assert all(isinstance(post, Dict) for post in subreddit_posts)

    for subreddit_post in subreddit_posts:
        assert subreddit_post.get("subreddit").lower() == TEST_SUBREDDIT_1.lower()


@pytest.mark.asyncio
async def test_get_posts_or_comments_from_a_user():
    """Tests getting posts from a user."""
    username: str = "AutoModerator"
    user_posts: List = await fetch_with_retry(
        api.get_posts_or_comments,
        kind="posts_from_a_user",
        username=username,
        limit=100,
    )

    assert isinstance(user_posts, List)
    assert len(user_posts) == 100
    assert all(isinstance(post, Dict) for post in user_posts)
    for user_post in user_posts:
        assert user_post.get("author").lower() == username.lower()


@pytest.mark.asyncio
async def test_get_new_posts():
    """Tests getting new posts."""
    new_posts = await fetch_with_retry(
        api.get_posts_or_comments,
        kind="new",
        limit=200,
    )

    now = datetime.now(timezone.utc)
    assert isinstance(new_posts, List)
    assert len(new_posts) == 200
    assert all(isinstance(post, Dict) for post in new_posts)
    for new_post in new_posts:
        created_timestamp = datetime.fromtimestamp(
            new_post.get("created"), timezone.utc
        )
        assert (
            now - timedelta(days=1) < created_timestamp
        ), f"Post {new_post.get('id')} was not created recently."


@pytest.mark.asyncio
async def test_get_new_users():
    """Tests getting new users."""
    new_users: List[Dict] = await fetch_with_retry(
        api.get_users,
        kind="new",
        timeframe="week",
        limit=100,
    )

    assert isinstance(new_users, List)
    assert len(new_users) == 100
    assert all(isinstance(user, Dict) for user in new_users)

    now = datetime.now(timezone.utc)
    for new_user in new_users:
        created_timestamp = datetime.fromtimestamp(
            new_user.get("created"), timezone.utc
        )
        assert (
            now - timedelta(days=7) < created_timestamp
        ), f"User {new_user.get('name')} was not created recently."


@pytest.mark.asyncio
async def test_get_new_subreddits():
    """Tests getting new subreddits."""
    new_subreddits = await fetch_with_retry(
        api.get_subreddits,
        timeframe="day",
        kind="new",
        limit=200,
    )

    now = datetime.now(timezone.utc)
    assert isinstance(new_subreddits, List)
    assert len(new_subreddits) == 200
    assert all(isinstance(subreddit, Dict) for subreddit in new_subreddits)
    for new_subreddit in new_subreddits:
        created_timestamp = datetime.fromtimestamp(
            new_subreddit.get("created"), timezone.utc
        )
        assert (
            now - timedelta(days=1) < created_timestamp
        ), f"Subreddit {new_subreddit.get('display_name')} was not created recently."


# -------------------------------- END ----------------------------------------- #
