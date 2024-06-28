# API & Integration

## Overview

The Knew Karma API offers a seamless way to interact with Reddit data, providing asynchronous access to user profiles,
subreddit information, posts, comments, and more.

This API is designed for developers with a basic understanding of
asynchronous programming.

To help you get started, I've included detailed examples showcasing how to utilise various
API features effectively.
Key Classes

The API exposes six primary classes, each tailored for different types of data retrieval:

## User

**User**: Represents a Reddit user and provides methods for getting data from the specified user.

Initialisation:

```python
User(username: str, time_format: TIME_FORMAT = "locale")
```

Initialises a **User** instance for getting profile, posts, and comments data from the specified user.

* `username`: Username of the user to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale"
  for a
  localized datetime string. Defaults to "locale".

### Methods

* **profile(session: aiohttp.ClientSession) -> dict**: Returns a user's profile data.
* **posts(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "all") ->
  list[dict]**: Returns a user's posts.
* **comments(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "all") ->
  list[dict]**: Returns a user's comments.
* **overview(limit: int, session: aiohttp.ClientSession) -> list[dict]**: Returns a user's most recent comments.
* **search_posts(session: aiohttp.ClientSession, keyword: str, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[dict]**: Returns a user's posts that contain the specified keywords.
* **search_comments(session: aiohttp.ClientSession, keyword: str, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[dict]**: Returns a user's comments that contain the specified keyword.
* **moderated_subreddits(session: aiohttp.ClientSession) -> list[dict]**: Returns subreddits moderated by the user.
* **top_subreddits(session: aiohttp.ClientSession, top_n: int, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[tuple]**: Returns a user's top n subreddits based on subreddit frequency in n posts.

## Subreddit

**Subreddit**: Represents a Reddit Community (Subreddit) and provides methods for getting data from the specified
subreddit.

Initialisation:

```
Subreddit(subreddit: str, time_format: TIME_FORMAT = "locale")
```

Initialises a RedditCommunity instance for getting profile and posts from the specified subreddit.

* `subreddit`: Name of the subreddit to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

* **profile(session: aiohttp.ClientSession) -> dict**: Returns a subreddit's profile data.
* **wiki_pages(session: aiohttp.ClientSession) -> list[str]**: Returns a subreddit's wiki pages.
* **wiki_page(page: str, session: aiohttp.ClientSession) -> dict**: Returns a subreddit's specified wiki page data.
* **posts(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "all") ->
  list[dict]**: Returns a subreddit's posts.
* **search(session: aiohttp.ClientSession, keyword: str, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[dict]**: Returns posts that contain a specified keyword from a subreddit.

## Subreddits

**Subreddits**: Represents Reddit subreddits and provides methods for getting related data.

Initialisation:

```python
Subreddits(time_format: TIME_FORMAT = "locale")
```

Initialises an instance for getting data from multiple subreddits.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods:

* **all(limit: int, session: aiohttp.ClientSession) -> list[dict]**: Returns all subreddits.
* **default(limit: int, session: aiohttp.ClientSession) -> list[dict]**: Returns default subreddits.
* **new(limit: int, session: aiohttp.ClientSession) -> list[dict]**: Returns new subreddits.
* **popular(limit: int, session: aiohttp.ClientSession) -> list[dict]**: Returns popular subreddits.

## Post

**Post**: Represents a Reddit post and provides method(s) for getting data from the specified post.

Initialisation:

```python
Post(post_id: str, subreddit: str, time_format: TIME_FORMAT = "locale")
```

Initialises an instance for getting data from a specified post.

* `post_id`: ID of the post to get data from.
* `subreddit`: Name of the subreddit where the post is located.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

* **profile(session: aiohttp.ClientSession) -> dict**: Returns a post's data.
* **comments(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all") -> list[dict]**: Returns a post's
  comments.

## Posts

**Posts**: Represents Reddit posts and provides methods for getting posts from various sources.

Initialisation:

```python
Posts(time_format: TIME_FORMAT = "locale")
```

Initialises an instance for getting data from multiple posts.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

* listing(session: aiohttp.ClientSession, listings_name: LISTING, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[dict]**: Returns posts from a specified listing.
* new(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all") -> list[dict]: Returns new posts.
* front_page(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "all") ->
  list[dict]: Returns posts from the Reddit front-page.

## Search

**Search**: Represents Reddit search functionality and provides methods for getting search results from different
entities.

Initialisation:

```python
Search(time_format: TIME_FORMAT = "locale")
```

Initialises an instance for performing searches across Reddit.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods:

* **users(query: str, limit: int, session: aiohttp.ClientSession) -> list[dict]**: Search users.
* **subreddits(query: str, limit: int, session: aiohttp.ClientSession) -> list[dict]**: Search subreddits.
* **posts(query: str, limit: int, session: aiohttp.ClientSession, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "
  all") -> list[dict]**: Returns posts matching the search query.

## Timeframes and Sorting

When fetching posts or comments, you can specify timeframes ("`hour`", "`day`", "`month`", "`year`") and sorting
criteria ("`
controversial`", "`new`", "`top`", "`best`", "`hot`", "`rising`"). Leaving these parameters unspecified defaults to
retrieving data
across all timeframes and sort criteria.

## Code Example: Fetching User Data

```python
import asyncio
import aiohttp
from knewkarma import User


async def fetch_user_data(username):
    user = User(username=username)


async with aiohttp.ClientSession() as session:
    profile = await user.profile(session=session)
posts = await user.posts(limit=5, session=session)
comments = await user.comments(limit=100, session=session)
print(profile, posts, comments)

asyncio.run(fetch_user_data("TheRealKSi"))
```

This example demonstrates how to initiate a **User** instance, fetch the user's profile, posts, and comments. Modify the
limit parameter to control the amount of data retrieved.

## Utilising `time_format` Parameter

The `time_format` parameter affects how timestamps are displayed in your results. Use "`concise`" for relative times (
e.g., "*5 minutes ago*") or "`locale`" for locale-based formatting. Here's how to apply it:

```python
posts = await user.posts(limit=5, session=session, time_format="concise")
```
