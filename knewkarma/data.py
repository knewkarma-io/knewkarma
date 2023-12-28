# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from dataclasses import dataclass

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


@dataclass
class User:
    name: str
    id: str
    icon_img: str
    is_verified: bool
    has_verified_email: bool
    is_mod: bool
    is_gold: bool
    is_blocked: bool
    is_employee: bool
    hidden_from_bots: bool
    accepts_followers: bool
    comment_karma: int
    link_karma: int
    awardee_karma: int
    total_karma: int
    joined_at: str
    community: dict
    raw_data: dict


# -------------------------------------------------------------------- #


@dataclass
class Community:
    name: str
    id: str
    description: str
    submit_text: str
    icon: str
    # icon_img: str
    community_type: str
    subscribers: int
    current_active_users: int
    is_nsfw: bool
    language: str
    whitelist_status: str
    url: str
    created_at: str
    raw_data: dict


# -------------------------------------------------------------------- #


@dataclass
class PreviewCommunity:
    name: str
    icon: str
    # id: str
    # description: str
    # submit_text: str
    # icon_img: str
    community_type: str
    subscribers: int
    # current_active_users: int
    # is_nsfw: bool
    # language: str
    whitelist_status: str
    url: str
    created_at: str
    raw_data: dict


@dataclass
class Post:
    title: str
    body: str
    id: str
    thumbnail: str
    author: str
    community: str
    community_id: str
    community_type: str
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
    upvotes: int
    upvote_ratio: float
    downvotes: int
    posted_at: str
    raw_data: dict


# -------------------------------------------------------------------- #


@dataclass
class Comment:
    body: str
    id: str
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
    commented_at: str
    community: str
    community_type: str
    post_id: str
    post_title: str
    author_is_premium: bool
    raw_data: dict


# -------------------------------------------------------------------- #


@dataclass
class WikiPage:
    revision_id: str
    revision_date: str
    content_markdown: str
    revised_by: User
    raw_data: dict


# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
