# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

from typing import Union, Literal

import aiohttp

from ._coreutils import log
from ._project import version, about_author

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

BASE_REDDIT_ENDPOINT: str = "https://www.reddit.com"
PYPI_PROJECT_ENDPOINT: str = "https://pypi.org/pypi/knewkarma/json"


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_data(session: aiohttp.ClientSession, endpoint: str) -> Union[dict, list]:
    """
    Fetches JSON data from a given API endpoint.

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
                f"(Python {python_version}; +{about_author})"
            },
        ) as response:
            if response.status == 200:
                return await response.json()
            else:
                error_message = await response.json()
                log.error(f"An API error occurred: {error_message}")
                return {}

    except aiohttp.ClientConnectionError as error:
        log.error(f"An HTTP error occurred: [red]{error}[/]")
        return {}
    except Exception as error:
        log.critical(f"An unknown error occurred: [red]{error}[/]")
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
    :param valid_key: The key to check for in the data if it's a dictionary.
    :return: The original data if valid, or an empty dictionary or list if invalid.
    """
    if isinstance(response_data, dict):
        if valid_key:
            return response_data if valid_key in response_data else {}
        else:
            return response_data  # Explicitly return the dictionary if valid_key is not provided
    elif isinstance(response_data, list):
        return response_data if response_data else []
    else:
        log.critical(
            f"Unknown data type ({response_data}: {type(response_data)}), expected a list or dict."
        )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_updates(session: aiohttp.ClientSession):
    """
    Gets and compares the current program version with the remote version.

    Assumes version format: major.minor.patch.prefix

    :param session: aiohttp session to use for the request.
    """

    # Make a GET request to PyPI to get the project's latest release.
    response: dict = await get_data(endpoint=PYPI_PROJECT_ENDPOINT, session=session)
    release: dict = process_response(response_data=response.get("info", {}))

    if release:
        remote_version: str = release.get("version")
        # Splitting the version strings into components
        remote_parts: list = remote_version.split(".")
        local_parts: list = version.split(".")

        update_message: str = ""

        # ---------------------------------------------------------- #

        # Check for differences in version parts
        if remote_parts[0] != local_parts[0]:
            update_message = (
                f"MAJOR update ({remote_version}) available:"
                f" It might introduce significant changes."
            )

        # ---------------------------------------------------------- #

        elif remote_parts[1] != local_parts[1]:
            update_message = (
                f"MINOR update ({remote_version}) available:"
                f" Includes small feature changes/improvements."
            )

        # ---------------------------------------------------------- #

        elif remote_parts[2] != local_parts[2]:
            update_message = (
                f"PATCH update ({remote_version}) available:"
                f" Generally for bug fixes and small tweaks."
            )

        # ---------------------------------------------------------- #

        elif (
            len(remote_parts) > 3
            and len(local_parts) > 3
            and remote_parts[3] != local_parts[3]
        ):
            update_message = (
                f"BUILD update ({remote_version}) available."
                f" Might be for specific builds or special versions."
            )

        # ---------------------------------------------------------- #

        if update_message:
            log.info(update_message)


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_profile(
    profile_source: str,
    session: aiohttp.ClientSession,
    profile_type: str = Literal["user_profile", "subreddit_profile"],
) -> dict:
    """
    Gets profile data from the specified profile_type and profile_source.

    :param profile_source: Source to get profile data from.
    :param session: aiohttp session to use for the request.
    :param profile_type: The type of profile that is to be fetched.
    """
    # Use a dictionary for direct mapping
    source_map: dict = {
        "user_profile": f"{BASE_REDDIT_ENDPOINT}/user/{profile_source}/about.json",
        "subreddit_profile": f"{BASE_REDDIT_ENDPOINT}/r/{profile_source}/about.json",
    }

    # Get the endpoint directly from the dictionary
    endpoint: str = source_map.get(profile_type, "")

    if not endpoint:
        raise ValueError(f"Invalid profile type in {source_map}: {profile_type}")

    profile_data = await get_data(endpoint=endpoint, session=session)
    return process_response(
        response_data=profile_data.get("data", {}), valid_key="created_utc"
    )


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def get_posts(
    limit: int,
    session: aiohttp.ClientSession,
    timeframe: str = Literal["all", "hour", "day", "week", "month", "year"],
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
    """
    Gets a specified number of posts, with a specified sorting criterion, from the specified source.

    :param timeframe: Timeframe from which to get posts.
    :param session: aiohttp session to use for the request.
    :param limit: Maximum number of posts to get.
    :param sort: Posts' sort criterion.
    :param posts_type: Type of posts to be fetched
    :param posts_source: Source from where posts will be fetched.
    """
    source_map = {
        "user_posts": f"{BASE_REDDIT_ENDPOINT}/user/{posts_source}/"
        f"submitted.json?sort={sort}&limit={limit}&t={timeframe}",
        "user_comments": f"{BASE_REDDIT_ENDPOINT}/user/{posts_source}/"
        f"comments.json?sort={sort}&limit={limit}&t={timeframe}",
        "subreddit_posts": f"{BASE_REDDIT_ENDPOINT}/r/{posts_source}.json?sort={sort}&limit={limit}&t={timeframe}",
        "search_posts": f"{BASE_REDDIT_ENDPOINT}/search.json?q={posts_source}&sort={sort}&limit={limit}&t={timeframe}",
        "listing_posts": f"{BASE_REDDIT_ENDPOINT}/r/{posts_source}.json?sort={sort}&limit={limit}&t={timeframe}",
        "front_page_posts": f"{BASE_REDDIT_ENDPOINT}/.json?sort={sort}&limit={limit}&t={timeframe}",
    }

    endpoint = source_map.get(posts_type, "")

    if not endpoint:
        raise ValueError(f"Invalid profile type in {source_map}: {posts_type}")

    all_posts = await paginated_posts(
        posts_endpoint=endpoint, limit=limit, session=session
    )

    return all_posts[:limit]


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #


async def paginated_posts(
    posts_endpoint: str, limit: int, session: aiohttp.ClientSession
) -> list:
    """
    Paginates and retrieves posts until the specified limit is reached.

    :param posts_endpoint: API endpoint for retrieving posts.
    :param limit: Limit of the number of posts to retrieve.
    :param session: aiohttp session to use for the request.
    :return: A list of all posts.
    """
    all_posts: list = []
    last_post_id: str = ""

    # Determine whether to use the 'after' parameter
    use_after: bool = limit > 100

    while len(all_posts) < limit:
        # ---------------------------------------------------------- #

        # Make the API request with the 'after' parameter if it's provided and the limit is more than 100
        if use_after and last_post_id:
            endpoint_with_after: str = f"{posts_endpoint}&after={last_post_id}"
        else:
            endpoint_with_after: str = posts_endpoint

        # ---------------------------------------------------------- #

        raw_posts_data: dict = await get_data(
            endpoint=endpoint_with_after, session=session
        )
        posts_list: list = raw_posts_data.get("data", {}).get("children", [])

        # If there are no more posts, break out of the loop
        if not posts_list:
            break

        all_posts.extend(process_response(response_data=posts_list))

        # We use the id of the last post in the list to paginate to the next posts
        last_post_id: str = all_posts[-1].get("data").get("id")

        # ---------------------------------------------------------- #

    return all_posts


# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
