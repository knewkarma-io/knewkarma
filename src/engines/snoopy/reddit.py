import typing as t
from logging import Logger
from types import SimpleNamespace

import aiohttp
from rich.status import Status

from engines import karmakaze
from toolbox import colours
from .api import RedditRequestHandler, RedditEndpoints

__all__ = ["RedditClient"]


class RedditClient:

    SORT = t.Literal["controversial", "new", "top", "best", "hot", "rising", "all"]
    TIMEFRAME = t.Literal["hour", "day", "week", "month", "year", "all"]
    TIME_FORMAT = t.Literal["concise", "locale"]
    COMMENTS_KIND = t.Literal["user_overview", "user", "post"]
    POSTS_KIND = t.Literal[
        "best",
        "controversial",
        "front_page",
        "new",
        "popular",
        "rising",
        "subreddit",
        "user",
        "search_subreddit",
    ]
    SEARCH_KIND = t.Literal["users", "subreddits", "posts"]
    SUBREDDITS_KIND = t.Literal["all", "default", "new", "popular", "user_moderated"]
    USERS_KIND = t.Literal["all", "popular", "new"]

    def __init__(self, user_agent: str):
        self.api_endpoints = RedditEndpoints
        self.response_sanitiser = karmakaze.RedditSanitiser
        self.request_handler = RedditRequestHandler(user_agent=user_agent)

    async def infra_status(
        self,
        session: aiohttp.ClientSession,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[t.Dict], None]:

        if status:
            status.update(f"Checking server status")

        status_response: t.Dict = await self.request_handler.send_request(
            session=session,
            endpoint=RedditEndpoints.INFRA_STATUS,
            proxy=proxy,
            proxy_auth=proxy_auth,
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

                status_components: t.Dict = await self.request_handler.send_request(
                    session=session,
                    endpoint=self.api_endpoints.INFRA_COMPONENTS,
                )

                if isinstance(status_components, t.Dict):
                    components: t.List[t.Dict] = status_components.get("components")

                    return components
        return None

    async def comments(
        self,
        session: aiohttp.ClientSession,
        kind: COMMENTS_KIND,
        limit: int,
        sort: SORT,
        timeframe: TIMEFRAME,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        **kwargs: str,
    ) -> t.List[SimpleNamespace]:

        comments_map = {
            "user_overview": f"{self.api_endpoints.USER}/{kwargs.get('username')}/overview.json",
            "user": f"{self.api_endpoints.USER}/{kwargs.get('username')}/comments.json",
            "post": f"{self.api_endpoints.SUBREDDIT}/{kwargs.get('subreddit')}"
            f"/comments/{kwargs.get('id')}.json",
        }

        if status:
            status.update(f"Getting {limit} comments from {kind}")

        endpoint = comments_map[kind]
        params = {"limit": limit, "sort": sort, "t": timeframe, "raw_json": 1}

        comments = await self.request_handler.paginate_response(
            session=session,
            endpoint=endpoint,
            proxy=proxy,
            proxy_auth=proxy_auth,
            params=params,
            limit=limit,
            sanitiser=self.response_sanitiser.comments,
            logger=logger,
            status=status,
            is_post_comments=True if kind == "post" else False,
        )

        if logger:
            logger.info(
                f"{colours.BOLD_GREEN}+{colours.BOLD_GREEN_RESET} Got {len(comments)} of {limit} comments from {kind}"
            )

        return comments

    async def post(
        self,
        id: str,
        subreddit: str,
        session: aiohttp.ClientSession,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        status: t.Optional[Status] = None,
    ) -> SimpleNamespace:
        if status:
            status.update(f"Getting data from post with id {id} in r/{subreddit}")

        response = await self.request_handler.send_request(
            session=session,
            endpoint=f"{self.api_endpoints.SUBREDDIT}/{subreddit}/comments/{id}.json",
            proxy=proxy,
            proxy_auth=proxy_auth,
        )
        sanitised_response = self.response_sanitiser.post(response=response)

        return sanitised_response

    async def posts(
        self,
        session: aiohttp.ClientSession,
        kind: POSTS_KIND,
        limit: int,
        sort: SORT,
        timeframe: TIMEFRAME,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        **kwargs: str,
    ) -> t.List[SimpleNamespace]:

        query = kwargs.get("query")
        subreddit = kwargs.get("subreddit")
        username = kwargs.get("username")

        posts_map = {
            "best": f"{self.api_endpoints.BASE}/r/{kind}.json",
            "controversial": f"{self.api_endpoints.BASE}/r/{kind}.json",
            "front_page": f"{self.api_endpoints.BASE}/.json",
            "new": f"{self.api_endpoints.BASE}/new.json",
            "popular": f"{self.api_endpoints.BASE}/r/{kind}.json",
            "rising": f"{self.api_endpoints.BASE}/r/{kind}.json",
            "subreddit": f"{self.api_endpoints.SUBREDDIT}/{subreddit}.json",
            "user": f"{self.api_endpoints.USER}/{username}/submitted.json",
            "search_subreddit": f"{self.api_endpoints.SUBREDDIT}/{subreddit}/search.json?q={query}&restrict_sr=1",
        }

        if status:
            status.update(
                f"Searching for '{query}' in {limit} posts from {subreddit}"
                if kind == "search_subreddit"
                else f"Getting {limit} {kind} posts"
            )

        endpoint = posts_map[kind]

        params = {"limit": limit, "sort": sort, "t": timeframe, "raw_json": 1}

        if kind == "search_subreddit":
            params = params.update({"q": query, "restrict_sr": 1})

        posts = await self.request_handler.paginate_response(
            session=session,
            endpoint=endpoint,
            proxy=proxy,
            proxy_auth=proxy_auth,
            params=params,
            limit=limit,
            sanitiser=self.response_sanitiser.posts,
            logger=logger,
            status=status,
        )

        if logger:
            logger.info(
                f"{colours.BOLD_GREEN}+{colours.BOLD_GREEN_RESET} Showing {len(posts)} of {limit} {kind} posts"
            )

        return posts

    async def search(
        self,
        session: aiohttp.ClientSession,
        kind: SEARCH_KIND,
        query: str,
        limit: int,
        sort: SORT,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.List[SimpleNamespace]:

        search_map = {
            "posts": self.api_endpoints.BASE,
            "subreddits": self.api_endpoints.SUBREDDITS,
            "users": self.api_endpoints.USERS,
        }

        endpoint = search_map[kind]
        endpoint += f"/search.json"
        params = {"q": query, "limit": limit, "sort": sort, "raw_json": 1}

        if kind == "posts":
            parser = self.response_sanitiser.posts
        elif kind == "subreddits":
            parser = self.response_sanitiser.subreddits
        else:
            parser = self.response_sanitiser.users

        if status:
            status.update(f"Searching for '{query}' in {limit} {kind}")

        results = await self.request_handler.paginate_response(
            session=session,
            endpoint=endpoint,
            proxy=proxy,
            proxy_auth=proxy_auth,
            params=params,
            sanitiser=parser,
            limit=limit,
            logger=logger,
            status=status,
        )

        if logger:
            logger.info(
                f"{colours.BOLD_GREEN}+{colours.BOLD_GREEN_RESET} Showing {len(results)} of {limit} {kind} search results"
            )

        return results

    async def subreddit(
        self,
        name: str,
        session: aiohttp.ClientSession,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        status: t.Optional[Status] = None,
    ) -> SimpleNamespace:
        if status:
            status.update(f"Getting data from subreddit r/{name}")

        response = await self.request_handler.send_request(
            session=session,
            endpoint=f"{self.api_endpoints.SUBREDDIT}/{name}/about.json",
            proxy=proxy,
            proxy_auth=proxy_auth,
        )
        sanitised_response = self.response_sanitiser.subreddit(response=response)

        return sanitised_response

    async def subreddits(
        self,
        session: aiohttp.ClientSession,
        kind: SUBREDDITS_KIND,
        limit: int,
        timeframe: TIMEFRAME,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        **kwargs: str,
    ) -> t.Union[t.List[SimpleNamespace], SimpleNamespace]:

        subreddits_map = {
            "all": f"{self.api_endpoints.SUBREDDITS}.json",
            "default": f"{self.api_endpoints.SUBREDDITS}/default.json",
            "new": f"{self.api_endpoints.SUBREDDITS}/new.json",
            "popular": f"{self.api_endpoints.SUBREDDITS}/popular.json",
            "user_moderated": f"{self.api_endpoints.USER}/{kwargs.get('username')}/moderated_subreddits.json",
        }

        if status:
            status.update(f"Getting {limit} {kind} subreddits")

        endpoint = subreddits_map[kind]
        params = {"raw_json": 1}

        if kind == "user_moderated":
            subreddits = await self.request_handler.send_request(
                session=session,
                endpoint=endpoint,
            )
        else:
            params.update({"limit": limit, "t": str(timeframe)})
            subreddits = await self.request_handler.paginate_response(
                session=session,
                endpoint=endpoint,
                proxy=proxy,
                proxy_auth=proxy_auth,
                params=params,
                sanitiser=self.response_sanitiser.subreddits,
                limit=limit,
                logger=logger,
                status=status,
            )

        if logger:
            logger.info(
                f"{colours.BOLD_GREEN}+{colours.BOLD_GREEN_RESET} Showing {len(subreddits)} of {limit} {kind} subreddits"
            )

        return subreddits

    async def user(
        self,
        name: str,
        session: aiohttp.ClientSession,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        status: t.Optional[Status] = None,
    ) -> SimpleNamespace:
        if status:
            status.update(f"Getting data from user u/{name}")

        response = await self.request_handler.send_request(
            session=session,
            endpoint=f"{self.api_endpoints.USER}/{name}/about.json",
            proxy=proxy,
            proxy_auth=proxy_auth,
        )
        sanitised_response = self.response_sanitiser.user(response=response)

        return sanitised_response

    async def users(
        self,
        session: aiohttp.ClientSession,
        kind: USERS_KIND,
        limit: int,
        timeframe: TIMEFRAME,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
    ) -> t.List[SimpleNamespace]:

        users_map = {
            "all": f"{self.api_endpoints.USERS}.json",
            "new": f"{self.api_endpoints.USERS}/new.json",
            "popular": f"{self.api_endpoints.USERS}/popular.json",
        }

        if status:
            status.update(f"Getting {limit} {kind} users")

        endpoint = users_map[kind]
        params = {
            "limit": limit,
            "t": timeframe,
        }

        users = await self.request_handler.paginate_response(
            session=session,
            endpoint=endpoint,
            proxy=proxy,
            proxy_auth=proxy_auth,
            params=params,
            sanitiser=self.response_sanitiser.users,
            limit=limit,
            logger=logger,
            status=status,
        )

        if logger:
            logger.info(
                f"{colours.BOLD_GREEN}+{colours.BOLD_GREEN_RESET} Showing {len(users)} of {limit} {kind} users"
            )

        return users

    async def wiki_page(
        self,
        name: str,
        subreddit: str,
        session: aiohttp.ClientSession,
        proxy: t.Optional[str] = None,
        proxy_auth: t.Optional[aiohttp.BasicAuth] = None,
        status: t.Optional[Status] = None,
    ) -> SimpleNamespace:
        if status:
            status.update(f"Getting data from wikipage {name} in r/{subreddit}")

        response = await self.request_handler.send_request(
            session=session,
            endpoint=f"{self.api_endpoints.SUBREDDIT}/{subreddit}/wiki/{name}.json",
            proxy=proxy,
            proxy_auth=proxy_auth,
        )
        sanitised_response = self.response_sanitiser.wiki_page(response=response)

        return sanitised_response


# -------------------------------- END ----------------------------------------- #
