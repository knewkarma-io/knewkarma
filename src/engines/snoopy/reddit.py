import time
import typing as t
from logging import Logger
from random import randint

import requests
from rich.status import Status

from engines.karmakaze.sanitiser import RedditSanitiser
from engines.karmakaze.schemas import User, Subreddit, Post, WikiPage, Comment
from tools import colours


class Reddit:
    SUBREDDITS_KIND = t.Literal["all", "default", "new", "popular", "user_moderated"]
    SORT = t.Literal["controversial", "new", "top", "best", "hot", "rising", "all"]
    TIMEFRAME = t.Literal["hour", "day", "week", "month", "year", "all"]

    BASE_URL: str = "https://reddit.com"
    ENDPOINTS: t.Dict[str, t.Union[str, t.Dict]] = {
        "subreddit": f"{BASE_URL}/r/%s",
        "subreddits": f"{BASE_URL}/subreddits",
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
        "post": lambda response: RedditSanitiser().post(response=response),
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

    def send_request(
        self,
        url: str,
        session: requests.Session,
        params: t.Optional[t.Dict] = None,
    ) -> t.Union[t.Dict, t.List, str, None]:
        """
        Internal method to send a GET request to a Reddit endpoint.

        :param url: The URL to request.
        :type url: str
        :param session: An aiohttp session object.
        :type session: requests.Session
        :param params: Optional query parameters to include in the request.
        :type params: Optional[Dict]
        :return: The parsed JSON response.
        :rtype: Union[Dict, List, str, None]
        """
        with session.get(
            url=url,
            headers={"User-Agent": self.user_agent},
            params=params,
        ) as response:
            data = response.json()
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

    def _paginate(
        self,
        url: str,
        session: requests.Session,
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
        :type session: requests.Session
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
        # in tools.logging, in order to see debug logs printed to the console.
        results = []
        after = None
        params = dict(initial_params) if initial_params else {}
        page = 1

        while len(results) < limit:
            params.update({"limit": 100})
            if after:
                params["after"] = after

            if isinstance(status, Status):
                status.update(f"Fetching page {page} (cursor={after})...")

            response = self.send_request(url=url, session=session, params=params)
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
                    logger.info(
                        f"{colours.BOLD_GREEN}✔{colours.BOLD_GREEN_RESET} Reached end of results (page shorter than limit)."
                    )
                break

            after = self.SANITISERS["after"](response=response)
            if not after:
                if isinstance(logger, Logger):
                    logger.debug(
                        f"{colours.BOLD_GREEN}✔{colours.BOLD_GREEN_RESET} No `after` cursor returned — stopping pagination."
                    )
                break

            page += 1

            # t.Optional delay between requests
            sleep_duration = randint(1, 5)
            if isinstance(status, Status):
                self._pagination_countdown(
                    status=status,
                    duration=sleep_duration,
                    current_count=len(results),
                    overall_count=limit,
                )
            else:
                time.sleep(sleep_duration)

        if isinstance(logger, Logger):
            # logger.info(f"Showing {len(results[:limit])} items")
            logger.debug(
                f"🏁 Pagination complete. Returning {len(results[:limit])} results.\n"
            )

        return results[:limit]

    @staticmethod
    def _pagination_countdown(
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
            time.sleep(0.01)  # Sleep for 10 milliseconds

    def _more_comments(
        self,
        session: requests.Session,
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
        if isinstance(status, Status):
            status.update("Fetching more comments...")

        url = f"{self.BASE_URL}/api/morechildren.json"
        params = {
            "api_type": "json",
            "link_id": f"t3_{post_id}",
            "children": ",".join(comment_ids[:limit]),
        }

        response = self.send_request(
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

    def comments(
        self,
        session: requests.Session,
        kind: t.Literal["user", "u_overview", "post"],
        limit: int,
        sort: SORT,
        timeframe: TIMEFRAME,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        **kwargs: str,
    ) -> t.List[Comment]:
        username = kwargs.get("username")
        subreddit = kwargs.get("subreddit")
        post_id = kwargs.get("id")

        endpoints = {
            "u_overview": self.ENDPOINTS["user"] % username + "/overview.json",
            "user": self.ENDPOINTS["user"] % username + "/comments.json",
            "post": self.ENDPOINTS["subreddit"] % subreddit
            + f"/comments/{post_id}.json",
        }

        endpoint = endpoints[kind]
        params = {"limit": limit, "sort": sort, "t": timeframe, "raw_json": 1}

        if isinstance(status, Status):
            status.update(f"Getting {limit} comments from {kind}...")

        comments = self._paginate(
            url=endpoint,
            session=session,
            limit=limit,
            sanitiser=self.SANITISERS["comments"],
            logger=logger,
            status=status,
            initial_params=params,
        )

        return comments

    def search(
        self,
        query: str,
        kind: t.Literal["posts", "subreddits", "users"],
        session: requests.Session,
        limit: int = 100,
        sort: SORT = "all",
        timeframe: TIMEFRAME = "all",
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[Post], t.List[Subreddit], t.List[User]]:
        """
        Search Reddit for users, subreddits, or posts.
        """
        if isinstance(status, Status):
            status.update(f"Searching for {query} in {kind}...")

        results = self._paginate(
            url=self.ENDPOINTS["search"][kind],
            session=session,
            sanitiser=self.SANITISERS[kind],
            limit=limit,
            key="id",
            initial_params={"q": query, "t": timeframe, "sort": sort},
            logger=logger,
            status=status,
        )

        return results

    def post(
        self,
        id: str,
        subreddit: str,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ) -> Post:
        if isinstance(status, Status):
            status.update(f"Getting data from post with id {id} in r/{subreddit}")

        response = self.send_request(
            session=session,
            url=self.ENDPOINTS["subreddit"] % f"{subreddit}/comments/{id}.json",
        )
        sanitised_response = self.SANITISERS["post"](response=response)

        return sanitised_response

    def posts(
        self,
        kind: t.Literal[
            "best",
            "controversial",
            "front_page",
            "new",
            "top",
            # "popular",
            "rising",
            "subreddit",
            "user",
            "search_subreddit",
        ],
        limit: int,
        session: requests.Session,
        sort: SORT = "all",
        timeframe: TIMEFRAME = "all",
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        **kwargs,
    ):
        """
        Retrieve posts from various Reddit endpoints.
        """
        username = kwargs.get("username")
        subreddit = kwargs.get("subreddit")
        query = kwargs.get("query")

        endpoints = {
            "front_page": f"{self.BASE_URL}/.json",
            "subreddit": f"{self.ENDPOINTS['subreddit']}" % subreddit + ".json",
            "user": f"{self.ENDPOINTS['user']}" % username + "/submitted.json",
            "search_subreddit": f"{self.ENDPOINTS['subreddit']}" % subreddit
            + "/search.json",
        }

        if kind in ["best", "controversial", "new", "top", "rising"]:
            endpoint = f"{self.BASE_URL}/{kind}.json"
        else:
            endpoint = endpoints[kind]

        params: dict = (
            {"q": query, "restrict_sr": 1} if kind == "search_subreddit" else {}
        )
        params.update({"sort": sort, "t": timeframe})

        if isinstance(status, Status):
            status.update(f"Getting {limit} posts from (listing) {kind}...")

        posts = self._paginate(
            url=endpoint,
            session=session,
            sanitiser=self.SANITISERS["posts"],
            limit=limit,
            initial_params=params,
            logger=logger,
            status=status,
        )

        return posts

    def user(
        self,
        name: str,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ) -> User:
        """
        Fetch a single Reddit user and sanitise the response.
        """
        if isinstance(status, Status):
            status.update(f"Getting profile data from user {name}...")

        response = self.send_request(
            url=self.ENDPOINTS["user"] % f"{name}/about.json", session=session
        )
        user = self.SANITISERS["user"](response=response)

        return user

    def users(
        self,
        session: requests.Session,
        kind: t.Literal["all", "popular", "new"],
        limit: int,
        timeframe: TIMEFRAME,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.List[User]:

        if kind == "all":
            endpoint = f"{self.ENDPOINTS["users"]}.json"
        else:
            endpoint = f"{self.ENDPOINTS['users']}/{kind}.json"

        params = {
            "limit": limit,
            "t": timeframe,
        }

        if isinstance(status, Status):
            status.update(f"Getting {limit} {kind} users...")

        users = self._paginate(
            url=endpoint,
            session=session,
            initial_params=params,
            sanitiser=self.SANITISERS["subreddits"],
            limit=limit,
            logger=logger,
            status=status,
        )

        return users

    def subreddit(
        self,
        name: str,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ) -> Subreddit:
        """
        Fetch a single subreddit and sanitise the response.
        """
        print(self.ENDPOINTS["subreddit"] % name)
        if isinstance(status, Status):
            status.update(f"Getting profile data from subreddit {name}...")

        response = self.send_request(
            url=self.ENDPOINTS["subreddit"] % f"{name}/about.json", session=session
        )
        subreddit = self.SANITISERS["subreddit"](response=response)

        return subreddit

    def subreddits(
        self,
        session: requests.Session,
        kind: SUBREDDITS_KIND,
        limit: int,
        timeframe: TIMEFRAME,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        **kwargs: str,
    ) -> t.Union[t.List[Subreddit], Subreddit]:

        endpoints = {
            "all": f"{self.ENDPOINTS['subreddits']}.json",
            "user_moderated": self.ENDPOINTS["user"] % kwargs.get("username")
            + "/moderated_subreddits.json",
        }

        if kind in ["default", "new", "popular"]:
            endpoint = f"{self.ENDPOINTS['subreddits']}/{kind}.json"
        else:
            endpoint = endpoints[kind]

        params = {"raw_json": 1}

        if isinstance(status, Status):
            desc = f"{limit} " if kind != "user_moderated" else ""
            status.update(f"Getting {desc}{kind} subreddits...")

        if kind == "user_moderated":
            response = self.send_request(
                url=endpoint,
                session=session,
            )
            subreddits = self.SANITISERS["subreddits"](response=response)
        else:
            params.update({"limit": limit, "t": str(timeframe)})
            subreddits = self._paginate(
                url=endpoint,
                session=session,
                initial_params=params,
                sanitiser=self.SANITISERS["subreddits"],
                limit=limit,
                logger=logger,
                status=status,
            )

        return subreddits

    def wiki_page(
        self,
        name: str,
        subreddit: str,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ) -> WikiPage:
        if isinstance(status, Status):
            status.update(f"Getting data from wikipage {name} of r/{subreddit}...")

        response = self.send_request(
            url=self.ENDPOINTS["wikipage"] % (subreddit, name), session=session
        )

        return self.SANITISERS["wikipage"](response=response)
