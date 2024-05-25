# Knew Karma API Documentation
## Overview
The Knew Karma API offers a powerful way to interact with Reddit data, providing asynchronous access to user profiles, subreddit information, posts, comments, and more. This API is designed for developers with a basic understanding of asynchronous programming. To help you get started, we've included detailed examples showcasing how to utilize various API features effectively.


## Key Classes
The API exposes six primary classes, each tailored for different types of data retrieval:
* `User`: Fetch data related to Reddit users, such as profiles, posts, and comments.
* `Subreddit` & `Subreddits`: Access information about specific subreddits, or a collection of subreddits.
* `Posts` & `Post`: Retrieve data on individual posts or collections of posts.
* `Search`: Perform searches across users, subreddits, and posts.


## Timeframes and Sorting
When fetching posts or comments, you can specify timeframes (`"hour"`, `"day"`, `"month"`, `"year"`) and sorting criteria (`"controversial"`, `"new"`, `"top"`, `"best"`, `"hot"`, `"rising"`). Leaving these parameters unspecified defaults to retrieving data across all timeframes and sort criteria.


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

This example demonstrates how to initiate a User instance, fetch the user's profile, posts, and comments. Modify the limit parameter to control the amount of data retrieved.

## Utilizing `time_format` Parameter
The time_format parameter affects how timestamps are displayed in your results. Use `"concise"` for relative times (e.g., `"5 minutes ago"`) or `"locale"` for locale-based formatting. Here's how to apply it:
```python
posts = await user.posts(limit=5, session=session, time_format="concise")
```