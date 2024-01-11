# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from sys import version as python_version
from typing import Union, Literal

import aiohttp
import rich
from rich.markdown import Markdown

from ._coreutils import console
from .docs import (
    Version,
    ABOUT_AUTHOR,
    DATA_SORT_CRITERION,
    DATA_TIMEFRAME,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

BASE_REDDIT_ENDPOINT: str = "https://www.reddit.com"
USER_DATA_ENDPOINT: str = f"{BASE_REDDIT_ENDPOINT}/u"
USERS_DATA_ENDPOINT: str = f"{BASE_REDDIT_ENDPOINT}/users"
COMMUNITY_DATA_ENDPOINT: str = f"{BASE_REDDIT_ENDPOINT}/r"
COMMUNITIES_DATA_ENDPOINT: str = f"{BASE_REDDIT_ENDPOINT}/subreddits"
GITHUB_RELEASE_ENDPOINT: str = (
    "https://api.github.com/repos/bellingcat/knewkarma/releases/latest"
)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_data(session: aiohttp.ClientSession, endpoint: str) -> Union[dict, list]:
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
                "User-Agent": f"Knew-Karma/{Version.version} "
                f"(Python {python_version}; +{ABOUT_AUTHOR})"
            },
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.json()
                console.log(f"An API error occurred: {error_message}")
                return {}

    except aiohttp.ClientConnectionError as error:
        console.log(f"An HTTP error occurred: [red]{error}[/]")
        return {}
    except Exception as error:
        console.log(f"An unknown error occurred: [red]{error}[/]")
        return {}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def process_response(
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
            return response_data  # Explicitly return the dictionary if valid_key is not provided
    elif isinstance(response_data, list):
        return response_data if response_data else []
    else:
        console.log(
            f"Unknown data type ({response_data}: {type(response_data)}), expected a list or dict."
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_updates(session: aiohttp.ClientSession):
    """
    Asynchronously gets and compares the current program version with the remote version.

    Assumes version format: major.minor.patch.prefix

    :param session: aiohttp session to use for the request.
    :type session: aiohttp.ClientSession
    """
    # Make a GET request to PyPI to get the project's latest release.
    response: dict = await get_data(endpoint=GITHUB_RELEASE_ENDPOINT, session=session)
    release: dict = process_response(response_data=response, valid_key="tag_name")

    if release:
        remote_version: str = release.get("tag_name")
        markup_release_notes: str = release.get("body")
        markdown_release_notes = Markdown(markup=markup_release_notes)

        # Splitting the version strings into components
        remote_parts: list = remote_version.split(".")

        update_message: str = f"%s update ({remote_version}) available"

        # ------------------------------------------------------------------------- #

        # Check for differences in version parts
        if remote_parts[0] != Version.major:
            update_message = update_message % "MAJOR"

        # ------------------------------------------------------------------------- #

        elif remote_parts[1] != Version.minor:
            update_message = update_message % "MINOR"

        # ------------------------------------------------------------------------- #

        elif remote_parts[2] != Version.patch:
            update_message = update_message % "PATCH"

        # ------------------------------------------------------------------------- #

        if update_message:
            console.log(update_message)
            rich.print(markdown_release_notes)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_profile(
    profile_source: str,
    profile_type: Literal["user", "community"],
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
        "user": f"{USER_DATA_ENDPOINT}/{profile_source}/about.json",
        "community": f"{COMMUNITY_DATA_ENDPOINT}/{profile_source}/about.json",
    }

    # ------------------------------------------------------------------------- #

    # Get the endpoint directly from the dictionary
    endpoint: str = profile_mapping.get(profile_type, "")

    # ------------------------------------------------------------------------- #

    profile_data = await get_data(endpoint=endpoint, session=session)
    return process_response(
        response_data=profile_data.get("data", {}), valid_key="created_utc"
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def __fetch_and_paginate(
    session: aiohttp.ClientSession,
    data_endpoint: str,
    process_func: callable,
    limit: int,
    **kwargs,
):
    """
    Fetches data in a paginated manner from a given endpoint and processes it using a specified function.

    :param session: aiohttp.ClientSession to use for the request.
    :type session: aiohttp.ClientSession
    :param data_endpoint: The data endpoint for the API request.
    :type data_endpoint: str
    :param process_func: Function to process each batch of data.
    :type process_func: callable
    :param limit: The maximum number of items to fetch.
    :type limit: int
    :param kwargs: Additional keyword arguments to pass to the processing function.
    :type kwargs: Any
    :return: A list of processed data items.
    :rtype: list[dict]
    """
    all_items = []
    last_item_id = ""
    paginate = limit > 100

    # ------------------------------------------------------------------------- #

    while len(all_items) < limit:
        if paginate and last_item_id:
            endpoint = f"{data_endpoint}&after={last_item_id}"
        else:
            endpoint = data_endpoint

        # -------------------------------------------------------------------- #

        raw_data = await get_data(session=session, endpoint=endpoint)
        data_list = raw_data.get("data", {}).get("children", [])

        if not data_list:
            break

        needed_count = limit - len(all_items)
        processed_data = process_func(response_data=data_list[:needed_count], **kwargs)

        # -------------------------------------------------------------------- #

        all_items.extend(processed_data)

        if len(data_list) > 0:
            last_item_id = data_list[-1].get("data").get("id")

        if needed_count <= 0:
            break

    return all_items


async def get_posts(
    session: aiohttp.ClientSession,
    limit: int,
    posts_type: Literal[
        "new",
        "front_page",
        "listing",
        "community",
        "user_posts",
        "user_overview",
        "user_comments",
    ],
    posts_source: str = None,
    timeframe: DATA_TIMEFRAME = "all",
    sort: DATA_SORT_CRITERION = "all",
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
        "new": f"{BASE_REDDIT_ENDPOINT}/new.json",
        "front_page": f"{BASE_REDDIT_ENDPOINT}/.json",
        "listing": f"{COMMUNITY_DATA_ENDPOINT}/{posts_source}.json?",
        "community": f"{COMMUNITY_DATA_ENDPOINT}/{posts_source}.json",
        "user_posts": f"{USER_DATA_ENDPOINT}/{posts_source}/submitted.json",
        "user_overview": f"{USER_DATA_ENDPOINT}/{posts_source}/overview.json",
        "user_comments": f"{USER_DATA_ENDPOINT}/{posts_source}/comments.json",
    }

    # ------------------------------------------------------------------------- #

    endpoint = source_map.get(posts_type, "")
    if posts_type == "new_posts":
        endpoint += f"?limit={limit}&sort={sort}"
    else:
        endpoint += f"?limit={limit}&sort={sort}&t={timeframe}"

    # ------------------------------------------------------------------------- #

    posts: list[dict] = await __fetch_and_paginate(
        session=session,
        data_endpoint=endpoint,
        process_func=process_response,
        limit=limit,
        valid_key="data",
    )

    # ------------------------------------------------------------------------- #

    return posts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_searches(
    session: aiohttp.ClientSession,
    search_type: Literal["users", "communities", "posts"],
    query: str,
    limit: int,
    sort: DATA_SORT_CRITERION = "all",
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
        "users": f"{USERS_DATA_ENDPOINT}/search.json",
        "communities": f"{COMMUNITIES_DATA_ENDPOINT}/search.json",
        "posts": f"{BASE_REDDIT_ENDPOINT}/search.json",
    }

    # ------------------------------------------------------------------------- #

    endpoint = search_mapping.get(search_type, "")
    if search_type == "posts":
        endpoint += f"?q={query}&limit={limit}&sort={sort}&t={timeframe}"
    else:
        endpoint += f"?q={query}&limit={limit}"

    # ------------------------------------------------------------------------- #

    search_results: list[dict] = await __fetch_and_paginate(
        session=session,
        data_endpoint=endpoint,
        process_func=process_response,
        limit=limit,
        valid_key="data",
    )

    # ------------------------------------------------------------------------- #

    return search_results


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_communities(
    communities_type: Literal["all", "default", "new", "popular"],
    limit: int,
    session: aiohttp.ClientSession,
) -> list[dict]:
    """
    Asynchronously gets the specified type of communities.

    :param communities_type: Type of communities to get.
    :type communities_type: str
    :param limit: Maximum number of communities to return.
    :type limit: int
    :param session: Aiohttp session to use for the request.
    :type session: aiohttp.ClientSession
    """
    communities_mapping: dict = {
        "all": f"{COMMUNITIES_DATA_ENDPOINT}.json",
        "default": f"{COMMUNITIES_DATA_ENDPOINT}/default.json",
        "new": f"{COMMUNITIES_DATA_ENDPOINT}/new.json",
        "popular": f"{COMMUNITIES_DATA_ENDPOINT}/popular.json",
    }

    endpoint = communities_mapping.get(communities_type, "")
    endpoint += f"?limit={limit}"

    # ------------------------------------------------------------------------- #

    communities: list[dict] = await __fetch_and_paginate(
        session=session,
        data_endpoint=endpoint,
        process_func=process_response,
        limit=limit,
        valid_key="data",
    )

    # ------------------------------------------------------------------------- #

    return communities


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
