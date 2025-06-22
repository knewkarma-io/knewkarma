import typing as t

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
from engines import karmakaze
from engines.karmakaze.schemas import User, WikiPage, Post, Comment, Subreddit

sanitise_and_parse = karmakaze.RedditSanitiser()


def test_comments_sanitation_and_parsing():
    comments = sanitise_and_parse.comments(RAW_COMMENTS[1])
    assert isinstance(comments, t.List)

    for comment in comments:
        assert isinstance(comment, Comment)
        assert isinstance(comment.subreddit, str)
        assert hasattr(comment, "ups")


def test_post_sanitation_and_parsing():
    post = sanitise_and_parse.post(RAW_POST)
    assert isinstance(post, Post)
    assert isinstance(post.ups, int)
    assert isinstance(post.upvote_ratio, (float, int))
    assert isinstance(post.is_robot_indexable, bool)


def test_posts_sanitation_and_parsing():
    posts = sanitise_and_parse.posts(RAW_POSTS)
    assert isinstance(posts, t.List)
    for post in posts:
        assert isinstance(post, Post)
        assert isinstance(post.num_comments, int)
        assert hasattr(post, "url")


def test_subreddit_sanitation_and_parsing():
    subreddit = sanitise_and_parse.subreddit(RAW_SUBREDDIT)
    assert isinstance(subreddit, Subreddit)
    assert isinstance(subreddit.active_user_count, int)
    assert hasattr(subreddit, "display_name")


def test_subreddits_sanitation_and_parsing():
    subreddits = sanitise_and_parse.subreddits(RAW_SUBREDDITS)
    assert isinstance(subreddits, t.List)
    for subreddit in subreddits:
        assert isinstance(subreddit, Subreddit)
        assert isinstance(subreddit.subscribers, int)
        assert hasattr(subreddit, "description")


def test_user_sanitation_and_parsing():
    user = sanitise_and_parse.user(RAW_USER)
    assert isinstance(user, User)
    assert isinstance(user.created, float)
    assert hasattr(user, "comment_karma")


def test_users_sanitation_and_parsing():
    users = sanitise_and_parse.users(RAW_USERS)
    assert isinstance(users, t.List)
    for user in users:
        assert isinstance(user, Subreddit)
        assert isinstance(user.accept_followers, bool)
        assert hasattr(user, "name")


def test_wiki_page_sanitation_and_parsing():
    wiki_page = sanitise_and_parse.wiki_page(RAW_WIKI_PAGE)
    assert isinstance(wiki_page, WikiPage)
    assert isinstance(wiki_page.revision_date, float)
    assert hasattr(wiki_page, "revision_id")
