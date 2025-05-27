import asyncio
import time
import typing as t
from logging import Logger
from random import randint
from types import SimpleNamespace

import aiohttp
from rich.status import Status

from toolbox import colours

__all__ = ["RedditEndpoints", "RedditRequestHandler"]


class RedditEndpoints:
    BASE: str = "https://www.reddit.com"
    USER: str = f"{BASE}/u"
    USERS: str = f"{BASE}/users"
    SUBREDDIT: str = f"{BASE}/r"
    SUBREDDITS: str = f"{BASE}/subreddits"
    USERNAME_AVAILABLE: str = f"{BASE}/api/username_available.json"

    INFRA_STATUS: str = "https://www.redditstatus.com/api/v2/status.json"
    INFRA_COMPONENTS: str = "https://www.redditstatus.com/api/v2/components.json"


class RedditRequestHandler:
    def __init__(self, user_agent: str):
        self.user_agent = user_agent

    async def send_request(
        self,
        session: aiohttp.ClientSession,
        endpoint: str,
        params: t.Optional[t.Dict] = None,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
    ) -> t.Union[t.Dict, t.List, bool, None]:

        try:
            async with session.get(
                url=endpoint,
                headers={"User-Agent": self.user_agent},
                params=params,
                proxy=proxy,
                proxy_auth=proxy_auth,
            ) as response:
                response.raise_for_status()
                response_data: t.Union[t.Dict, t.List] = await response.json()
                return response_data

        except Exception as error:
            raise error

    async def paginate_response(
        self,
        session: aiohttp.ClientSession,
        endpoint: str,
        limit: int,
        sanitiser: t.Callable,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        params: t.Optional[t.Dict] = None,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        is_post_comments: t.Optional[bool] = False,
    ) -> t.List[SimpleNamespace]:

        all_items: t.List = []
        seen_ids: set = set()
        seen_afters: set = set()
        last_item_id = None

        while len(all_items) < limit:
            response = await self.send_request(
                session=session,
                endpoint=(
                    f"{endpoint}?after={last_item_id}&count={len(all_items)}"
                    if last_item_id
                    else endpoint
                ),
                params=params,
                proxy=proxy,
                proxy_auth=proxy_auth,
            )

            if is_post_comments:
                semaphore = asyncio.Semaphore(3)
                items = await self._process_post_comments(
                    session=session,
                    endpoint=endpoint,
                    proxy=proxy,
                    proxy_auth=proxy_auth,
                    response=sanitiser(response[1]),
                    sanitiser=sanitiser,
                    limit=limit,
                    status=status,
                    logger=logger,
                    semaphore=semaphore,
                )
            else:
                items = sanitiser(response=response).children

            if not items:
                break

            # ✅ Deduplicate using Reddit's fullname (e.g., "t2_abcd1234")
            unique_items = []
            for item in items:
                item_id = getattr(item, "name", None)  # Prefer Reddit fullname

                # Fallbacks if fullname is missing
                if not item_id:
                    item_id = getattr(item, "id", None)
                if not item_id and hasattr(item, "data"):
                    item_id = item.data.name or item.data.id

                # Add only if unique
                if item_id and item_id not in seen_ids:
                    seen_ids.add(item_id)
                    unique_items.append(item)
                else:
                    if item_id:
                        logger.warning(f"Skipping duplicate item: {item_id}")

            items_to_limit = limit - len(all_items)
            all_items.extend(unique_items[:items_to_limit])

            # Determine the next `after` token
            last_item_id = (
                sanitiser(response=response[1]).after
                if is_post_comments
                else sanitiser(response=response).after
            )

            # Prevent infinite loops due to repeated `after` tokens
            if not last_item_id or last_item_id in seen_afters:
                # logger.warning(
                #    "No more items or repeating 'after' token detected. Stopping pagination."
                # )
                break
            seen_afters.add(last_item_id)

            # t.Optional delay between requests
            sleep_duration = randint(1, 5)
            if status:
                await self._pagination_countdown_timer(
                    status=status,
                    duration=sleep_duration,
                    current_count=len(all_items),
                    overall_count=limit,
                )
            else:
                await asyncio.sleep(sleep_duration)

        return all_items

    async def _paginate_more_items(
        self,
        session: aiohttp.ClientSession,
        more_items_ids: t.List[str],
        endpoint: str,
        sanitiser: t.Callable,
        fetched_items: t.List[t.Dict],
        limit: int,
        semaphore: asyncio.Semaphore,
        status: t.Optional[Status] = None,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        logger: t.Optional[Logger] = None,
    ):
        """
        Fetch additional items (comments) and paginate them concurrently while respecting the given limit.

        :param session: The aiohttp session used for making requests.
        :param more_items_ids: t.List of additional item IDs to fetch.
        :param endpoint: The API endpoint to fetch the items.
        :param sanitiser: A callable used to sanitise and parse the response.
        :param fetched_items: t.List of already fetched items.
        :param limit: The maximum number of items to fetch.
        :param semaphore: A semaphore limiting the number of concurrent tasks.
        :param status: t.Optional status object for displaying progress.
        :param proxy: t.Optional proxy URL for the request.
        :param proxy_auth: t.Optional proxy authentication.
        """

        remaining_items = limit - len(fetched_items)

        if remaining_items <= 0:
            return  # Stop if we've already hit the limit

        if logger:
            logger.info(f"Found {len(more_items_ids)} additional comments")

        # Create a list to hold all the asynchronous tasks
        tasks = []

        for more_id in more_items_ids:
            if len(fetched_items) >= limit:
                break  # Stop if we've already fetched enough items

            # Each task will fetch and process one additional item
            tasks.append(
                self._fetch_and_process_item(
                    session=session,
                    more_id=more_id,
                    endpoint=endpoint,
                    sanitiser=sanitiser,
                    fetched_items=fetched_items,
                    overall_items_limit=limit,  # Fixed this typo
                    semaphore=semaphore,
                    status=status,
                    proxy=proxy,
                    proxy_auth=proxy_auth,
                )
            )

        # Run all tasks concurrently, respecting the semaphore
        await asyncio.gather(*tasks)

    async def _fetch_and_process_item(
        self,
        session: aiohttp.ClientSession,
        more_id: str,
        endpoint: str,
        sanitiser: t.Callable,
        fetched_items: t.List[t.Dict],
        overall_items_limit: int,
        semaphore: asyncio.Semaphore,
        status: t.Optional[Status] = None,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
    ):
        """
        Fetch and process a single item (comment) from the API, limited by the semaphore.

        :param session: The aiohttp session used for making requests.
        :param more_id: The ID of the additional item to fetch.
        :param endpoint: The API endpoint to fetch the item.
        :param sanitiser: A callable used to sanitise and parse the response.
        :param fetched_items: t.List of already fetched items.
        :param overall_items_limit: The overall number of items needed.
        :param semaphore: A semaphore limiting the number of concurrent tasks.
        :param status: t.Optional status object for displaying progress.
        :param proxy: t.Optional proxy URL for the request.
        :param proxy_auth: t.Optional proxy authentication.
        """

        async with semaphore:  # Limit the number of concurrent tasks
            # Check if we've already reached the overall limit
            if len(fetched_items) >= overall_items_limit:
                return

            # Construct the endpoint for each additional comment ID
            more_endpoint = f"{endpoint}?comment={more_id}"

            # Make an asynchronous request to fetch the additional comments
            more_response = await self.send_request(
                session=session,
                endpoint=more_endpoint,
                proxy=proxy,
                proxy_auth=proxy_auth,
            )

            # Extract the items (comments) from the response
            more_items = sanitiser(response=more_response[1])

            # Determine how many more items we can add without exceeding the limit
            items_to_add = min(
                overall_items_limit - len(fetched_items), len(more_items.children)
            )

            # Add the allowed number of items to the main items list
            fetched_items.extend(more_items.children[:items_to_add])

            # If we've reached the overall limit, stop further processing
            if len(fetched_items) >= overall_items_limit:
                return

            # Introduce a random sleep duration to avoid rate-limiting
            sleep_duration = randint(1, 5)
            await self._pagination_countdown_timer(
                duration=sleep_duration,
                overall_count=overall_items_limit,
                current_count=len(fetched_items),
                status=status,
            )

    async def _process_post_comments(self, **kwargs):
        # If the request is for post comments, handle the response accordingly.
        items = []  # Initialise a list to store fetched items.
        more_items_ids = []  # Initialise a list to store IDs from "more" items.

        # Iterate over the children in the response to extract comments or "more" items.
        for item in kwargs.get("response").children:
            if item.kind == "t1":
                # If the item is a comment (kind == "t1"), add it to the items list.
                items.append(item)
            elif item.kind == "more":
                # If the item is of kind "more", extract the IDs for additional comments.
                more_items_ids.extend(item.data.children)

        # If there are more items to fetch (kind == "more"), make additional requests.
        if more_items_ids:
            await self._paginate_more_items(
                session=kwargs.get("session"),
                proxy=kwargs.get("proxy"),
                proxy_auth=kwargs.get("proxy_auth"),
                logger=kwargs.get("logger"),
                status=kwargs.get("status"),
                fetched_items=items,
                more_items_ids=more_items_ids,
                endpoint=kwargs.get("endpoint"),
                limit=kwargs.get("limit"),
                sanitiser=kwargs.get("sanitiser"),
                semaphore=kwargs.get("semaphore"),
            )

        return items

    @staticmethod
    async def _pagination_countdown_timer(
        duration: int,
        current_count: int,
        overall_count: int,
        status: t.Optional[Status] = None,
    ):

        end_time: float = time.time() + duration
        while time.time() < end_time:
            remaining_time: float = end_time - time.time()
            remaining_seconds: int = int(remaining_time)
            remaining_milliseconds: int = int(
                (remaining_time - remaining_seconds) * 100
            )

            countdown_text: str = (
                f"{colours.CYAN}{current_count}{colours.CYAN_RESET} of {colours.CYAN}{overall_count}{colours.CYAN_RESET} items fetched, "
                f"resuming in {colours.CYAN}{remaining_seconds}.{remaining_milliseconds:02}{colours.CYAN_RESET} seconds"
            )

            (
                status.update(countdown_text)
                if status
                else print(countdown_text.strip("[,],/,cyan"))
            )
            await asyncio.sleep(0.01)  # Sleep for 10 milliseconds


# -------------------------------- END ----------------------------------------- #
