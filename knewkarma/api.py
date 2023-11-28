# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from typing import Union, Literal

import requests

from ._coreutils import log
from ._metadata import (
    DEFAULT_DATA_LIMIT,
    version,
)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


class Api:
    def __init__(self, base_reddit_endpoint: str, pypi_project_endpoint: str):
        """
        Initialise the API class with the base Reddit endpoint and the project's pypi endpoint.
        """
        self._base_reddit_endpoint = base_reddit_endpoint
        self._pypi_project_endpoint = pypi_project_endpoint

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    @staticmethod
    def _get_data(endpoint: str) -> Union[dict, list]:
        """
        Fetches JSON data from a given API endpoint asynchronously using aiohttp.

        :param endpoint: The API endpoint to fetch data from.
        :return: Returns JSON data as a dictionary or list. Returns an empty dict if fetching fails.
        """
        from sys import version as python_version

        try:
            with requests.Session() as session:
                with session.get(
                    endpoint,
                    headers={
                        "User-Agent": f"Knew-Karma/{version} "
                        f"(Python {python_version}; +https://about.me/rly0nheart)"
                    },
                ) as response:
                    if response.status_code == 200:
                        return response.json()
                    else:
                        log.error(f"An API error occurred: {response.json()}")
                        return {}
        except requests.exceptions.ConnectionError as error:
            log.error(f"An HTTP error occurred: {error}")
            return {}
        except Exception as error:
            log.critical(f"An unknown error occurred: {error}")
            return {}

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    @staticmethod
    def _validate_data(
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

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def get_updates(self):
        """
        Gets and compares the current program version with the remote version
        Assumes version format: major.minor.patch.prefix
        """
        import sys

        # Make a GET request to PyPI to get the project's latest release.
        response: dict = self._get_data(endpoint=self._pypi_project_endpoint)
        release: dict = self._validate_data(data=response.get("info", {}))

        if release:
            if release.get("name") != "knewkarma":
                log.critical(
                    f"PyPI project endpoint was modified "
                    f"{self._pypi_project_endpoint}: knewkarma/__init__.py: Line 7"
                )
                sys.exit()

            remote_version: str = release.get("version")
            # Splitting the version strings into components
            remote_parts: list = remote_version.split(".")
            local_parts: list = version.split(".")

            update_message: str = ""

            # Check for differences in version parts
            if remote_parts[0] != local_parts[0]:
                update_message = (
                    f"MAJOR update ({remote_version}) available."
                    f" It might introduce significant changes."
                )

            elif remote_parts[1] != local_parts[1]:
                update_message = (
                    f"MINOR update ({remote_version}) available."
                    f" Includes small feature changes/improvements."
                )

            elif remote_parts[2] != local_parts[2]:
                update_message = (
                    f"PATCH update ({remote_version}) available."
                    f" Generally for bug fixes and small tweaks."
                )

            elif (
                len(remote_parts) > 3
                and len(local_parts) > 3
                and remote_parts[3] != local_parts[3]
            ):
                update_message = (
                    f"BUILD update ({remote_version}) available."
                    f" Might be for specific builds or special versions."
                )

            if update_message:
                log.info(update_message)

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def get_profile(
        self,
        profile_source: str,
        profile_type: str = Literal["user_profile", "subreddit_profile"],
    ) -> dict:
        """
        Retrieves profile data from a specified source.

        :param profile_type: Type of profile to retrieve: Literal["user_profile", "subreddit_profile"].
        :param profile_source: source from where the profile should be retrieved: user/subreddit name.
        :return: A JSON object containing profile data.
        """
        profile_type_map: list = [
            (
                "user_profile",
                f"{self._base_reddit_endpoint}/user/{profile_source}/about.json",
            ),
            (
                "subreddit_profile",
                f"{self._base_reddit_endpoint}/r/{profile_source}/about.json",
            ),
        ]

        profile_endpoint: str = ""
        for type_name, type_endpoint in profile_type_map:
            if type_name == profile_type:
                profile_endpoint = type_endpoint

        profile: dict = self._get_data(endpoint=profile_endpoint)
        return self._validate_data(
            data=profile.get("data", {}), valid_key="created_utc"
        )

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def _paginate_posts(
        self,
        posts_endpoint: str,
        posts_limit: int = DEFAULT_DATA_LIMIT,
        after: str = None,
    ) -> list:
        """
        Paginates through posts data and retrieves posts until the specified limit is reached.

        :param posts_endpoint: API endpoint for retrieving posts.
        :param posts_limit: Limit on the number of posts to retrieve.
        :param after: The 'after' parameter to paginate through posts.
        :return: A list of posts.
        """
        all_posts = []
        use_after = posts_limit > 100  # Determine whether to use the 'after' parameter

        while len(all_posts) < posts_limit:
            # Make the API request with the 'after' parameter if it's provided and the limit is more than 100
            if use_after and after:
                endpoint_with_after = f"{posts_endpoint}&after={after}"
            else:
                endpoint_with_after = posts_endpoint

            posts_data: dict = self._get_data(endpoint=endpoint_with_after)
            posts_children: list = posts_data.get("data", {}).get("children", [])

            # If there are no more posts, break out of the loop
            if not posts_children:
                break

            all_posts.extend(self._validate_data(data=posts_children))
            after = all_posts[-1]["data"]["id"]

        return all_posts

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def get_posts(
        self,
        posts_limit: int = DEFAULT_DATA_LIMIT,
        posts_sort: str = Literal[
            "all",
            "controversial",
            "new",
            "top",
            "best",
            "hot",
            "rising",
        ],
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
        :param posts_sort: Criterion by which the posts should be sorted.
        :param posts_limit: Limit on the number of posts to retrieve.
        :return: A list of posts.
        """
        posts_type_map: list = [
            (
                "user_posts",
                f"{self._base_reddit_endpoint}/user/{posts_source}/submitted.json"
                f"?sort={posts_sort}&limit={posts_limit}",
            ),
            (
                "user_comments",
                f"{self._base_reddit_endpoint}/user/{posts_source}/comments.json"
                f"?sort={posts_sort}&limit={posts_limit}",
            ),
            (
                "subreddit_posts",
                f"{self._base_reddit_endpoint}/r/{posts_source}.json"
                f"?sort={posts_sort}&limit={posts_limit}",
            ),
            (
                "search_posts",
                f"{self._base_reddit_endpoint}/search.json"
                f"?q={posts_source}&sort={posts_sort}&limit={posts_limit}",
            ),
            (
                "listing_posts",
                f"{self._base_reddit_endpoint}/r/{posts_source}.json"
                f"?sort={posts_sort}&limit={posts_limit}",
            ),
            (
                "front_page_posts",
                f"{self._base_reddit_endpoint}/.json"
                f"?sort={posts_sort}&limit={posts_limit}",
            ),
        ]
        posts_endpoint: str = ""
        for type_name, type_endpoint in posts_type_map:
            if type_name == posts_type:
                posts_endpoint = type_endpoint

        all_posts = self._paginate_posts(posts_endpoint, posts_limit)

        # Return only the number of posts requested (posts_limit)
        return all_posts[:posts_limit]

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

    def get_post_data(
        self,
        subreddit: str,
        post_id: str,
        comments_limit: int = DEFAULT_DATA_LIMIT,
        comments_sort: str = Literal[
            "all", "controversial", "new", "top", "best", "hot", "rising"
        ],
    ) -> tuple:
        """
        Gets a post's data.

        :param subreddit: The subreddit in which the post was posted.
        :param post_id: ID of the post.
        :param comments_sort: Criterion by which the post's comments' will be sorted.
        :param comments_limit: Maximum of comments to fetch.
        :returns: A tuple of a post's data (raw_data, post_information, list_of_comments) if valid,
           otherwise return a tuple containing an empty dict, dict and list.
        """
        data: dict = self._get_data(
            endpoint=f"{self._base_reddit_endpoint}/r/{subreddit}/comments/{post_id}.json"
            f"?sort={comments_sort}&limit={comments_limit}"
        )
        return (
            self._validate_data(data=data, valid_key="upvote_ratio"),
            self._validate_data(
                data=data[0].get("data", {}).get("children", [])[0].get("data", {}),
                valid_key="upvote_ratio",
            ),
            self._validate_data(data=data[1].get("data", {}).get("children", [])),
        )

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
