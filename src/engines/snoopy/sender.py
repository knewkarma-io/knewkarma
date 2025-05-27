import asyncio
import time
import typing as t
from logging import Logger
from random import randint

import aiohttp
from rich.status import Status

from engines.karmakaze.sanitiser import RedditSanitiser
from engines.karmakaze.schemas import User, Subreddit, Post, WikiPage, Comment
from toolbox import colours


class Reddit:
    SORT = t.Literal["controversial", "new", "top", "best", "hot", "rising", "all"]
    TIMEFRAME = t.Literal["hour", "day", "week", "month", "year", "all"]

    # Step 1: Define the base URL separately
    BASE_URL: str = "https://reddit.com"

    # Step 2: Now use the base URL to build the full endpoints dictionary
    ENDPOINTS: t.Dict[str, t.Union[str, t.Dict]] = {
        "base": BASE_URL,
        "subreddit": f"{BASE_URL}/r/%s",
        "user": f"{BASE_URL}/u/%s",
        "users": f"{BASE_URL}/users",
        "search": {
            "users": f"{BASE_URL}/users/search.json",
            "subreddits": f"{BASE_URL}/subreddits/search.json",
            "posts": f"{BASE_URL}/search.json",
        },
        "wikipage": f"{BASE_URL}/r/%s/wiki/%s.json",
        "username_available": f"{BASE_URL}/api/username_available.json",
        "infrastructure": {
            "status": "https://www.redditstatus.com/api/v2/status.json",
            "components": "https://www.redditstatus.com/api/v2/components.json",
        },
    }

    SANITISERS: t.Dict[str, t.Callable] = {
        "users": lambda response: RedditSanitiser().users(response=response),
        "user": lambda response: RedditSanitiser().user(response=response),
        "subreddits": lambda response: RedditSanitiser().subreddits(response=response),
        "subreddit": lambda response: RedditSanitiser().subreddit(response=response),
        "posts": lambda response: RedditSanitiser().posts(response=response),
        "wikipage": lambda response: RedditSanitiser().wiki_page(response=response),
        "after": lambda response: RedditSanitiser().get_after(response=response),
        "comment": lambda response: RedditSanitiser().comment(response=response),
        "comments": lambda response: RedditSanitiser().comments(response=response),
    }

    def __init__(self, user_agent: str):
        """
        Initialise the Reddit client.

        :param user_agent: The User-Agent string to use for HTTP requests.
        :type user_agent: str
        """
        self.user_agent = user_agent

    async def infra_status(
        self,
        session: aiohttp.ClientSession,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[t.Dict], None]:

        if status:
            status.update(f"Checking server status")

        status_response: t.Dict = await self.send_request(
            session=session,
            url=self.ENDPOINTS["infrastructure"]["status"],
        )

        indicator = status_response.get("status").get("indicator")
        description = status_response.get("status").get("description")
        if description:
            if indicator == "none":
                description = (
                    f"{colours.BOLD_GREEN}✔{colours.BOLD_GREEN_RESET} {description}"
                )
                (
                    logger.info(description)
                    if logger
                    else print(description.strip("[,]./,bold,green"))
                )
            else:
                status_message = f"{colours.BOLD_YELLOW}✘{colours.BOLD_YELLOW_RESET} {description} ({colours.YELLOW}{indicator}{colours.YELLOW_RESET})"
                (
                    logger.warning(status_message)
                    if logger
                    else print(status_message.strip("[,],/,bold,yellow"))
                )

                if status:
                    status.update("Getting status components")

                status_components: t.Dict = await self.send_request(
                    session=session,
                    url=self.ENDPOINTS["infrastructure"]["components"],
                )

                if isinstance(status_components, t.Dict):
                    components: t.List[t.Dict] = status_components.get("components")

                    return components
        return None

    async def send_request(
        self,
        url: str,
        session: aiohttp.ClientSession,
        params: t.Optional[t.Dict] = None,
    ) -> t.Union[t.Dict, t.List, str, None]:
        """
        Internal method to send a GET request to a Reddit endpoint.

        :param url: The URL to request.
        :type url: str
        :param session: An aiohttp session object.
        :type session: aiohttp.ClientSession
        :param params: Optional query parameters to include in the request.
        :type params: Optional[Dict]
        :return: The parsed JSON response.
        :rtype: Union[Dict, List, str, None]
        """
        async with session.get(
            url=url,
            headers={"User-Agent": self.user_agent},
            params=params,
        ) as response:
            data = await response.json()
            return data

    @staticmethod
    def _deduplicate(existing: list, new_items: list, key: str = "id") -> list:
        """
        Remove duplicate items based on a unique key and merge with existing.

        :param existing: The list of already seen items.
        :type existing: list
        :param new_items: The list of new items to be deduplicated.
        :type new_items: list
        :param key: The attribute name to use as a unique identifier.
        :type key: str
        :return: A list of unique items.
        :rtype: list
        """
        seen_ids = {getattr(item, key) for item in existing if hasattr(item, key)}
        return existing + [
            item for item in new_items if getattr(item, key, None) not in seen_ids
        ]

    async def _paginate(
        self,
        url: str,
        session: aiohttp.ClientSession,
        sanitiser: t.Callable[[dict], t.Optional[list]],
        limit: int = 100,
        key: str = "id",
        initial_params: t.Optional[dict] = None,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> list:
        """
        Generic paginator to fetch paginated Reddit listings using the `after` cursor.

        :param url: The API endpoint to request.
        :type url: str
        :param session: An aiohttp session for making requests.
        :type session: aiohttp.ClientSession
        :param sanitiser: A function to convert raw JSON into sanitised Python objects.
        :type sanitiser: Callable[[dict], Optional[list]]
        :param limit: Total number of items to retrieve.
        :type limit: int
        :param key: The attribute to use for deduplication.
        :type key: str
        :param initial_params: Base query parameters.
        :type initial_params: Optional[dict]
        :return: A deduplicated list of sanitised objects.
        :rtype: list
        """
        # Set logging level to logging.NOTSET
        # and show_level to True
        # in toolbox.logging, in order to see debug logs printed to the console.
        results = []
        after = None
        params = dict(initial_params) if initial_params else {}
        page = 1

        while len(results) < limit:
            params.update({"limit": 100})
            if after:
                params["after"] = after

            if isinstance(status, Status):
                status.update(f"Fetching page {page} (after={after})...")

            response = await self.send_request(url=url, session=session, params=params)
            items = sanitiser(response) or []

            if isinstance(logger, Logger):
                logger.debug(f"🧼 Sanitised {len(items)} items on this page.")

            before_dedupe = len(results)
            results = self._deduplicate(results, items, key=key)
            added = len(results) - before_dedupe

            if isinstance(logger, Logger):
                logger.debug(
                    f"➕ Added {added} new unique items. Total so far: {len(results)}"
                )

            if len(items) < params["limit"]:
                if isinstance(logger, Logger):
                    logger.debug("✅ Reached end of results (page shorter than limit).")
                break

            after = self.SANITISERS["after"](response=response)
            if not after:
                if isinstance(logger, Logger):
                    logger.debug("✅ No `after` cursor returned — stopping pagination.")
                break

            page += 1

            # t.Optional delay between requests
            sleep_duration = randint(1, 5)
            if isinstance(status, Status):
                await self._pagination_countdown(
                    status=status,
                    duration=sleep_duration,
                    current_count=len(results),
                    overall_count=limit,
                )
            else:
                await asyncio.sleep(sleep_duration)

        if isinstance(logger, Logger):
            logger.debug(
                f"🏁 Pagination complete. Returning {len(results[:limit])} results.\n"
            )
        return results[:limit]

    @staticmethod
    async def _pagination_countdown(
        duration: int,
        current_count: int,
        overall_count: int,
        status: Status,
    ):

        end_time: float = time.time() + duration
        while time.time() < end_time:
            remaining_time: float = end_time - time.time()
            remaining_seconds: int = int(remaining_time)
            remaining_milliseconds: int = int(
                (remaining_time - remaining_seconds) * 100
            )

            countdown_text: str = (
                f"{colours.CYAN}{current_count}{colours.CYAN_RESET}"
                f" of {colours.CYAN}{overall_count}{colours.CYAN_RESET}"
                f" items fetched, "
                f"resuming in {colours.CYAN}{remaining_seconds}"
                f".{remaining_milliseconds:02}{colours.CYAN_RESET} seconds"
            )
            status.update(countdown_text)
            await asyncio.sleep(0.01)  # Sleep for 10 milliseconds

    async def _more_comments(
        self,
        session: aiohttp.ClientSession,
        post_id: str,
        comment_ids: t.List[str],
        status: t.Optional[Status] = None,
        limit: int = 50,
    ) -> t.List[Comment]:
        """
        Fetch additional "more" comments from Reddit using /api/morechildren.json.

        :param session: aiohttp session.
        :param post_id: The full Reddit post ID (e.g., 't3_abcd123').
        :param comment_ids: List of comment IDs to fetch (not fullnames).
        :param status: Optional status UI feedback (rich.Status).
        :param limit: Max number of comments to return.
        :return: A list of parsed comment objects.
        """
        if status:
            status.update("Fetching more comments...")

        url = f"{self.BASE_URL}/api/morechildren.json"
        params = {
            "api_type": "json",
            "link_id": f"t3_{post_id}",
            "children": ",".join(comment_ids[:limit]),
        }

        response = await self.send_request(
            url=url,
            session=session,
            params=params,
        )

        # Reddit wraps the returned comments in 'json' -> 'data' -> 'things'
        raw_items = response.get("json", {}).get("data", {}).get("things", [])

        # These are typically of kind: "t1"
        comments = [
            self.SANITISERS["comment"](response={"data": item["data"]})
            for item in raw_items
            if item["kind"] == "t1"
        ]

        return [c for c in comments if c is not None]

    async def comments(
        self,
        session: aiohttp.ClientSession,
        kind: t.Literal["user_comments", "user_overview"],
        limit: int,
        sort: SORT,
        timeframe: TIMEFRAME,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        **kwargs: str,
    ) -> t.List[Comment]:
        username = kwargs.get("username")
        subreddit_name = kwargs.get("subreddit")
        post_id = kwargs.get("id")

        comments_map = {
            "user_overview": self.ENDPOINTS["user"] % username + "/overview.json",
            "user": self.ENDPOINTS["user"] % username + "/comments.json",
            # "post": f"{self.api_endpoints.SUBREDDIT}/{kwargs.get('subreddit')}"
            # f"/comments/{kwargs.get('id')}.json",
        }

        if isinstance(status, Status):
            status.update(f"Getting {limit} comments from {kind}")

        endpoint = comments_map[kind]
        params = {"limit": limit, "sort": sort, "t": timeframe, "raw_json": 1}

        comments = await self._paginate(
            url=endpoint,
            session=session,
            limit=limit,
            sanitiser=self.SANITISERS["comments"],
            status=status,
            initial_params=params,
        )

        if isinstance(logger, Logger):
            logger.info(
                f"{colours.BOLD_GREEN}+{colours.BOLD_GREEN_RESET} Got {len(comments)} of {limit} comments from {kind}"
            )

        return comments

    async def search(
        self,
        query: str,
        kind: t.Literal["posts", "subreddits", "users"],
        session: aiohttp.ClientSession,
        limit: int = 100,
        sort: SORT = "all",
        timeframe: TIMEFRAME = "all",
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[Post], t.List[Subreddit], t.List[User]]:
        """
        Search Reddit for users, subreddits, or posts.

        :param query: The search query string.
        :type query: str
        :param kind: The type of search ('posts', 'subreddits', or 'users').
        :type kind: Literal["posts", "subreddits", "users"]
        :param session: An aiohttp session.
        :type session: aiohttp.ClientSession
        :param limit: Number of results to return.
        :type limit: int
        :param sort: Sorting option (e.g., 'top', 'new', 'hot').
        :type sort: Literal
        :param timeframe: Time window for sorting ('day', 'week', 'month', etc).
        :type timeframe: Literal
        :return: A list of sanitised results.
        :rtype: Union[List[Post], List[Subreddit], List[User]]
        """
        if isinstance(status, Status):
            status.update(f"Searching for {query} in {kind}...")

        results = await self._paginate(
            url=self.ENDPOINTS["search"][kind],
            session=session,
            sanitiser=self.SANITISERS[kind],
            limit=limit,
            key="id",
            initial_params={"q": query, "t": timeframe, "sort": sort},
        )
        if isinstance(logger, Logger):
            logger.info(f"Showing {len(results)} {kind} for {query}")

        return results

    async def posts(
        self,
        kind: t.Literal[
            "best",
            "controversial",
            "front_page",
            "new",
            "popular",
            "rising",
            "subreddit",
            "user",
            "search_subreddit",
        ],
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT = "all",
        timeframe: TIMEFRAME = "all",
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        **kwargs,
    ):
        """
        Retrieve posts from various Reddit endpoints.

        :param kind: The kind of posts to retrieve (e.g., 'best', 'new', 'subreddit').
        :type kind: Literal
        :param limit: The maximum number of posts to return.
        :type limit: int
        :param session: An aiohttp session.
        :type session: aiohttp.ClientSession
        :param sort: Sort order (default is 'all').
        :type sort: Literal
        :param timeframe: Time filter for sorting.
        :type timeframe: Literal
        :param kwargs: Additional options such as 'subreddit', 'username', or 'query'.
        :return: A list of sanitised Post objects.
        :rtype: list
        """
        username = kwargs.get("username")
        subreddit = kwargs.get("subreddit")
        query = kwargs.get("query")

        posts_map = {
            "best": f"{self.BASE_URL}/{kind}.json",
            "controversial": f"{self.BASE_URL}/{kind}.json",
            "front_page": f"{self.BASE_URL}/.json",
            "new": f"{self.BASE_URL}/new.json",
            "popular": f"{self.BASE_URL}/{kind}.json",
            "rising": f"{self.BASE_URL}/{kind}.json",
            "subreddit": f"{self.ENDPOINTS['subreddit']}" % subreddit + ".json",
            "user": f"{self.ENDPOINTS['user']}" % username + "/submitted.json",
            "search_subreddit": f"{self.ENDPOINTS['subreddit']}" % subreddit
            + "/search.json",
        }

        if isinstance(status, Status):
            status.update(f"Getting {limit} posts from (listing) {kind}...")

        params: dict = (
            {"q": query, "restrict_sr": 1} if kind == "search_subreddit" else {}
        )
        params.update({"sort": sort, "t": timeframe})

        posts = await self._paginate(
            url=posts_map[kind],
            session=session,
            sanitiser=self.SANITISERS["posts"],
            limit=limit,
            initial_params=params,
        )

        if isinstance(logger, Logger):
            logger.info(f"Showing {len(posts)} from (listing) {kind}")

        return posts

    async def user(
        self,
        name: str,
        session: aiohttp.ClientSession,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> User:
        """
        Fetch a single Reddit user and sanitise the response.

        :param name: The Reddit username.
        :type name: str
        :param session: An aiohttp session.
        :type session: aiohttp.ClientSession
        :return: A sanitised User object.
        :rtype: User
        """
        if isinstance(status, Status):
            status.update(f"Getting profile data from user {name}...")

        response = await self.send_request(
            url=self.ENDPOINTS["user"] % name + "/about.json", session=session
        )
        user = self.SANITISERS["user"](response=response)

        if isinstance(logger, Logger):
            logger.info(f"Showing profile data for user {name}")

        return user

    async def users(
        self,
        session: aiohttp.ClientSession,
        kind: t.Literal["all", "popular", "new"],
        limit: int,
        timeframe: TIMEFRAME,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
    ) -> t.List[User]:

        users_map = {
            "all": f"{self.ENDPOINTS['users']}.json",
            "new": f"{self.ENDPOINTS['users']}/new.json",
            "popular": f"{self.ENDPOINTS['users']}/popular.json",
        }

        if status:
            status.update(f"Getting {limit} {kind} users")

        endpoint = users_map[kind]
        params = {
            "limit": limit,
            "t": timeframe,
        }

        users = await self._paginate(
            url=endpoint,
            session=session,
            initial_params=params,
            sanitiser=self.SANITISERS["subreddits"],
            limit=limit,
            logger=logger,
            status=status,
        )

        if logger:
            logger.info(
                f"{colours.BOLD_GREEN}+{colours.BOLD_GREEN_RESET} Showing {len(users)} {kind} users"
            )

        return users

    async def subreddit(
        self,
        name: str,
        session: aiohttp.ClientSession,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> Subreddit:
        """
        Fetch a single subreddit and sanitise the response.

        :param name: The name of the subreddit (without the 'r/').
        :type name: str
        :param session: An aiohttp session.
        :type session: aiohttp.ClientSession
        :return: A sanitised Subreddit object.
        :rtype: Subreddit
        """
        if isinstance(status, Status):
            status.update(f"Getting profile data from subreddit {name}...")

        response = await self.send_request(
            url=f"{self.ENDPOINTS['subreddit']}" % name, session=session
        )
        subreddit = self.SANITISERS["subreddit"](response=response)

        if isinstance(logger, Logger):
            logger.info(f"Showing profile data for subreddit {name}")

        return subreddit

    async def wiki_page(
        self,
        name: str,
        subreddit: str,
        session: aiohttp.ClientSession,
        status: t.Optional[Status] = None,
    ) -> WikiPage:
        if status:
            status.update(f"Getting data from wikipage {name} of r/{subreddit}")

        response = await self.send_request(
            url=self.ENDPOINTS["wikipage"] % (subreddit, name), session=session
        )

        return self.SANITISERS["wikipage"](response=response)
