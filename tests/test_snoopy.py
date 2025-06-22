from platform import python_version, platform

import pytest
import requests

from engines.karmakaze.schemas import User, Subreddit, Comment, Post
from engines.snoopy.reddit import Reddit
from knewkarma.meta.about import Project
from knewkarma.meta.version import Version


@pytest.fixture(scope="module")
def reddit():
    return Reddit(
        user_agent=f"pytest-integration-test for "
        f"{Project.name.replace(' ', '-')}/{Version.release} "
        f"(Python {python_version} on {platform}; +{Project.documentation})"
    )


@pytest.fixture
def session():
    return requests.Session()


def test_user_profile_fetch(reddit, session):
    user = reddit.user("spez", session=session)
    assert isinstance(user, User)
    assert user.created == 1118030400
    assert user.subreddit.name == "t5_3k30p"
    assert user.subreddit.public_description == "Reddit CEO"
    assert user.name.lower() == "spez"


def test_subreddit_profile_fetch(reddit, session):
    subreddit = reddit.subreddit("python", session=session)
    assert isinstance(subreddit, Subreddit)
    assert subreddit.display_name.lower() == "python"
    assert subreddit.created == 1201230879
    assert subreddit.user_flair_type == "text"
    assert subreddit.name == "t5_2qh0y"


def test_wiki_page_fetch(reddit, session): ...


def test_user_comments(reddit, session):
    comments = reddit.comments(
        session=session,
        kind="user",
        username="spez",
        limit=5,
        sort="new",
        timeframe="all",
    )
    # TODO: Add more assertions
    assert isinstance(comments, list)
    assert all(isinstance(comment, Comment) for comment in comments)


def test_search_subreddits(reddit, session):
    query = "Python"
    subreddits = reddit.search(
        query=query,
        kind="subreddits",
        session=session,
        limit=5,
        sort="relevance",
        timeframe="all",
    )
    assert isinstance(subreddits, list)
    for subreddit in subreddits:
        assert isinstance(subreddit, Subreddit)
        assert query.lower() in subreddit.display_name.lower()


def test_search_users(reddit, session):
    query = "John"
    users = reddit.search(query=query, kind="users", session=session, limit=20)
    assert isinstance(users, list)
    assert any(query.lower() in user.name.lower() for user in users)
    assert all(isinstance(user, User) for user in users)


def test_search_posts(reddit, session):
    query = "aliens"
    posts = reddit.search(query=query, kind="posts", session=session, limit=20)
    assert isinstance(posts, list)
    assert all(isinstance(post, Post) for post in posts)
    assert any(
        query.lower() in post.title.lower() or post.selftext.lower() for post in posts
    )


def test_post_fetch(reddit, session):
    post = reddit.post(id="1lhlolt", subreddit="BeAmazed", session=session)
    assert isinstance(post, Post)
    assert post.subreddit.lower() == "beamazed"
    assert post.created == 1750591723
    assert post.title == "She Was Right All Along"
