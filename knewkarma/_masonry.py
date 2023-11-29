# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from datetime import datetime
from typing import Union

from rich import print as xprint
from rich.text import Text
from rich.tree import Tree

from . import Api
from ._coreutils import convert_timestamp_to_datetime, data_broker, save_data, log


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class Masonry:
    def __init__(self, api: Api):
        """
        Initialises the Masonry class responsible for visualising API data into tree structures.

        :param api: API object from which data will be retrieved.
        """

        self._api = api

        # Tree/Branch styling
        self.DIM = "dim"
        self.BOLD = "bold"
        self.ITALIC = "italic"
        self.BOLD_BLUE = "bold blue"
        self.BOLD_BRIGHT_BLUE = "bold bright_blue"

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def create_tree(
        self,
        tree_title: str,
        tree_data: Union[dict, list] = None,
        additional_text: str = None,
        additional_data: [(str, Union[dict, list])] = None,
    ) -> Tree:
        """
        Creates a tree structure and populates it with the given data.

        :param tree_title: Title of the tree.
        :param tree_data: Data to populate the tree with.
        :param additional_text: Additional text to add at the end of the tree.
        :param additional_data: A list of tuples containing additional data such that should be added to the tree.
           Data format: ("title" [str], data [dict or list])
        :returns: A populated or emtpy tree structure.
        """
        if not tree_data:
            return Tree(tree_title, style=self.BOLD, guide_style=self.BOLD_BRIGHT_BLUE)

        tree: Tree = Tree(
            tree_title, style=self.BOLD, guide_style=self.BOLD_BRIGHT_BLUE
        )
        data_types: list = [dict, list]
        if type(tree_data) in data_types:
            if isinstance(tree_data, dict):
                for data_key, data_value in tree_data.items():
                    tree.add(f"{data_key}: {data_value}", style=self.DIM)
            else:
                for count, item in enumerate(tree_data, start=1):
                    tree.add(f"{count}: {item}", style=self.DIM)

            if additional_data:
                for title, branch_data in additional_data:
                    if type(branch_data) in data_types:
                        if isinstance(branch_data, dict):
                            self.add_branch(
                                target_tree=tree,
                                branch_title=title,
                                branch_data=branch_data,
                            )
                        else:
                            for item in branch_data:
                                self.add_branch(
                                    target_tree=tree,
                                    branch_title=title,
                                    branch_data=item,
                                )

            if additional_text:
                tree.add(Text(additional_text), style=self.ITALIC)

        return tree

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def add_branch(
        self,
        target_tree: Tree,
        branch_title: str,
        branch_data: Union[dict, list],
        additional_text: str = None,
    ):
        """
        Adds a branch to an existing tree.

        This is a utility method for adding detailed branches
        to a tree created using the create_tree method.

        :param target_tree: The tree to which the branch will be added.
        :param branch_title: Title of the branch.
        :param branch_data: Data for the branch, either a dict or a list.
        :param additional_text: Additional text to be appended at the end of the branch.
        :returns: The updated tree with the new branch.
        """
        data_types: list = [dict, list]
        if type(branch_data) in data_types:
            branch: Tree = target_tree.add(branch_title, guide_style=self.BOLD_BLUE)
            if isinstance(branch_data, dict):
                for data_key, data_value in branch_data.items():
                    branch.add(f"{data_key}: {data_value}", style=self.DIM)
            else:
                for count, item in enumerate(branch_data, start=1):
                    branch.add(f"{count}. {item}")

            if additional_text:
                branch.add(Text(additional_text), style=self.ITALIC)

            return target_tree

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    async def profile_tree(
        self,
        profile_source: str,
        profile_type: str,
        save_to_json: bool = False,
        save_to_csv: bool = False,
    ):
        profile_data: dict = await self._api.get_profile(
            profile_type=profile_type, profile_source=profile_source
        )

        if profile_data:
            if profile_type == "user_profile":
                formatted_profile: dict = data_broker(
                    api_data=profile_data, data_file="user/profile.json"
                )
                additional_data: list = [
                    (
                        profile_data.get("subreddit").get("display_name"),
                        data_broker(
                            profile_data.get("subreddit"),
                            data_file="user/subreddit.json",
                        ),
                    ),
                    (
                        "Verification",
                        data_broker(profile_data, data_file="user/verification.json"),
                    ),
                    (
                        "Snoovatar",
                        data_broker(profile_data, data_file="user/snoovatar.json"),
                    ),
                    (
                        "Karma",
                        data_broker(profile_data, data_file="user/karma.json"),
                    ),
                ]
            else:
                formatted_profile: dict = data_broker(
                    api_data=profile_data, data_file="subreddit/profile.json"
                )

                additional_data: list = [
                    (
                        "Allows",
                        data_broker(
                            api_data=profile_data, data_file="subreddit/allows.json"
                        ),
                    ),
                    (
                        "Banner",
                        data_broker(
                            api_data=profile_data, data_file="subreddit/banner.json"
                        ),
                    ),
                    (
                        "Header",
                        data_broker(
                            api_data=profile_data, data_file="subreddit/header.json"
                        ),
                    ),
                    (
                        "Flairs",
                        data_broker(
                            api_data=profile_data, data_file="subreddit/flairs.json"
                        ),
                    ),
                ]

            xprint(
                self.create_tree(
                    tree_title=profile_data.get("public_description")
                    if profile_type == "subreddit_profile"
                    else profile_data.get("subreddit").get("title"),
                    tree_data=formatted_profile,
                    additional_data=additional_data,
                    additional_text=profile_data.get("submit_text")
                    if profile_type == "subreddit_profile"
                    else None,
                )
            )

            save_data(
                data=profile_data,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{profile_source}_{profile_type.upper()}",
            )

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    async def post_data_tree(
        self,
        post_id: str,
        post_subreddit: str,
        comments_limit: int,
        comments_sort: str,
        save_to_json: bool,
    ):
        (raw_data, post_data, comments_list) = await self._api.get_post_data(
            post_id=post_id,
            subreddit=post_subreddit,
            comments_sort=comments_sort,
            comments_limit=comments_limit,
        )

        if post_data:
            post_tree: Tree = self.create_tree(
                tree_title=f"{post_data.get('title')} | by {post_data.get('author')}",
                tree_data=data_broker(
                    api_data=post_data, data_file="post/profile.json"
                ),
                additional_text=post_data.get("selftext"),
            )

            if comments_list:
                comments_branch: Tree = post_tree.add("Comments")

                # Remove last item from the list
                # (because it does not contain any comment data... trust me, I know😂)
                comments_list.pop()
                for comment in comments_list:
                    comment_data: dict = comment.get("data")
                    self.add_branch(
                        target_tree=comments_branch,
                        branch_title=convert_timestamp_to_datetime(
                            timestamp=comment_data.get("created")
                        ),
                        branch_data=data_broker(
                            api_data=comment_data,
                            data_file="shared/comment.json",
                        ),
                        additional_text=comment_data.get("body"),
                    )

            xprint(post_tree)
            save_data(
                data=raw_data,
                save_to_json=save_to_json,
                filename=f"{post_data.get('id')}_POST_DATA",
            )

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    async def posts_tree(
        self,
        sorted_by: str,
        limited_to: int,
        posts_type: str,
        save_to_json: bool = False,
        posts_source: str = None,
        show_author: bool = False,
    ):
        posts_list: list = await self._api.get_posts(
            sorted_by=sorted_by,
            limited_to=limited_to,
            posts_type=posts_type,
            posts_source=posts_source,
        )

        if posts_list:
            posts_tree: Tree = self.create_tree(
                tree_title=f"{limited_to} {posts_type} - {datetime.now()}"
            )

            for post in posts_list:
                # Set branch title to show the post author's username if the show_author is True.
                if show_author:
                    branch_title: str = (
                        f"{convert_timestamp_to_datetime(post.get('data').get('created'))} | by"
                        f" u/{post.get('data').get('author')}: {post.get('data').get('title')}"
                    )
                else:
                    # Otherwise, set the title of the branch to the title of the post.
                    branch_title: str = (
                        f"{convert_timestamp_to_datetime(post.get('data').get('created'))}: "
                        f"{post.get('data').get('title')}"
                    )

                self.add_branch(
                    branch_title=branch_title,
                    target_tree=posts_tree,
                    branch_data=data_broker(
                        api_data=post.get("data"), data_file="post/profile.json"
                    ),
                    additional_text=post.get("data").get("selftext"),
                )

            xprint(posts_tree)
            save_data(
                data=posts_list,
                save_to_json=save_to_json,
                filename=f"{posts_source}_{posts_type.upper()}",
            )
        else:
            log.info(f"No '{posts_type}' found for '{posts_source}'.")

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    async def user_comments_tree(
        self,
        username: str,
        sorted_by: str,
        limited_to: int,
        save_to_json: bool,
    ):
        comments_list: list = await self._api.get_posts(
            sorted_by=sorted_by,
            limited_to=limited_to,
            posts_type="user_comments",
            posts_source=username,
        )

        if comments_list:
            comments_tree: Tree = self.create_tree(
                tree_title=f"{username}'s {sorted_by} {limited_to} comments"
            )

            for comment in comments_list:
                raw_comment_data: dict = comment.get("data")
                self.add_branch(
                    target_tree=comments_tree,
                    branch_title=convert_timestamp_to_datetime(
                        timestamp=raw_comment_data.get("created")
                    ),
                    branch_data=data_broker(
                        api_data=raw_comment_data, data_file="shared/comment.json"
                    ),
                    additional_text=raw_comment_data.get("body"),
                )

            xprint(comments_tree)
            save_data(
                data=comments_list,
                save_to_json=save_to_json,
                filename=f"{username}_COMMENTS",
            )
        else:
            log.info(f"No comments found for user '{username}'")

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #