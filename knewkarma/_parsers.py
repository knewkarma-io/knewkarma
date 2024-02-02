# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from typing import Union

from ._coreutils import time_since
from .data import User, Post, Comment, Community, PreviewCommunity, WikiPage


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def parse_users(__data: Union[list[dict], dict]) -> Union[list[User], User]:
    """
    Parses raw user data into User objects.

    :param __data: User data in the form of a list of dictionaries or a single dictionary.
    :type __data: Union[list[dict], dict]
    :return: A single User object or list of User objects.
    :rtype: Union[list[User], User]
    """

    # ------------------------------------------------------------------------------- #

    def build_user(user: dict) -> User:
        """
        Helper function to create a User object from a dictionary.

        :param user: A dictionary containing user data.
        :return: A User object.
        """
        return User(
            name=user.get("name"),
            id=user.get("id"),
            icon_img=user.get("icon_img"),
            is_verified=user.get("verified"),
            has_verified_email=user.get("has_verified_email"),
            is_gold=user.get("is_gold"),
            is_mod=user.get("is_mod"),
            is_employee=user.get("is_employee"),
            is_blocked=user.get("is_blocked"),
            hidden_from_bots=user.get("hide_from_robots"),
            accepts_followers=user.get("accept_followers"),
            comment_karma=user.get("comment_karma"),
            link_karma=user.get("link_karma"),
            awardee_karma=user.get("awardee_karma"),
            total_karma=user.get("total_karma"),
            community=user.get("subreddit"),
            created=time_since(timestamp=user.get("created")),
            raw_data=user,
        )

    # ------------------------------------------------------------------------------- #

    if isinstance(__data, list) and len(__data) != 0:
        converted_data = [build_user(user.get("data")) for user in __data]

    elif isinstance(__data, dict) and "is_employee" in __data:
        converted_data = build_user(__data)
    else:
        raise ValueError(
            f"Unexpected data type {type(__data).__name__}. Expected {list} or {dict}"
        )

    return converted_data


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def parse_posts(data: Union[dict, list]) -> Union[Post, list[Post]]:
    """
    Parses raw post data into a Post object.

    :param data: Raw post data to parse.
    :type data: Union[dict, list]
    :rtype: Union[dict, list]
    """

    def build_post(post_data: dict) -> Post:
        return Post(
            title=post_data.get("title"),
            thumbnail=post_data.get("thumbnail"),
            id=post_data.get("id"),
            body=post_data.get("selftext"),
            author=post_data.get("author"),
            community=post_data.get("subreddit"),
            community_id=post_data.get("subreddit_id"),
            community_type=post_data.get("subreddit_type"),
            upvotes=post_data.get("ups"),
            upvote_ratio=post_data.get("upvote_ratio"),
            downvotes=post_data.get("downs"),
            gilded=post_data.get("gilded"),
            is_nsfw=post_data.get("over_18"),
            is_shareable=post_data.get("is_reddit_media_domain"),
            is_edited=post_data.get("edited"),
            comments=post_data.get("num_comments"),
            hide_from_bots=post_data.get("is_robot_indexable"),
            score=post_data.get("score"),
            domain=post_data.get("domain"),
            permalink=post_data.get("permalink"),
            is_locked=post_data.get("locked"),
            is_archived=post_data.get("archived"),
            created=time_since(timestamp=post_data.get("created")),
            raw_data=data,
        )

    if isinstance(data, dict):
        return build_post(post_data=data)

    elif isinstance(data, list):
        return [build_post(post.get("data")) for post in data if post.get("data")]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def parse_comments(comments: list[dict]) -> list[Comment]:
    """
    Parses raw comments data into a list of Comment objects.
    :param comments: A list of comment dictionaries to convert.
    :type comments: list[dict]
    :return: A list of Comment objects, each containing converted data about a comment.
    :rtype: list[Comment]
    """
    if len(comments) != 0:
        comments_list: list = []
        for comment in comments:
            comment_data: dict = comment.get("data")
            comments_list.append(
                Comment(
                    body=comment_data.get("body"),
                    id=comment_data.get("id"),
                    author=comment_data.get("author"),
                    author_is_premium=comment_data.get("author_premium"),
                    upvotes=comment_data.get("ups"),
                    downvotes=comment_data.get("downs"),
                    is_nsfw=comment_data.get("over_18"),
                    is_edited=comment_data.get("edited"),
                    score=comment_data.get("score"),
                    hidden_score=comment_data.get("score_hidden"),
                    gilded=comment_data.get("gilded"),
                    is_stickied=comment_data.get("stickied"),
                    is_locked=comment_data.get("locked"),
                    is_archived=comment_data.get("archived"),
                    created=time_since(timestamp=comment_data.get("created")),
                    community=comment_data.get("subreddit_name_prefixed"),
                    community_type=comment_data.get("subreddit_type"),
                    post_id=comment_data.get("link_id"),
                    post_title=comment_data.get("link_title", "NaN"),
                    raw_data=comment_data,
                )
            )

        return comments_list


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def parse_communities(
    __data: Union[list, dict], is_preview: bool = False
) -> Union[list[Union[Community, PreviewCommunity]], Community]:
    """
    Parses raw community data into Community objects.

    :param __data: Community data in the form of a list or a single dictionary.
    :type __data: Union[list, dict]
    :param is_preview: A boolean value to determine if the community is a preview.
    :type is_preview: bool
    :return: A single Community object or a list of Community objects.
    :rtype: Union[list[Community], Community]
    """

    # ------------------------------------------------------------------------------- #

    def build_community(
        community: dict,
    ) -> Union[Community, PreviewCommunity]:
        """
        Helper function to build a Community or PreviewCommunity object from a dictionary.

        :param community: A dictionary containing community data.
        :type community: dict
        :return: A Community or PreviewCommunity object.
        :rtype: Union[Community, PreviewCommunity]
        """
        if is_preview:
            community_obj = PreviewCommunity(
                name=community.get("display_name"),
                icon=community.get("community_icon").split("?")[0],
                community_type=community.get("subreddit_type"),
                subscribers=community.get("subscribers"),
                whitelist_status=community.get("whitelist_status"),
                url=community.get("url"),
                created=time_since(timestamp=community.get("created")),
                raw_data=community,
            )
        else:
            community_obj = Community(
                name=community.get("display_name"),
                id=community.get("id"),
                description=community.get("public_description"),
                submit_text=community.get("submit_text"),
                icon=community.get("community_icon").split("?")[0],
                community_type=community.get("subreddit_type"),
                subscribers=community.get("subscribers"),
                current_active_users=community.get("accounts_active"),
                is_nsfw=community.get("over18"),
                language=community.get("lang"),
                whitelist_status=community.get("whitelist_status"),
                url=community.get("url"),
                created=time_since(timestamp=community.get("created")),
                raw_data=community,
            )

        return community_obj

    # ------------------------------------------------------------------------------- #

    if isinstance(__data, list) and len(__data) != 0:
        community_data = [build_community(community=community) for community in __data]

    elif isinstance(__data, dict) and "subreddit_type" in __data:
        community_data = build_community(community=__data)
    else:
        raise ValueError(
            f"Unexpected data type {type(__data).__name__}. Expected {list} or {dict}"
        )

    return community_data


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def parse_community_wiki_page(wiki_page: dict) -> WikiPage:
    """
    Parses raw community wiki page data into a WikiPage object.

    :param wiki_page: Raw wiki page data to be converted.
    :type wiki_page: dict
    :return: A WikiPage object.
    :rtype: WikiPage
    """
    if "revision_id" in wiki_page:
        page_data: dict = wiki_page.get("data")
        user: dict = page_data.get("revision_by").get("data")

        return WikiPage(
            revision_id=page_data.get("revision_id"),
            revision_date=time_since(timestamp=page_data.get("revision_date")),
            content_markdown=page_data.get("content_md"),
            revised_by=User(
                name=user.get("name"),
                id=user.get("id"),
                icon_img=user.get("icon_img"),
                is_verified=user.get("verified"),
                has_verified_email=user.get("has_verified_email"),
                is_gold=user.get("is_gold"),
                is_mod=user.get("is_mod"),
                is_employee=user.get("is_employee"),
                is_blocked=user.get("is_blocked"),
                hidden_from_bots=user.get("hide_from_robots"),
                accepts_followers=user.get("accept_followers"),
                comment_karma=user.get("comment_karma"),
                link_karma=user.get("link_karma"),
                awardee_karma=user.get("awardee_karma"),
                total_karma=user.get("total_karma"),
                community=user.get("subreddit"),
                created=time_since(timestamp=user.get("created")),
                raw_data=user,
            ),
            raw_data=page_data,
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
