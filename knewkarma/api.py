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

    def get_updates(self):
        """
        Gets and compares the remote version with the local version.
        Assumes version format: major.minor.patch.prefix
        """
        import os
        import sys
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
                sys.exit()

            remote_version: str = release.get("version")
            # Splitting the version strings into components
            remote_parts = remote_version.split('.')
            local_parts = __version__.split('.')

            update_message: str = ""
            notification_timeout: int = 0
            icon_file: str = "icon.ico" if os.name == "nt" else "icon.png"

            # Check for differences in version parts
            if remote_parts[0] != local_parts[0]:
                update_message = (f"MAJOR update ({remote_version}) available."
                                  f" It might introduce significant changes.")
                notification_timeout = 60
            elif remote_parts[1] != local_parts[1]:
                update_message = (f"MINOR update ({remote_version}) available."
                                  f" Includes small feature changes/improvements.")
                notification_timeout = 50
            elif remote_parts[2] != local_parts[2]:
                update_message = (f"PATCH update ({remote_version}) available."
                                  f" Generally for bug fixes and small tweaks.")
                notification_timeout = 30
            elif len(remote_parts) > 3 and len(local_parts) > 3 and remote_parts[3] != local_parts[3]:
                update_message = (f"BUILD update ({remote_version}) available."
                                  f" Might be for specific builds or special versions.")
                notification_timeout = 15

            try:
                # Catch and ignore all warnings (specific warning is at:
                # https://github.com/kivy/plyer/blob/
                # 8c0e11ff2e356ea677e96b0d7907d000c8f4bbd0/plyer/platforms/linux/notification.py#L99C8-L99C8)
                with warnings.catch_warnings():
                    warnings.simplefilter("ignore")

                    # Notify user about the new release.
                    notification.notify(
                        update_message,
                        app_icon=f"{os.path.join(CURRENT_FILE_DIRECTORY, 'icons', icon_file)}",
                        timeout=notification_timeout,
                    )
            except NotImplementedError:  # Gets raised on systems that do not have a desktop environment
                log.info(update_message)

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

        profile_endpoint: str = ""
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
        posts_endpoint: str = ""
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
