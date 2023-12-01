# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from typing import Union, Literal

import aiohttp

from ._coreutils import log
from ._metadata import (
    version,
)

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

BASE_REDDIT_ENDPOINT: str = "https://www.reddit.com"
PYPI_PROJECT_ENDPOINT: str = "https://pypi.org/project/knewkarma/json"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def _get_data(session: aiohttp.ClientSession, endpoint: str) -> Union[dict, list]:
    """
    Fetches JSON data from a given API endpoint asynchronously using aiohttp.

    :param session: aiohttp session to use for the request.
    :param endpoint: The API endpoint to fetch data from.
    :return: Returns JSON data as a dictionary or list. Returns an empty dict if fetching fails.
    """
    from sys import version as python_version

    try:
        async with session.get(
            endpoint,
            headers={
                "User-Agent": f"Knew-Karma/{version} "
                f"(Python {python_version}; +https://about.me/rly0nheart)"
            },
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.json()
                log.error(f"An API error occurred: {error_message}")
                return {}

    except aiohttp.ClientConnectionError as error:
        log.error(f"An HTTP error occurred: {error}")
        return {}
    except Exception as error:
        log.critical(f"An unknown error occurred: {error}")
        return {}


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


def _validate_data(data: Union[dict, list], valid_key: str = None) -> Union[dict, list]:
    """
    Validates the input data. If it's a dictionary and a valid_key is provided,
    checks for the presence of the key in the dictionary. If it's a list, it
    ensures the list is not empty.

    :param data: The data to validate, which should be a dictionary, list or set.
    :param valid_key: The key to check for in the data if it's a dictionary.
    :return: The original data if valid, or an empty dictionary or list if invalid.
    """
    if isinstance(data, dict):
        if valid_key:
            return data if valid_key in data else {}
        else:
            return data  # Explicitly return the dictionary if valid_key is not provided
    elif isinstance(data, list):
        return data if data else []
    else:
        log.critical(
            f"Unknown data type ({data}: {type(data).__name__}), expected a list or dict."
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_updates(session: aiohttp.ClientSession):
    """
    Gets and compares the current program version with the remote version
    Assumes version format: major.minor.patch.prefix
    """
    import sys

    # Make a GET request to PyPI to get the project's latest release.
    response: dict = await _get_data(endpoint=PYPI_PROJECT_ENDPOINT, session=session)
    release: dict = _validate_data(data=response.get("info", {}))

    if release:
        if release.get("name") != "knewkarma":
            log.critical(
                f"PyPI project endpoint was modified "
                f"{PYPI_PROJECT_ENDPOINT}: knewkarma/__init__.py: Line 15"
            )
            sys.exit()

        remote_version: str = release.get("version")
        # Splitting the version strings into components
        remote_parts: list = remote_version.split(".")
        local_parts: list = version.split(".")

        update_message: str = ""

        # Check for differences in version parts
        if remote_parts[0] != local_parts[0]:
            update_message = (
                f"MAJOR update ({remote_version}) available."
                f" It might introduce significant changes."
            )

        elif remote_parts[1] != local_parts[1]:
            update_message = (
                f"MINOR update ({remote_version}) available."
                f" Includes small feature changes/improvements."
            )

        elif remote_parts[2] != local_parts[2]:
            update_message = (
                f"PATCH update ({remote_version}) available."
                f" Generally for bug fixes and small tweaks."
            )

        elif (
            len(remote_parts) > 3
            and len(local_parts) > 3
            and remote_parts[3] != local_parts[3]
        ):
            update_message = (
                f"BUILD update ({remote_version}) available."
                f" Might be for specific builds or special versions."
            )

        if update_message:
            log.info(update_message)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_profile(
    profile_source: str,
    session: aiohttp.ClientSession,
    profile_type: str = Literal["user_profile", "subreddit_profile"],
) -> dict:
    # Use a dictionary for direct mapping
    source_map: dict = {
        "user_profile": f"{BASE_REDDIT_ENDPOINT}/user/{profile_source}/about.json",
        "subreddit_profile": f"{BASE_REDDIT_ENDPOINT}/r/{profile_source}/about.json",
    }

    # Get the endpoint directly from the dictionary
    endpoint: str = source_map.get(profile_type, "user")

    if not endpoint:
        raise ValueError(f"Invalid source type: {profile_type}")

    profile = await _get_data(endpoint=endpoint, session=session)
    return _validate_data(data=profile.get("data", {}), valid_key="created_utc")


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_posts(
    session: aiohttp.ClientSession,
    limit: int,
    sort: str = Literal[
        "all",
        "controversial",
        "new",
        "top",
        "best",
        "hot",
        "rising",
    ],
    posts_type: str = Literal[
        "user_posts",
        "user_comments",
        "subreddit_posts",
        "search_posts",
        "listing_posts",
        "front_page_posts",
    ],
    posts_source: str = None,
) -> list:
    source_map = {
        "user_posts": f"{BASE_REDDIT_ENDPOINT}/user/{posts_source}/submitted.json?sort={sort}&limit={limit}",
        "user_comments": f"{BASE_REDDIT_ENDPOINT}/user/{posts_source}/comments.json?sort={sort}&limit={limit}",
        "subreddit_posts": f"{BASE_REDDIT_ENDPOINT}/r/{posts_source}.json?sort={sort}&limit={limit}",
        "search_posts": f"{BASE_REDDIT_ENDPOINT}/search.json?q={posts_source}&sort={sort}&limit={limit}",
        "listing_posts": f"{BASE_REDDIT_ENDPOINT}/r/{posts_source}.json?sort={sort}&limit={limit}",
        "front_page_posts": f"{BASE_REDDIT_ENDPOINT}/.json?sort={sort}&limit={limit}",
    }

    endpoint = source_map.get(posts_type, "")

    if not endpoint:
        raise ValueError(f"Invalid posts type: {posts_type}")

    all_posts = await _paginate_posts(
        posts_endpoint=endpoint, limit=limit, session=session
    )

    return all_posts[:limit]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def _paginate_posts(
    posts_endpoint: str, limit: int, session: aiohttp.ClientSession
) -> list:
    """
    Paginates through posts' data and retrieves posts until the specified limit is reached.

    :param posts_endpoint: API endpoint for retrieving posts.
    :param limit: Limit of the number of posts to retrieve.
    :return: A list of posts.
    """
    all_posts: list = []
    last_post_id: str = ""

    # Determine whether to use the 'after' parameter
    use_after: bool = limit > 100

    while len(all_posts) < limit:
        # Make the API request with the 'after' parameter if it's provided and the limit is more than 100
        if use_after and last_post_id:
            endpoint_with_after: str = f"{posts_endpoint}&after={last_post_id}"
        else:
            endpoint_with_after: str = posts_endpoint

        posts_data: dict = await _get_data(
            endpoint=endpoint_with_after, session=session
        )
        posts_children: list = posts_data.get("data", {}).get("children", [])

        # If there are no more posts, break out of the loop
        if not posts_children:
            break

        all_posts.extend(_validate_data(data=posts_children))

        # We use the id of the last post in the list to paginate to the next posts
        last_post_id: str = all_posts[-1].get("data").get("id")

    return all_posts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
