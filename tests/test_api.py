from datetime import timezone, datetime, timedelta

import requests
from tenacity import retry, stop_after_attempt, wait_fixed, retry_if_exception_type

from knewkarma.api import Api

api = Api()

TEST_USERNAME: str = "AutoModerator"
TEST_SUBREDDIT_1: str = "AskScience"
TEST_SUBREDDIT_2: str = "AskReddit"


@retry(
    stop=stop_after_attempt(5),
    wait=wait_fixed(15),
    retry=retry_if_exception_type(requests.ConnectionError),
)
def get_with_retry(get_function, *args, **kwargs):
    with requests.Session() as session:
        return get_function(*args, session=session, **kwargs)


def test_search_for_posts():
    """Tests searching for posts that contain a query string from all over Reddit."""
    search_posts_query: str = "coronavirus"
    search_posts: list[dict] = get_with_retry(
        api.search_entities,
        entity_type="posts",
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


def test_search_for_posts_in_a_subreddit():
    """Tests searching for posts that match the search query from a subreddit."""
    search_query: str = "Rick and Morty"
    posts_subreddit: str = "AdultSwim"
    search_results = get_with_retry(
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
        assert post_data.get("subreddit").lower() == posts_subreddit.lower()
        assert (
                search_query.lower() in post_data.get("title").lower()
                or post_data.get("selftext").lower()
        )


def test_search_for_subreddits():
    """Tests searching for subreddits."""
    search_subreddits_query: str = "science"
    search_subreddits: list[dict] = get_with_retry(
        api.search_entities,
        entity_type="subreddits",
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


def test_search_for_users():
    """Tests searching for users."""
    search_users_query: str = "john"
    search_users: list[dict] = get_with_retry(
        api.search_entities,
        entity_type="users",
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


def test_get_user_and_subreddit_profiles():
    """Tests getting user and subreddit profiles."""
    user_profile: dict = get_with_retry(
        api.get_entity,
        entity_type="user",
        username=TEST_USERNAME,
    )

    assert user_profile.get("id") == "6l4z3"
    assert user_profile.get("created") == 1325741068

    subreddit_profile: dict = get_with_retry(
        api.get_entity,
        entity_type="subreddit",
        subreddit=TEST_SUBREDDIT_2,
    )

    assert subreddit_profile.get("id") == "2qh1i"
    assert subreddit_profile.get("created") == 1201233135


def test_get_posts_from_a_subreddit():
    """Tests getting posts from a subreddit."""
    subreddit_posts: list = get_with_retry(
        api.get_posts,
        posts_type="subreddit_posts",
        subreddit=TEST_SUBREDDIT_1,
        limit=50,
    )

    assert isinstance(subreddit_posts, list)
    assert len(subreddit_posts) == 50

    for subreddit_post in subreddit_posts:
        post_data: dict = subreddit_post.get("data")
        print(post_data)
        assert subreddit_posts[0].get("kind") == "t3"
        assert post_data.get("subreddit").lower() == TEST_SUBREDDIT_1.lower()


def test_get_posts_from_a_user():
    """Tests getting posts from a user."""
    username: str = "AutoModerator"
    user_posts: list = get_with_retry(
        api.get_posts,
        posts_type="user_posts",
        username=username,
        limit=100,
    )

    assert isinstance(user_posts, list)
    assert len(user_posts) == 100
    for user_post in user_posts:
        post_data: dict = user_post.get("data")
        assert user_posts[0].get("kind") == "t3"
        assert post_data.get("author").lower() == username.lower()


def test_get_new_posts():
    """Tests getting new posts."""
    new_posts = get_with_retry(
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


def test_get_new_users():
    """Tests getting new users."""
    new_users: list[dict] = get_with_retry(
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


def test_get_new_subreddits():
    """Tests getting new subreddits."""
    new_subreddits = get_with_retry(
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

# -------------------------------- END ----------------------------------------- #
