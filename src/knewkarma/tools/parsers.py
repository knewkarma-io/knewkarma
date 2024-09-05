from types import SimpleNamespace
from typing import Union

from .terminal import Notify
from .timing import timestamp_to_readable
from ..api import TIME_FORMAT

__all__ = [
    "parse_users",
    "parse_posts",
    "parse_subreddits",
    "parse_comments",
    "parse_wiki_page",
]

notify = Notify


def parse_comments(
    raw_comments: Union[list[dict], dict], time_format: TIME_FORMAT
) -> Union[list[SimpleNamespace], SimpleNamespace]:
    """
    Parses raw Reddit comments data and returns a simplified format.

    :param raw_comments: A list of dictionaries, each representing raw comment data, or a single dictionary.
    :type raw_comments: Union[list[dict], dict]
    :param time_format: Specifies the time format to use in the output, e.g., 'locale' or 'concise'.
    :type time_format: TIME_FORMAT
    :return: Parsed comments data as a list of SimpleNamespace objects if the input is a list,
       or a single SimpleNamespace object if the input is a dictionary.
    :rtype: Union[list[SimpleNamespace], SimpleNamespace]
    """

    def build_comment(comment_data: dict) -> SimpleNamespace:
        """
        Parses a single raw comment dictionary and returns it in a simplified format.

        :param comment_data: A dictionary containing raw data for a single Reddit comment.
        :type comment_data: dict
        :return: A SimpleNamespace object containing parsed comment data.
        :rtype: SimpleNamespace
        """
        return SimpleNamespace(
            **{
                "body": comment_data.get("body"),
                "id": comment_data.get("id"),
                "author": comment_data.get("author"),
                "author_is_premium": comment_data.get("author_premium"),
                "upvotes": comment_data.get("ups"),
                "downvotes": comment_data.get("downs"),
                "subreddit": comment_data.get("subreddit_name_prefixed"),
                "subreddit_type": comment_data.get("subreddit_type"),
                "post_id": comment_data.get("link_id"),
                "post_title": comment_data.get("link_title"),
                "is_nsfw": comment_data.get("over_18"),
                "is_edited": comment_data.get("edited"),
                "score": comment_data.get("score"),
                "hidden_score": comment_data.get("score_hidden"),
                "gilded": comment_data.get("gilded"),
                "is_stickied": comment_data.get("stickied"),
                "is_locked": comment_data.get("locked"),
                "is_archived": comment_data.get("archived"),
                "subreddit_id": comment_data.get("subreddit_id"),
                "author_is_blocked": comment_data.get("author_is_blocked"),
                "link_author": comment_data.get("link_author"),
                "replies": comment_data.get("replies"),
                "saved": comment_data.get("saved"),
                "can_mod_post": comment_data.get("can_mod_post"),
                "send_replies": comment_data.get("send_replies"),
                "parent_id": comment_data.get("parent_id"),
                "author_fullname": comment_data.get("author_fullname"),
                "controversiality": comment_data.get("controversiality"),
                "body_html": comment_data.get("body_html"),
                "link_permalink": comment_data.get("link_permalink"),
                "name": comment_data.get("name"),
                "treatment_tags": comment_data.get("treatment_tags"),
                "awarders": comment_data.get("awarders"),
                "all_awardings": comment_data.get("all_awardings"),
                "quarantine": comment_data.get("quarantine"),
                "link_url": comment_data.get("link_url"),
                "created": timestamp_to_readable(
                    timestamp=comment_data.get("created"),
                    time_format=time_format,
                ),
            }
        )

    if isinstance(raw_comments, list) and len(raw_comments) != 0:
        return [
            build_comment(comment_data=comment.get("data")) for comment in raw_comments
        ]
    elif isinstance(raw_comments, dict):
        return build_comment(comment_data=raw_comments)
    else:
        notify.raise_exception(
            TypeError,
            f"Unexpected data type ({raw_comments}: {type(raw_comments)}). Expected list[dict]",
        )


def parse_posts(
    raw_posts: Union[dict, list], time_format: TIME_FORMAT
) -> Union[list[SimpleNamespace], SimpleNamespace]:
    """
    Parses raw Reddit posts data and returns a simplified format.

    :param raw_posts: A list of dictionaries, each representing raw post data, or a single dictionary.
    :type raw_posts: Union[list[dict], dict]
    :param time_format: Specifies the time format to use in the output, e.g., 'locale' or 'concise'.
    :type time_format: TIME_FORMAT
    :return: Parsed post data as a list of SimpleNamespace objects if the input is a list, or a single SimpleNamespace object if the input is a dictionary.
    :rtype: Union[list[SimpleNamespace], SimpleNamespace]
    """

    def build_post(post_data: dict) -> SimpleNamespace:
        """
        Parses a single raw post dictionary and returns it in a simplified format.

        :param post_data: A dictionary containing raw data for a single Reddit post.
        :type post_data: dict
        :return: A SimpleNamespace object containing parsed post data.
        :rtype: SimpleNamespace
        """
        return SimpleNamespace(
            **{
                "author": post_data.get("author"),
                "title": post_data.get("title"),
                "body": post_data.get("selftext"),
                "id": post_data.get("id"),
                "subreddit": post_data.get("subreddit"),
                "subreddit_id": post_data.get("subreddit_id"),
                "subreddit_type": post_data.get("subreddit_type"),
                "subreddit_subscribers": post_data.get("subreddit_subscribers"),
                "upvotes": post_data.get("ups"),
                "upvote_ratio": post_data.get("upvote_ratio"),
                "downvotes": post_data.get("downs"),
                "thumbnail": post_data.get("thumbnail"),
                "gilded": post_data.get("gilded"),
                "is_video": post_data.get("is_video"),
                "is_nsfw": post_data.get("over_18"),
                "is_shareable": post_data.get("is_reddit_media_domain"),
                "is_robot_indexable": post_data.get("is_robot_indexable"),
                "permalink": post_data.get("permalink"),
                "is_locked": post_data.get("locked"),
                "is_archived": post_data.get("archived"),
                "domain": post_data.get("domain"),
                "score": post_data.get("score"),
                "comments": post_data.get("num_comments"),
                "saved": post_data.get("saved"),
                "clicked": post_data.get("clicked"),
                "hidden": post_data.get("hidden"),
                "pwls": post_data.get("pwls"),
                "hide_score": post_data.get("hide_score"),
                "num_crossposts": post_data.get("num_crossposts"),
                "parent_whitelist_status": post_data.get("parent_whitelist_status"),
                "name": post_data.get("name"),
                "quarantine": post_data.get("quarantine"),
                "link_flair_text_color": post_data.get("link_flair_text_color"),
                "is_original_content": post_data.get("is_original_content"),
                "can_mod_post": post_data.get("can_mod_post"),
                "is_created_from_ads_ui": post_data.get("is_created_from_ads_ui"),
                "author_premium": post_data.get("author_premium"),
                "is_self": post_data.get("is_self"),
                "link_flair_type": post_data.get("link_flair_type"),
                "wls": post_data.get("wls"),
                "author_flair_type": post_data.get("author_flair_type"),
                "allow_live_comments": post_data.get("allow_live_comments"),
                "no_follow": post_data.get("no_follow"),
                "is_crosspostable": post_data.get("is_crosspostable"),
                "pinned": post_data.get("pinned"),
                "author_is_blocked": post_data.get("author_is_blocked"),
                "link_flair_background_color": post_data.get(
                    "link_flair_background_color"
                ),
                "author_fullname": post_data.get("author_fullname"),
                "whitelist_status": post_data.get("whitelist_status"),
                "edited": timestamp_to_readable(
                    timestamp=post_data.get("edited"), time_format=time_format
                ),
                "url": post_data.get("url"),
                "created": timestamp_to_readable(
                    timestamp=post_data.get("created"), time_format=time_format
                ),
            }
        )

    if isinstance(raw_posts, list):
        return [
            build_post(post_data=post.get("data"))
            for post in raw_posts
            if post.get("data")
        ]
    elif isinstance(raw_posts, dict):
        return build_post(post_data=raw_posts)
    else:
        notify.raise_exception(
            TypeError,
            f"Unexpected data type ({raw_posts}: {type(raw_posts)}). Expected dict",
        )


def parse_subreddits(
    raw_subreddits: Union[list[dict], dict], time_format: TIME_FORMAT
) -> Union[list[SimpleNamespace], SimpleNamespace]:
    """
    Parses raw Reddit subreddits data and returns a simplified format.

    :param raw_subreddits: A list of dictionaries, each representing raw subreddit data, or a single dictionary.
    :type raw_subreddits: Union[list[dict], dict]
    :param time_format: Specifies the time format to use in the output, e.g., 'locale' or 'concise'.
    :type time_format: TIME_FORMAT
    :return: Parsed subreddit data as a list of SimpleNamespace objects if the input is a list, or a single SimpleNamespace object if the input is a dictionary.
    :rtype: Union[list[SimpleNamespace], SimpleNamespace]
    """

    def build_subreddit(subreddit_data: dict) -> SimpleNamespace:
        """
        Parses a single raw subreddit dictionary and returns it in a simplified format.

        :param subreddit_data: A dictionary containing raw data for a single subreddit.
        :type subreddit_data: dict
        :return: A SimpleNamespace object containing parsed subreddit data.
        :rtype: SimpleNamespace
        """
        return SimpleNamespace(
            **{
                "title": subreddit_data.get("title"),
                "display_name": subreddit_data.get("display_name"),
                "id": subreddit_data.get("id"),
                "description": subreddit_data.get("public_description"),
                "submit_text": subreddit_data.get("submit_text"),
                "submit_text_html": subreddit_data.get("submit_text_html"),
                "icon": (
                    subreddit_data.get("icon_img").split("?")[0]
                    if subreddit_data.get("icon_img")
                    else ""
                ),
                "type": subreddit_data.get("subreddit_type"),
                "subscribers": subreddit_data.get("subscribers"),
                "current_active_users": subreddit_data.get("accounts_active"),
                "is_nsfw": subreddit_data.get("over18"),
                "language": subreddit_data.get("lang"),
                "whitelist_status": subreddit_data.get("whitelist_status"),
                "url": subreddit_data.get("url"),
                "user_flair_position": subreddit_data.get("user_flair_position"),
                "spoilers_enabled": subreddit_data.get("spoilers_enabled"),
                "allow_galleries": subreddit_data.get("allow_galleries"),
                "show_media_preview": subreddit_data.get("show_media_preview"),
                "allow_videogifs": subreddit_data.get("allow_videogifs"),
                "allow_videos": subreddit_data.get("allow_videos"),
                "allow_images": subreddit_data.get("allow_images"),
                "allow_polls": subreddit_data.get("allow_polls"),
                "public_traffic": subreddit_data.get("public_traffic"),
                "description_html": subreddit_data.get("description_html"),
                "emojis_enabled": subreddit_data.get("emojis_enabled"),
                "primary_color": subreddit_data.get("primary_color"),
                "key_color": subreddit_data.get("key_color"),
                "banner_background_color": subreddit_data.get(
                    "banner_background_color"
                ),
                "icon_size": subreddit_data.get("icon_size"),
                "header_size": subreddit_data.get("header_size"),
                "banner_size": subreddit_data.get("banner_size"),
                "link_flair_enabled": subreddit_data.get("link_flair_enabled"),
                "restrict_posting": subreddit_data.get("restrict_posting"),
                "restrict_commenting": subreddit_data.get("restrict_commenting"),
                "submission_type": subreddit_data.get("submission_type"),
                "free_form_reports": subreddit_data.get("free_form_reports"),
                "wiki_enabled": subreddit_data.get("wiki_enabled"),
                "community_icon": (
                    subreddit_data.get("community_icon").split("?")[0]
                    if subreddit_data.get("community_icon")
                    else ""
                ),
                "banner_background_image": subreddit_data.get(
                    "banner_background_image"
                ),
                "mobile_banner_image": subreddit_data.get("mobile_banner_image"),
                "allow_discovery": subreddit_data.get("allow_discovery"),
                "is_crosspostable_subreddit": subreddit_data.get(
                    "is_crosspostable_subreddit"
                ),
                "notification_level": subreddit_data.get("notification_level"),
                "suggested_comment_sort": subreddit_data.get("suggested_comment_sort"),
                "disable_contributor_requests": subreddit_data.get(
                    "disable_contributor_requests"
                ),
                "community_reviewed": subreddit_data.get("community_reviewed"),
                "original_content_tag_enabled": subreddit_data.get(
                    "original_content_tag_enabled"
                ),
                "has_menu_widget": subreddit_data.get("has_menu_widget"),
                "videostream_links_count": subreddit_data.get(
                    "videostream_links_count"
                ),
                "created": timestamp_to_readable(
                    timestamp=subreddit_data.get("created"), time_format=time_format
                ),
            }
        )

    if isinstance(raw_subreddits, list) and len(raw_subreddits) != 0:
        return [
            build_subreddit(subreddit_data=subreddit.get("data"))
            for subreddit in raw_subreddits
        ]
    elif isinstance(raw_subreddits, dict) and "subreddit_type" in raw_subreddits:
        return build_subreddit(subreddit_data=raw_subreddits)
    else:
        notify.raise_exception(
            TypeError,
            f"Unexpected data type ({raw_subreddits}: {type(raw_subreddits)}). Expected list[dict] | dict",
        )


def parse_wiki_page(wiki_page: dict, time_format: TIME_FORMAT) -> SimpleNamespace:
    """
    Parses raw Reddit wiki page data and returns a simplified format.

    :param wiki_page: A dictionary representing raw wiki page data.
    :type wiki_page: dict
    :param time_format: Specifies the time format to use in the output, e.g., 'locale' or 'concise'.
    :type time_format: TIME_FORMAT
    :return: Parsed wiki page data as a SimpleNamespace object.
    :rtype: SimpleNamespace
    """
    if isinstance(wiki_page, dict) and "revision_id" in wiki_page:
        user: dict = wiki_page.get("revision_by").get("data")

        return SimpleNamespace(
            **{
                "revision_id": wiki_page.get("revision_id"),
                "revision_date": timestamp_to_readable(
                    timestamp=wiki_page.get("revision_date"), time_format=time_format
                ),
                "content_markdown": wiki_page.get("content_md"),
                "revised_by": {
                    "name": user.get("name"),
                    "id": user.get("id"),
                    "avatar_url": user.get("icon_img"),
                    "is_verified": user.get("verified"),
                    "has_verified_email": user.get("has_verified_email"),
                    "is_gold": user.get("is_gold"),
                    "is_mod": user.get("is_mod"),
                    "is_blocked": user.get("is_blocked"),
                    "is_employee": user.get("is_employee"),
                    "hidden_from_bots": user.get("hide_from_robots"),
                    "accepts_followers": user.get("accept_followers"),
                    "comment_karma": user.get("comment_karma"),
                    "link_karma": user.get("link_karma"),
                    "awardee_karma": user.get("awardee_karma"),
                    "total_karma": user.get("total_karma"),
                    "subreddit": user.get("subreddit"),
                },
                "kind": wiki_page.get("kind"),
                "may_revise": wiki_page.get("may_revise"),
                "reason": wiki_page.get("reason"),
                "content_html": wiki_page.get("content_html"),
                "created": timestamp_to_readable(
                    timestamp=user.get("created"), time_format=time_format
                ),
            }
        )
    else:
        notify.raise_exception(
            TypeError,
            f"Unexpected data type ({wiki_page}: {type(wiki_page)}). Expected dict",
        )


def parse_users(
    raw_users: Union[list[dict], dict], time_format: TIME_FORMAT
) -> Union[list[SimpleNamespace], SimpleNamespace]:
    """
    Parses raw Reddit user data and returns a simplified format.

    :param raw_users: A list of dictionaries, each representing raw user data, or a single dictionary.
    :type raw_users: Union[list[dict], dict]
    :param time_format: Specifies the time format to use in the output, e.g., 'locale' or 'concise'.
    :type time_format: TIME_FORMAT
    :return: Parsed user data as a list of SimpleNamespace objects if the input is a list, or a single SimpleNamespace object if the input is a dictionary.
    :rtype: Union[list[SimpleNamespace], SimpleNamespace]
    """

    def build_user(user_data: dict) -> SimpleNamespace:
        """
        Parses a single raw user dictionary and returns it in a simplified format.

        :param user_data: A dictionary containing raw data for a single Reddit user.
        :type user_data: dict
        :return: A SimpleNamespace object containing parsed user data.
        :rtype: SimpleNamespace
        """
        return SimpleNamespace(
            **{
                "name": user_data.get("name"),
                "id": user_data.get("id"),
                "avatar_url": user_data.get("icon_img"),
                "is_verified": user_data.get("verified"),
                "has_verified_email": user_data.get("has_verified_email"),
                "is_gold": user_data.get("is_gold"),
                "is_mod": user_data.get("is_mod"),
                "is_blocked": user_data.get("is_blocked"),
                "is_employee": user_data.get("is_employee"),
                "hidden_from_bots": user_data.get("hide_from_robots"),
                "accepts_followers": user_data.get("accept_followers"),
                "comment_karma": user_data.get("comment_karma"),
                "link_karma": user_data.get("link_karma"),
                "awardee_karma": user_data.get("awardee_karma"),
                "total_karma": user_data.get("total_karma"),
                "subreddit": user_data.get("subreddit"),
                "is_friend": user_data.get("is_friend"),
                "snoovatar_img": user_data.get("snoovatar_img"),
                "awarder_karma": user_data.get("awarder_karma"),
                "pref_show_snoovatar": user_data.get("pref_show_snoovatar"),
                "has_subscribed": user_data.get("has_subscribed"),
                "created": timestamp_to_readable(
                    timestamp=user_data.get("created"), time_format=time_format
                ),
            }
        )

    if isinstance(raw_users, list) and len(raw_users) != 0:
        return [build_user(user_data=user.get("data")) for user in raw_users]

    elif isinstance(raw_users, dict) and "is_employee" in raw_users:
        return build_user(user_data=raw_users)
    else:
        notify.raise_exception(
            TypeError,
            f"Unexpected data type ({raw_users}: {type(raw_users)}). Expected list[dict] | dict",
        )


# -------------------------------- END ----------------------------------------- #
