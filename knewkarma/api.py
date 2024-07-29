import asyncio
from random import randint
from sys import version as python_version
from typing import Union, Literal

import aiohttp
from rich.markdown import Markdown

from .help import Help
from .tools.general_utils import console
from .tools.time_utils import countdown_timer
from .version import Version

__all__ = ["Api", "python_version", "SORT_CRITERION", "TIMEFRAME", "TIME_FORMAT"]

SORT_CRITERION = Literal["controversial", "new", "top", "best", "hot", "rising", "all"]
TIMEFRAME = Literal["hour", "day", "week", "month", "year", "all"]
TIME_FORMAT = Literal["concise", "locale"]


class Api:
    """Represents the Knew Karma API and provides methods for getting various data from the Reddit API."""

    def __init__(self):
        self.base_endpoint: str = "https://www.reddit.com"
        self._user_endpoint: str = f"{self.base_endpoint}/u"
        self._users_endpoint: str = f"{self.base_endpoint}/users"
        self.subreddit_endpoint: str = f"{self.base_endpoint}/r"
        self._subreddits_endpoint: str = f"{self.base_endpoint}/subreddits"

    @staticmethod
    async def make_request(
        endpoint: str,
        session: aiohttp.ClientSession,
    ) -> Union[dict, list]:
        """
        Asynchronously sends a request to the specified endpoint and returns JSON or list response.

        :param endpoint: The API endpoint to fetch data from.
        :type endpoint: str
        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: JSON data as a dictionary or list. Returns an empty dict if fetching fails.
        :rtype: Union[dict, list]
        """
        try:
            async with session.get(
                endpoint,
                headers={
                    "User-Agent": f"Knew-Karma/{Version.release} "
                    f"(Python {python_version}; +{Help.documentation})"
                },
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_message = await response.json()
                    console.log(
                        f"[red]✘[/] An API error occurred: [red]{error_message}[/]"
                    )
                    return {}

        except aiohttp.ClientConnectionError as error:
            console.log(f"[red]✘[/] An HTTP error occurred: [red]{error}[/]")
            return {}
        except Exception as error:
            console.log(f"[red]✘[/] An unknown error occurred: [red]{error}[/]")
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
            raise ValueError(
                f"Unknown data type ({response_data}: {type(response_data)}), expected a List[Dict] or Dict."
            )

    async def update_checker(self, session: aiohttp.ClientSession):
        """
        Asynchronously checks for updates by comparing the current local version with the remote version.

        Assumes version format: major.minor.patch.prefix

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        """
        # Make a GET request to PyPI to get the project's latest release.
        response: dict = await self.make_request(
            endpoint="https://api.github.com/repos/bellingcat/knewkarma/releases/latest",
            session=session,
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

            update_level: str = ""

            # Check for differences in version parts
            if remote_parts[0] != Version.major:
                update_level = "MAJOR"

            elif remote_parts[1] != Version.minor:
                update_level = "MINOR"

            elif remote_parts[2] != Version.patch:
                update_level = "PATCH"

            if update_level:
                upgrade_instructions = Markdown(
                    markup=f"""
## How To Upgrade
* **Snap Package**: *`sudo snap refresh knewkarma`*
* **PyPI Package**: *`pip install --upgrade knewkarma`*
"""
                )
                console.log(
                    f"\n[bold]{update_level}[/] update available: [underline]{remote_version}[/]",
                    justify="center",
                )
                console.log(markdown_release_notes)
                console.log(upgrade_instructions, "\n")

    async def _paginate(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        **kwargs,
    ) -> list[dict]:
        """
        Asynchronously fetches and processes data in a paginated manner
        from a specified endpoint until the specified limit
        of items is reached or there are no more items to fetch. It uses a specified processing function
        to handle the data from each request, ensuring no duplicates are returned.

        :param limit: Maximum number of results to return.
        :type limit: int
        :param session: An Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dict objects, each containing paginated data.
        :rtype: list[dict]
        """
        all_items = []
        last_item_id = None
        status: console.status = kwargs.get("status")

        if status:
            status.update("Initialising bulk data retrieval job...")

        while len(all_items) < limit:
            paginated_endpoint = (
                f"{kwargs.get('endpoint')}&after={last_item_id}&count={len(all_items)}"
                if last_item_id
                else kwargs.get("endpoint")
            )

            response = await self.make_request(
                session=session, endpoint=paginated_endpoint
            )

            items = response.get("data", {}).get("children", [])

            if not items:
                break

            processed_items = kwargs.get("data_processor")(response_data=items)
            items_to_limit = limit - len(all_items)
            all_items.extend(processed_items[:items_to_limit])

            last_item_id = response.get("data").get("after")

            if len(all_items) == limit:
                break

            sleep_duration: int = randint(1, 10)

            if status:
                await countdown_timer(
                    status=status,
                    duration=sleep_duration,
                    current_count=len(all_items),
                    limit=limit,
                )
            else:
                await asyncio.sleep(sleep_duration)

        return all_items

    async def get_entity(
        self,
        entity_type: Literal["post", "subreddit", "user", "wiki_page"],
        session: aiohttp.ClientSession,
        **kwargs,
    ) -> dict:
        """
        Asynchronously fetches a data from the specified entity.

        :param entity_type: The type of entity to get data from
        :type entity_type: str
        :param session: aiohttp session to use for the request.
        :return: A dictionary containing a specified entity's data.
        :rtype: dict
        """
        status: console.status = kwargs.get("status")
        if status:
            status.update("Initialising single data retrieval job...")

        # Use a dictionary for direct mapping
        entity_mapping: dict = {
            "post": f"{self.subreddit_endpoint}/{kwargs.get('post_subreddit')}"
            f"/comments/{kwargs.get('post_id')}.json",
            "user": f"{self._user_endpoint}/{kwargs.get('username')}/about.json",
            "subreddit": f"{self.subreddit_endpoint}/{kwargs.get('subreddit')}/about.json",
            "wiki_page": f"{self.subreddit_endpoint}/{kwargs.get('subreddit')}/wiki/{kwargs.get('page_name')}.json",
        }

        # Get the endpoint directly from the dictionary
        endpoint: str = entity_mapping.get(entity_type, "")

        entity_data = await self.make_request(endpoint=endpoint, session=session)

        return self._process_response(
            response_data=entity_data.get("data", {}),
            valid_key="content_md" if entity_type == "wiki_page" else "created_utc",
        )

    async def get_posts(
        self,
        posts_type: Literal[
            "best",
            "controversial",
            "front_page",
            "new",
            "popular",
            "rising",
            "subreddit_posts",
            "search_subreddit_posts",
            "user_posts",
            "user_overview",
            "user_comments",
            "post_comments",
        ],
        limit: int,
        session: aiohttp.ClientSession,
        timeframe: TIMEFRAME = "all",
        sort: SORT_CRITERION = "all",
        **kwargs,
    ) -> list[dict]:
        """
        Asynchronously gets a specified number of posts, with a specified sorting criterion, from the specified source.

        :param session: aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to get.
        :type limit: int
        :param posts_type: Type of posts to be fetched.
        :type posts_type: str
        :param sort: Posts' sort criterion.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing post data.
        :rtype: list[dict]
        """
        source_map = {
            "best": f"{self.base_endpoint}/r/{posts_type}.json",
            "controversial": f"{self.base_endpoint}/r/{posts_type}.json",
            "front_page": f"{self.base_endpoint}/.json",
            "new": f"{self.base_endpoint}/new.json",
            "popular": f"{self.base_endpoint}/r/{posts_type}.json",
            "rising": f"{self.base_endpoint}/r/{posts_type}.json",
            "subreddit_posts": f"{self.subreddit_endpoint}/{kwargs.get('subreddit')}.json",
            "user_posts": f"{self._user_endpoint}/{kwargs.get('username')}/submitted.json",
            "user_overview": f"{self._user_endpoint}/{kwargs.get('username')}/overview.json",
            "user_comments": f"{self._user_endpoint}/{kwargs.get('username')}/comments.json",
            "post_comments": f"{self.subreddit_endpoint}/{kwargs.get('post_subreddit')}"
            f"/comments/{kwargs.get('post_id')}.json",
            "search_subreddit_posts": f"{self.subreddit_endpoint}/{kwargs.get('subreddit')}"
            f"/search.json?q={kwargs.get('query')}&restrict_sr=1",
        }

        endpoint = source_map.get(posts_type, "")
        endpoint += f"?limit={limit}&sort={sort}&t={timeframe}&raw_json=1"

        posts: list[dict] = await self._paginate(
            limit=limit,
            session=session,
            status=kwargs.get("status"),
            endpoint=endpoint,
            data_processor=self._process_response,
        )

        return posts

    async def get_subreddits(
        self,
        session: aiohttp.ClientSession,
        subreddits_type: Literal["all", "default", "new", "popular", "user_moderated"],
        limit: int,
        timeframe: TIMEFRAME = "all",
        **kwargs,
    ) -> Union[list[dict], dict]:
        """
        Asynchronously gets the specified type of subreddits.

        :param subreddits_type: Type of subreddits to get.
        :type subreddits_type: str
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get subreddits.
        :type timeframe: Literal
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :return: A list of dictionaries, each containing subreddit data,
            or a single dictionary containing subreddit data.
        :rtype: Union[list[dict], dict]
        """
        subreddits_mapping: dict = {
            "all": f"{self._subreddits_endpoint}.json",
            "default": f"{self._subreddits_endpoint}/default.json",
            "new": f"{self._subreddits_endpoint}/new.json",
            "popular": f"{self._subreddits_endpoint}/popular.json",
            "user_moderated": f"{self._user_endpoint}/{kwargs.get('username')}/moderated_subreddits.json",
        }

        endpoint = subreddits_mapping.get(subreddits_type, "")
        if subreddits_type == "user_moderated":
            subreddits: dict = await self.make_request(
                endpoint=endpoint,
                session=session,
            )
        else:
            endpoint += f"?limit={limit}&t={timeframe}"

            subreddits: list[dict] = await self._paginate(
                limit=limit,
                session=session,
                status=kwargs.get("status"),
                endpoint=endpoint,
                data_processor=self._process_response,
            )

        return subreddits

    async def get_users(
        self,
        session: aiohttp.ClientSession,
        users_type: Literal["all", "popular", "new"],
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Asynchronously gets the specified type of subreddits.

        :param users_type: Type of users to get.
        :type users_type: str
        :param limit: Maximum number of users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get users.
        :type timeframe: Literal
        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `console.status` used to display animated status messages.
        :return: A list of dictionaries, each containing user data.
        :rtype: list[dict]
        """
        users_mapping: dict = {
            "all": f"{self._users_endpoint}.json",
            "new": f"{self._users_endpoint}/new.json",
            "popular": f"{self._users_endpoint}/popular.json",
        }

        endpoint = users_mapping.get(users_type, "")
        endpoint += f"?limit={limit}&t={timeframe}"
        users: list[dict] = await self._paginate(
            limit=limit,
            session=session,
            status=status,
            endpoint=endpoint,
            data_processor=self._process_response,
        )

        return users

    async def search_entities(
        self,
        session: aiohttp.ClientSession,
        entity_type: Literal["users", "subreddits", "posts"],
        query: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: console.status = None,
    ) -> list[dict]:
        """
        Asynchronously searches from a specified results type that match the specified query.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param entity_type: Type of entity to search for.
        :type entity_type: Literal[str]
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of results to get.
        :type limit: int
        :param sort: Posts' sort criterion.
        :type sort: str
        :param status: An instance of `console.status` used to display animated status messages.
        :return: A list of dictionaries, each containing search result data.
        :rtype: list[dict]
        """
        search_mapping: dict = {
            "posts": self.base_endpoint,
            "subreddits": self._subreddits_endpoint,
            "users": self._users_endpoint,
        }

        endpoint = search_mapping.get(entity_type, "")
        endpoint += f"/search.json?q={query}&limit={limit}&sort={sort}"

        search_results: list[dict] = await self._paginate(
            limit=limit,
            session=session,
            status=status,
            endpoint=endpoint,
            data_processor=self._process_response,
        )

        return search_results
