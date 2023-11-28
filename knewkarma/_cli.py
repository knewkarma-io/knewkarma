# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import argparse

from ._masonry import Masonry


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class Cli:
    def __init__(self, arguments: argparse, tree_masonry: Masonry):
        # +++++++++++++++++++++++++++++++++++++++++++++++++++ #

        self._arguments = arguments

        # +++++++++++++++++++++++++++++++++++++++++++++++++++ #

        data_limit: int = arguments.data_limit
        data_sort: str = arguments.sort_criterion
        save_to_json: bool = arguments.json
        save_to_csv: bool = arguments.csv

        # +++++++++++++++++++++++++++++++++++++++++++++++++++ #

        self.argument_mapping: dict = {
            "user": {
                "profile": lambda: tree_masonry.profile_tree(
                    profile_type="user_profile",
                    profile_source=arguments.username,
                    save_to_json=save_to_json,
                    save_to_csv=save_to_csv,
                ),
                "posts": lambda: tree_masonry.posts_tree(
                    posts_type="user_posts",
                    posts_source=arguments.username,
                    posts_limit=data_limit,
                    sort_criterion=data_sort,
                    save_to_json=save_to_json,
                ),
                "comments": lambda: tree_masonry.user_comments_tree(
                    username=arguments.username,
                    comments_limit=data_limit,
                    sort_criterion=data_sort,
                    save_to_json=save_to_json,
                ),
            },
            "subreddit": {
                "profile": lambda: tree_masonry.profile_tree(
                    profile_type="subreddit_profile",
                    profile_source=arguments.subreddit,
                    save_to_json=save_to_json,
                    save_to_csv=save_to_csv,
                ),
                "posts": lambda: tree_masonry.posts_tree(
                    posts_type="subreddit_posts",
                    posts_source=arguments.subreddit,
                    show_author=True,
                    posts_limit=data_limit,
                    sort_criterion=data_sort,
                    save_to_json=save_to_json,
                ),
            },
            "posts": {
                "front_page": lambda: tree_masonry.posts_tree(
                    posts_type="front_page_posts",
                    show_author=True,
                    posts_limit=data_limit,
                    sort_criterion=data_sort,
                    save_to_json=save_to_json,
                ),
                "listing": lambda: tree_masonry.posts_tree(
                    posts_type="listing_posts",
                    posts_source=arguments.listing,
                    show_author=True,
                    posts_limit=data_limit,
                    sort_criterion=data_sort,
                    save_to_json=save_to_json,
                ),
            },
            "post": lambda: tree_masonry.post_data_tree(
                post_id=arguments.post_id,
                post_subreddit=arguments.post_subreddit,
                comments_limit=data_limit,
                comments_sort=data_sort,
                save_to_json=save_to_json,
            ),
            "search": lambda: tree_masonry.posts_tree(
                posts_type="search_posts",
                posts_source=arguments.query,
                show_author=True,
                posts_limit=data_limit,
                sort_criterion=data_sort,
                save_to_json=save_to_json,
            ),
        }

    # +++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def execute_cli(self):
        """
        Determines the operation mode based on command-line arguments or interactive input,
        and executes the corresponding handler function.
        """
        import asyncio
        from typing import Union, Callable

        from ._coreutils import log

        if self._arguments.mode in self.argument_mapping:
            mode_action: Union[dict, Callable] = self.argument_mapping.get(
                self._arguments.mode
            )
            if isinstance(mode_action, dict):
                for action_name, action_function in mode_action.items():
                    if getattr(self._arguments, action_name) and hasattr(
                        self._arguments, action_name
                    ):
                        asyncio.run(action_function())
                        break
                    else:
                        log.warning(
                            f"knewkarma {self._arguments.mode}: missing one or more expected argument(s): "
                            f"{list(mode_action.keys())}"
                        )
                        break
            elif callable(mode_action):
                asyncio.run(mode_action())
            else:
                log.critical(
                    f"Unknown action type for {mode_action}: {type(mode_action).__name__}. "
                    f"Expected Dict or Callable."
                )

    # +++++++++++++++++++++++++++++++++++++++++++++++++++ #
