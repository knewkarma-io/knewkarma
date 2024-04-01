import asyncio
from random import randint
from sys import version as python_version
from typing import Union, Literal

import aiohttp
from rich.markdown import Markdown

from ._utils import console
from .version import Version

SORT_CRITERION = Literal[
    "controversial",
    "new",
    "top",
    "best",
    "hot",
    "rising",
]

DATA_LISTING = Literal["best", "controversial", "popular", "rising"]
DATA_TIMEFRAME = Literal["hour", "day", "week", "month", "year"]
TIME_FORMAT = Literal["concise", "datetime"]


class Api:
    """Represents the Knew Karma API and provides methods for getting various data from the Reddit API."""

    def __init__(self):
        self.base_reddit_endpoint: str = "https://www.reddit.com"
        self._user_data_endpoint: str = f"{self.base_reddit_endpoint}/u"
        self._users_data_endpoint: str = f"{self.base_reddit_endpoint}/users"
        self.subreddit_data_endpoint: str = f"{self.base_reddit_endpoint}/r"
        self._subreddits_data_endpoint: str = f"{self.base_reddit_endpoint}/subreddits"
        self._github_release_endpoint: str = (
            "https://api.github.com/repos/bellingcat/knewkarma/releases/latest"
        )

    @staticmethod
    async def get_data(
        session: aiohttp.ClientSession, endpoint: str
    ) -> Union[dict, list]:
        """
        Asynchronously fetches JSON data from a given API endpoint.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param endpoint: The API endpoint to fetch data from.
        :type endpoint: str
        :return: Returns JSON data as a dictionary or list. Returns an empty dict if fetching fails.
        :rtype: Union[dict, list]
        """
        try:
            async with session.get(
                endpoint,
                headers={
                    "User-Agent": f"Knew-Karma/{Version.release} "
                    f"(Python {python_version}; +https://knewkarma-wiki.readthedocs.io)"
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.json()
                    console.log(f"[red]✘[/] An API error occurred: {error_message}")
                    return {}

        except aiohttp.ClientConnectionError as error:
            console.log(f"[red]✘[/] An HTTP error occurred: {error}")
            return {}
        except Exception as error:
            console.log(f"[red]✘[/] An unknown error occurred: {error}")
            return {}

    @staticmethod
    def _process_response(
        response_data: Union[dict, list], valid_key: str = None
    ) -> Union[dict, list]:
        """
        Processes and validates the API response data.

        If it's a dictionary and a valid_key is provided,
        checks for the presence of the key in the response dictionary.

        If it's a list, it ensures the list is not empty.

        :param response_data: The API response data to validate, which should be a dictionary or list.
        :type response_data: Union[dict, list]
        :param valid_key: The key to check for in the data if it's a dictionary.
        :type valid_key: str
        :return: The original data if valid, or an empty dictionary or list if invalid.
        :rtype: Union[dict, list]
        """
        if isinstance(response_data, dict):
            if valid_key:
                return response_data if valid_key in response_data else {}
            else:
                return response_data
        elif isinstance(response_data, list):
            return response_data if response_data else []
        else:
            console.log(
                f"Unknown data type ({response_data}: {type(response_data)}), expected a list or dict."
            )

    async def get_updates(self, session: aiohttp.ClientSession):
        """
        Asynchronously gets and compares the current program version with the remote version.

        Assumes version format: major.minor.patch.prefix

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        # Make a GET request to PyPI to get the project's latest release.
        response: dict = await self.get_data(
            endpoint=self._github_release_endpoint, session=session
        )
        release: dict = self._process_response(
            response_data=response, valid_key="tag_name"
        )

        if release:
            remote_version: str = release.get("tag_name")
            markup_release_notes: str = release.get("body")
            markdown_release_notes = Markdown(markup=markup_release_notes)

            # Splitting the version strings into components
            remote_parts: list = remote_version.split(".")

            update_message: str = f"%s update ({remote_version}) available"

            # Check for differences in version parts
            if remote_parts[0] != Version.major:
                update_message = update_message % "MAJOR"

            elif remote_parts[1] != Version.minor:
                update_message = update_message % "MINOR"

            elif remote_parts[2] != Version.patch:
                update_message = update_message % "PATCH"

            if update_message:
                console.log(update_message)
                console.log(markdown_release_notes)

    async def get_profile(
        self,
        profile_source: str,
        profile_type: Literal["user", "subreddit"],
        session: aiohttp.ClientSession,
    ) -> dict:
        """
        Asynchronously fetches a profile from the specified source.

        :param profile_source: Source to get profile data from.
        :type profile_source: str
        :param profile_type: The type of profile that is to be fetched.
        :type profile_type: str
        :param session: aiohttp session to use for the request.
        :return: A dictionary object containing profile data from the specified source.
        :rtype: dict
        """
        # Use a dictionary for direct mapping
        profile_mapping: dict = {
            "user": f"{self._user_data_endpoint}/{profile_source}/about.json",
            "subreddit": f"{self.subreddit_data_endpoint}/{profile_source}/about.json",
        }

        # Get the endpoint directly from the dictionary
        endpoint: str = profile_mapping.get(profile_type, "")

        profile_data = await self.get_data(endpoint=endpoint, session=session)
        return self._process_response(
            response_data=profile_data.get("data", {}), valid_key="created_utc"
        )

    async def _paginate(
        self,
        session: aiohttp.ClientSession,
        endpoint: str,
        process_func: callable,
        limit: int,
    ) -> list[dict]:
        """
        Asynchronously fetches and processes data in a paginated manner
        from a specified endpoint until the specified limit
        of items is reached or there are no more items to fetch. It uses a specified processing function
        to handle the data from each request, ensuring no duplicates are returned.

        :param session: An Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param endpoint: Endpoint to get paginated data from.
        :type endpoint: str
        :param process_func: A callable function for processing response data.
        :type process_func: callable
        :param limit: Maximum number of results to return.
        :type limit: int
        :return: A list of dict objects, each containing paginated data.
        :rtype: list[dict]
        """
        all_items = []
        last_item_id = None
        while len(all_items) < limit:
            paginated_endpoint = (
                f"{endpoint}&after={last_item_id}&count={len(all_items)}"
                if last_item_id
                else endpoint
            )

            response = await self.get_data(session=session, endpoint=paginated_endpoint)
            items = response.get("data", {}).get("children", [])

            if not items:
                break

            processed_items = process_func(response_data=items)
            items_to_limit = limit - len(all_items)
            all_items.extend(processed_items[:items_to_limit])

            last_item_id = response.get("data").get("after")

            if len(all_items) == limit:
                break

            sleep_delay: int = randint(1, 10)
            console.log(
                f"[green]✔[/] Fetched {len(all_items)}/{limit} items so far. Resuming in {sleep_delay} seconds...",
            )
            await asyncio.sleep(sleep_delay)

        console.log(f"[green]✔[/] Successfully fetched {len(all_items)}/{limit} items!")
        return all_items

    async def get_posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        posts_type: Literal[
            "new_posts",
            "front_page_posts",
            "listing_posts",
            "subreddit_posts",
            "user_posts",
            "user_overview",
            "user_comments",
        ],
        posts_source: str = None,
        timeframe: DATA_TIMEFRAME = "all",
        sort: SORT_CRITERION = "all",
    ) -> list[dict]:
        """
        Asynchronously gets a specified number of posts, with a specified sorting criterion, from the specified source.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to get.
        :type limit: int
        :param posts_type: Type of posts to be fetched.
        :type posts_type: str
        :param posts_source: Source from where posts will be fetched.
        :type posts_source: str
        :param sort: Posts' sort criterion.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str

        :return: A list of dictionaries, each containing data of a post.
        :rtype: list[dict]
        """
        source_map = {
            "new_posts": f"{self.base_reddit_endpoint}/new.json",
            "front_page_posts": f"{self.base_reddit_endpoint}/.json",
            "listing_posts": f"{self.subreddit_data_endpoint}/{posts_source}.json?",
            "subreddit_posts": f"{self.subreddit_data_endpoint}/{posts_source}.json",
            "user_posts": f"{self._user_data_endpoint}/{posts_source}/submitted.json",
            "user_overview": f"{self._user_data_endpoint}/{posts_source}/overview.json",
            "user_comments": f"{self._user_data_endpoint}/{posts_source}/comments.json",
        }

        endpoint = source_map.get(posts_type, "")
        if posts_type == "new_posts":
            endpoint += f"?limit={limit}&sort={sort}&raw_json=1"
        else:
            endpoint += f"?limit={limit}&sort={sort}&t={timeframe}&raw_json=1"

        posts: list[dict] = await self._paginate(
            session=session,
            endpoint=endpoint,
            process_func=self._process_response,
            limit=limit,
        )

        return posts

    async def get_search_results(
        self,
        session: aiohttp.ClientSession,
        search_type: Literal["users", "subreddits", "posts"],
        query: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: DATA_TIMEFRAME = "all",
    ) -> list[dict]:
        """
        Asynchronously searches from a specified results type that match the specified query.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param search_type: Type of results to get.
        :type search_type: str
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of results to get.
        :type limit: int
        :param sort: Posts' sort criterion.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: str
        """
        search_mapping: dict = {
            "users": f"{self._users_data_endpoint}/search.json",
            "subreddits": f"{self._subreddits_data_endpoint}/search.json",
            "posts": f"{self.base_reddit_endpoint}/search.json",
        }

        endpoint = search_mapping.get(search_type, "")
        if search_type == "posts":
            endpoint += f"?q={query}&limit={limit}&sort={sort}&t={timeframe}"
        else:
            endpoint += f"?q={query}&limit={limit}"

        search_results: list[dict] = await self._paginate(
            session=session,
            endpoint=endpoint,
            process_func=self._process_response,
            limit=limit,
        )

        return search_results

    async def get_subreddits(
        self,
        subreddits_type: Literal["all", "default", "new", "popular"],
        limit: int,
        session: aiohttp.ClientSession,
    ) -> list[dict]:
        """
        Asynchronously gets the specified type of subreddits.

        :param subreddits_type: Type of subreddits to get.
        :type subreddits_type: str
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        subreddits_mapping: dict = {
            "all": f"{self._subreddits_data_endpoint}.json",
            "default": f"{self._subreddits_data_endpoint}/default.json",
            "new": f"{self._subreddits_data_endpoint}/new.json",
            "popular": f"{self._subreddits_data_endpoint}/popular.json",
        }

        endpoint = subreddits_mapping.get(subreddits_type, "")
        endpoint += f"?limit={limit}"

        subreddits: list[dict] = await self._paginate(
            session=session,
            endpoint=endpoint,
            process_func=self._process_response,
            limit=limit,
        )

        return subreddits
