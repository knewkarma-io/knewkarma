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

    def check_updates(self):
        """
        Checks if there's a new release of a project on GitHub.
        If there is, it shows a notification to the user about the release.
        """
        import os

        from plyer import notification

        from .coreutils import CURRENT_FILE_DIRECTORY

        # Make a GET request to the GitHub API to get the latest release of the project.
        response = self.get_data(endpoint=self.updates_endpoint)

        if response:
            remote_version = response.get("tag_name")

            # Check if the remote version tag matches the current version tag.
            if remote_version != __version__:
                # Set icon file to show in the desktop notification
                icon_file = "icon.ico" if os.name == "nt" else "icon.png"

                # Notify user about the new release.
                notification.notify(
                    title="Knew Karma",
                    message=message(
                        message_type="info",
                        message_key="update",
                        program_name="Knew Karma",
                        program_call_name="knewkarma",
                        release_version=remote_version,
                    ),
                    app_icon=f"{os.path.join(CURRENT_FILE_DIRECTORY, 'icons', icon_file)}",
                    timeout=20,
                )

    def get_user_profile(self, username: str) -> dict:
        """
        Gets a specified Reddit user's profile data.

        :param username: Username to query.
        :returns: A JSON object containing a user's profile if data is valid,
           otherwise return an empty dictionary.
        """
        data = self.get_data(endpoint=self.user_profile_endpoint % username)
        return data.get("data") if data else {}

    def get_user_posts(self, username: str, sort: str, limit: int) -> list:
        """
        Gets a specified Reddit user's posts.

        :param username: Username to query.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Number of posts to fetch.
        :returns: A list of JSON objects containing post if data is valid,
           otherwise return an empty list.
        """
        posts = self.get_data(
            endpoint=self.user_posts_endpoint % (username, sort, limit)
        )
        return posts.get("data").get("children") if posts else []

    def get_user_comments(self, username: str, sort: str, limit: int) -> list:
        """
        Gets a specified Reddit user's comments.

        :param username: Username to query.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Number of comments to fetch.
        :returns: A list of JSON objects containing comments' data if valid,
           otherwise return an empty list.
        """
        comments = self.get_data(
            endpoint=self.user_comments_endpoint % (username, sort, limit)
        )
        return comments.get("data").get("children") if comments else []

    def get_subreddit_profile(self, subreddit: str) -> dict:
        """
        Gets a specified Reddit subreddit's profile data.

        :param subreddit: Subreddit to query.
        :returns: A JSON object containing a subreddit's profile if data is valid,
           otherwise return an empty dictionary.
        """
        data = self.get_data(endpoint=self.subreddit_profile_endpoint % subreddit)
        return data.get("data") if data else {}

    def get_subreddit_posts(self, subreddit: str, sort: str, limit: int) -> list:
        """
        Gets a specified Subreddit's posts.

        :param subreddit: Subreddit to query.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Number of posts to fetch.
        :returns: A list of JSON objects containing posts' data if valid,
           otherwise return an empty list.
        """
        posts = self.get_data(
            endpoint=self.subreddit_posts_endpoint % (subreddit, sort, limit)
        )
        return posts.get("data").get("children") if posts else []

    def get_search_results(self, query: str, sort: str, limit: int):
        """
        Gets posts that match a user-provided query.

        :param query: Search query
        :param sort: Posts' sorting criterion.
        :param limit: Maximum number of posts to return.
        """
        results = self.get_data(self.search_endpoint % (query, sort, limit))
        return results.get("data").get("children")

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
        return (
            (
                data[0].get("data").get("children")[0].get("data"),
                data[1].get("data").get("children") if data else exit(),
            )
            if data[0] or data[1]
            else ({}, [])
        )

    def get_post_listings(self, listing: str, sort: str, limit: int) -> list:
        """
        Gets posts from a specified listing.

        :param listing: Listing to get posts from
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Maximum of comments to fetch.
        :returns: A list of JSON objects containing posts' data if valid,
           otherwise return an empty list.
        """
        posts = self.get_data(
            endpoint=self.post_listings_endpoint % (listing, sort, limit)
        )
        return posts.get("data").get("children") if posts else []

    def get_front_page_posts(self, sort: str, limit: int) -> list:
        """
        Gets posts from the Reddit front-page.

        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Maximum of comments to fetch.
        :returns: A list of JSON objects containing posts' data if valid,
           otherwise return an empty list.
        """
        posts = self.get_data(endpoint=self.front_page_endpoint % (sort, limit))
        return posts.get("data").get("children") if posts else []
