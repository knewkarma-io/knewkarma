import asyncio
from pprint import pprint
from random import randint
from sys import version as python_version
from typing import Callable, Literal, Union, Optional, List, Dict, Tuple

import aiohttp
import karmakaze
from rich.markdown import Markdown
from rich.prompt import Confirm
from rich.status import Status

from .about import About
from .tools.general import console, countdown_timer, make_panel
from .tools.package import update_pypi_package, is_snap_package
from .tools.terminal import Notify, Style
from .version import Version

__all__ = ["Api", "SORT_CRITERION", "TIMEFRAME", "TIME_FORMAT"]

notify = Notify
style = Style

SORT_CRITERION = Literal["controversial", "new", "top", "best", "hot", "rising", "all"]
TIMEFRAME = Literal["hour", "day", "week", "month", "year", "all"]
TIME_FORMAT = Literal["concise", "locale"]


class Api:
    """Represents the Knew Karma API and provides methods for getting various data from the Reddit API."""

    def __init__(self):
        self._sanitise = karmakaze.Sanitise()
        self.base_endpoint = "https://www.reddit.com"
        self._user_endpoint = f"{self.base_endpoint}/user"
        self._users_endpoint = f"{self.base_endpoint}/users"
        self.subreddit_endpoint = f"{self.base_endpoint}/r"
        self._subreddits_endpoint = f"{self.base_endpoint}/subreddits"
        self.reddit_status_endpoint = "https://www.redditstatus.com/api/v2/status.json"
        self.reddit_status_components_endpoint = (
            "https://www.redditstatus.com/api/v2/components.json"
        )

    async def _paginate_more_items(
            self,
            session: aiohttp.ClientSession,
            more_items_ids: List[str],
            endpoint: str,
            fetched_items: List[Dict],
    ):
        for more_id in more_items_ids:
            # Construct the endpoint for each additional comment ID.
            more_endpoint = f"{endpoint}&comment={more_id}"
            # Make an asynchronous request to fetch the additional comments.
            more_response = await self.make_request(
                session=session, endpoint=more_endpoint
            )
            # Extract the items (comments) from the response.
            more_items = more_response[1].get("data", {}).get("children", [])

            # Add the fetched items to the main items list.
            fetched_items.extend(more_items)

    async def _paginate_items(
            self,
            session: aiohttp.ClientSession,
            sanitiser: Callable,
            limit: int,
            **kwargs: Union[str, Status],
    ) -> List[Dict]:
        """
        Asynchronously fetches and processes data in a paginated manner
        from a specified endpoint until the specified limit
        of items is reached or there are no more items to fetch. It uses a specified processing function
        to handle the data from each request, ensuring no duplicates are returned.

        :param session: An Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param sanitiser: A callable used to sanitise response data.
        :type sanitiser: Callable
        :param limit: Maximum number of results to return.
        :type limit: int
        :return: A list of dict objects, each containing paginated data.
        :rtype: List[Dict]
        """

        # Initialise an empty list to store all items across paginated requests.
        all_items = []
        # Initialise the ID of the last item fetched to None (used for pagination).
        last_item_id = None

        # Continue fetching data until the limit is reached or no more items are available.
        while len(all_items) < limit:
            # Construct the paginated endpoint URL.
            # If last_item_id is set, use it to fetch the next page of data.
            paginated_endpoint = (
                f"{kwargs.get('endpoint')}&after={last_item_id}&count={len(all_items)}"
                if last_item_id
                else kwargs.get("endpoint")
            )

            # Make an asynchronous request to the constructed endpoint.
            response = await self.make_request(
                session=session, endpoint=paginated_endpoint
            )

            # If the request is for post comments, handle the response accordingly.
            if kwargs.get("posts_type") == "post_comments":
                items = []  # Initialise a list to store fetched items.
                more_items_ids = []  # Initialise a list to store IDs from "more" items.

                # Iterate over the children in the response to extract comments or "more" items.
                for item in response[1].get("data", {}).get("children", []):
                    if item.get("kind") == "t1":
                        # If the item is a comment (kind == "t1"), add it to the items list.
                        items.append(item)
                    elif item.get("kind") == "more":
                        # If the item is of kind "more", extract the IDs for additional comments.
                        more_items_ids.extend(item)

                # If there are more items to fetch (kind == "more"), make additional requests.
                if more_items_ids:
                    await self._paginate_more_items(
                        session=session,
                        fetched_items=items,
                        more_items_ids=more_items_ids,
                        endpoint=kwargs.get("endpoint"),
                    )
            else:
                # If not handling comments, simply extract the items from the response.
                items = response

            # If no items are found, break the loop as there's nothing more to fetch.
            if not items:
                break

            # Sanitise the fetched items using the provided sanitiser callable.
            sanitised_items: Callable = sanitiser(items)
            # Determine how many more items are needed to reach the limit.
            items_to_limit = limit - len(all_items)
            # Add the processed items to the all_items list, up to the specified limit.
            all_items.extend(sanitised_items[:items_to_limit])

            # Update the last_item_id to the ID of the last fetched item for pagination.
            last_item_id = (
                response[1].get("data").get("after")
                if kwargs.get("posts_type") == "post_comments"
                else response.get("data").get("after")
            )

            # If we've reached the specified limit, break the loop.
            if len(all_items) == limit:
                break

            # Introduce a random sleep duration between 1 and 5 seconds to avoid rate-limiting.
            sleep_duration = randint(1, 5)

            # If a status object is provided, use it to display a countdown timer.
            if kwargs.get("status"):
                await countdown_timer(
                    status=kwargs.get("status"),
                    duration=sleep_duration,
                    current_count=len(all_items),
                    overall_count=limit,
                )
            else:
                # Otherwise, just sleep for the calculated duration.
                await asyncio.sleep(sleep_duration)

        # Return the list of all fetched and processed items.
        return all_items

    @staticmethod
    async def make_request(
            endpoint: str,
            session: aiohttp.ClientSession,
    ) -> Union[Dict, List, None]:
        """
        Asynchronously sends a GET request to the specified API endpoint and returns JSON or list response.

        :param endpoint: The API endpoint to fetch data from.
        :type endpoint: str
        :param session: A aiohttp.ClientSession to use for the request. to use for the request.
        :type session: aiohttp.ClientSession
        :return: JSON data as a dictionary or list. Returns an empty dict if fetching fails.
        :rtype: Union[Dict, List]
        """

        try:
            async with session.get(
                    endpoint,
                    headers={
                        "User-Agent": f"{About.name.replace(' ', '-')}/{Version.release} "
                                      f"(Python {python_version}; +{About.documentation})"
                    },
            ) as response:
                response.raise_for_status()
                response_data: Union[Dict, List] = await response.json()
                return response_data

        except aiohttp.ClientConnectionError as connection_error:
            notify.exception(error=connection_error, exception_type="HTTP")
            return
        except aiohttp.ClientResponseError as api_error:
            notify.exception(error=api_error, exception_type="API")
        except Exception as unexpected_error:
            notify.exception(error=unexpected_error, exception_type="unexpected")
            return

    async def check_reddit_status(
            self, session: aiohttp.ClientSession, status: Optional[Status] = None
    ):
        """
        Asynchronously checks Reddit API and infrastructure status.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        """

        if status:
            notify.update_status(
                message=f"Checking Reddit {style.bold}API & Infrastructure{style.reset} status",
                status=status,
            )

        status_response: Dict = await self.make_request(
            endpoint=self.reddit_status_endpoint, session=session
        )
        indicator = status_response.get("status").get("indicator")
        description = status_response.get("status").get("description")
        if description:
            if indicator == "none" and description == "All Systems Operational":
                notify.ok(description)
            else:
                notify.warning(f"{indicator}: {description}")
                if status:
                    notify.update_status("Getting status components", status=status)
                status_components: Dict = await self.make_request(
                    endpoint=self.reddit_status_components_endpoint, session=session
                )
                if isinstance(status_components, Dict):
                    components: List[Dict] = status_components.get("components")
                    if components:
                        for component in components:
                            component_name = component.get("name")
                            component_status = component.get("status")
                            component_description = component.get("description")

                            component_summary = (
                                f"  - {component_name} ({
                                style.green if component_status == 'operational'
                                else style.yellow}{component_status}{style.reset})"
                                f" {'' if not component_description else f'| {component_description}'}"
                            )
                            if component_status == "operational":
                                console.print(component_summary)

    async def check_for_updates(
            self, session: aiohttp.ClientSession, status: Optional[Status] = None
    ):
        """
        Asynchronously checks for updates by comparing the current local version with the remote version.

        Assumes version format: major.minor.patch.prefix

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        """

        if status:
            notify.update_status(message="Checking for updates", status=status)

        # Make a GET request to GitHub to get the project's latest release.
        response = await self.make_request(
            endpoint=f"https://api.github.com/repos/{About.author[1]}/{About.package}/releases/latest",
            session=session,
        )

        if response.get("tag_name"):
            remote_version_str = response.get("tag_name")
            markup_release_notes = response.get("body")

            # Splitting the version strings into components
            local_version_parts = [
                Version.major[0],
                Version.minor[0],
                Version.patch[0],
            ]
            remote_version_parts: List = remote_version_str.split(".")

            local_major: int = local_version_parts[0]
            local_minor: int = local_version_parts[1]
            local_patch: int = local_version_parts[2]

            remote_major = int(remote_version_parts[0])
            remote_minor = int(remote_version_parts[1])
            remote_patch = int(remote_version_parts[2])

            update_level = ""

            # Check for differences in version parts
            if remote_major != local_major:
                update_level = f"{style.red}{Version.major[1]}{style.reset}"

            elif remote_minor != local_minor:
                update_level = f"{style.yellow}{Version.minor[1]}{style.reset}"

            elif remote_patch != local_patch:
                update_level = f"{style.green}{Version.patch[1]}{style.reset}"

            if update_level:
                markdown_release_notes = Markdown(markup=markup_release_notes)
                make_panel(
                    title=f"{style.bold}{update_level} Update Available ({style.cyan}{remote_version_str}{style.reset}){style.reset}",
                    content=markdown_release_notes,
                    subtitle=f"{style.bold}{style.italic}Thank you, for using {About.name}!{style.reset}{style.reset} ❤️ ",
                )

                # Skip auto-updating of the snap package
                if not is_snap_package(package=About.package):
                    status.stop()
                    if Confirm.ask(
                            f"{style.bold}Would you like to get these updates?{style.reset}",
                            case_sensitive=False,
                            default=False,
                            console=console,
                    ):
                        update_pypi_package(package=About.package, status=status)
                    else:
                        status.start()
            else:
                notify.ok(message=f"Up-to-date ({Version.full})")

    async def get_entity(
            self,
            entity_type: Literal["post", "subreddit", "user", "wiki_page"],
            session: aiohttp.ClientSession,
            **kwargs: Union[str, Status],
    ) -> Dict:
        """
        Asynchronously gets data from the specified entity.

        :param entity_type: The type of entity to get data from
        :type entity_type: str
        :param session: A aiohttp.ClientSession to use for the request. to use for the request.
        :return: A dictionary containing a specified entity's data.
        :rtype: Dict
        """

        username = kwargs.get("username")
        subreddit = kwargs.get("subreddit")
        post_id = kwargs.get("post_id")
        post_subreddit = kwargs.get("post_subreddit")

        # Use a dictionary for direct mapping
        entity_map = {
            "post": (
                f"{self.subreddit_endpoint}/{post_subreddit}"
                f"/comments/{post_id}.json",
                lambda: self._sanitise.post,
            ),
            "user": (
                f"{self._user_endpoint}/{username}/about.json",
                lambda: self._sanitise.subreddit_or_user,
            ),
            "subreddit": (
                f"{self.subreddit_endpoint}/{subreddit}/about.json",
                lambda: self._sanitise.subreddit_or_user,
            ),
            "wiki_page": (
                f"{self.subreddit_endpoint}/{subreddit}/wiki/{kwargs.get('page_name')}.json",
                lambda: self._sanitise.wiki_page,
            ),
        }
        status: Status = kwargs.get("status")
        if status:
            target_entity: Union[str, Tuple] = (
                    username or subreddit or (post_id, post_subreddit)
            )
            notify.update_status(
                message=f"Retrieving {entity_type} <{style.green}{target_entity}{style.reset}> data",
                status=status,
            )

        selected_entity = entity_map.get(entity_type)
        pprint(selected_entity)
        for endpoint, sanitiser in selected_entity:
            response = await self.make_request(endpoint=endpoint, session=session)
            entity = sanitiser(response=response)

            return entity

    async def get_posts(
            self,
            session: aiohttp.ClientSession,
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
            timeframe: TIMEFRAME = "all",
            sort: SORT_CRITERION = "all",
            **kwargs: Union[Status, str],
    ) -> List[Dict]:
        """
        Asynchronously gets a specified number of posts, with a specified sorting criterion, from the specified source.

        :param session: An aiohttp.ClientSession to use for the request. to use for the request.
        :type session: aiohttp.ClientSession
        :param posts_type: Type of posts to be fetched.
        :type posts_type: str
        :param limit: Maximum number of posts to get.
        :type limit: int
        :param sort: Posts' sort criterion.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing post data.
        :rtype: List[Dict]
        """

        posts_map = {
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

        endpoint = posts_map.get(posts_type, "")
        endpoint += f"?limit={limit}&sort={sort}&t={timeframe}&raw_json=1"

        sanitiser = (
            self._sanitise.comments
            if posts_type in ["user_comments", "user_overview", "post_comments"]
            else self._sanitise.posts
        )

        posts = await self._paginate_items(
            session=session,
            sanitiser=sanitiser,
            limit=limit,
            posts_type=posts_type,
            status=kwargs.get("status"),
            endpoint=endpoint,
        )

        return posts

    async def get_subreddits(
            self,
            session: aiohttp.ClientSession,
            subreddits_type: Literal["all", "default", "new", "popular", "user_moderated"],
            limit: int,
            timeframe: TIMEFRAME = "all",
            **kwargs: Union[str, Status],
    ) -> Union[List[Dict], Dict]:
        """
        Asynchronously gets the specified type of subreddits.

        :param session: Aiohttp session to use for the request.
        :type session: aiohttp.ClientSession
        :param subreddits_type: Type of subreddits to get.
        :type subreddits_type: str
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get subreddits.
        :type timeframe: Literal
        :return: A list of dictionaries, each containing subreddit data,
            or a single dictionary containing subreddit data.
        :rtype: Union[List[Dict], Dict]
        """

        subreddits_mapping = {
            "all": f"{self._subreddits_endpoint}.json",
            "default": f"{self._subreddits_endpoint}/default.json",
            "new": f"{self._subreddits_endpoint}/new.json",
            "popular": f"{self._subreddits_endpoint}/popular.json",
            "user_moderated": f"{self._user_endpoint}/{kwargs.get('username')}/moderated_subreddits.json",
        }

        endpoint = subreddits_mapping.get(subreddits_type, "")
        if subreddits_type == "user_moderated":
            subreddits = await self.make_request(
                endpoint=endpoint,
                session=session,
            )
        else:
            endpoint += f"?limit={limit}&t={timeframe}"

            subreddits = await self._paginate_items(
                session=session,
                sanitiser=self._sanitise.subreddits_or_users,
                limit=limit,
                status=kwargs.get("status"),
                endpoint=endpoint,
            )

        return subreddits

    async def get_users(
            self,
            session: aiohttp.ClientSession,
            users_type: Literal["all", "popular", "new"],
            limit: int,
            timeframe: TIMEFRAME = "all",
            status: Optional[Status] = None,
    ) -> List[Dict]:
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
        :param status: An instance of `rich.status.Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of dictionaries, each containing user data.
        :rtype: List[Dict]
        """

        users_mapping = {
            "all": f"{self._users_endpoint}.json",
            "new": f"{self._users_endpoint}/new.json",
            "popular": f"{self._users_endpoint}/popular.json",
        }

        endpoint = users_mapping.get(users_type, "")
        endpoint += f"?limit={limit}&t={timeframe}"

        users = await self._paginate_items(
            session=session,
            sanitiser=self._sanitise.subreddits_or_users,
            limit=limit,
            status=status,
            endpoint=endpoint,
        )

        return users

    async def search_entities(
            self,
            session: aiohttp.ClientSession,
            entity_type: Literal["users", "subreddits", "posts"],
            query: str,
            limit: int,
            sort: SORT_CRITERION = "all",
            status: Optional[Status] = None,
    ) -> List[Dict]:
        """
        Asynchronously searches specified entities that match the specified query.

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
        :param status: An instance of `rich.status.Status` used to display animated status messages.
        :return: A list of dictionaries, each containing search result data.
        :rtype: List[Dict]
        """

        search_mapping = {
            "posts": self.base_endpoint,
            "subreddits": self._subreddits_endpoint,
            "users": self._users_endpoint,
        }

        endpoint = search_mapping.get(entity_type, "")
        endpoint += f"/search.json?q={query}&limit={limit}&sort={sort}"

        sanitiser = (
            self._sanitise.posts
            if entity_type == "posts"
            else self._sanitise.subreddit_or_user
        )

        search_results = await self._paginate_items(
            session=session,
            sanitiser=sanitiser,
            limit=limit,
            status=status,
            endpoint=endpoint,
        )

        return search_results

# -------------------------------- END ----------------------------------------- #
