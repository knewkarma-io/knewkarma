# API & Integration

## Overview

The Knew Karma API offers a seamless way to interact with Reddit data, providing asynchronous access to user profiles,
subreddit information, posts, comments, and more.

This API is designed for developers with a basic understanding of
asynchronous programming.

To help you get started, I've included detailed examples showcasing how to utilise various
API features effectively.

The API exposes 7 primary classes, each tailored for different types of data retrieval:

## Post

**Post**: Represents a Reddit post and provides method(s) for getting data from the specified post.

Initialisation:

```python
Post(post_id: str, post_subreddit: str, time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from a specified post.

* `post_id`: ID of the post to get data from.
* `subreddit`: Name of the subreddit where the post is located.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

* `data(session: aiohttp.ClientSession) -> dict`: Returns a post's data.
* `comments(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all") -> list[dict)`: Returns a post's
  comments.

## Posts

**Posts**: Represents Reddit posts and provides methods for getting posts from various sources.

Initialisation:

```python
Posts(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple posts.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

* `best(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns posts from the best
  listing.
* `controversial(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns posts from
  the controversial
  listing.
* `front_page(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all") ->
  list[dict]`: Returns posts from the Reddit front-page.
* `new(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = str) ->
  list[dict]`: Returns new posts.
* `popular(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns posts from the
  popular
  listing.
* `rising(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns posts from the
  rising
  listing.

## Search

**Search**: Represents Reddit search functionality and provides methods for getting search results from different
entities.

Initialisation:

```python
Search(query: str, time_format: Literal["concise", "locale"])
```

Initialises an instance for performing searches across Reddit.

* `query`: Search query.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods:

* `posts(timeframe: Literal[str], sort: Literal[str],limit: int, session: aiohttp.ClientSession) -> list[dict]`:
  Returns posts matching the search query.
* `subreddits(timeframe: Literal[str], sort: Literal[str],limit: int, session: aiohttp.ClientSession) -> list[dict]`:
  Search subreddits.
* `users(timeframe: Literal[str], sort: Literal[str], limit: int, session: aiohttp.ClientSession) -> list[dict]`:
  Search users.

## Subreddit

**Subreddit**: Represents a Reddit subreddit and provides methods for getting data from it.

Initialisation:

```python
Subreddit(subreddit: str, time_format: Literal["concise", "locale"])
```

Initialises a RedditCommunity instance for getting profile and posts from the specified subreddit.

* `subreddit`: Name of the subreddit to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

* `profile(session: aiohttp.ClientSession) -> dict`: Returns a subreddit's profile data.
* `wiki_pages(session: aiohttp.ClientSession) -> list[str]`: Returns a subreddit's wiki pages.
* `wiki_page(page: str, session: aiohttp.ClientSession) -> dict`: Returns a subreddit's specified wiki page data.
* `posts(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "all") ->
  list[dict]`: Returns a subreddit's posts.
* `search(session: aiohttp.ClientSession, keyword: str, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[dict]`: Returns posts that contain a specified keyword from a subreddit.

## Subreddits

**Subreddits**: Represents subreddits and provides methods for getting related data.

Initialisation:

```python
Subreddits(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple subreddits.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods:

* `all(limit: int, timeframe: TIMEFRAME = "all", session: aiohttp.ClientSession) -> list[dict]`: Returns all
  subreddits.
* `default(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns default subreddits.
* `new(limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all") -> list[dict]`: Returns new
  subreddits.
* `popular(limit: int, session: aiohttp.ClientSession, timeframe: TIMEFRAME = "all") -> list[dict]`: Returns popular
  subreddits.

## User

**User**: Represents a Reddit user and provides methods for getting data from the specified user.

Initialisation:

```python
User(username: str, time_format: Literal["concise", "locale"])
```

Initialises a **User** instance for getting profile, posts, and comments data from the specified user.

* `username`: Username of the user to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale"
  for a
  localized datetime string. Defaults to "locale".

### Methods

* `profile(session: aiohttp.ClientSession) -> dict`: Returns a user's profile data.
* `posts(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "all") ->
  list[dict]`: Returns a user's posts.
* `comments(session: aiohttp.ClientSession, limit: int, sort: SORT_CRITERION = "all", timeframe: TIMEFRAME = "all") ->
  list[dict]`: Returns a user's comments.
* `overview(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns a user's most recent comments.
* `search_posts(session: aiohttp.ClientSession, keyword: str, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[dict]`: Returns a user's posts that contain the specified keywords.
* `search_comments(session: aiohttp.ClientSession, keyword: str, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[dict]`: Returns a user's comments that contain the specified keyword.
* `moderated_subreddits(session: aiohttp.ClientSession) -> list[dict]`: Returns subreddits moderated by the user.
* `top_subreddits(session: aiohttp.ClientSession, top_n: int, limit: int, sort: SORT_CRITERION = "all", timeframe:
  TIMEFRAME = "all") -> list[tuple]`: Returns a user's top n subreddits based on subreddit frequency in n posts.

## Users

**Users**: Represents Reddit users and provides methods for getting related data.

Initialisation:

```python
Users(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple users.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods:

* `all(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns all users.
* `new(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns new users.
* `popular(limit: int, session: aiohttp.ClientSession) -> list[dict]`: Returns popular users.

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

The `time_format` parameter (or `--time-format` in the CLI) affects how timestamps are displayed in your results.
Use "`concise`" for relative times (
e.g., "*5 minutes ago*") or "`locale`" for locale-based formatting. Here's how to apply it:

```python
posts = await user.posts(limit=5, time_format="concise", session=session)
```

## Random Cool-Down for Bulk Results

To avoid hitting rate limits, Knew Karma includes a random cool-down or sleep timer ranging from 1 to 10 seconds for
bulk results that exceed 100. This feature ensures smooth and uninterrupted data retrieval while adhering to Reddit's
API usage.

## Important Note on Data Fetching

Knew Karma is designed to fetch recent data from Reddit. It directly interacts with the Reddit API to access up-to-date
information, including the latest posts, comments, and user activity.

If you need to access historical Reddit data, I recommend using the [Pushshift API](https://api.pushshift.io/docs),
which is
specifically designed for retrieving large volumes of historical data, including posts, comments, and
other Reddit activity.


