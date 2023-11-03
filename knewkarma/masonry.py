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
        is_empty: bool = False,
        tree_data: Union[dict, list] = None,
        additional_text: str = None,
        additional_data: [(str, Union[dict, list])] = None,
    ) -> Tree:
        """
        Creates a tree structure  and populates it with the given data.

        :param tree_title: Title of the tree.
        :param is_empty: A boolean value indicating whether the tree is empty.
        :param tree_data: Data to populate the tree with.
        :param additional_text: Additional text to add at the end of the tree.
        :param additional_data: A list of tuples containing additional data such that should be added to the tree.
           Data format: ("title" [str], data [dict or list])
        :returns: A populated or emtpy tree structure.
        """
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

        return (
            Tree(tree_title, style="bold", guide_style="bold bright_blue")
            if is_empty
            else tree
        )

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

    def branch_posts(self, target_tree: Tree, posts: list, show_author: bool = False):
        """
        Adds a Post branch to a specified tree.

        :param target_tree: Tree to add the branch to.
        :param posts: The post data to add to the branch.
        :param show_author: A boolean value to determine whether
         the post author's username should be shown in the branch title.
        """
        for post_index, post in enumerate(posts, start=1):
            post = post.get("data")

            # Set branch title to show the post author's username if the show_author is True.
            if show_author:
                branch_title = (
                    f"[italic]{convert_timestamp_to_datetime(post.get('created'))} b"
                    f"y u/{post.get('author')}:[/] [bold]{post.get('title')}[/]"
                )
            else:
                # Otherwise, set the title of the branch to the title of the post.
                branch_title = (
                    f"[italic]{convert_timestamp_to_datetime(post.get('created'))}:[/] "
                    f"[bold]{post.get('title')}[/]"
                )

            # Add a post branch to target_tree.
            post_branch = target_tree.add(branch_title)

            # Iterate over each key and value in the re-formatted post data dictionary.
            # And them to post_branch.
            for key, value in self.data_broker.post_data(raw_post=post).items():
                post_branch.add(f"{key}: {value}", style="dim")

            # Add post selftext to the end of post_branch.
            post_branch.add(post.get("selftext"))

    def tree_user_profile(self, username: str, save_to_csv: bool, save_to_json: bool):
        """
        Asynchronously visualises a user's profile data in a Tree structure.

        :param username: The user to visualise profile data for.
        :param save_to_json: A boolean value indicating whether data should be saved to a JSON file.
        :param save_to_csv: A boolean value indicating whether data should be saved to a CSV file.
        """
        # Get profile data from the API
        raw_profile = self.api.get_user_profile(username=username)
        if raw_profile:
            # Separate the profile data in categories
            (
                profile,
                subreddit,
                verification,
                snoovatar,
                karma,
            ) = self.data_broker.user_data(raw_data=raw_profile)

            print(
                self.create_tree(
                    tree_title=raw_profile.get("subreddit").get("title"),
                    tree_data=profile,
                    additional_data=[
                        ("Snoovatar", snoovatar),
                        (raw_profile.get("subreddit").get("display_name"), subreddit),
                        ("Verification", verification),
                        ("Karma", karma),
                    ],
                )
            )

            save_data(
                data=raw_profile,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{username}_profile",
            )

    def tree_user_posts(
        self,
        username: str,
        sort: str,
        limit: int,
        save_to_json: bool,
    ):
        """
        Asynchronously visualises a user's posts in a Tree structure.

        :param username: The user to visualise posts for.
        :param sort: Sort criterion of the posts (default is all).
        :param limit: Maximum number of posts to show.
        :param save_to_json: A boolean value indicating whether data should be saved to a JSON file.
        """
        # Get posts from the API and add filters accordingly
        raw_posts = self.api.get_user_posts(
            username=username,
            sort=sort,
            limit=limit,
        )
        if raw_posts:
            # Initialise a tree structure to visualise the results.
            posts_tree = self.create_tree(
                tree_title=f"Visualising user's (@{username}) [cyan]{limit}[/] [green]{sort}[/] posts",
                is_empty=True,
            )
            for raw_post in raw_posts:
                self.add_branch(
                    target_tree=posts_tree,
                    branch_title=raw_post.get("data").get("title"),
                    branch_data=self.data_broker.post_data(
                        raw_post=raw_post.get("data")
                    ),
                    additional_text=raw_post.get("data").get("selftext"),
                )

            # Print the visualised tree structure.
            print(posts_tree)

            save_data(
                data=raw_posts[0],
                save_to_json=save_to_json,
                filename=f"{username}_posts",
            )

    def tree_user_comments(
        self, username: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Visualises a user's comments in a Tree structure.

        :param username: The user to visualise comments for.
        :param sort: Sort criterion of the comments (default is all).
        :param limit: Maximum number of comments to show.
        :param save_to_json: A boolean value indicating whether data should be saved to a JSON file.
        """
        # Initialise a tree structure to visualise the results.
        comments_tree = self.create_tree(
            tree_title=f"Visualising {username}'s [green]{sort}[/] [cyan]{limit}[/] comments",
            is_empty=True,
        )

        # Get comments from the API and add filters accordingly
        raw_comments = self.api.get_user_comments(
            username=username, sort=sort, limit=limit
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

    def tree_subreddit_profile(
        self, subreddit: str, save_to_csv: bool, save_to_json: bool
    ):
        """
        Visualises a user's profile data in a Tree structure.

        :param subreddit: The subreddit to visualise profile data for.
        :param save_to_json: A boolean value indicating whether data should be saved to a JSON file.
        :param save_to_csv: A boolean value indicating whether data should be saved to a CSV file.
        """
        # Get subreddit data from the API
        raw_profile = self.api.get_subreddit_profile(subreddit=subreddit)

        if raw_profile:
            (
                profile,
                allows,
                banner,
                header,
                flair,
            ) = self.data_broker.subreddit_data(raw_data=raw_profile)

            print(
                self.create_tree(
                    tree_title=raw_profile.get("public_description"),
                    tree_data=profile,
                    additional_data=[
                        ("Allows", allows),
                        ("Banner", banner),
                        ("Header", header),
                        ("Flairs", flair),
                    ],
                    additional_text=raw_profile.get("submit_text"),
                )
            )

            save_data(
                data=raw_profile,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{subreddit}_profile",
            )

    def tree_subreddit_posts(
        self, subreddit: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Visualises a subreddit's posts in a Tree structure.

        :param subreddit: The subreddit to visualise posts for.
        :param sort: Sort criterion of the posts (default is all).
        :param limit: Maximum number of posts to show.
         :param save_to_json: A boolean value indicating whether data should be saved to a JSON file.
        """
        # Initialise a tree structure to visualise the results.
        posts_tree = self.create_tree(
            tree_title=f"Visualising subreddit's (r/{subreddit}) [cyan]{limit}[/] [green]{sort}[/] posts",
            is_empty=True,
        )

        raw_posts = self.api.get_subreddit_posts(
            subreddit=subreddit,
            sort=sort,
            limit=limit,
        )

        if raw_posts:
            for raw_post in raw_posts:
                raw_post_data = raw_post.get("data")
                self.add_branch(
                    branch_title=f"[italic]{convert_timestamp_to_datetime(raw_post_data.get('created'))} by"
                    f" u/{raw_post_data.get('author')}:[/] [bold]{raw_post_data.get('title')}[/]",
                    target_tree=posts_tree,
                    branch_data=self.data_broker.post_data(raw_post=raw_post_data),
                    additional_text=raw_post_data.get("selftext"),
                )

            print(posts_tree)

            save_data(
                data=raw_posts[0],
                save_to_json=save_to_json,
                filename=f"{subreddit}_posts",
            )

    def tree_search_results(
        self, query: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Visualises search results in a tree structure.

        :param query: Search query.
        :param sort: Sort criterion of the results (default is all).
        :param limit: Maximum number of results to show.
        :param save_to_json: A boolean value indicating whether data should be saved to a JSON file.
        """
        # Initialise a tree structure to visualise the results.
        results_tree = self.create_tree(
            tree_title=f"Visualising {limit} results for [italic]{query}[/] - {datetime.now()}",
            is_empty=True,
        )

        # Get search results from the API and add filters accordingly
        raw_results = self.api.get_search_results(query=query, sort=sort, limit=limit)

        if raw_results:
            for raw_result in raw_results:
                raw_result_data = raw_result.get("data")
                self.add_branch(
                    branch_title=f"[italic]{convert_timestamp_to_datetime(raw_result_data.get('created'))} by"
                    f" u/{raw_result_data.get('author')}:[/] [bold]{raw_result_data.get('title')}[/]",
                    target_tree=results_tree,
                    branch_data=self.data_broker.post_data(raw_post=raw_result_data),
                    additional_text=raw_result_data.get("selftext"),
                )

            print(results_tree)

            save_data(
                data=raw_results[0],
                save_to_json=save_to_json,
                filename=f"{query}_search-results",
            )

    def tree_post_data(
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
            post_id=post_id, subreddit=post_subreddit, sort=sort, limit=limit
        )

        if raw_post:
            post_tree = self.create_tree(
                tree_title=f"{raw_post.get('title')} by {raw_post.get('author')}",
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

    def tree_post_listings(
        self, listing: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Visualises posts from a specified listing in a tree structure.

        :param listing: Listing to get posts from.
        :param sort: Sort criterion of the posts (default is all).
        :param limit: Maximum number of posts to show.
        :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
        """
        # Get posts from the API and add filters accordingly
        raw_posts = self.api.get_post_listings(listing=listing, sort=sort, limit=limit)

        # Initialise a tree structure to visualise the posts.
        posts_tree = self.create_tree(
            tree_title=f"Visualising {sort} {limit} posts from the '{listing}' listing",
            is_empty=True,
        )

        if raw_posts:
            for raw_post in raw_posts:
                raw_post_data = raw_post.get("data")
                self.add_branch(
                    branch_title=f"{convert_timestamp_to_datetime(raw_post_data.get('created'))} by"
                    f" u/{raw_post_data.get('author')}: [bold]{raw_post_data.get('title')}[/]",
                    target_tree=posts_tree,
                    branch_data=self.data_broker.post_data(raw_post=raw_post_data),
                    additional_text=raw_post_data.get("selftext"),
                )

            print(posts_tree)

            save_data(
                data=raw_posts[0],
                save_to_json=save_to_json,
                filename=f"{listing}_posts",
            )

    def tree_front_page_posts(self, sort: str, limit: int, save_to_json: bool):
        """
        Visualises posts from the Reddit front-page in a tree structure.

        :param sort: Sort criterion of the posts (default is all).
        :param limit: Maximum number of posts to show.
        :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
        """
        # Get front page posts from the API and add filters accordingly
        raw_posts = self.api.get_front_page_posts(sort=sort, limit=limit)

        # Initialise a tree structure to visualise the posts.
        posts_tree = self.create_tree(
            tree_title=f"Visualising {sort} {limit} posts from the front-page",
            is_empty=True,
        )

        if raw_posts:
            for raw_post in raw_posts:
                raw_post_data = raw_post.get("data")
                self.add_branch(
                    branch_title=f"{convert_timestamp_to_datetime(raw_post_data.get('created'))} by"
                    f" u/{raw_post_data.get('author')}: [bold]{raw_post_data.get('title')}[/]",
                    target_tree=posts_tree,
                    branch_data=self.data_broker.post_data(raw_post=raw_post_data),
                    additional_text=raw_post_data.get("selftext"),
                )

            save_data(
                data=raw_posts[0],
                save_to_json=save_to_json,
                filename=f"frontpage_posts",
            )

            print(posts_tree)
