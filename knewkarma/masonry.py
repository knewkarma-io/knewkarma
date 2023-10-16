from datetime import datetime
from typing import Union

from glyphoji import glyph
from rich import print
from rich.tree import Tree

from .api import API
from .coreutils import convert_timestamp_to_datetime, format_api_data, save_data


class TreeMasonry:
    def __init__(self):
        self.api = API()
        self.mallet = DataMasonry()

    @staticmethod
    async def add_branch(
        target_tree: Tree,
        branch_title: str,
        branch_data: dict,
        is_post: bool = False,
        post_text: str = None,
    ):
        """
        Add a branch to a specified Tree.

        :param target_tree: The existing Tree to add the branch to.
        :param branch_title: The title for the new branch.
        :param branch_data: The data for the new branch in dictionary format.
        :param is_post: A boolean value to determine whether a branch is a post.
        :param post_text: If is_post is set to True, post_text will contain the posts selftext.
        """
        branch = target_tree.add(f"[bold]{branch_title}[/]")
        for key, value in branch_data.items():
            branch.add(f"{key}: {value}", style="dim")
        if is_post:
            from rich.text import Text

            branch.add(Text(post_text), style="italic")

    async def branch_posts(
        self, target_tree: Tree, posts: list, show_author: bool = False
    ):
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

            # Get re-formatted post data from the data masons.
            post_data = self.mallet.post_data(raw_post=post)

            # Iterate over each key and value in the re-formatted post data dictionary.
            # And them to post_branch.
            for key, value in post_data.items():
                post_branch.add(f"{key}: {value}", style="dim")

            # Add post selftext to the end of post_branch.
            post_branch.add(post.get("selftext"))

    async def branch_subreddit(
        self,
        target_tree: Tree,
        subreddit_data: dict = None,
        is_user_subreddit: bool = False,
        user_subreddit_title: str = None,
        user_subreddit_data: dict = None,
    ):
        """
        Adds a Subreddit profile branch to a specified tree.

        :param target_tree: Tree to add the branch to.
        :param subreddit_data: The subreddit data to add to the branch.
        :param is_user_subreddit: A boolean to determine if profile is a user subreddit.
        :param user_subreddit_title: If it's a user subreddit, this specifies the subreddit title to add to the branch.
        :param user_subreddit_data: If it's a user subreddit, this specifies the subreddit data to add to the branch.

        """

        if is_user_subreddit:
            await self.add_branch(
                target_tree=target_tree,
                branch_title=user_subreddit_title,
                branch_data=user_subreddit_data,
            )
        else:
            # Get re-formatted/re-formatted subreddit profile data
            (
                profile,
                allows,
                banner,
                header,
                flair,
            ) = self.mallet.subreddit_data(raw_data=subreddit_data)

            # Add the main profile branch to the target tree
            # Set title to 'display_name' if data is for a user subreddit.
            # Otherwise, use 'public_description'.
            # Note:
            #     Every Reddit user has a user subreddit that starts with u_ (e.g., u_AutoModerator).
            await self.add_branch(
                target_tree=target_tree,
                branch_title=f"[bold]{f'{glyph.busts_in_silhouette} Subreddit' if is_user_subreddit else subreddit_data.get('public_description')}[/]",
                branch_data=profile,
            )

            # Add additional branches if it's not a user subreddit.
            # Add a Banner branch to target_tree.
            await self.add_branch(
                target_tree=target_tree,
                branch_title=f"{glyph.thumbs_up} [bold]Allows[/]",
                branch_data=allows,
            )

            # Add a Banner branch to target_tree.
            await self.add_branch(
                target_tree=target_tree,
                branch_title=f"{glyph.puzzle_piece} [bold]Banner[/]",
                branch_data=banner,
            )

            # Add a Header branch to target_tree.
            await self.add_branch(
                target_tree=target_tree,
                branch_title=f"{glyph.memo} [bold]Header[/]",
                branch_data=header,
            )

            # Add a Flairs branch to target_tree.
            await self.add_branch(
                target_tree=target_tree,
                branch_title=f"{glyph.four_leaf_clover} [bold]Flairs[/]",
                branch_data=flair,
            )

            # Add submit_text (subreddit rules) at the end of the tree
            target_tree.add(subreddit_data.get("submit_text"), style="italic")

    async def branch_comments(self, target_tree: Tree, comments: list):
        """
        Adds a Comments branch to a specified tree.

        :param target_tree: Tree to add the branch to.
        :param comments: List of comments to add to the branch.
        """
        for comment_index, comment in enumerate(comments, start=1):
            comment_data = self.mallet.comment_data(comment.get("data"))
            await self.add_branch(
                target_tree=target_tree,
                branch_title=convert_timestamp_to_datetime(
                    timestamp=comment.get("data").get("created")
                ),
                branch_data=comment_data,
                is_post=True,
                post_text=comment.get("data").get("body", "[[red]not applicable[/]]"),
            )

            if comment.get("data").get("replies"):
                replies_branch = target_tree.add("Replies")
                for reply in (
                    comment.get("data").get("replies").get("data").get("children")
                ):
                    await self.add_branch(
                        target_tree=replies_branch,
                        branch_title=convert_timestamp_to_datetime(
                            timestamp=reply.get("data").get("created")
                        ),
                        branch_data=self.mallet.comment_data(reply.get("data")),
                        is_post=True,
                        post_text=reply.get("data").get(
                            "body", "[[red]not applicable[/]]"
                        ),
                    )

    async def tree_user_profile(
        self, username: str, save_to_csv: bool, save_to_json: bool
    ):
        """
        Asynchronously visualises a user's profile data in a Tree structure.

        :param username: The user to visualise profile data for.
        :param save_to_json: A boolean value indicating whether data should be save to a JSON file.
        :param save_to_csv: A boolean value indicating whether data should be save to a CSV file.
        """
        # Get profile data from the API
        data = await self.api.get_user_profile(username=username)
        if data:
            user_tree = Tree(
                f"{data.get('subreddit').get('title')}",
                guide_style="bold bright_blue",
            )

            # Separate the profile data in categories
            (
                profile,
                subreddit,
                verification,
                snoovatar,
                karma,
            ) = self.mallet.user_data(raw_data=data)
            for key, value in profile.items():
                user_tree.add(f"{key}: {value}")

            # Add a branch for the user's subreddit.
            # Note (again lol): Every Reddit user has a user subreddit that starts with u_ (e.g., u_AutoModerator).
            await self.branch_subreddit(
                target_tree=user_tree,
                is_user_subreddit=True,
                user_subreddit_title=data.get("subreddit").get("display_name"),
                user_subreddit_data=subreddit,
            )

            # Add a branch for the user's verification status
            await self.add_branch(
                target_tree=user_tree,
                branch_data=verification,
                branch_title=f"{glyph.check_mark_button} [bold]Verification[/]",
            )

            # Add a branch for the user's Karma count
            await self.add_branch(
                target_tree=user_tree,
                branch_data=karma,
                branch_title=f"{glyph.four_leaf_clover} [bold]Karma[/]",
            )

            # Print the visualised tree structure.
            print(user_tree)

            save_data(
                data=data,
                save_to_csv=save_to_csv,
                save_to_json=save_to_json,
                filename=f"{username}_profile",
            )

    async def tree_user_posts(
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
        :param save_to_json: A boolean value indicating whether data should be save to a JSON file.
        """
        # Initialise a tree structure to visualise the results.
        posts_tree = Tree(
            f"[bold]Showing {username}'s "
            f"[cyan]{limit}[/] [green]{sort}[/] posts[/]",
            guide_style="bold bright_blue",
        )

        # Get posts from the API and add filters accordingly
        posts = await self.api.get_user_posts(
            username=username,
            sort=sort,
            limit=limit,
        )

        if posts:
            # Add a branch for each post to posts_tree
            await self.branch_posts(target_tree=posts_tree, posts=posts)

            # Print the visualised tree structure.
            print(posts_tree)

            save_data(
                data=posts[0],
                save_to_json=save_to_json,
                filename=f"{username}_posts",
            )

    async def tree_user_comments(
        self, username: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Asynchronously visualises a user's comments in a Tree structure.

        :param username: The user to visualise comments for.
        :param sort: Sort criterion of the comments (default is all).
        :param limit: Maximum number of comments to show.
        :param save_to_json: A boolean value indicating whether data should be save to a JSON file.
        """
        # Initialise a tree structure to visualise the results.
        comments_tree = Tree(
            f"[bold]Showing {username}'s [green]{sort}[/] [cyan]{limit}[/] comments[/]",
            guide_style="bold bright_blue",
        )

        # Get comments from the API and add filters accordingly
        comments = await self.api.get_user_comments(
            username=username, sort=sort, limit=limit
        )

        if comments:
            # Add a branch for each comment to comments_tree
            await self.branch_comments(target_tree=comments_tree, comments=comments)

            # Print the visualised tree structure.
            print(comments_tree)

            save_data(
                data=comments[0],
                save_to_json=save_to_json,
                filename=f"{username}_comments",
            )

    async def tree_subreddit_profile(
        self, subreddit: str, save_to_csv: bool, save_to_json: bool
    ):
        """
        Asynchronously visualises a user's profile data in a Tree structure.

        :param subreddit: The subreddit to visualise profile data for.
        :param save_to_json: A boolean value indicating whether data should be save to a JSON file.
        :param save_to_csv: A boolean value indicating whether data should be save to a CSV file.
        """
        # Get subreddit data from the API
        data = await self.api.get_subreddit_profile(subreddit=subreddit)

        if data:
            # Initialise a tree structure to visualise the results.
            subreddit_tree = Tree(
                f"[bold]{data.get('title')}[/]", guide_style="bold bright_blue"
            )

            # Create a subreddit profile tree
            await self.branch_subreddit(target_tree=subreddit_tree, subreddit_data=data)

            # Print the visualised tree structure.
            print(subreddit_tree)

            save_data(
                data=data,
                save_to_json=save_to_json,
                filename=f"{subreddit}_profile",
            )

    async def tree_subreddit_posts(
        self, subreddit: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Asynchronously visualises a subreddit's posts in a Tree structure.

        :param subreddit: The subreddit to visualise posts for.
        :param sort: Sort criterion of the posts (default is all).
        :param limit: Maximum number of posts to show.
         :param save_to_json: A boolean value indicating whether data should be save to a JSON file.
        """
        # Initialise a tree structure to visualise the results.
        posts_tree = Tree(
            f"[bold]Showing r/{subreddit}'s [cyan]{limit}[/] [green]{sort}[/] posts[/]",
            guide_style="bold bright_blue",
        )

        posts = await self.api.get_subreddit_posts(
            subreddit=subreddit,
            sort=sort,
            limit=limit,
        )

        if posts:
            await self.branch_posts(
                target_tree=posts_tree, posts=posts, show_author=True
            )

            # Print the visualised tree structure.
            print(posts_tree)

            save_data(
                data=posts[0],
                save_to_json=save_to_json,
                filename=f"{subreddit}_posts",
            )

    async def tree_search_results(
        self, query: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Asynchronously visualises search results in a tree structure.

        :param query: Search query.
        :param sort: Sort criterion of the results (default is all).
        :param limit: Maximum number of results to show.
        :param save_to_json: A boolean value indicating whether data should be save to a JSON file.
        """
        # Initialise a tree structure to visualise the results.
        results_tree = Tree(
            f"[bold]{datetime.now()}[/]",
            guide_style="bold bright_blue",
        )

        # Get search results from the API and add filters accordingly
        results = await self.api.search(query=query, sort=sort, limit=limit)

        if results:
            # Add a branch for each result to results_tree
            await self.branch_posts(
                target_tree=results_tree, posts=results, show_author=True
            )

            # Print the visualised tree structure.
            print(results_tree)

            save_data(
                data=results[0],
                save_to_json=save_to_json,
                filename=f"{query}_results",
            )

    import argparse

    async def tree_post_data(
        self,
        arguments: argparse,
    ):
        """
        Asynchronously visualises a post's data in a tree structure.

        :param arguments: Argparse object containing command-line arguments.

        Expected Arguments
        ------------------
        - args.id: Post's ID
        - args.subreddit: Subreddit in which the post was posted.
        - args.sort: Post data (comments/awards) sort criterion.
        - args.limit: Maximum number of comments/awards to get.
        - args.profile: Use to get a post's data without comments or awards.
        - args.comments: Use to get a post's comments.
        - args.csv: Use to save data to a SCV file.
        - args.json: Use to save data to a JSON file.
        """
        post_id = arguments.id
        post_subreddit = arguments.subreddit
        sort = arguments.sort
        limit = arguments.limit

        raw_post, raw_comments = await self.api.get_post_data(
            post_id=post_id, subreddit=post_subreddit, sort=sort, limit=limit
        )

        post, comment = self.mallet.post_data(
            raw_post=raw_post, raw_comments=raw_comments
        )

        if raw_post or raw_comments:
            if arguments.profile:
                if raw_post:
                    post_tree = Tree(
                        f"{raw_post.get('title')} by {raw_post.get('author')}",
                        guide_style="bold bright_blue",
                    )
                    for key, value in post.items():
                        post_tree.add(f"{key}: {value}", style="dim")
                    post_tree.add(raw_post.get("selftext"))

                    print(post_tree)

                    save_data(
                        data=post,
                        save_to_csv=arguments.csv,
                        save_to_json=arguments.json,
                        filename=f"{raw_post.get('id')}_post_profile",
                    )

            if arguments.comments:
                if raw_comments:
                    comments_tree = Tree(
                        f"[bold]Showing [cyan]{limit}[/] [green]{sort}[/] comments for post {post_id}[/]",
                        guide_style="bold bright_blue",
                    )
                    # Add a branch for each comment to comments_tree
                    await self.branch_comments(
                        target_tree=comments_tree, comments=raw_comments
                    )

                    # Print the visualised tree structure.
                    print(comments_tree)

                    save_data(
                        data=raw_comments[0],
                        save_to_json=arguments.json,
                        filename=f"{raw_post.get('id')}_comments",
                    )

    async def tree_post_listings(
        self, listing: str, sort: str, limit: int, save_to_json: bool
    ):
        """
        Asynchronously visualises posts from a specified listing in a tree structure.

        :param listing: Listing to get posts from.
        :param sort: Sort criterion of the posts (default is all).
        :param limit: Maximum number of posts to show.
        :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
        """
        # Get posts from the API and add filters accordingly
        posts = await self.api.get_post_listings(
            listing=listing, sort=sort, limit=limit
        )

        # Initialise a tree structure to visualise the posts.
        posts_tree = Tree(
            f"[bold]Showing {sort} {limit} posts from the '{listing}' listing[/]",
            guide_style="bold bright_blue",
        )

        if posts:
            # Add a branch for each posts to posts_tree
            await self.branch_posts(
                target_tree=posts_tree, posts=posts, show_author=True
            )

            # Print the visualised tree structure.
            print(posts_tree)

            save_data(
                data=posts[0],
                save_to_json=save_to_json,
                filename=f"{listing}_posts",
            )

    async def tree_front_page_posts(self, sort: str, limit: int, save_to_json: bool):
        """
        Asynchronously visualises posts from the Reddit front-page in a tree structure.

        :param sort: Sort criterion of the posts (default is all).
        :param limit: Maximum number of posts to show.
        :param save_to_json: A boolean value to indicate whether to save data as a JSON file.
        """
        # Get front page posts from the API and add filters accordingly
        posts = await self.api.get_front_page_posts(sort=sort, limit=limit)

        # Initialise a tree structure to visualise the posts.
        posts_tree = Tree(
            f"[bold]Showing {sort} {limit} posts from the front-page[/]",
            guide_style="bold bright_blue",
        )

        if posts:
            # Add a branch for each posts to posts_tree
            await self.branch_posts(
                target_tree=posts_tree, posts=posts, show_author=True
            )

            # Print the visualised tree structure.
            print(posts_tree)

            save_data(
                data=posts[0],
                save_to_json=save_to_json,
                filename=f"frontpage_posts",
            )


class DataMasonry:
    """
    The TreeData class holds methods used to re-restructure the API data in-order to get only the relevant information.
    """

    @staticmethod
    def user_data(raw_data: dict) -> tuple:
        """
        Re-formats raw user data from the API to the structure of the json files in the user directory.

        Data Files
        ----------
        - user/profile.json: Holds the structure for a user profile data.
        - user/subreddit.json: Holds the structure for a user subreddit data
        - user/verified.json: Holds the structure for a user's verified status.
        - user/snoovatar.json: (I don't even why 'snoovatar' is a word😂)
           Holds the structure for a user's snoovatar data.
        - user/karma.json: Holds the structure for a user's karma count.

        :param raw_data: Raw data from API.
        :returns: A tuple Re-formatted data
        """
        profile = format_api_data(api_data=raw_data, data_file="user/profile.json")
        subreddit = format_api_data(
            api_data=raw_data.get("subreddit"), data_file="user/subreddit.json"
        )
        verification = format_api_data(
            api_data=raw_data, data_file="user/verified.json"
        )
        snoovatar = format_api_data(api_data=raw_data, data_file="user/snoovatar.json")
        karma = format_api_data(api_data=raw_data, data_file="user/karma.json")

        return profile, subreddit, verification, snoovatar, karma

    @staticmethod
    def subreddit_data(raw_data: dict) -> tuple:
        """
        Re-formats raw subreddit data from the API to the structure of the json files in the subreddit directory.

        Data Files
        ----------
        - subreddit/profile.json: Holds the structure for a subreddit profile data.
        - subreddit/allows.json: Holds the structure for a subreddit's allowed content policies.
        - subreddit/banner.json: Holds the structure for a subreddit's banner data.
        - subreddit/header.json: Holds the structure for a subreddit's header data.
        - subreddit/flair.json: Holds the structure for a subreddit's flair data.

        :param raw_data: Raw data from API.
        :returns: A tuple of Re-formatted data
        """
        profile = format_api_data(api_data=raw_data, data_file="subreddit/profile.json")
        allows = format_api_data(api_data=raw_data, data_file="subreddit/allows.json")
        banner = format_api_data(api_data=raw_data, data_file="subreddit/banner.json")
        header = format_api_data(api_data=raw_data, data_file="subreddit/header.json")
        flairs = format_api_data(api_data=raw_data, data_file="subreddit/flairs.json")
        return profile, allows, banner, header, flairs

    @staticmethod
    def post_data(raw_post: dict, raw_comments: list = None) -> Union[tuple, dict]:
        """
        Re-formats raw post data from the API to the structure of the json files in the post directory.

        Data Files
        ----------
        - post/profile.json: Holds the structure for a post's profile data.
        - shared/comment.json: Holds the structure for a post's comments.
        - post/award.json: Holds the structure for a post's awards. (not yet implemented)

        :param raw_post: Raw post data from API.
        :param raw_comments: Raw post comments data from API.
        :returns: A tuple of Re-formatted post data if raw_comments has got valid data,
          else a dictionary containing profile data only.
        """
        profile = format_api_data(api_data=raw_post, data_file="post/profile.json")
        comment = None

        if raw_comments:
            for comment in raw_comments:
                comment = format_api_data(
                    api_data=comment, data_file="shared/comment.json"
                )
            return profile, comment
        else:
            return profile

    @staticmethod
    def comment_data(raw_data: dict) -> dict:
        comment_data = format_api_data(
            api_data=raw_data, data_file="shared/comment.json"
        )
        return comment_data
