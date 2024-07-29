from typing import Union

from .time_utils import timestamp_to_readable
from ..api import TIME_FORMAT

__all__ = [
    "parse_users",
    "parse_posts",
    "parse_subreddits",
    "parse_comments",
    "parse_wiki_page",
]


def parse_users(
    data: Union[list[dict], dict], time_format: TIME_FORMAT
) -> Union[list[dict], dict]:
    """
    Parses a list of/a single object of raw user data.

    :param data: A list of dict objects, each containing raw user data.
    :type data: list[dict]
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A list of parsed dict objects, each containing user data Or a dict object containing user data.
    :rtype: Union[list[dict], dict]

    Usage::

        >>> from knewkarma.tools import parsing_utils

        >>> # The raw user data could also be a list of object containing user data in the same format.
        >>> raw_user = {
        >>>                 "kind": "t2",
        >>>                 "data": {
        >>>                             "is_employee": False,
        >>>                             "is_friend": False,
        >>>                             "subreddit": {
        >>>                                             "default_set": True, ...
        >>> ...}

        >>> cleaned_user = parsing_utils.parse_users(data=raw_user, time_format = "locale")
    """

    def build_user(user: dict) -> dict:
        """
        Parses raw user data to get only the needed data.

        :param user: Raw user data.
        :type user: dict
        :return: A dict object containing parsed user data.
        :rtype: dict
        """
        return {
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
            "is_friend": user.get("is_friend"),
            "snoovatar_img": user.get("snoovatar_img"),
            "awarder_karma": user.get("awarder_karma"),
            "pref_show_snoovatar": user.get("pref_show_snoovatar"),
            "has_subscribed": user.get("has_subscribed"),
            "created": timestamp_to_readable(
                timestamp=user.get("created"), time_format=time_format
            ),
        }

    if isinstance(data, list) and len(data) != 0:
        converted_data = [build_user(user.get("data")) for user in data]

    elif isinstance(data, dict) and "is_employee" in data:
        converted_data = build_user(data)
    else:
        raise ValueError(
            f"Unknown data type ({data}: {type(data)}), expected a List[Dict] or Dict."
        )

    return converted_data


def parse_posts(
    data: Union[dict, list], time_format: TIME_FORMAT
) -> Union[list[dict], dict]:
    """
    Parses a list/single object of raw post data.

    :param data: A list of dict objects, each containing raw post data.
    :type data: list[dict]
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A list of parsed dict objects, each containing post data Or a dict object containing post data.
    :rtype: Union[list[dict], dict]

    Usage::

        >>> from knewkarma.tools import parsing_utils

        >>> # The raw post data could also be a list of object containing post data in the same format.
        >>> raw_post = {
        >>>                 "kind": "t3",
        >>>                 "data": {
        >>>                             "approved_at_utc": None,
        >>>                             "subreddit": "OnePiece",
        >>>                             "selftext": "**Chapter 1120** is out on...",
        >>>                             "author_fullname": "t2_6l4z3", ...
        >>> ...}

        >>> cleaned_post = parsing_utils.parse_posts(data=raw_post, time_format = "locale")
    """

    def build_post(post: dict) -> dict:
        """
        Parses raw post data to get only the needed data.

        :param post: Raw post data.
        :type post: dict
        :return: A dict object containing parsed post data.
        :rtype: dict
        """
        return {
            "author": post.get("author"),
            "title": post.get("title"),
            "body": post.get("selftext"),
            "id": post.get("id"),
            "subreddit": post.get("subreddit"),
            "subreddit_id": post.get("subreddit_id"),
            "subreddit_type": post.get("subreddit_type"),
            "subreddit_subscribers": post.get("subreddit_subscribers"),
            "upvotes": post.get("ups"),
            "upvote_ratio": post.get("upvote_ratio"),
            "downvotes": post.get("downs"),
            "thumbnail": post.get("thumbnail"),
            "gilded": post.get("gilded"),
            "is_video": post.get("is_video"),
            "is_nsfw": post.get("over_18"),
            "is_shareable": post.get("is_reddit_media_domain"),
            "is_robot_indexable": post.get("is_robot_indexable"),
            "permalink": post.get("permalink"),
            "is_locked": post.get("locked"),
            "is_archived": post.get("archived"),
            "domain": post.get("domain"),
            "score": post.get("score"),
            "comments": post.get("num_comments"),
            "saved": post.get("saved"),
            "clicked": post.get("clicked"),
            "hidden": post.get("hidden"),
            "pwls": post.get("pwls"),
            "hide_score": post.get("hide_score"),
            "num_crossposts": post.get("num_crossposts"),
            "parent_whitelist_status": post.get("parent_whitelist_status"),
            "name": post.get("name"),
            "quarantine": post.get("quarantine"),
            "link_flair_text_color": post.get("link_flair_text_color"),
            "is_original_content": post.get("is_original_content"),
            "can_mod_post": post.get("can_mod_post"),
            "is_created_from_ads_ui": post.get("is_created_from_ads_ui"),
            "author_premium": post.get("author_premium"),
            "is_self": post.get("is_self"),
            "link_flair_type": post.get("link_flair_type"),
            "wls": post.get("wls"),
            "author_flair_type": post.get("author_flair_type"),
            "allow_live_comments": post.get("allow_live_comments"),
            "no_follow": post.get("no_follow"),
            "is_crosspostable": post.get("is_crosspostable"),
            "pinned": post.get("pinned"),
            "author_is_blocked": post.get("author_is_blocked"),
            "link_flair_background_color": post.get("link_flair_background_color"),
            "author_fullname": post.get("author_fullname"),
            "whitelist_status": post.get("whitelist_status"),
            "edited": timestamp_to_readable(
                timestamp=post.get("edited"), time_format=time_format
            ),
            "url": post.get("url"),
            "created": timestamp_to_readable(
                timestamp=post.get("created"), time_format=time_format
            ),
        }

    if isinstance(data, dict):
        return build_post(post=data)
    elif isinstance(data, list):
        return [build_post(post.get("data")) for post in data if post.get("data")]
    else:
        raise ValueError(f"Unknown data type ({data}: {type(data)}), expected a Dict.")


def parse_comments(comments: list[dict], time_format: TIME_FORMAT) -> list[dict]:
    """
    Parses a list of raw comments data to get only the needed data in each item.

    :param comments: A list of dict objects, each containing raw comment data.
    :type comments: list[dict]
    :param time_format: Time format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A list of parsed dict objects, each containing comments data.
    :rtype: list[dict]

    Usage::

        >>> from knewkarma.tools import parsing_utils

        >>> # The raw comment data could also be a list of object containing comment data in the same format.
        >>> raw_comment = {
        >>>                 "kind": "t1",
        >>>                 "data": {
        >>>                             "subreddit_id": "t5_2ybb3",
        >>>                             "approved_at_utc": None,
        >>>                             "author_is_blocked": False,
        >>>                             "comment_type": None, ...
        >>> ...}

        >>> cleaned_comment = parsing_utils.parse_comments(data=raw_comment, time_format = "locale")
    """
    comments_list: list = []
    if isinstance(comments, list) and all(
        isinstance(comment, dict) for comment in comments
    ):
        for comment in comments:
            comment_data: dict = comment.get("data")
            comments_list.append(
                {
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

        return comments_list
    else:
        raise ValueError(
            f"Unknown data type ({comments}: {type(comments)}), expected a List[Dict]."
        )


def parse_subreddits(data: Union[list, dict], time_format) -> Union[list[dict], dict]:
    """
    Parses a list/single object of raw subreddits data.

    :param data: A list of dict objects, each containing raw subreddit data.
    :type data: list[dict]
    :param time_format: TIme format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A list of parsed dict objects, each containing subreddits data Or a dict object containing subreddit data.
    :rtype: Union[list[dict], dict]

    Usage::

        >>> from knewkarma.tools import parsing_utils

        >>> # The raw subreddit data could also be a list of object containing subreddit data in the same format.
        >>> raw_subreddit = {
        >>>                 "kind": "t5",
        >>>                 "data": {
        >>>                             "user_flair_background_color": None,
        >>>                             "submit_text_html": "&lt;...strong&gt;BEFORE YOU SUBMIT, &lt;a...",
        >>>                             "restrict_posting": True,
        >>>                             "free_form_reports": True, ...
        >>> ...}

        >>> cleaned_subreddit = parsing_utils.parse_subreddits(data=raw_subreddit, time_format = "locale")
    """

    def build_subreddit(
        subreddit: dict,
    ) -> dict:
        """
        Parses raw subreddit data to get only the needed data.

        :param subreddit: Raw subreddit data.
        :type subreddit: dict
        :return: A dict object containing parsed subreddit data.
        :rtype: dict
        """
        return {
            "title": subreddit.get("title"),
            "display_name": subreddit.get("display_name"),
            "id": subreddit.get("id"),
            "description": subreddit.get("public_description"),
            "submit_text": subreddit.get("submit_text"),
            "submit_text_html": subreddit.get("submit_text_html"),
            "icon": (
                subreddit.get("icon_img").split("?")[0]
                if subreddit.get("icon_img")
                else ""
            ),
            "type": subreddit.get("subreddit_type"),
            "subscribers": subreddit.get("subscribers"),
            "current_active_users": subreddit.get("accounts_active"),
            "is_nsfw": subreddit.get("over18"),
            "language": subreddit.get("lang"),
            "whitelist_status": subreddit.get("whitelist_status"),
            "url": subreddit.get("url"),
            "user_flair_position": subreddit.get("user_flair_position"),
            "spoilers_enabled": subreddit.get("spoilers_enabled"),
            "allow_galleries": subreddit.get("allow_galleries"),
            "show_media_preview": subreddit.get("show_media_preview"),
            "allow_videogifs": subreddit.get("allow_videogifs"),
            "allow_videos": subreddit.get("allow_videos"),
            "allow_images": subreddit.get("allow_images"),
            "allow_polls": subreddit.get("allow_polls"),
            "public_traffic": subreddit.get("public_traffic"),
            "description_html": subreddit.get("description_html"),
            "emojis_enabled": subreddit.get("emojis_enabled"),
            "primary_color": subreddit.get("primary_color"),
            "key_color": subreddit.get("key_color"),
            "banner_background_color": subreddit.get("banner_background_color"),
            "icon_size": subreddit.get("icon_size"),
            "header_size": subreddit.get("header_size"),
            "banner_size": subreddit.get("banner_size"),
            "link_flair_enabled": subreddit.get("link_flair_enabled"),
            "restrict_posting": subreddit.get("restrict_posting"),
            "restrict_commenting": subreddit.get("restrict_commenting"),
            "submission_type": subreddit.get("submission_type"),
            "free_form_reports": subreddit.get("free_form_reports"),
            "wiki_enabled": subreddit.get("wiki_enabled"),
            "community_icon": (
                subreddit.get("community_icon").split("?")[0]
                if subreddit.get("community_icon")
                else ""
            ),
            "banner_background_image": subreddit.get("banner_background_image"),
            "mobile_banner_image": subreddit.get("mobile_banner_image"),
            "allow_discovery": subreddit.get("allow_discovery"),
            "is_crosspostable_subreddit": subreddit.get("is_crosspostable_subreddit"),
            "notification_level": subreddit.get("notification_level"),
            "suggested_comment_sort": subreddit.get("suggested_comment_sort"),
            "disable_contributor_requests": subreddit.get(
                "disable_contributor_requests"
            ),
            "community_reviewed": subreddit.get("community_reviewed"),
            "original_content_tag_enabled": subreddit.get(
                "original_content_tag_enabled"
            ),
            "has_menu_widget": subreddit.get("has_menu_widget"),
            "videostream_links_count": subreddit.get("videostream_links_count"),
            "created": timestamp_to_readable(
                timestamp=subreddit.get("created"), time_format=time_format
            ),
        }

    if isinstance(data, list) and len(data) != 0:
        subreddit_data = [
            build_subreddit(subreddit=subreddit.get("data")) for subreddit in data
        ]
    elif isinstance(data, dict) and "subreddit_type" in data:
        subreddit_data = build_subreddit(subreddit=data)
    else:
        raise ValueError(
            f"Unknown data type ({data}: {type(data)}), expected a List[Dict] or Dict."
        )

    return subreddit_data


def parse_wiki_page(wiki_page: dict, time_format: TIME_FORMAT) -> dict:
    """
    Parses raw subreddit wiki page data to get only the needed data.

    :param wiki_page: Raw wiki page data.
    :type wiki_page: dict
    :param time_format: Time format for the parsed data.
    :type time_format: Literal[locale, concise]
    :return: A dict object of parsed wiki page data.
    :rtype: dict

    Usage::

        >>> from knewkarma.tools import parsing_utils

        >>> raw_wiki_page = {
        >>>                 "kind": "wikipage",
        >>>                 "data": {
        >>>                             "content_md": "[\u21e6 Index](https://www.reddit.com/r/OnePiece/wiki/index)...",
        >>>                             "revision_date": 1671478514,
        >>>                             "revision_by": {"kind": "t2", "data":...,
        >>>                             "revision_id": "42ab00c4-7fd4-11ed-9528-a6b541c5c78b", ...
        >>> ...}

        >>> cleaned_wiki_page = parsing_utils.parse_wiki_page(data=raw_wiki_page, time_format = "locale")
    """
    if isinstance(wiki_page, dict) and "revision_id" in wiki_page:
        user: dict = wiki_page.get("revision_by").get("data")

        return {
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
    else:
        raise ValueError(
            f"Unknown data type ({wiki_page}: {type(wiki_page)}), expected a Dict."
        )
