# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from dataclasses import dataclass

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@dataclass
class User:
    name: str
    id: str
    is_verified: bool
    has_verified_email: bool
    is_blocked: bool
    is_gold: bool
    is_mod: bool
    is_employee: bool
    hidden_from_bots: bool
    accepts_followers: bool
    comment_karma: int
    link_karma: int
    awardee_karma: int
    total_karma: int
    created_at: str
    subreddit: dict
    raw_data: dict


# -------------------------------------------------------------------- #


@dataclass
class Subreddit:
    name: str
    id: str
    description: str
    submit_text: str
    icon_img: str
    subreddit_type: str
    subscribers: int
    current_active_users: int
    is_nsfw: bool
    language: str
    created_at: str
    raw_data: dict


# -------------------------------------------------------------------- #


@dataclass
class Post:
    id: str
    thumbnail: str
    title: str
    text: str
    author: str
    subreddit: str
    subreddit_id: str
    subreddit_type: str
    upvotes: int
    upvote_ratio: float
    downvotes: int
    gilded: int
    is_nsfw: bool
    is_shareable: bool
    is_edited: bool
    comments: int
    hide_from_bots: bool
    score: float
    domain: str
    permalink: str
    is_locked: bool
    is_archived: bool
    created_at: str
    raw_post: dict


# -------------------------------------------------------------------- #


@dataclass
class Comment:
    id: str
    text: str
    author: str
    upvotes: int
    downvotes: int
    is_nsfw: bool
    is_edited: bool
    score: float
    hidden_score: bool
    gilded: int
    is_stickied: bool
    is_locked: bool
    is_archived: bool
    created_at: str
    subreddit: str
    subreddit_type: str
    post_id: str
    post_title: str
    author_is_premium: bool
    raw_data: dict


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
