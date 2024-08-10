import time
from random import randint
from sys import version as python_version
from typing import Callable, Literal, Union

import requests
from rich.markdown import Markdown
from rich.prompt import Confirm

from .about import About
from .tools.misc_utils import console, create_panel
from .tools.package_utils import is_pypi_package, update_pypi_package, is_snap_package
from .tools.styling_utils import Prefix, Text
from .tools.time_utils import countdown_timer
from .version import Version

__all__ = ["Api", "SORT_CRITERION", "TIMEFRAME", "TIME_FORMAT"]

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
                f"Unknown data type ({response_data}: {type(response_data)}), expected a list[dict] or dict."
            )

    def _paginate_response(
            self,
            limit: int,
            session: requests.Session,
            data_processor: Callable,
            **kwargs: Union[str, console.status],
    ) -> list[dict]:
        """
        Fetches and processes data in a paginated manner
        from a specified endpoint until the specified limit
        of items is reached or there are no more items to fetch. It uses a specified processing function
        to handle the data from each request, ensuring no duplicates are returned.

        :param limit: Maximum number of results to return.
        :type limit: int
        :param session: An Aiohttp session to use for the request.
        :type session: requests.Session
        :param data_processor: A callable used to process response data.
        :type data_processor: Callable
        :return: A list of dict objects, each containing paginated data.
        :rtype: list[dict]
        """
        all_items = []
        last_item_id = None

        while len(all_items) < limit:
            paginated_endpoint = (
                f"{kwargs.get('endpoint')}&after={last_item_id}&count={len(all_items)}"
                if last_item_id
                else kwargs.get("endpoint")
            )

            response = self.make_request(session=session, endpoint=paginated_endpoint)

            # TODO: We're adding all t1 (comment) items to the list,
            #  because the post comments response includes an item with kind "more",
            #  which happens to be a list of comment ids that have already been fetched.
            #  I feel like the handling of this can be cleaner, unlike what I did here.
            if kwargs.get("posts_type") == "post_comments":
                items: list = []
                for item in response[1].get("data", {}).get("children", []):
                    if item.get("kind") == "t1":
                        items.append(item)
            else:
                items = response.get("data", {}).get("children", [])

            if not items:
                break

            processed_items: Callable = data_processor(response_data=items)
            items_to_limit: int = limit - len(all_items)
            all_items.extend(processed_items[:items_to_limit])

            last_item_id = (
                response[1].get("data").get("after")
                if kwargs.get("posts_type") == "post_comments"
                else response.get("data").get("after")
            )

            if len(all_items) == limit:
                break

            sleep_duration: int = randint(1, 10)

            if kwargs.get("status"):
                countdown_timer(
                    status=kwargs.get("status"),
                    duration=sleep_duration,
                    current_count=len(all_items),
                    overall_count=limit,
                )
            else:
                time.sleep(sleep_duration)

        return all_items

    @staticmethod
    def make_request(
            endpoint: str,
            session: requests.Session,
    ) -> Union[dict, list]:
        """
        Sends a  GET request to the specified endpoint and returns JSON or list response.

        :param endpoint: The API endpoint to fetch data from.
        :type endpoint: str
        :param session: A requests.Session to use for the request. to use for the request.
        :type session: requests.Session
        :return: JSON data as a dictionary or list. Returns an empty dict if fetching fails.
        :rtype: Union[dict, list]
        """
        try:
            with session.get(
                    endpoint,
                    headers={
                        "User-Agent": f"{About.name.replace(' ', '-')}/{Version.release} "
                                      f"(Python {python_version}; +{About.documentation})"
                    },
            ) as response:
                if response.status_code == 200:
                    return response.json()
                else:
                    error_message: dict = response.json()
                    console.log(
                        f"{Prefix.error} An API error occurred: {error_message}"
                    )
                    return {}

        except requests.ConnectionError as connection_error:
            console.log(f"{Prefix.error} An HTTP error occurred: {connection_error}")
            return {}
        except Exception as unexpected_error:
            console.log(
                f"{Prefix.error} An unexpected error occurred: {unexpected_error}"
            )
            return {}

    def check_updates(self, session: requests.Session, status: console.status):
        """
        Checks for updates by comparing the current local version with the remote version.

        Assumes version format: major.minor.patch.prefix

        :param session: A requests.Session to use for the request. to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type status: Console.console.status
        """
        # Make a GET request to PyPI to get the project's latest release.
        response: dict = self.make_request(
            endpoint=f"https://api.github.com/repos/bellingcat/{About.package}/releases/latest",
            session=session,
        )
        release: dict = self._process_response(
            response_data=response, valid_key="tag_name"
        )

        if release:
            remote_version_str: str = release.get("tag_name")
            markup_release_notes: str = release.get("body")

            # Splitting the version strings into components
            local_version_parts: list = [Version.major[0], Version.minor[0], Version.patch[0]]
            remote_version_parts: list = remote_version_str.split(".")

            update_level: str = ""

            # Check for differences in version parts
            if remote_version_parts[0] != local_version_parts[0]:
                update_level = f"{Text.red}{Version.major[1]}{Text.reset}"

            elif remote_version_parts[1] != local_version_parts[1]:
                update_level = f"{Text.yellow}{Version.minor[1]}{Text.reset}"

            elif remote_version_parts[2] != local_version_parts[2]:
                update_level = f"{Text.green}{Version.patch[1]}{Text.reset}"

            if update_level:
                markdown_release_notes = Markdown(markup=markup_release_notes)
                create_panel(
                    title=f"{Text.bold}{update_level} update ({Text.cyan}{remote_version_str}{Text.reset}){Text.reset}",
                    content=markdown_release_notes,
                    subtitle=f"{Text.bold}{Text.italic}Thank you, for using {About.name}!{Text.reset}{Text.reset} ❤️ ",
                )

                # Skip auto-updating of the snap package
                if is_snap_package(package=About.package):
                    pass
                elif is_pypi_package(package=About.package):
                    status.stop()
                    if Confirm.ask(
                            f"{Text.bold}Would you like to install this update?{Text.reset}",
                            default=False,
                            console=console,
                    ):
                        update_pypi_package(package=About.package)

                    console.clear()
                    status.start()

    def get_entity(
            self,
            entity_type: Literal["post", "subreddit", "user", "wiki_page"],
            session: requests.Session,
            **kwargs: str,
    ) -> dict:
        """
        Gets data from the specified entity.

        :param entity_type: The type of entity to get data from
        :type entity_type: str
        :param session: A requests.Session to use for the request. to use for the request.
        :return: A dictionary containing a specified entity's data.
        :rtype: dict
        """
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

        response = self.make_request(endpoint=endpoint, session=session)
        if entity_type == "post":
            entity_data = response[0].get("data").get("children")[0]
        else:
            entity_data = response

        return self._process_response(
            response_data=entity_data.get("data", {}),
            valid_key="content_md" if entity_type == "wiki_page" else "created_utc",
        )

    def get_posts(
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
            session: requests.Session,
            timeframe: TIMEFRAME = "all",
            sort: SORT_CRITERION = "all",
            **kwargs: Union[console.status, str],
    ) -> list[dict]:
        """
        Gets a specified number of posts, with a specified sorting criterion, from the specified source.

        :param session: A requests.Session to use for the request. to use for the request.
        :type session: requests.Session
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

        posts: list[dict] = self._paginate_response(
            limit=limit,
            session=session,
            posts_type=posts_type,
            status=kwargs.get("status"),
            endpoint=endpoint,
            data_processor=self._process_response,
        )

        return posts

    def get_subreddits(
            self,
            session: requests.Session,
            subreddits_type: Literal["all", "default", "new", "popular", "user_moderated"],
            limit: int,
            timeframe: TIMEFRAME = "all",
            **kwargs: Union[str, console.status],
    ) -> Union[list[dict], dict]:
        """
        Gets the specified type of subreddits.

        :param subreddits_type: Type of subreddits to get.
        :type subreddits_type: str
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get subreddits.
        :type timeframe: Literal
        :param session: Aiohttp session to use for the request.
        :type session: requests.Session
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
            subreddits: dict = self.make_request(
                endpoint=endpoint,
                session=session,
            )
        else:
            endpoint += f"?limit={limit}&t={timeframe}"

            subreddits: list[dict] = self._paginate_response(
                limit=limit,
                session=session,
                status=kwargs.get("status"),
                endpoint=endpoint,
                data_processor=self._process_response,
            )

        return subreddits

    def get_users(
            self,
            session: requests.Session,
            users_type: Literal["all", "popular", "new"],
            limit: int,
            timeframe: TIMEFRAME = "all",
            status: console.status = None,
    ) -> list[dict]:
        """
        Gets the specified type of subreddits.

        :param users_type: Type of users to get.
        :type users_type: str
        :param limit: Maximum number of users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get users.
        :type timeframe: Literal
        :param session: Aiohttp session to use for the request.
        :type session: requests.Session
        :param status: An instance of `console.status` used to display animated status messages.
        :type status: Console.console.status
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
        users: list[dict] = self._paginate_response(
            limit=limit,
            session=session,
            status=status,
            endpoint=endpoint,
            data_processor=self._process_response,
        )

        return users

    def search_entities(
            self,
            session: requests.Session,
            entity_type: Literal["users", "subreddits", "posts"],
            query: str,
            limit: int,
            sort: SORT_CRITERION = "all",
            status: console.status = None,
    ) -> list[dict]:
        """
        Searches from a specified results type that match the specified query.

        :param session: Aiohttp session to use for the request.
        :type session: requests.Session
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

        search_results: list[dict] = self._paginate_response(
            limit=limit,
            session=session,
            status=status,
            endpoint=endpoint,
            data_processor=self._process_response,
        )

        return search_results

# -------------------------------- END ----------------------------------------- #
