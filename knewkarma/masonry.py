from datetime import datetime
from typing import Union

from rich import print
from rich.text import Text
from rich.tree import Tree

from .coreutils import convert_timestamp_to_datetime, save_data


class Masonry:
    def __init__(self):
        from .api import Api
        from .brokers import Broker

        self.api = Api(
            base_reddit_endpoint="https://www.reddit.com",
            base_github_api_endpoint="https://api.github.com",
        )
        self.data_broker = Broker()

    def create_tree(
        self,
        tree_title: str,
        tree_data: Union[dict, list] = None,
        additional_text: str = None,
        additional_data: [(str, Union[dict, list])] = None,
    ) -> Tree:
        """
        Creates a tree structure  and populates it with the given data.

        :param tree_title: Title of the tree.
        :param tree_data: Data to populate the tree with.
        :param additional_text: Additional text to add at the end of the tree.
        :param additional_data: A list of tuples containing additional data such that should be added to the tree.
           Data format: ("title" [str], data [dict or list])
        :returns: A populated or emtpy tree structure.
        """
        if not tree_data:
            return Tree(tree_title, style="bold", guide_style="bold bright_blue")

        tree = Tree(tree_title, style="bold", guide_style="bold bright_blue")
        data_types = [dict, list]
        if type(tree_data) in data_types:
            if isinstance(tree_data, dict):
                for data_key, data_value in tree_data.items():
                    tree.add(f"{data_key}: {data_value}", style="dim")
            else:
                for count, item in enumerate(tree_data, start=1):
                    tree.add(f"{count}: {item}", style="dim")

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
                tree.add(Text(additional_text), style="italic")

        return tree

    @staticmethod
    def add_branch(
        target_tree: Tree,
        branch_title: str,
        branch_data: Union[dict, list],
        additional_text: str = None,
    ):
        """
        Populates a branch with the given data and adds it to the specified tree.

        :param target_tree: The existing Tree to add the branch to.
        :param branch_title: The title for the new branch.
        :param branch_data: The data for the new branch in dictionary format.
        :param additional_text: Additional text to add at the end of the tree.
        :returns: A populated branch.
        """
        data_types = [dict, list]
        if type(branch_data) in data_types:
            branch = target_tree.add(branch_title, guide_style="bold blue")
            if isinstance(branch_data, dict):
                for data_key, data_value in branch_data.items():
                    branch.add(f"{data_key}: {data_value}", style="dim")
            else:
                for count, item in enumerate(branch_data, start=1):
                    branch.add(f"{count}. {item}")

            if additional_text:
                branch.add(Text(additional_text), style="italic")

            return target_tree

    def profile_tree(
        self,
        profile_source: str,
        profile_type: str,
        save_to_json: bool = False,
        save_to_csv: bool = False,
    ):
        raw_profile = self.api.get_profile(
            profile_type=profile_type, profile_source=profile_source
        )
        if raw_profile:
            if profile_type == "user_profile":
                # Separate the profile data in categories
                brokered_profile = self.data_broker.user_data(raw_data=raw_profile)
                additional_data = [
                    (
                        raw_profile.get("subreddit").get("display_name"),
                        brokered_profile[1],
                    ),
                    (
                        "Verification",
                        brokered_profile[2],
                    ),
                    ("Snoovatar", brokered_profile[3]),
                    ("Karma", brokered_profile[4]),
                ]
            else:
                brokered_profile = self.data_broker.subreddit_data(raw_data=raw_profile)
                additional_data = [
                    ("Allows", brokered_profile[1]),
                    ("Banner", brokered_profile[2]),
                    ("Header", brokered_profile[3]),
                    ("Flairs", brokered_profile[4]),
                ]

            print(
                self.create_tree(
                    tree_title=raw_profile.get("public_description")
                    if profile_type == "subreddit_profile"
                    else raw_profile.get("subreddit").get("title"),
                    tree_data=brokered_profile[0],
                    additional_data=additional_data,
                    additional_text=raw_profile.get("submit_text")
                    if profile_type == "subreddit_profile"
                    else None,
                )
            )

            save_data(
                data=raw_profile,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{profile_source}_profile",
            )

    def posts_tree(
        self,
        sort_criterion: str,
        posts_limit: int,
        posts_type: str,
        save_to_json: bool = False,
        posts_source: str = None,
        show_author: bool = False,
    ):
        raw_posts = self.api.get_posts(
            sort_criterion=sort_criterion,
            posts_limit=posts_limit,
            posts_type=posts_type,
            posts_source=posts_source,
        )

        if raw_posts:
            posts_tree = self.create_tree(
                tree_title=f"Visualising {posts_limit} {posts_type} - {datetime.now()}"
            )

            for post in raw_posts:
                # Set branch title to show the post author's username if the show_author is True.
                if show_author:
                    branch_title = (
                        f"[italic]{convert_timestamp_to_datetime(post.get('data').get('created'))} | by"
                        f" u/{post.get('data').get('author')}:[/] [bold]{post.get('data').get('title')}[/]"
                    )
                else:
                    # Otherwise, set the title of the branch to the title of the post.
                    branch_title = (
                        f"[italic]{convert_timestamp_to_datetime(post.get('data').get('created'))}:[/] "
                        f"[bold]{post.get('data').get('title')}[/]"
                    )

                self.add_branch(
                    branch_title=branch_title,
                    target_tree=posts_tree,
                    branch_data=self.data_broker.post_data(raw_post=post.get("data")),
                    additional_text=post.get("data").get("selftext"),
                )

            print(posts_tree)

            save_data(
                data=raw_posts[0],
                save_to_json=save_to_json,
                filename=f"{posts_source}_{posts_type}",
            )

    def user_comments_tree(
        self,
        username: str,
        sort_criterion: str,
        comments_limit: int,
        save_to_json: bool,
    ):
        # Initialise a tree structure to visualise the results.
        comments_tree = self.create_tree(
            tree_title=f"Visualising {username}'s [green]{sort_criterion}[/] [cyan]{comments_limit}[/] comments"
        )

        # Get comments from the API and add filters accordingly
        raw_comments = self.api.get_posts(
            sort_criterion=sort_criterion,
            posts_limit=comments_limit,
            posts_type="user_comments",
            posts_source=username,
        )

        if raw_comments:
            for raw_comment in raw_comments:
                raw_comment_data = raw_comment.get("data")
                self.add_branch(
                    target_tree=comments_tree,
                    branch_title=convert_timestamp_to_datetime(
                        timestamp=raw_comment_data.get("created")
                    ),
                    branch_data=self.data_broker.comment_data(
                        raw_comment=raw_comment_data
                    ),
                    additional_text=raw_comment_data.get("body"),
                )

            # Print the visualised tree structure.
            print(comments_tree)

            save_data(
                data=raw_comments[0],
                save_to_json=save_to_json,
                filename=f"{username}_comments",
            )

    def post_data_tree(
        self,
        post_id: str,
        post_subreddit: str,
        sort: str,
        limit: int,
        save_to_csv: bool,
        save_to_json: bool,
        show_comments: bool,
    ):
        """
        Visualises a post's data in a tree structure.

        :param post_id: Post's ID
        :param post_subreddit:
        :param sort: Post data (comments/awards) sort criterion.
        :param limit: Maximum number of comments/awards to get.
        :param save_to_json: A boolean value indicating whether data should be saved to a JSON file.
        :param save_to_csv: A boolean value indicating whether data should be saved to a CSV file.
        :param show_comments: A boolean value indicating whether a comments
           branch should be shown in the post tree.

        """

        raw_post, raw_comments = self.api.get_post_data(
            post_id=post_id,
            subreddit=post_subreddit,
            sort_criterion=sort,
            comments_limit=limit,
        )

        if raw_post:
            post_tree = self.create_tree(
                tree_title=f"{raw_post.get('title')} | by {raw_post.get('author')}",
                tree_data=self.data_broker.post_data(raw_post=raw_post),
                additional_text=raw_post.get("selftext"),
            )

            save_data(
                data=raw_post,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{raw_post.get('id')}_post_profile",
            )

            if show_comments:
                if raw_comments:
                    comments_branch = post_tree.add(
                        f"[bold]Visualising [cyan]{limit}[/] [green]{sort}[/] comments for post {post_id}[/]"
                    )
                    raw_comments.pop()  # Remove last item from the list (it does not contain any comment data)
                    for raw_comment in raw_comments:
                        raw_comment_data = raw_comment.get("data")
                        self.add_branch(
                            target_tree=comments_branch,
                            branch_title=convert_timestamp_to_datetime(
                                timestamp=raw_comment_data.get("created")
                            ),
                            branch_data=self.data_broker.comment_data(
                                raw_comment=raw_comment_data
                            ),
                            additional_text=raw_comment_data.get("body"),
                        )

                    save_data(
                        data=raw_comments,
                        save_to_json=save_to_json,
                        filename=f"{raw_post.get('id')}_comments",
                    )

            print(post_tree)
