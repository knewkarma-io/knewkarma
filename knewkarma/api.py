from typing import Optional, Union

import aiohttp

from .coreutils import log
from .messages import message


class API:
    BASE_ENDPOINT = "https://www.reddit.com"
    USER_DATA_ENDPOINT = f"{BASE_ENDPOINT}/user"
    SUBREDDIT_DATA_ENDPOINT = f"{BASE_ENDPOINT}/r"

    def __init__(self):
        """
        Initialise the API class with various Reddit API endpoints.
        """
        self.updates_endpoint = (
            "https://api.github.com/repos/bellingcat/knewkarma/releases/latest"
        )
        # :param username: The Reddit username
        self.user_profile_endpoint = f"{API.USER_DATA_ENDPOINT}/%s/about.json"

        # :param username: The Reddit username
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of posts to fetch
        self.user_posts_endpoint = (
            f"{API.USER_DATA_ENDPOINT}/%s/submitted.json?sort=%s&limit=%s"
        )

        # :param username: The Reddit username
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of comments to fetch
        self.user_comments_endpoint = (
            f"{API.USER_DATA_ENDPOINT}/%s/comments.json?sort=%s&limit=%s"
        )

        # :param subreddit: The subreddit name
        self.subreddit_profile_endpoint = f"{API.SUBREDDIT_DATA_ENDPOINT}/%s/about.json"

        # :param subreddit: The subreddit name
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of posts to fetch
        self.subreddit_posts_endpoint = (
            f"{API.SUBREDDIT_DATA_ENDPOINT}/%s.json?sort=%s&limit=%s"
        )

        # :param subreddit: The subreddit name
        # :param post_id: The Reddit post ID
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of comments to fetch
        self.post_comments_endpoint = (
            f"{API.SUBREDDIT_DATA_ENDPOINT}/%s/comments/%s.json?sort=%s&limit=%s"
        )

        # :param query: Search query
        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of search results to fetch
        self.search_endpoint = f"{API.BASE_ENDPOINT}/search.json?q=%s&sort=%s&limit=%s"

        # :param limit: Number of popular posts to fetch
        self.post_listings_endpoint = (
            f"{API.SUBREDDIT_DATA_ENDPOINT}/%s.json?sort=%s&limit=%s"
        )

        # :param sort: Sorting criterion ('new', 'hot', etc.)
        # :param limit: Number of front-page posts to fetch
        self.front_page_endpoint = f"{API.BASE_ENDPOINT}/.json?sort=%s&limit=%s"

    @staticmethod
    async def get_data(endpoint: str) -> Optional[Union[dict, list, None]]:
        """
        Asynchronously fetches JSON data from a given API endpoint.

        :param endpoint: The API endpoint to fetch data from.
        :return: Returns JSON data as a dictionary or list. Returns None if fetching fails.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(endpoint) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        error_message = await response.json()
                        log.error(
                            message(
                                message_type="error",
                                message_key="api_error",
                                error_message=error_message,
                            )
                        )
        except aiohttp.ClientError as e:
            log.error(
                message(
                    message_type="error",
                    message_key="http_error",
                    error_message=str(e),
                )
            )
        except Exception as e:
            log.critical(
                message(
                    message_type="error",
                    message_key="unexpected_error",
                    error_message=str(e),
                )
            )

    async def get_updates(self):
        """
        This function checks if there's a new release of a project on GitHub.
        If there is, it shows a notification to the user about the release.
        """
        from . import __version__
        from plyer import notification

        # Make a GET request to the GitHub API to get the latest release of the project.
        response = await self.get_data(endpoint=self.updates_endpoint)

        if response:
            remote_version = response.get("tag_name")

            # Check if the remote version tag matches the current version tag.
            if remote_version != __version__:
                # Notify user about the new release.
                notification.notify(
                    title=f"Knew Karma",
                    message=message(
                        message_type="info", message_key="update", version=__version__
                    ),
                    timeout=20,
                )

    async def get_user_profile(self, username: str) -> dict:
        """
        Asynchronously gets a specified Reddit user's profile data.

        :param username: Username to query.
        :returns: A JSON object containing a user's profile if data is valid,
           otherwise return an empty dictionary.
        """
        data = await self.get_data(endpoint=self.user_profile_endpoint % username)
        return data.get("data") if data else {}

    async def get_user_posts(self, username: str, sort: str, limit: int) -> list:
        """
        Asynchronously gets a specified Reddit user's posts.

        :param username: Username to query.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Number of posts to fetch.
        :returns: A list of JSON objects containing post if data is valid,
           otherwise return an empty list.
        """
        posts = await self.get_data(
            endpoint=self.user_posts_endpoint % (username, sort, limit)
        )
        return posts.get("data").get("children") if posts else []

    async def get_user_comments(self, username: str, sort: str, limit: int) -> list:
        """
        Asynchronously gets a specified Reddit user's comments.

        :param username: Username to query.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Number of comments to fetch.
        :returns: A list of JSON objects containing comments' data if valid,
           otherwise return an empty list.
        """
        comments = await self.get_data(
            endpoint=self.user_comments_endpoint % (username, sort, limit)
        )
        return comments.get("data").get("children") if comments else []

    async def get_subreddit_profile(self, subreddit: str) -> dict:
        """
        Asynchronously gets a specified Reddit subreddit's profile data.

        :param subreddit: Subreddit to query.
        :returns: A JSON object containing a subreddit's profile if data is valid,
           otherwise return an empty dictionary.
        """
        data = await self.get_data(endpoint=self.subreddit_profile_endpoint % subreddit)
        return data.get("data") if data else {}

    async def get_subreddit_posts(self, subreddit: str, sort: str, limit: int) -> list:
        """
        Asynchronously gets a specified Subreddit's posts.

        :param subreddit: Subreddit to query.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Number of posts to fetch.
        :returns: A list of JSON objects containing posts' data if valid,
           otherwise return an empty list.
        """
        posts = await self.get_data(
            endpoint=self.subreddit_posts_endpoint % (subreddit, sort, limit)
        )
        return posts.get("data").get("children") if posts else []

    async def search(self, query: str, sort: str, limit: int):
        results = await self.get_data(self.search_endpoint % (query, sort, limit))
        return results.get("data").get("children")

    async def get_post_data(
        self, subreddit: str, post_id: str, sort: str, limit: int
    ) -> tuple:
        """
        Asynchronously gets a post's data.

        :param subreddit: The subreddit in which the post was posted.
        :param post_id: ID of the post.
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Maximum of comments to fetch.
        :returns: A tuple of a post's data (post_information, list_of_comments) if valid,
           otherwise return a tuple containing an empty dict and list.
        """
        post_comments_endpoint = (
            f"{API.SUBREDDIT_DATA_ENDPOINT}/%s/comments/%s.json?sort=%s&limit=%s"
        )
        data = await self.get_data(
            endpoint=post_comments_endpoint % (subreddit, post_id, sort, limit)
        )

        return (
            (
                data[0].get("data").get("children")[0].get("data"),
                data[1].get("data").get("children") if data else exit(),
            )
            if data[0] or data[1]
            else ({}, [])
        )

    async def get_post_listings(self, listing: str, sort: str, limit: int) -> list:
        """
        Asynchronously gets posts from a specified listing.

        :param listing: Listing to get posts from
        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Maximum of comments to fetch.
        :returns: A list of JSON objects containing posts' data if valid,
           otherwise return an empty list.
        """
        posts = await self.get_data(
            endpoint=self.post_listings_endpoint % (listing, sort, limit)
        )
        return posts.get("data").get("children") if posts else []

    async def get_front_page_posts(self, sort: str, limit: int) -> list:
        """
        Asynchronously gets posts from the Reddit front-page.

        :param sort: Sorting criterion ('new', 'hot', etc.).
        :param limit: Maximum of comments to fetch.
        :returns: A list of JSON objects containing posts' data if valid,
           otherwise return an empty list.
        """
        posts = await self.get_data(endpoint=self.front_page_endpoint % (sort, limit))
        return posts.get("data").get("children") if posts else []
