import argparse

from rich.prompt import Prompt, Confirm

from .masonry import Masonry


class Executor:
    def __init__(self, arguments: argparse, tree_masonry: Masonry):
        """
        Executor class is responsible for executing methods depending on the user's passed command-line arguments.

        :param arguments: An argparse object containing command-line arguments.
        :param tree_masonry: An instance of the Masonry class that will be used to access tree structures
          for different types of returned data.
        """
        self.tree_masonry = tree_masonry
        self.arguments = arguments
        self.handlers = self.Handlers(executor=self)

    def cli(self):
        operation_mode: str = self.arguments.mode or Prompt.ask(
            "Select target to get data from",
            choices=["user", "subreddit", "post", "posts", "search"],
        )
        if operation_mode == "user":
            self.handlers.user_handler(
                username=self.arguments.username
                if hasattr(self.arguments, "username")
                else Prompt.ask("Username", default="automoderator")
            )

        elif operation_mode == "subreddit":
            self.handlers.subreddit_handler(
                subreddit=self.arguments.subreddit
                if hasattr(self.arguments, "subreddit")
                else Prompt.ask("Subreddit", default="osint")
            )

        elif operation_mode == "search":
            self.tree_masonry.posts_tree(
                posts_type="search_posts",
                posts_source=self.arguments.query
                if hasattr(self.arguments, "query")
                else Prompt.ask("Search query", default="osint"),
                show_author=True,
                sort_criterion=self.arguments.sort or self.handlers.data_sort_criterion,
                posts_limit=self.arguments.limit or self.handlers.data_limit,
                save_to_json=self.arguments.json or self.handlers.save_to_json,
            )

        elif operation_mode == "post":
            self.tree_masonry.post_data_tree(
                post_id=self.arguments.post_id
                if hasattr(self.arguments, "post_id")
                else Prompt.ask("Post ID", default="12csg48"),
                post_subreddit=self.arguments.post_subreddit
                if hasattr(self.arguments, "post_subreddit")
                else Prompt.ask("Post source subreddit", default="osint"),
                sort=self.arguments.sort or self.handlers.data_sort_criterion,
                limit=self.arguments.limit or self.handlers.data_limit,
                show_comments=self.arguments.comments
                if hasattr(self.arguments, "show_comments")
                else Confirm.ask("Would you like to show comments?", default=False),
                save_to_csv=self.arguments.csv or self.handlers.save_to_csv,
                save_to_json=self.arguments.json or self.handlers.save_to_json,
            )
        elif operation_mode == "posts":
            self.handlers.posts_handler()

    class Handlers:
        def __init__(self, executor):
            from . import DATA_SORT_LISTINGS

            self.arguments: argparse = executor.arguments
            self.tree_masonry: Masonry = executor.tree_masonry
            self.data_sort_criterion: str = self.arguments.sort or Prompt.ask(
                "Set (bulk data) output  sort criterion",
                choices=DATA_SORT_LISTINGS,
                default="all",
            )
            self.data_limit: int = self.arguments.limit or Prompt.ask(
                "Set (bulk data) output  limit", default=10
            )
            self.save_to_json: bool = self.arguments.json or Confirm.ask(
                "Would you like to save output to a JSON file?", default=False
            )
            self.save_to_csv: bool = self.arguments.csv or Confirm.ask(
                "Would you like to save output to a CSV file?", default=False
            )

        def get_action(self, actions_map: dict, default_action: str) -> str:
            """
            Gets the action based on command-line arguments or interactive input.

            :param actions_map: A dictionary mapping action names to their corresponding functions.
            :param default_action: The default action to choose if no command-line argument is provided.
            :return: The chosen action name.
            """
            # Determine action from CLI arguments, default to None if not found
            action: str = next(
                (
                    action_name
                    for action_name in actions_map
                    if getattr(self.arguments, action_name, False)
                ),
                None,
            )

            # If no CLI argument for action, ask user interactively
            return action or Prompt.ask(
                "What type of data would you like to get?",
                choices=list(actions_map.keys()),
                default=default_action,
            )

        def user_handler(self, username: str):
            user_actions_map: dict = {
                "profile": lambda: self.tree_masonry.profile_tree(
                    profile_type="user_profile",
                    profile_source=username,
                    save_to_json=self.save_to_json,
                    save_to_csv=self.save_to_csv,
                ),
                "posts": lambda: self.tree_masonry.posts_tree(
                    posts_source=username,
                    posts_type="user_posts",
                    posts_limit=self.data_limit,
                    sort_criterion=self.data_sort_criterion,
                    save_to_json=self.save_to_json,
                ),
                "comments": lambda: self.tree_masonry.user_comments_tree(
                    username=username,
                    sort_criterion=self.data_sort_criterion,
                    comments_limit=self.data_limit,
                    save_to_json=self.save_to_json,
                ),
            }

            action: str = self.get_action(
                actions_map=user_actions_map, default_action="profile"
            )

            user_actions_map.get(action)()

        def subreddit_handler(self, subreddit: str):
            subreddit_actions_map: dict = {
                "profile": lambda: self.tree_masonry.profile_tree(
                    profile_type="subreddit_profile",
                    profile_source=subreddit,
                    save_to_json=self.save_to_json,
                    save_to_csv=self.save_to_csv,
                ),
                "posts": lambda: self.tree_masonry.posts_tree(
                    posts_source=subreddit,
                    posts_type="subreddit_posts",
                    posts_limit=self.data_limit,
                    sort_criterion=self.data_sort_criterion,
                    save_to_json=self.save_to_json,
                ),
            }

            action: str = self.get_action(
                actions_map=subreddit_actions_map, default_action="profile"
            )
            subreddit_actions_map.get(action)()

        def posts_handler(self):
            posts_actions_map: dict = {
                "front_page": lambda: self.tree_masonry.posts_tree(
                    posts_type="front_page_posts",
                    posts_limit=self.data_limit,
                    show_author=True,
                    sort_criterion=self.data_sort_criterion,
                    save_to_json=self.save_to_json,
                ),
                "listing": lambda: self.tree_masonry.posts_tree(
                    posts_type="listing_posts",
                    posts_source=self.arguments.listing,
                    posts_limit=self.data_limit,
                    show_author=True,
                    sort_criterion=self.data_sort_criterion,
                    save_to_json=self.save_to_json,
                ),
            }
            action: str = self.get_action(
                actions_map=posts_actions_map, default_action="front_page"
            )
            posts_actions_map.get(action)()
