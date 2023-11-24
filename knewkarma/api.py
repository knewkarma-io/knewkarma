from typing import Union, Literal

import requests

from . import __version__
from .coreutils import log


class Api:
    def __init__(self, base_reddit_endpoint: str):
        """
        Initialise the API class with the base Reddit endpoint.
        """
        self.base_reddit_endpoint = base_reddit_endpoint

    @staticmethod
    def get_data(endpoint: str) -> Union[dict, list]:
        """
        Fetches JSON data from a given API endpoint.

        :param endpoint: The API endpoint to fetch data from.
        :return: Returns JSON data as a dictionary or list. Returns an empty dict if fetching fails.
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
                        error_message: dict = response.json()
                        log.error(f"An API error occurred: {error_message}")
                        return {}
        except requests.exceptions.RequestException as error:
            log.error(f"An HTTP error occurred: {error}")
            return {}
        except Exception as error:
            log.critical(f"An unknown error occurred: {error}")
            return {}

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
                f"Unknown data type ({data}: {type(data).__name__}), expected a list or dict."
            )

    def check_updates(self):
        """
        Checks if there's a new release of a project on GitHub.
        If there is, it shows a notification to the user about the release.
        """
        import os
        import warnings

        from plyer import notification

        from . import CURRENT_FILE_DIRECTORY, __pypi_project_endpoint__

        # Make a GET request to PyPI to get the project's latest release.
        response: dict = self.get_data(endpoint=__pypi_project_endpoint__)
        release: dict = self.validate_data(data=response.get("info", {}))

        if release:
            if release.get("name") != "knewkarma":
                log.critical(
                    f"PyPI project endpoint was modified "
                    f"{__pypi_project_endpoint__}: knewkarma/__init__.py: Line 20"
                )
                exit()

            remote_version: str = release.get("version")
            update_notice: str = (
                f"A new release of Knew Karma is available (from {__version__} to {remote_version}). "
                f"To update, run: pip install --upgrade {release.get('name')}"
            )
            # Check if the remote version tag matches the current version tag.
            if remote_version != __version__:
                # Set icon file to show in the desktop notification
                icon_file: str = "icon.ico" if os.name == "nt" else "icon.png"
                try:
                    # Catch and ignore all warnings (specific warning is at:
                    # https://github.com/kivy/plyer/blob/
                    # 8c0e11ff2e356ea677e96b0d7907d000c8f4bbd0/plyer/platforms/linux/notification.py#L99C8-L99C8)
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")

                        # Notify user about the new release.
                        notification.notify(
                            update_notice,
                            app_icon=f"{os.path.join(CURRENT_FILE_DIRECTORY, 'icons', icon_file)}",
                            timeout=60,
                        )
                except (
                        NotImplementedError
                ):  # Gets raised on Termux and Raspbian (so far).
                    log.info(update_notice)

    def get_profile(
            self,
            profile_source: str,
            profile_type: str = Literal["user_profile", "subreddit_profile"],
    ) -> dict:
        """
        Retrieves profile data from a specified source.

        :param profile_type: Type of profile to retrieve.
        :param profile_source: source from where the profile should be retrieved.
        :return: A JSON object containing profile data.
        """
        profile_type_map: list = [
            (
                "user_profile",
                f"{self.base_reddit_endpoint}/user/{profile_source}/about.json",
            ),
            (
                "subreddit_profile",
                f"{self.base_reddit_endpoint}/r/{profile_source}/about.json",
            ),
        ]

        profile_endpoint = None
        for type_name, type_endpoint in profile_type_map:
            if type_name == profile_type:
                profile_endpoint = type_endpoint

        profile: dict = self.get_data(endpoint=profile_endpoint)
        return self.validate_data(data=profile.get("data", {}), valid_key="created_utc")

    def get_posts(
            self,
            posts_sort_criterion: str,
            posts_limit: int,
            posts_type: str = Literal[
                "user_posts",
                "user_comments",
                "subreddit_posts",
                "search_posts",
                "listing_posts",
                "front_page_posts",
            ],
            posts_source: str = None,
    ) -> list:
        """
        Retrieves posts from a specified source.

        :param posts_type: Type of posts to retrieve.
        :param posts_source: Source from where the posts should be retrieved.
        :param posts_sort_criterion: Criterion by which the posts should be sorted.
        :param posts_limit: Limit on the number of posts to retrieve.
        :return: A list of posts.
        """
        posts_type_map: list = [
            (
                "user_posts",
                f"{self.base_reddit_endpoint}/user/{posts_source}/submitted.json"
                f"?sort={posts_sort_criterion}&limit={posts_limit}",
            ),
            (
                "user_comments",
                f"{self.base_reddit_endpoint}/user/{posts_source}/comments.json"
                f"?sort={posts_sort_criterion}&limit={posts_limit}",
            ),
            (
                "subreddit_posts",
                f"{self.base_reddit_endpoint}/r/{posts_source}.json"
                f"?sort={posts_sort_criterion}&limit={posts_limit}",
            ),
            (
                "search_posts",
                f"{self.base_reddit_endpoint}/search.json"
                f"?q={posts_source}&sort={posts_sort_criterion}&limit={posts_limit}",
            ),
            (
                "listing_posts",
                f"{self.base_reddit_endpoint}/r/{posts_source}.json"
                f"?sort={posts_sort_criterion}&limit={posts_limit}",
            ),
            (
                "front_page_posts",
                f"{self.base_reddit_endpoint}/.json"
                f"?sort={posts_sort_criterion}&limit={posts_limit}",
            ),
        ]
        posts_endpoint = None
        for type_name, type_endpoint in posts_type_map:
            if type_name == posts_type:
                posts_endpoint = type_endpoint

        posts: dict = self.get_data(endpoint=posts_endpoint)

        return self.validate_data(data=posts.get("data", {}).get("children", []))

    def get_post_data(
            self,
            subreddit: str,
            post_id: str,
            comments_sort_criterion: str,
            comments_limit: int,
    ) -> tuple:
        """
        Gets a post's data.

        :param subreddit: The subreddit in which the post was posted.
        :param post_id: ID of the post.
        :param comments_sort_criterion: Criterion by which the post's comments' will be sorted.
        :param comments_limit: Maximum of comments to fetch.
        :returns: A tuple of a post's data (raw_data, post_information, list_of_comments) if valid,
           otherwise return a tuple containing an empty dict, dict and list.
        """
        data: dict = self.get_data(
            endpoint=f"{self.base_reddit_endpoint}/r/{subreddit}/comments/{post_id}.json"
                     f"?sort={comments_sort_criterion}&limit={comments_limit}"
        )
        return (
            self.validate_data(data=data, valid_key="upvote_ratio"),
            self.validate_data(
                data=data[0].get("data", {}).get("children", [])[0].get("data", {}),
                valid_key="upvote_ratio",
            ),
            self.validate_data(data=data[1].get("data", {}).get("children", [])),
        )
