import argparse

from .brokers import Broker
from .coreutils import log
from .masonry import Masonry
from .modules.subreddit import Subreddit
from .modules.user import User


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
        self.data_broker = Broker()

    def execute_cli_arguments(self):
        """
        Executes a command-line arguments based cli of Knew Karma.
        """
        if self.arguments.mode == "user":
            user = User(
                username=self.arguments.username,
                tree_masonry=self.tree_masonry,
                data_broker=self.data_broker,
            )
            self.handlers.user_mode_handler(user_object=user)

        elif self.arguments.mode == "subreddit":
            subreddit = Subreddit(
                subreddit=self.arguments.subreddit,
                tree_masonry=self.tree_masonry,
                data_broker=self.data_broker,
            )
            self.handlers.subreddit_mode_handler(subreddit_object=subreddit)

        elif self.arguments.mode == "search":
            self.tree_masonry.posts_tree(
                posts_type="search_posts",
                posts_source=self.arguments.query,
                show_author=True,
                sort_criterion=self.arguments.sort,
                posts_limit=self.arguments.limit,
                save_to_json=self.arguments.json,
            )

        elif self.arguments.mode == "post":
            self.tree_masonry.post_data_tree(
                post_id=self.arguments.post_id,
                post_subreddit=self.arguments.post_subreddit,
                sort=self.arguments.sort,
                limit=self.arguments.limit,
                show_comments=self.arguments.comments,
                save_to_csv=self.arguments.csv,
                save_to_json=self.arguments.json,
            )
        elif self.arguments.mode == "posts":
            if self.arguments.listing:
                self.tree_masonry.posts_tree(
                    posts_type="listing_posts",
                    posts_source=self.arguments.listing,
                    posts_limit=self.arguments.limit,
                    show_author=True,
                    sort_criterion=self.arguments.sort,
                    save_to_json=self.arguments.json,
                )
            else:
                log.warning(
                    "No specific argument provided, executing default function: [italic]front_page[/]"
                )
                self.tree_masonry.posts_tree(
                    posts_type="front_page_posts",
                    posts_limit=self.arguments.limit,
                    show_author=True,
                    sort_criterion=self.arguments.sort,
                    save_to_json=self.arguments.json,
                )

    class Handlers:
        def __init__(self, executor):
            self.arguments = executor.arguments
            self.tree_masonry = executor.tree_masonry
            self.data_sort_criterion: str = self.arguments.sort
            self.data_limit: int = self.arguments.limit
            self.save_to_json: bool = self.arguments.json
            self.save_to_csv: bool = self.arguments.csv

        def execute_functions(self, argument_map: dict):
            """
            Execute functions from a mapping if their corresponding command line arguments are True.
            If no argument is provided, execute the first function from the argument_map.

            :param argument_map: A dictionary mapping command line arguments to functions.
            """
            executed = False
            for argument, function in argument_map.items():
                if getattr(self.arguments, argument, False):
                    function()
                    executed = True

            # If no functions were executed, execute the first function by default
            if not executed:
                default_argument, default_function = next(iter(argument_map.items()))
                log.warning(
                    f"No specific argument provided, executing default function: [italic]{default_argument}[/]"
                )
                default_function()

        def user_mode_handler(self, user_object: User):
            user_argument_map = {
                "profile": lambda: user_object.profile(
                    save_to_json=self.save_to_json,
                    save_to_csv=self.save_to_csv,
                ),
                "posts": lambda: user_object.posts(
                    sort_criterion=self.data_sort_criterion,
                    posts_limit=self.data_limit,
                    save_to_json=self.save_to_json,
                ),
                "comments": lambda: user_object.comments(
                    sort_criterion=self.data_sort_criterion,
                    comments_limit=self.data_limit,
                    save_to_json=self.save_to_json,
                ),
            }

            self.execute_functions(argument_map=user_argument_map)

        def subreddit_mode_handler(self, subreddit_object: Subreddit):
            subreddit_argument_map = {
                "profile": lambda: subreddit_object.profile(
                    save_to_json=self.save_to_json, save_to_csv=self.save_to_csv
                ),
                "posts": lambda: subreddit_object.posts(
                    sort_criterion=self.data_sort_criterion,
                    posts_limit=self.data_limit,
                    save_to_json=self.save_to_json,
                ),
            }
            self.execute_functions(argument_map=subreddit_argument_map)
