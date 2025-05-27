from types import SimpleNamespace
from typing import List

import karmakaze
from conftest import (
    RAW_COMMENTS,
    RAW_POST,
    RAW_POSTS,
    RAW_SUBREDDIT,
    RAW_USER,
    RAW_SUBREDDITS,
    RAW_USERS,
    RAW_WIKI_PAGE,
)

sanitise_and_parse = karmakaze.SanitiseAndParse()


def test_comments_sanitation_and_parsing():
    comments = sanitise_and_parse.comments(RAW_COMMENTS[1])
    assert isinstance(comments.children, List)

    for comment in comments.children:
        assert isinstance(comment, SimpleNamespace)
        assert isinstance(comment.data.subreddit, str)
        assert hasattr(comment.data, "ups")


def test_post_sanitation_and_parsing():
    post = sanitise_and_parse.post(RAW_POST)
    assert isinstance(post, SimpleNamespace)
    assert isinstance(post.data.ups, int)
    assert isinstance(post.data.upvote_ratio, (float, int))
    assert isinstance(post.data.is_robot_indexable, bool)


def test_posts_sanitation_and_parsing():
    posts = sanitise_and_parse.posts(RAW_POSTS).children
    assert isinstance(posts, List)
    for post in posts:
        assert isinstance(post, SimpleNamespace)
        assert isinstance(post.data.num_comments, int)
        assert hasattr(post.data, "url")


def test_subreddit_sanitation_and_parsing():
    subreddit = sanitise_and_parse.subreddit(RAW_SUBREDDIT)
    assert isinstance(subreddit, SimpleNamespace)
    assert isinstance(subreddit.data.active_user_count, int)
    assert hasattr(subreddit.data, "display_name")


def test_subreddits_sanitation_and_parsing():
    subreddits = sanitise_and_parse.subreddits(RAW_SUBREDDITS)
    assert isinstance(subreddits.children, List)
    for subreddit in subreddits.children:
        assert isinstance(subreddit, SimpleNamespace)
        assert isinstance(subreddit.data.subscribers, int)
        assert hasattr(subreddit.data, "description")


def test_user_sanitation_and_parsing():
    user = sanitise_and_parse.user(RAW_USER)
    assert isinstance(user, SimpleNamespace)
    assert isinstance(user.data.created, float)
    assert hasattr(user.data, "comment_karma")


def test_users_sanitation_and_parsing():
    users = sanitise_and_parse.users(RAW_USERS)
    assert isinstance(users.children, List)
    for user in users.children:
        assert isinstance(user, SimpleNamespace)
        assert isinstance(user.data.accept_followers, bool)
        assert hasattr(user.data, "name")


def test_wiki_page_sanitation_and_parsing():
    wiki_page = sanitise_and_parse.wiki_page(RAW_WIKI_PAGE)
    assert isinstance(wiki_page, SimpleNamespace)
    assert isinstance(wiki_page.data.revision_date, int)
    assert hasattr(wiki_page.data, "revision_id")
