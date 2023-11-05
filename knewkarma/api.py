from typing import Optional, Union

import requests

from . import __version__
from .coreutils import log
from .messages import message


class Api:
    def __init__(
        self,
        base_reddit_endpoint: str,
        base_github_api_endpoint: str,
    ):
        """
        Initialise the API class with various Reddit API endpoints.
        """
        self.updates_endpoint = (
            f"{base_github_api_endpoint}/repos/bellingcat/knewkarma/releases/latest"
        )
        # :param username: The Reddit username
        self.user_profile_endpoint = f"{base_reddit_endpoint}/user/%s/about.json"

        # :param username: The Reddit username
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of posts to fetch
        self.user_posts_endpoint = (
            f"{base_reddit_endpoint}/user/%s/submitted.json?sort=%s&limit=%s"
        )

        # :param username: The Reddit username
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of comments to fetch
        self.user_comments_endpoint = (
            f"{base_reddit_endpoint}/user/%s/comments.json?sort=%s&limit=%s"
        )

        # :param subreddit: The subreddit name
        self.subreddit_profile_endpoint = f"{base_reddit_endpoint}/r/%s/about.json"

        # :param subreddit: The subreddit name
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of posts to fetch
        self.subreddit_posts_endpoint = (
            f"{base_reddit_endpoint}/r/%s.json?sort=%s&limit=%s"
        )

        # :param subreddit: The subreddit name
        # :param post_id: The Reddit post ID
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of comments to fetch
        self.post_comments_endpoint = (
            f"{base_reddit_endpoint}/r/%s/comments/%s.json?sort=%s&limit=%s"
        )

        # :param query: Search query
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of search results to fetch
        self.search_endpoint = (
            f"{base_reddit_endpoint}/search.json?q=%s&sort=%s&limit=%s"
        )

        # :param limit: Number of popular posts to fetch
        self.post_listings_endpoint = (
            f"{base_reddit_endpoint}/r/%s.json?sort=%s&limit=%s"
        )

        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of front-page posts to fetch
        self.front_page_endpoint = f"{base_reddit_endpoint}/.json?sort=%s&limit=%s"

    @staticmethod
    def get_data(endpoint: str) -> Optional[Union[dict, list, None]]:
        """
        Fetches JSON data from a given API endpoint.

        :param endpoint: The API endpoint to fetch data from.
        :return: Returns JSON data as a dictionary or list. Returns None if fetching fails.
        """
        from sys import version as python_version

        try:
            with requests.Session() as session:
                with session.get(
                    url=endpoint,
                    headers={
                        "User-Agent": f"Knew-Karma/{__version__} "
                        f"(Python {python_version}; +https://about.me/rly0nheart)"
                    },
                ) as response:
                    if response.status_code == 200:
                        return response.json()
                    else:
                        error_message = response.json()
                        log.error(
                            message(
                                message_type="error",
                                message_key="api_error",
                                error_message=error_message,
                            )
                        )
        except requests.exceptions.RequestException as error:
            log.error(
                message(
                    message_type="error",
                    message_key="http_error",
                    error_message=error,
                )
            )
        except Exception as error:
            log.critical(
                message(
                    message_type="error",
                    message_key="unexpected_error",
                    error_message=error,
                )
            )

    @staticmethod
    def validate_data(
        data: Union[dict, list], valid_key: str = None
    ) -> Union[dict, list]:
        """
        Validates the input data. If it's a dictionary and a valid_key is provided,
        checks for the presence of the key in the dictionary. If it's a list, it
        ensures the list is not empty.

        :param data: The data to validate, which should be a dictionary, list or set.
        :param valid_key: The key to check for in the data if it's a dictionary.
        :return: The original data if valid, or an empty dictionary or list if invalid.
        """
        if isinstance(data, dict):
            if valid_key:
                return data if valid_key in data else {}
            else:
                return data  # Explicitly return the dictionary if valid_key is not provided
        elif isinstance(data, list):
            return data if data else []
        else:
            log.critical(
                message(
                    message_type="critical",
                    message_key="unknown_critical",
                    critical_message=f"Unknown data type ({type(data).__name__}), expected a list or dict.",
                )
            )

    def check_updates(self):
        """
        Checks if there's a new release of a project on GitHub.
        If there is, it shows a notification to the user about the release.
        """
        import os

        from plyer import notification

        from . import CURRENT_FILE_DIRECTORY

        # Make a GET request to the GitHub API to get the latest release of the project.
        response = self.get_data(endpoint=self.updates_endpoint)

        if response.get("tag_name"):
            remote_version = response.get("tag_name")

            # Check if the remote version tag matches the current version tag.
            if remote_version != __version__:
                # Set icon file to show in the desktop notification
                icon_file = "icon.ico" if os.name == "nt" else "icon.png"

                try:
                    # Notify user about the new release.
                    notification.notify(
                        title="Knew Karma",
                        message=message(
                            message_type="info",
                            message_key="update_found",
                            program_name="Knew Karma",
                            program_call_name="knewkarma",
                            release_version=remote_version,
                            current_version=__version__,
                        ),
                        app_icon=f"{os.path.join(CURRENT_FILE_DIRECTORY, 'icons', icon_file)}",
                        timeout=60,
                    )
                except NotImplementedError:  # Gets raised on Termux
                    log.info(
                        message(
                            message_type="info",
                            message_key="update_found",
                            program_name="Knew Karma",
                            program_call_name="knewkarma",
                            release_version=remote_version,
                            current_version=__version__,
                        )
                    )

    def get_user_profile(self, username: str) -> dict:
        """
        Gets a specified Reddit user's profile data.

        :param username: Username to query.
        :returns: A JSON object containing a user's profile if data is valid,
           otherwise return an empty dictionary.
        """
        data = self.get_data(endpoint=self.user_profile_endpoint % username)
        return self.validate_data(data=data.get("data"), valid_key="accept_followers")

    def get_subreddit_profile(self, subreddit: str) -> dict:
        """
        Gets a specified Reddit subreddit's profile data.

        :param subreddit: Subreddit to query.
        :returns: A JSON object containing a subreddit's profile if data is valid,
           otherwise return an empty dictionary.
        """
        data = self.get_data(endpoint=self.subreddit_profile_endpoint % subreddit)
        return self.validate_data(data=data.get("data"), valid_key="subscribers")

    def get_post_data(
        self, subreddit: str, post_id: str, sort: str, limit: int
    ) -> tuple:
        """
        Gets a post's data.

        :param subreddit: The subreddit in which the post was posted.
        :param post_id: ID of the post.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Maximum of comments to fetch.
        :returns: A tuple of a post's data (post_information, list_of_comments) if valid,
           otherwise return a tuple containing an empty dict and list.
        """
        data = self.get_data(
            endpoint=self.post_comments_endpoint % (subreddit, post_id, sort, limit)
        )
        return self.validate_data(
            data=data[0].get("data").get("children")[0].get("data"),
            valid_key="upvote_ratio",
        ), self.validate_data(data=data[1].get("data").get("children"))

    def get_posts(
        self,
        sort_criterion: str,
        posts_limit: int,
        posts_type: str,
        posts_source: str = None,
    ) -> list:
        posts_type_map = [
            (
                "user_posts",
                self.user_posts_endpoint % (posts_source, sort_criterion, posts_limit),
            ),
            (
                "user_comments",
                self.user_comments_endpoint
                % (posts_source, sort_criterion, posts_limit),
            ),
            (
                "subreddit_posts",
                self.subreddit_posts_endpoint
                % (posts_source, sort_criterion, posts_limit),
            ),
            (
                "search_posts",
                self.search_endpoint % (posts_source, sort_criterion, posts_limit),
            ),
            (
                "listing_posts",
                self.post_listings_endpoint
                % (posts_source, sort_criterion, posts_limit),
            ),
            (
                "front_page_posts",
                self.front_page_endpoint % (sort_criterion, posts_limit),
            ),
        ]
        posts_endpoint = None
        for post_type, endpoint in posts_type_map:
            if post_type == posts_type:
                posts_endpoint = endpoint

        posts = self.get_data(endpoint=posts_endpoint)

        return self.validate_data(data=posts.get("data").get("children"))
