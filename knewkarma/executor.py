import argparse

from rich.prompt import Prompt, Confirm

from .coreutils import DATA_SORT_LISTINGS
from .masonry import Masonry
from .messages import message


class Executor:
    def __init__(self, arguments: argparse, tree_masonry: Masonry):
        """
        Executor class is responsible for executing methods
        depending on the user's passed command-line arguments or interactive command-line commands.

        :param arguments: An argparse object containing command-line arguments.
        :param tree_masonry: An instance of the Masonry class that will be used to access tree structures
          for different types of returned data.
        """
        self.tree_masonry = tree_masonry
        self.arguments = arguments
        self.wizard = self.Wizards(executor=self)

    class Wizards:
        def __init__(self, executor):
            self.tree_masonry = executor.tree_masonry

        def user_cli_wizard(
            self,
            username: str,
            save_to_json: bool,
            save_to_csv: bool,
            data_limit: int,
            data_sort: str,
        ) -> dict:
            """
            Maps "user" interactive wizard commands to their methods.

            :param username: Selected target username to get data from.
            :param save_to_json: A boolean value indicating whether User data should be written to a JSON file.
            :param save_to_csv: A boolean value indicating whether User data should be written to a CSV file.
            :param data_limit: Maximum number of bulk data to get from user (posts, comments).
            :param data_sort: Bulk data sort criterion.
            :return: A dictionary with user commands mapped to their methods.
            """
            return {
                "profile": lambda: self.tree_masonry.tree_user_profile(
                    username=username,
                    save_to_csv=save_to_csv,
                    save_to_json=save_to_json,
                ),
                "comments": lambda: self.tree_masonry.tree_user_comments(
                    username=username,
                    limit=data_limit,
                    sort=data_sort,
                    save_to_json=save_to_json,
                ),
                "posts": lambda: self.tree_masonry.tree_user_posts(
                    username=username,
                    sort=data_sort,
                    limit=data_limit,
                    save_to_json=save_to_json,
                ),
            }

        def subreddit_cli_wizard(
            self,
            subreddit: str,
            save_to_json: bool,
            save_to_csv: bool,
            data_sort: str,
            data_limit: int,
        ) -> dict:
            """
            Maps "subreddit" interactive wizard commands to their methods.

            :param subreddit: Selected target subreddit to get data from.
            :param save_to_json: A boolean value indicating whether User data should be written to a JSON file.
            :param save_to_csv: A boolean value indicating whether Subreddit data should be written to a CSV file.
            :param data_limit: Maximum number of bulk data to get from user (posts, comments).
            :param data_sort: Bulk data sort criterion.
            :return: A dictionary with subreddit commands mapped to their methods.
            """
            return {
                "profile": lambda: self.tree_masonry.tree_subreddit_profile(
                    subreddit=subreddit,
                    save_to_csv=save_to_csv,
                    save_to_json=save_to_json,
                ),
                "posts": lambda: self.tree_masonry.tree_subreddit_posts(
                    subreddit=subreddit,
                    save_to_json=save_to_json,
                    sort=data_sort,
                    limit=data_limit,
                ),
            }

        def post_cli_wizard(
            self,
            post_id: str,
            post_subreddit: str,
            data_sort: str,
            data_limit: int,
            show_comments: bool,
            save_to_json: bool,
            save_to_csv: bool,
        ):
            """
            Maps "post" interactive wizard commands to their methods.

            :param post_id: Selected target post ID to get data from.
            :param post_subreddit: Selected subreddit to which the post was posted in.
            :param save_to_json: A boolean value indicating whether User data should be written to a JSON file.
            :param save_to_csv: A boolean value indicating whether Post data should be written to a CSV file.
            :param data_limit: Maximum number of bulk data to get from user (posts, comments).
            :param show_comments: A boolean value indicating whether
              a comments branch should be visualised in the post_tree.
            :param data_sort: Bulk data sort criterion.
            """
            self.tree_masonry.tree_post_data(
                post_id=post_id,
                post_subreddit=post_subreddit,
                sort=data_sort,
                limit=data_limit,
                show_comments=show_comments,
                save_to_json=save_to_json,
                save_to_csv=save_to_csv,
            )

        def posts_cli_wizard(
            self,
            posts_sort: str,
            posts_limit: int,
            save_to_json: bool,
        ) -> dict:
            """
            Maps "posts" interactive wizard commands to their methods/functions.

            :param save_to_json: A boolean value indicating whether User data should be written to a JSON file.
            :param posts_limit: Maximum number of bulk data to get from user (posts, comments).
            :param posts_sort: Bulk data sort criterion.
            :return: A dictionary with posts commands mapped to their methods/functions.
            """

            def get_listing():
                listing = Prompt.ask(
                    "listing",
                    choices=["best", "rising", "controversial"],
                    default="all",
                )
                return self.tree_masonry.tree_post_listings(
                    listing=listing,
                    sort=posts_sort,
                    limit=posts_limit,
                    save_to_json=save_to_json,
                )

            def get_search():
                search_query = Prompt.ask("query")
                return self.tree_masonry.tree_search_results(
                    query=search_query,
                    sort=posts_sort,
                    limit=posts_limit,
                    save_to_json=save_to_json,
                )

            return {
                "frontpage": lambda: self.tree_masonry.tree_front_page_posts(
                    sort=posts_sort,
                    limit=posts_limit,
                    save_to_json=save_to_json,
                ),
                "listing": get_listing,
                "search": get_search,
            }

    def execute_cli_arguments(self):
        """
        Executes a command-line arguments based cli of Knew Karma.
        """
        if self.arguments.mode == "user":
            if self.arguments.posts:
                self.tree_masonry.tree_user_posts(
                    username=self.arguments.username,
                    sort=self.arguments.sort,
                    limit=self.arguments.limit,
                    save_to_json=self.arguments.json,
                )
            elif self.arguments.comments:
                self.tree_masonry.tree_user_comments(
                    username=self.arguments.username,
                    sort=self.arguments.sort,
                    limit=self.arguments.limit,
                    save_to_json=self.arguments.json,
                )
            else:
                self.tree_masonry.tree_user_profile(
                    username=self.arguments.username,
                    save_to_csv=self.arguments.csv,
                    save_to_json=self.arguments.json,
                )

        elif self.arguments.mode == "subreddit":
            if self.arguments.posts:
                self.tree_masonry.tree_subreddit_posts(
                    subreddit=self.arguments.subreddit,
                    sort=self.arguments.sort,
                    limit=self.arguments.limit,
                    save_to_json=self.arguments.json,
                )
            else:
                self.tree_masonry.tree_subreddit_profile(
                    subreddit=self.arguments.subreddit,
                    save_to_csv=self.arguments.csv,
                    save_to_json=self.arguments.json,
                )
        elif self.arguments.mode == "search":
            self.tree_masonry.tree_search_results(
                query=self.arguments.query,
                sort=self.arguments.sort,
                limit=self.arguments.limit,
                save_to_json=self.arguments.json,
            )
        elif self.arguments.mode == "post":
            self.tree_masonry.tree_post_data(
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
                self.tree_masonry.tree_post_listings(
                    listing=self.arguments.listing,
                    sort=self.arguments.sort,
                    limit=self.arguments.limit,
                    save_to_json=self.arguments.json,
                )
            else:
                self.tree_masonry.tree_front_page_posts(
                    sort=self.arguments.sort,
                    limit=self.arguments.limit,
                    save_to_json=self.arguments.json,
                )

    def execute_cli_wizards(self):
        """
        Executes an interactive cli of Knew Karma.
        """
        commands = ["user", "subreddit", "posts", "search"]
        while True:
            command = Prompt.ask("knewkarma", choices=commands + ["quit"])
            if command == "quit":
                break
            bulk_data_limit = (
                Prompt.ask(
                    message(message_type="prompt", message_key="set_output_limit"),
                    default="10",
                    show_default=True,
                )
                if command in commands
                else None
            )
            bulk_data_sort = (
                Prompt.ask(
                    message(
                        message_type="prompt", message_key="set_output_sort_criterion"
                    ),
                    default="all",
                    show_default=True,
                    choices=DATA_SORT_LISTINGS,
                )
                if command in commands
                else None
            )
            save_to_json = (
                True
                if Confirm.ask(
                    message(
                        message_type="prompt",
                        message_key="confirm",
                        prompt_message="save output data to a JSON file",
                    ),
                    default=False,
                    show_default=True,
                )
                else False
            )
            save_to_csv = (
                True
                if Confirm.ask(
                    message(
                        message_type="prompt",
                        message_key="confirm",
                        prompt_message="save output data to a CSV file",
                    ),
                    default=False,
                    show_default=True,
                )
                else False
            )
            if command == "user":
                username = Prompt.ask(
                    message(
                        message_type="prompt",
                        message_key="enter_something",
                        what_to_enter="target username",
                    )
                )
                while True:
                    user_option = Prompt.ask(
                        f"u/{username}",
                        choices=["profile", "comments", "posts", "back"],
                    )
                    user_action = self.wizard.user_cli_wizard(
                        username=username,
                        save_to_json=save_to_json,
                        save_to_csv=save_to_csv,
                        data_sort=bulk_data_sort,
                        data_limit=bulk_data_limit,
                    ).get(user_option)
                    if user_option == "back":
                        break
                    elif user_action:
                        user_action()

            elif command == "subreddit":
                subreddit = Prompt.ask(
                    message(
                        message_type="prompt",
                        message_key="enter_something",
                        what_to_enter="target subreddit name",
                    )
                )

                while True:
                    subreddit_option = Prompt.ask(
                        f"r/{subreddit}",
                        choices=["profile", "posts", "back"],
                    )

                    subreddit_action = self.wizard.subreddit_cli_wizard(
                        subreddit=subreddit,
                        save_to_json=save_to_json,
                        save_to_csv=save_to_csv,
                        data_sort=bulk_data_sort,
                        data_limit=bulk_data_limit,
                    ).get(subreddit_option)

                    if subreddit_option == "back":
                        break
                    elif subreddit_action:
                        subreddit_action()

            elif command == "post":
                post_id = Prompt.ask(
                    message(
                        message_type="prompt",
                        message_key="enter_something",
                        what_to_enter="post ID",
                    )
                )
                post_subreddit = Prompt.ask(
                    message(
                        message_type="prompt",
                        message_key="enter_something",
                        what_to_enter="post's source subreddit",
                    )
                )
                show_comments = (
                    True
                    if Confirm.ask(
                        message(
                            message_type="prompt",
                            message_key="confirm",
                            prompt_message="show a comments' branch in the output",
                        ),
                        default=False,
                        show_default=True,
                    )
                    else False
                )
                self.wizard.post_cli_wizard(
                    post_id=post_id,
                    post_subreddit=post_subreddit,
                    show_comments=show_comments,
                    data_sort=bulk_data_sort,
                    data_limit=bulk_data_limit,
                    save_to_json=save_to_json,
                    save_to_csv=save_to_csv,
                )
            elif command == "posts":
                while True:
                    posts_option = Prompt.ask(
                        "[italic]Get posts from...[/]",
                        choices=["frontpage", "listing", "search", "back"],
                    )
                    if posts_option == "back":
                        break

                    posts_action = self.wizard.posts_cli_wizard(
                        posts_sort=bulk_data_sort,
                        posts_limit=bulk_data_limit,
                        save_to_json=save_to_json,
                    ).get(posts_option)

                    if posts_action:
                        posts_action()
