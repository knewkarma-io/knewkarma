import typing as t

from pydantic import BaseModel, HttpUrl


class Listing(BaseModel):
    kind: str
    data: t.Dict[str, t.Any]  # To keep it flexible for nested comments


class Comment(BaseModel):
    subreddit_id: str
    approved_at_utc: t.Optional[float] = None
    author_is_blocked: bool
    comment_type: t.Optional[str] = None
    awarders: t.List[str]
    mod_reason_by: t.Optional[str] = None
    banned_by: t.Optional[str] = None
    author_flair_type: t.Optional[str] = None
    total_awards_received: int
    subreddit: str
    author_flair_template_id: t.Optional[str] = None
    likes: t.Optional[bool] = None
    replies: t.Union[Listing, str]
    user_reports: t.List[t.Any]
    saved: bool
    id: str
    banned_at_utc: t.Optional[float] = None
    mod_reason_title: t.Optional[str] = None
    gilded: int
    archived: bool
    collapsed_reason_code: t.Optional[str] = None
    no_follow: bool
    author: str
    can_mod_post: bool
    created_utc: float
    send_replies: bool
    parent_id: str
    score: int
    author_fullname: t.Optional[str] = None
    approved_by: t.Optional[str] = None
    mod_note: t.Optional[str] = None
    all_awardings: t.List[dict]
    collapsed: bool
    body: str
    edited: t.Union[bool, float]
    top_awarded_type: t.Optional[str] = None
    author_flair_css_class: t.Optional[str] = None
    name: str
    is_submitter: bool
    author_flair_richtext: t.Optional[t.List[dict]] = None
    author_patreon_flair: t.Optional[bool] = None
    body_html: str
    removal_reason: t.Optional[str] = None
    collapsed_reason: t.Optional[str] = None
    distinguished: t.Optional[str] = None
    associated_award: t.Optional[dict] = None
    stickied: bool
    author_premium: t.Optional[bool] = None
    can_gild: bool
    gildings: t.Dict[str, int]
    unrepliable_reason: t.Optional[str] = None
    author_flair_text_color: t.Optional[str] = None
    score_hidden: bool
    permalink: str
    subreddit_type: str
    locked: bool
    report_reasons: t.Optional[t.List[str]] = None
    created: float
    author_flair_text: t.Optional[str] = None
    treatment_tags: t.List[str]
    link_id: str
    subreddit_name_prefixed: str
    controversiality: int
    depth: t.Optional[int] = None
    author_flair_background_color: t.Optional[str] = None
    collapsed_because_crowd_control: t.Optional[str] = None
    mod_reports: t.List[t.Any]
    num_reports: t.Optional[int] = None
    ups: int


class Post(BaseModel):
    subreddit: str
    selftext: t.Optional[str] = None
    title: str
    link_flair_richtext: t.List[dict]
    subreddit_name_prefixed: str
    hidden: bool
    pwls: t.Optional[int] = None
    link_flair_css_class: t.Optional[str] = None
    thumbnail_height: t.Optional[int] = None
    top_awarded_type: t.Optional[str] = None
    hide_score: bool
    name: str
    quarantine: bool
    link_flair_text_color: t.Optional[str] = None
    upvote_ratio: float
    subreddit_type: str
    ups: int
    total_awards_received: int
    media_embed: t.Dict[str, t.Any]
    thumbnail_width: t.Optional[int] = None
    is_original_content: bool
    secure_media: t.Optional[dict] = None
    is_reddit_media_domain: bool
    is_meta: bool
    category: t.Optional[str] = None
    secure_media_embed: t.Dict[str, t.Any]
    link_flair_text: t.Optional[str] = None
    can_mod_post: bool
    score: int
    approved_by: t.Optional[str] = None
    is_created_from_ads_ui: bool
    thumbnail: str
    edited: t.Union[bool, float]
    gildings: t.Dict[str, int]
    content_categories: t.Optional[t.List[str]] = None
    is_self: bool
    mod_note: t.Optional[str] = None
    created: float
    link_flair_type: str
    wls: t.Optional[int] = None
    removed_by_category: t.Optional[str] = None
    banned_by: t.Optional[str] = None
    domain: str
    allow_live_comments: bool
    selftext_html: t.Optional[str] = None
    suggested_sort: t.Optional[str] = None
    banned_at_utc: t.Optional[float] = None
    archived: bool
    no_follow: bool
    is_crosspostable: bool
    pinned: bool
    over_18: bool
    all_awardings: t.List[dict]
    awarders: t.List[str]
    media_only: bool
    can_gild: bool
    spoiler: bool
    locked: bool
    treatment_tags: t.List[str]
    removed_by: t.Optional[str] = None
    distinguished: t.Optional[str] = None
    subreddit_id: str
    mod_reason_by: t.Optional[str] = None
    removal_reason: t.Optional[str] = None
    link_flair_background_color: t.Optional[str] = None
    id: str
    is_robot_indexable: bool
    author: str
    discussion_type: t.Optional[str] = None
    num_comments: int
    media: t.Optional[dict] = None
    contest_mode: bool
    permalink: str
    stickied: bool
    url: str
    subreddit_subscribers: int
    created_utc: float
    num_crossposts: int
    is_video: bool


class UserSubreddit(BaseModel):
    default_set: bool
    banner_img: t.Optional[str]
    allowed_media_in_comments: t.List[str]
    free_form_reports: bool
    community_icon: t.Optional[str]
    show_media: bool
    icon_color: t.Optional[str]
    display_name: str
    header_img: t.Optional[str]
    title: str
    previous_names: t.List[str]
    over_18: bool
    icon_size: t.Optional[t.List[int]]
    primary_color: str
    icon_img: t.Optional[HttpUrl]
    description: str
    submit_link_label: str
    header_size: t.Optional[t.List[int]]
    restrict_posting: bool
    restrict_commenting: bool
    subscribers: int
    submit_text_label: str
    is_default_icon: bool
    link_flair_position: str
    display_name_prefixed: str
    key_color: str
    name: str
    is_default_banner: bool
    url: str
    quarantine: bool
    banner_size: t.Optional[t.List[int]]
    user_is_moderator: t.Optional[bool]
    accept_followers: bool
    public_description: str
    link_flair_enabled: bool
    disable_contributor_requests: bool
    subreddit_type: str


class User(BaseModel):
    is_employee: t.Optional[bool] = None
    subreddit: t.Optional[UserSubreddit] = None
    snoovatar_size: t.Optional[t.List[int]] = None
    awardee_karma: t.Optional[int] = None
    id: t.Optional[str] = None
    verified: t.Optional[bool] = None
    is_gold: t.Optional[bool] = None
    is_mod: t.Optional[bool] = None
    awarder_karma: t.Optional[int] = None
    has_verified_email: t.Optional[bool] = None
    icon_img: t.Optional[HttpUrl] = None
    hide_from_robots: t.Optional[bool] = None
    link_karma: t.Optional[int] = None
    is_blocked: t.Optional[bool] = None
    total_karma: t.Optional[int] = None
    pref_show_snoovatar: t.Optional[bool] = None
    name: t.Optional[str] = None
    created: t.Optional[float] = None
    created_utc: t.Optional[float] = None
    snoovatar_img: t.Optional[str] = None
    comment_karma: t.Optional[int] = None
    accept_followers: t.Optional[bool] = None
    has_subscribed: t.Optional[bool] = None
    is_suspended: t.Optional[bool] = None


class CommentContributionSettings(BaseModel):
    allowed_media_types: t.Optional[t.List[str]] = None


class ModeratedSubreddit(BaseModel):
    icon_img: t.Optional[str] = None
    display_name: str
    display_name_prefixed: str
    title: str
    url: str
    sr: str
    sr_display_name_prefixed: str
    created_utc: int
    key_color: str
    created: int
    mod_permissions: t.List
    over_18: bool
    subscribers: int
    community_icon: str
    icon_size: t.Optional[t.List[int]] = None
    banner_img: t.Optional[str] = None
    banner_size: t.Optional[t.List[int]] = None
    primary_color: str
    subreddit_type: str
    name: str


class Subreddit(BaseModel):
    submit_text_html: t.Optional[str] = None
    restrict_posting: t.Optional[bool] = None
    free_form_reports: t.Optional[bool] = None
    wiki_enabled: t.Optional[bool] = None
    display_name: str
    header_img: t.Optional[HttpUrl] = None
    title: str
    allow_galleries: t.Optional[bool] = None
    icon_size: t.Optional[t.List[int]] = None
    primary_color: t.Optional[str] = None
    active_user_count: t.Optional[int] = None
    icon_img: t.Optional[str] = None
    display_name_prefixed: str
    accounts_active: t.Optional[int] = None
    public_traffic: t.Optional[bool] = None
    subscribers: t.Optional[int] = None
    user_flair_richtext: t.List[dict]
    name: str
    quarantine: t.Optional[bool] = None
    hide_ads: t.Optional[bool] = None
    prediction_leaderboard_entry_type: t.Optional[int] = None
    emojis_enabled: bool
    advertiser_category: t.Optional[str] = None
    public_description: str
    comment_score_hide_mins: t.Optional[int] = None
    allow_predictions: bool
    community_icon: str
    banner_background_image: str
    original_content_tag_enabled: t.Optional[bool] = None
    community_reviewed: t.Optional[bool] = None
    submit_text: t.Optional[str] = None
    description_html: t.Optional[str] = None
    spoilers_enabled: t.Optional[bool] = None
    comment_contribution_settings: CommentContributionSettings
    allow_talks: bool
    header_size: t.Optional[t.List[int]] = None
    user_flair_position: t.Optional[str] = None
    all_original_content: t.Optional[bool] = None
    has_menu_widget: bool
    key_color: t.Optional[str] = None
    can_assign_user_flair: bool
    created: float
    wls: t.Optional[int] = None
    show_media_preview: t.Optional[bool] = None
    submission_type: t.Optional[str] = None
    allowed_media_in_comments: t.List[str]
    allow_videogifs: bool
    should_archive_posts: t.Optional[bool] = None
    user_flair_type: str
    allow_polls: t.Optional[bool] = None
    collapse_deleted_comments: t.Optional[bool] = None
    emojis_custom_size: t.Optional[t.List[int]] = None
    public_description_html: t.Optional[str] = None
    allow_videos: bool
    is_crosspostable_subreddit: bool
    should_show_media_in_comments_setting: bool
    can_assign_link_flair: bool
    accounts_active_is_fuzzed: t.Optional[bool] = None
    allow_prediction_contributors: bool
    submit_text_label: t.Optional[str] = None
    link_flair_position: t.Optional[str] = None
    user_flair_enabled_in_sr: t.Optional[bool] = None
    allow_discovery: t.Optional[bool] = None
    accept_followers: t.Optional[bool] = None
    user_sr_theme_enabled: t.Optional[bool] = None
    link_flair_enabled: t.Optional[bool] = None
    disable_contributor_requests: t.Optional[bool] = None
    subreddit_type: str
    banner_img: t.Optional[str] = None
    banner_background_color: t.Optional[str] = None
    show_media: t.Optional[bool] = None
    id: str
    over18: t.Optional[bool] = None
    header_title: t.Optional[str] = None
    description: t.Optional[str] = None
    submit_link_label: t.Optional[str] = None
    restrict_commenting: t.Optional[bool] = None
    allow_images: t.Optional[bool] = None
    lang: t.Optional[str] = None
    url: str
    created_utc: float
    banner_size: t.Optional[t.List[int]] = None
    mobile_banner_image: t.Optional[str] = None
    allow_predictions_tournament: bool


class WikiPage(BaseModel):
    content_md: str
    content_html: str
    may_revise: bool
    reason: t.Optional[str] = None
    revision_date: float
    revision_id: str
    revision_by: User
