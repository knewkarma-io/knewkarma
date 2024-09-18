import re
from collections import Counter
from types import SimpleNamespace
from typing import Literal, Union, Optional, List

import aiohttp
from karmakaze import Parse
from rich.status import Status

from .shared_imports import api, SORT_CRITERION, TIMEFRAME, TIME_FORMAT
from .tools.data import plot_bar_chart

__all__ = [
    "Comment",
    "Post",
    "Posts",
    "Search",
    "Subreddit",
    "Subreddits",
    "User",
    "Users",
]


class Comment:
    """Represents a Reddit comment and provides methods for interacting with it."""

    pass


class Post:
    """Represents a Reddit post and provides methods for fetching post data and comments."""

    def __init__(self, id: str, subreddit: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Post` instance to fetch the post's data and comments.

        :param id: The ID of the Reddit post to retrieve.
        :type id: str
        :param subreddit: The subreddit where the post was created.
        :type subreddit: str
        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """

        self._id = id
        self._subreddit = subreddit
        self._parse = Parse(time_format=time_format)

    async def data(
        self, session: aiohttp.ClientSession, status: Optional[Status] = None
    ) -> SimpleNamespace:
        """
        Asynchronously retrieves data for a Reddit post, excluding comments.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A `SimpleNamespace` object containing parsed post data.
        :rtype: SimpleNamespace
        """

        post_data = await api.get_entity(
            session=session,
            status=status,
            entity_type="post",
            post_id=self._id,
            post_subreddit=self._subreddit,
        )

        parsed_post = self._parse.post(post_data)

        return parsed_post if post_data else SimpleNamespace

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves comments for a Reddit post.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of comments to retrieve.
        :type limit: int
        :param sort: The sorting criterion for the comments. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed comment data.
        :rtype: List[SimpleNamespace]
        """

        comments_data = await api.get_posts(
            session=session,
            status=status,
            posts_type="post_comments",
            post_id=self._id,
            post_subreddit=self._subreddit,
            limit=limit,
            sort=sort,
        )

        parsed_comments = self._parse.comments(comments_data)

        return parsed_comments if comments_data else [SimpleNamespace]


class Posts:
    """Represents Reddit posts and provides methods for retrieving posts from various sources."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Posts` instance for retrieving posts such as 'best', 'controversial',
        'front-page', 'new', 'popular', and 'rising'.

        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """
        self._parse = Parse(time_format=time_format)

    async def best(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the best posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        best_posts = await api.get_posts(
            session=session,
            status=status,
            posts_type="best",
            timeframe=timeframe,
            limit=limit,
        )

        parsed_posts = self._parse.posts(best_posts)

        return parsed_posts if best_posts else [SimpleNamespace]

    async def controversial(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the controversial posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        controversial_posts = await api.get_posts(
            session=session,
            status=status,
            posts_type="controversial",
            timeframe=timeframe,
            limit=limit,
        )

        parsed_posts = self._parse.posts(controversial_posts)

        return parsed_posts if controversial_posts else [SimpleNamespace]

    async def front_page(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        sort: SORT_CRITERION = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the front-page posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        front_page_posts = await api.get_posts(
            posts_type="front_page",
            limit=limit,
            timeframe=timeframe,
            sort=sort,
            status=status,
            session=session,
        )

        parsed_posts = self._parse.posts(front_page_posts)

        return parsed_posts if front_page_posts else [SimpleNamespace]

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        sort: SORT_CRITERION = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the new posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        new_posts = await api.get_posts(
            posts_type="new",
            limit=limit,
            timeframe=timeframe,
            sort=sort,
            status=status,
            session=session,
        )

        parsed_posts = self._parse.posts(new_posts)

        return parsed_posts if new_posts else [SimpleNamespace]

    async def popular(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the popular posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """
        popular_posts = await api.get_posts(
            session=session,
            status=status,
            posts_type="popular",
            timeframe=timeframe,
            limit=limit,
        )

        parsed_posts = self._parse.posts(popular_posts)

        return parsed_posts if popular_posts else [SimpleNamespace]

    async def rising(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves the rising posts.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        rising_posts = await api.get_posts(
            session=session,
            status=status,
            posts_type="rising",
            timeframe=timeframe,
            limit=limit,
        )

        parsed_posts = self._parse.posts(rising_posts)

        return parsed_posts if rising_posts else [SimpleNamespace]


class Search:
    """
    Represents the Reddit search functionality and provides methods for retrieving search results
    from different entities.
    """

    def __init__(self, query: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Search` instance for searching posts, subreddits, and users.

        :param query: The search query string.
        :type query: str
        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """

        self._query = query
        self._parse = Parse(time_format=time_format)

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves posts that match with the specified query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param sort: Sorting criterion for posts. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await api.search_entities(
            session=session,
            status=status,
            query=self._query,
            entity_type="posts",
            sort=sort,
            limit=limit,
        )

        parsed_posts = self._parse.posts(search_results)

        return parsed_posts if search_results else [SimpleNamespace]

    async def subreddits(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves subreddits that match with the specified query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to retrieve.
        :type limit: int
        :param sort: Sorting criterion for subreddits. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed subreddit data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await api.search_entities(
            session=session,
            status=status,
            query=self._query,
            entity_type="subreddits",
            sort=sort,
            limit=limit,
        )

        parsed_subreddits = self._parse.subreddits(search_results)

        return parsed_subreddits if search_results else [SimpleNamespace]

    async def users(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves users that match with the specified query.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of users to retrieve.
        :type limit: int
        :param sort: Sorting criterion for users. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed user data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await api.search_entities(
            session=session,
            status=status,
            query=self._query,
            entity_type="users",
            sort=sort,
            limit=limit,
        )

        parsed_users = self._parse.users(search_results)

        return parsed_users if search_results else [SimpleNamespace]


class Subreddit:
    """Represents a Reddit community (subreddit) and provides methods for retrieving its data."""

    def __init__(self, name: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `Subreddit` instance to get a subreddit's profile, wiki pages, and posts data,
        and to search for posts containing a specified query.

        :param name: The name of the subreddit to retrieve data from.
        :type name: str
        :param time_format: Format for displaying time, either 'concise' or 'locale'. Defaults to 'locale'.
        :type time_format: Literal["concise", "locale"]
        """

        self._name = name
        self._time_format = (
            time_format  # This will also be accessed in the comments method
        )
        self._parse = Parse(time_format=self._time_format)

    async def comments(
        self,
        session: aiohttp.ClientSession,
        posts_limit: int,
        comments_per_post: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves comments from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param posts_limit: Maximum number of posts to retrieve comments from.
        :type posts_limit: int
        :param comments_per_post: Maximum number of comments to retrieve per post.
        :type comments_per_post: int
        :param sort: Sorting criterion for the posts and comments. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param timeframe: The timeframe from which to retrieve posts and comments. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed comment data.
        :rtype: List[SimpleNamespace]
        """

        posts = await self.posts(
            session=session,
            status=status,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
        )
        all_comments: List = []
        for post in posts:
            post = Post(
                id=post.get("id"),
                subreddit=post.get("subreddit"),
                time_format=self._time_format,
            )
            post_comments = await post.comments(
                session=session, limit=comments_per_post, sort=sort, status=status
            )

            all_comments.extend(post_comments)

        return all_comments

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves posts from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of posts to retrieve.
        :type limit: int
        :param sort: Sorting criterion for the posts. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param timeframe: The timeframe from which to retrieve posts. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of `SimpleNamespace` objects, each containing parsed post data.
        :rtype: List[SimpleNamespace]
        """

        subreddit_posts = await api.get_posts(
            session=session,
            status=status,
            posts_type="subreddit_posts",
            subreddit=self._name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        parsed_posts = self._parse.posts(subreddit_posts)

        return parsed_posts if subreddit_posts else [SimpleNamespace]

    async def profile(
        self, session: aiohttp.ClientSession, status: Optional[Status] = None
    ) -> SimpleNamespace:
        """
        Asynchronously retrieves a subreddit's profile data.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param status: An optional `Status` object for displaying status messages.
        :type status: Optional[rich.status.Status]
        :return: A `SimpleNamespace` object containing the parsed subreddit profile data.
        :rtype: SimpleNamespace
        """

        subreddit_profile = await api.get_entity(
            session=session,
            status=status,
            entity_type="subreddit",
            subreddit=self._name,
        )

        parsed_profile = self._parse.subreddit(subreddit_profile)

        return parsed_profile if subreddit_profile else SimpleNamespace

    async def search_comments(
        self,
        session: aiohttp.ClientSession,
        query: str,
        posts_limit: int,
        comments_per_post: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously retrieves comments that contain the specified query from a subreddit.

        :param session: An `aiohttp.ClientSession` for making the HTTP request.
        :type session: aiohttp.ClientSession
        :param query: Search query.
        :type query: str
        :param posts_limit: Maximum number of posts to retrieve comments from.
        :type posts_limit: int
        :param comments_per_post: Maximum number of comments to retrieve for each post.
        :type comments_per_post: int
        :param sort: Sorting criterion for the comments. Defaults to "all".
        :type sort: SORT_CRITERION, optional
        :param timeframe: The timeframe from which to retrieve comments. Defaults to "all".
        :type timeframe: TIMEFRAME, optional
        :param status: An instance of `Status` used to display animated status messages.
        :type: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing comment data.
        :rtype: List[SimpleNamespace]
        """

        posts = await self.posts(
            session=session,
            status=status,
            limit=posts_limit,
            sort=sort,
            timeframe=timeframe,
        )
        all_comments: List = []
        found_comments: List = []
        for post in posts:
            post = Post(
                id=post.get("id"),
                subreddit=self._name,
                time_format=self._time_format,
            )

            comments = await post.comments(
                session=session, limit=comments_per_post, status=status
            )

            all_comments.extend(comments)

        pattern = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        for comment in all_comments:
            match: re.Match = regex.search(comment.body)
            if match:
                found_comments.append(comment)

        if found_comments:
            return found_comments

    async def search_posts(
        self,
        session: aiohttp.ClientSession,
        query: str,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get posts that contain the specified query string from a subreddit.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param query: Search query.
        :type query: str
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing post data.
        :rtype: List[SimpleNamespace]
        """

        search_results = await api.get_posts(
            session=session,
            status=status,
            posts_type="search_subreddit_posts",
            subreddit=self._name,
            query=query,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        parsed_posts = self._parse.posts(search_results)

        return parsed_posts if search_results else [SimpleNamespace]

    async def wiki_pages(
        self, session: aiohttp.ClientSession, status: Optional[Status] = None
    ) -> List[str]:
        """
        Asynchronously get a subreddit's wiki pages.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of strings, each representing a wiki page.
        :rtype: List[str]
        """

        if status:
            status.update(
                f"Retrieving wiki pages from subreddit ({self._name})",
            )

        pages = await api.make_request(
            endpoint=f"{api.subreddit_endpoint}/{self._name}/wiki/pages.json",
            session=session,
        )

        return pages.get("data")

    async def wiki_page(
        self,
        page_name: str,
        session: aiohttp.ClientSession,
        status: Optional[Status] = None,
    ) -> SimpleNamespace:
        """
        Asynchronously get a subreddit's specified wiki page data.

        :param page_name: Wiki page to get data from.
        :type page_name: str
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of strings, each representing a wiki page.
        :rtype: List[str]
        """

        wiki_page = await api.get_entity(
            session=session,
            status=status,
            entity_type="wiki_page",
            page_name=page_name,
            subreddit=self._name,
        )

        parsed_wiki_page = self._parse.wiki_page(wiki_page)

        return parsed_wiki_page if wiki_page else SimpleNamespace


class Subreddits:
    """Represents Reddit subreddits and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Subreddits()` instance for getting `all`, `default`, `new` and `popular` subreddits.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """

        self._parse = Parse(time_format=time_format)

    async def all(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get all subreddits.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get all subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]

        Note:
            -*imitating Morphius' voice*- "the only limitation you have at this point is the matrix's rate-limit."
        """

        all_subreddits = await api.get_subreddits(
            session=session,
            status=status,
            subreddits_type="all",
            limit=limit,
            timeframe=timeframe,
        )

        parsed_subreddits = self._parse.subreddits(all_subreddits)

        return parsed_subreddits if all_subreddits else [SimpleNamespace]

    async def default(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get default subreddits.

        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        default_subreddits = await api.get_subreddits(
            session=session,
            status=status,
            subreddits_type="default",
            timeframe="all",
            limit=limit,
        )

        parsed_subreddits = self._parse.subreddits(default_subreddits)

        return parsed_subreddits if default_subreddits else [SimpleNamespace]

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get new subreddits.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """
        new_subreddits = await api.get_subreddits(
            session=session,
            status=status,
            subreddits_type="new",
            limit=limit,
            timeframe=timeframe,
        )

        parsed_subreddits = self._parse.subreddits(new_subreddits)

        return parsed_subreddits if new_subreddits else [SimpleNamespace]

    async def popular(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get popular subreddits.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of subreddits to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular subreddits.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        popular_subreddits = await api.get_subreddits(
            session=session,
            status=status,
            subreddits_type="popular",
            limit=limit,
            timeframe=timeframe,
        )

        parsed_subreddits = self._parse.subreddits(popular_subreddits)

        return parsed_subreddits if popular_subreddits else [SimpleNamespace]


class User:
    """Represents a Reddit user and provides methods for getting data from the specified user."""

    def __init__(self, name: str, time_format: TIME_FORMAT = "locale"):
        """
        Initialises a `User()` instance for getting a user's `profile`, `posts` and `comments` data.

        :param name: Username to get data from.
        :type name: str
        :param time_format: Time format of the output data. Use "concise" for a human-readable
                        time difference, or "locale" for a localized datetime string. Defaults to "locale".
        :type time_format: Literal["concise", "locale"]
        """

        self._name = name
        self._parse = Parse(time_format=time_format)

    async def comments(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's comments.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to return.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which tyo get comments.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing comment data.
        :rtype: List[SimpleNamespace]
        """

        user_comments = await api.get_posts(
            session=session,
            status=status,
            username=self._name,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        parsed_comments = self._parse.comments(user_comments)

        return parsed_comments if user_comments else [SimpleNamespace]

    async def moderated_subreddits(
        self, session: aiohttp.ClientSession, status: Optional[Status] = None
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get subreddits moderated by user.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing subreddit data.
        :rtype: List[SimpleNamespace]
        """

        subreddits = await api.get_subreddits(
            session=session,
            status=status,
            subreddits_type="user_moderated",
            username=self._name,
            limit=0,
        )

        parsed_subreddits = self._parse.subreddits(subreddits)

        return parsed_subreddits if subreddits else [SimpleNamespace]

    async def overview(
        self,
        limit: int,
        session: aiohttp.ClientSession,
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's most recent comments.

        :param limit: Maximum number of comments to return.
        :type limit: int
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing data about a recent comment.
        :rtype: List[SimpleNamespace]
        """

        user_overview = await api.get_posts(
            username=self._name,
            posts_type="user_overview",
            limit=limit,
            status=status,
            session=session,
        )

        parsed_overview = self._parse.comments(user_overview)

        return parsed_overview if user_overview else [SimpleNamespace]

    async def posts(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's posts.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to return.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing post data.
        :rtype: List[SimpleNamespace]
        """

        user_posts = await api.get_posts(
            session=session,
            status=status,
            username=self._name,
            posts_type="user_posts",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )

        parsed_posts = self._parse.posts(user_posts)

        return parsed_posts if user_posts else [SimpleNamespace]

    async def profile(
        self, session: aiohttp.ClientSession, status: Optional[Status] = None
    ) -> SimpleNamespace:
        """
        Asynchronously get a user's profile data.

        :param session: A aiohttp.ClientSession session to use for the request.
        :type session: aiohttp.ClientSession
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A SimpleNamespace object containing user profile data.
        :rtype: SimpleNamespace
        """

        user_profile = await api.get_entity(
            username=self._name, entity_type="user", status=status, session=session
        )

        parsed_profile = self._parse.user(user_profile)

        return parsed_profile if user_profile else SimpleNamespace

    async def search_posts(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's posts that match with the specified search query.

        :param query: Search query.
        :type query: str
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of posts to search from.
        :type limit: int
        :param sort: Sort criterion for the posts.
        :type sort: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing post data.
        :rtype: List[SimpleNamespace]
        """

        pattern = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        user_posts = await api.get_posts(
            session=session,
            status=status,
            posts_type="user_posts",
            username=self._name,
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )
        found_posts = []

        for post in user_posts:
            post_data = post.get("data")

            match: re.Match = regex.search(post_data.get("title", "")) or regex.search(
                post_data.get("selftext", "")
            )

            if match:
                found_posts.append(post)

        parsed_post = self._parse.posts(found_posts)

        return parsed_post if found_posts else [SimpleNamespace]

    async def search_comments(
        self,
        query: str,
        limit: int,
        session: aiohttp.ClientSession,
        sort: SORT_CRITERION = "all",
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get a user's comments that contain the specified search query.

        :param query: Search query.
        :type query: str
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :type session: aiohttp.ClientSession.
        :param limit: Maximum number of comments to search from.
        :type limit: int
        :param sort: Sort criterion for the comments.
        :type sort: str
        :param timeframe: Timeframe from which to get comments.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing comment data.
        :rtype: List[SimpleNamespace]
        """

        pattern: str = rf"(?i)\b{re.escape(query)}\b"
        regex: re.Pattern = re.compile(pattern, re.IGNORECASE)

        user_comments = await api.get_posts(
            session=session,
            status=status,
            username=self._name,
            posts_type="user_comments",
            limit=limit,
            sort=sort,
            timeframe=timeframe,
        )
        found_comments = []

        for comment in user_comments:
            match = regex.search(comment.get("data", {}).get("body", ""))
            if match:
                found_comments.append(comment)

        parsed_comments = self._parse.comments(found_comments)

        return parsed_comments if user_comments else [SimpleNamespace]

    async def top_subreddits(
        self,
        session: aiohttp.ClientSession,
        top_n: int,
        limit: int,
        filename: str = None,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> Union[List[tuple[str, int]], None]:
        """
        Asynchronously get a user's top n subreddits based on subreddit frequency in n posts and saves the analysis to a file.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param top_n: Communities arranging number.
        :type top_n: int
        :param limit: Maximum number of posts to scrape.
        :type limit: int
        :param filename: Filename to which the analysis will be saved.
        :type filename: str
        :param timeframe: Timeframe from which to get posts.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        """

        posts = await api.get_posts(
            session=session,
            status=status,
            posts_type="user_posts",
            username=self._name,
            limit=limit,
            timeframe=timeframe,
        )

        if posts:
            # Extract subreddit names
            subreddits = [post.get("data", {}).get("subreddit") for post in posts]

            # Count the occurrences of each subreddit
            subreddit_counts: Counter = Counter(subreddits)

            # Get the most common subreddits
            top_subreddits: List[tuple[str, int]] = subreddit_counts.most_common(top_n)

            # Prepare data for plotting
            subreddit_names = [subreddit[0] for subreddit in top_subreddits]
            subreddit_frequencies = [subreddit[1] for subreddit in top_subreddits]

            plot_bar_chart(
                data=dict(zip(subreddit_names, subreddit_frequencies)),
                title=f"top {top_n}/{limit} subreddits analysis",
                xlabel="Subreddits",
                ylabel="Frequency",
                figure_size=(top_n + 10, 5),
                colours=["lightblue"] * top_n,
                filename=f"{filename + '_' if filename else ''}top_{top_n}_of_{limit}_subreddits",
            )
            return top_subreddits


class Users:
    """Represents Reddit users and provides methods for getting related data."""

    def __init__(self, time_format: TIME_FORMAT = "locale"):
        """
        Initialises the `Users()` instance for getting `new`, `popular` and `all` users.

        :param time_format: Time format of the output data. Use `concise` for a human-readable
                        time difference, or `locale` for a localized datetime string. Defaults to `locale`.
        :type time_format: Literal["concise", "locale"]
        """  #
        self._parse = Parse(time_format=time_format)

    async def new(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get new users.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of new users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get new posts.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing a user's data.
        :rtype: List[SimpleNamespace]
        """

        new_users = await api.get_users(
            session=session,
            status=status,
            users_type="new",
            limit=limit,
            timeframe=timeframe,
        )

        parsed_users = self._parse.users(new_users)

        return parsed_users if new_users else [SimpleNamespace]

    async def popular(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get popular users.

        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param limit: Maximum number of popular users to return.
        :type limit: int
        :param timeframe: Timeframe from which to get popular posts.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing a user's data.
        :rtype: List[SimpleNamespace]
        """

        popular_users = await api.get_users(
            users_type="popular",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        parsed_users = self._parse.users(popular_users)

        return parsed_users if popular_users else [SimpleNamespace]

    async def all(
        self,
        session: aiohttp.ClientSession,
        limit: int,
        timeframe: TIMEFRAME = "all",
        status: Optional[Status] = None,
    ) -> List[SimpleNamespace]:
        """
        Asynchronously get all users.

        :param limit: Maximum number of all users to return.
        :type limit: int
        :param session: A aiohttp.ClientSession to use for the request.
        :type session: aiohttp.ClientSession
        :param timeframe: Timeframe from which to get all posts.
        :type timeframe: Literal[str]
        :param status: An instance of `Status` used to display animated status messages.
        :type status: Optional[rich.status.Status]
        :return: A list of SimpleNamespace objects, each containing a user's data.
        :rtype: List[SimpleNamespace]
        """

        all_users = await api.get_users(
            users_type="all",
            limit=limit,
            timeframe=timeframe,
            status=status,
            session=session,
        )

        parsed_users = self._parse.users(all_users)

        return parsed_users if all_users else [SimpleNamespace]


# -------------------------------- END ----------------------------------------- #
