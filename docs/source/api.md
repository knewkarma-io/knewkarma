# Developer Interface

## Overview

The Knew Karma API offers a seamless way to interact with Reddit data, providing asynchronous access to user profiles,
subreddit information, posts, comments, and more.

This API is designed for developers with a basic understanding of
asynchronous programming.

To help you get started, I've included detailed examples showcasing how to utilise various
API features effectively.

The API exposes 7 primary classes, each tailored for different types of data retrieval:

#### <span style="font-size: 131%;"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Post</strong></span>

Represents a Reddit post and provides method(s) for getting data from the specified post.

### Initialisation

```python
Post(post_id: str, post_subreddit: str, time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from a specified post.

* `post_id`: ID of the post to get data from.
* `subreddit`: Name of the subreddit where the post is located.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

##### <span class="method-name"><span class="italic">Post.</span><strong>data</strong>(session: aiohttp.ClientSession) -> dict</span>

Returns a post's data. This method fetches the detailed data of a specified Reddit post.

##### <span class="method-name"><span class="italic">Post.</span><strong>comments</strong>(session: aiohttp.ClientSession, limit: int, sort: Literal[str] = "all") -> list[dict]</span>

Returns a post's comments. This method retrieves comments from the specified post. You can limit the number of comments
returned and sort them based on a specified criterion.

#### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Posts</strong></span>

Represents Reddit posts and provides methods for getting posts from various sources.

### Initialisation

```python
Posts(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple posts.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

##### <span class="method-name"><span class="italic">Posts.</span><strong>best</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns posts from the best listing. This method retrieves the best posts according to Reddit's algorithm. You can limit
the number of posts returned.

##### <span class="method-name"><span class="italic">Posts.</span><strong>controversial</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns posts from the controversial listing. This method fetches posts that are considered controversial based on
Reddit's algorithm. You can limit the number of posts returned.

##### <span class="method-name"><span class="italic">Posts.</span><strong>front_page</strong>(session: aiohttp.ClientSession, limit: int, sort: Literal[str] = "all") -> list[dict]</span>

Returns posts from the Reddit front-page. This method retrieves posts from Reddit's front page. You can limit the number
of posts returned and sort them based on a specified criterion.

##### <span class="method-name"><span class="italic">Posts.</span><strong>new</strong>(session: aiohttp.ClientSession, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[dict]</span>

Returns new posts. This method fetches new posts. You can limit the number of posts returned, sort them based on a
specified criterion, and filter them by a timeframe.

##### <span class="method-name"><span class="italic">Posts.</span><strong>popular</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns posts from the popular listing. This method retrieves popular posts. You can limit the number of posts returned.

##### <span class="method-name"><span class="italic">Posts.</span><strong>rising</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns posts from the rising listing. This method fetches rising posts. You can limit the number of posts returned.

#### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Search</strong></span>

Represents Reddit search functionality and provides methods for getting search results from
different entities.

### Initialisation

```python
Search(query: str, time_format: Literal["concise", "locale"])
```

Initialises an instance for performing searches across Reddit.

* `query`: Search query.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

##### <span class="method-name"><span class="italic">Search.</span><strong>posts</strong>(timeframe: Literal[str], sort: Literal[str], limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns posts matching the search query. This method retrieves posts that match the search query. You can limit the
number of posts returned, sort them based on a specified criterion, and filter them by a timeframe.

##### <span class="method-name"><span class="italic">Search.</span><strong>subreddits</strong>(timeframe: Literal[str], sort: Literal[str], limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Search subreddits. This method searches for subreddits that match the query. You can limit the number of subreddits
returned, sort them based on a specified criterion, and filter them by a timeframe.

##### <span class="method-name"><span class="italic">Search.</span><strong>users</strong>(timeframe: Literal[str], sort: Literal[str], limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Search users. This method searches for users that match the query. You can limit the number of users returned, sort them
based on a specified criterion, and filter them by a timeframe.

#### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Subreddit</strong></span>

Represents a Reddit subreddit and provides methods for getting data from it.

### Initialisation

```python
Subreddit(subreddit: str, time_format: Literal["concise", "locale"])
```

Initialises a Subreddit instance for getting profile and posts from the specified subreddit.

* `subreddit`: Name of the subreddit to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

##### <span class="method-name"><span class="italic">Subreddit.</span><strong>profile</strong>(session: aiohttp.ClientSession) -> dict</span>

Returns a subreddit's profile data. This method fetches the profile data of a specified subreddit.

##### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_pages</strong>(session: aiohttp.ClientSession) -> list[str]</span>

Returns a subreddit's wiki pages. This method retrieves the wiki pages of a specified subreddit.

##### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_page</strong>(page: str, session: aiohttp.ClientSession) -> dict</span>

Returns a subreddit's specified wiki page data. This method fetches the data of a specified wiki page from a subreddit.

##### <span class="method-name"><span class="italic">Subreddit.</span><strong>posts</strong>(session: aiohttp.ClientSession, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[dict]</span>

Returns a subreddit's posts. This method retrieves posts from a specified subreddit. You can limit the number of posts
returned, sort them based on a specified criterion, and filter them by a timeframe.

##### <span class="method-name"><span class="italic">Subreddit.</span><strong>search</strong>(session: aiohttp.ClientSession, keyword: str, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[dict]</span>

Returns posts that contain a specified keyword from a subreddit. This method searches for posts in a subreddit that
contain the specified keyword. You can limit the number of posts returned, sort them based on a specified criterion, and
filter them by a timeframe.

#### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Subreddits</strong></span>

Represents subreddits and provides methods for getting related data.

### Initialisation

```python
Subreddits(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple subreddits.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

##### <span class="method-name"><span class="italic">Subreddits.</span><strong>all</strong>(limit: int, timeframe: Literal[str] = "all", session: aiohttp.ClientSession) -> list[dict]</span>

Returns all subreddits. This method retrieves all subreddits. You can limit the number of subreddits returned and filter
them by a timeframe.

##### <span class="method-name"><span class="italic">Subreddits.</span><strong>default</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns default subreddits. This method fetches the default subreddits. You can limit the number of subreddits returned.

##### <span class="method-name"><span class="italic">Subreddits.</span><strong>new</strong>(limit: int, session: aiohttp.ClientSession, timeframe: Literal[str] = "all") -> list[dict]</span>

Returns new subreddits. This method retrieves new subreddits. You can limit the number of subreddits returned and filter
them by a timeframe.

##### <span class="method-name"><span class="italic">Subreddits.</span><strong>popular</strong>(limit: int, session: aiohttp.ClientSession, timeframe: Literal[str] = "all") -> list[dict]</span>

Returns popular subreddits. This method fetches popular subreddits. You can limit the number of subreddits returned and
filter them by a timeframe.

#### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>User</strong></span>

Represents a Reddit user and provides methods for getting data from the specified user.

### Initialisation

```python
User(username: str, time_format: Literal["concise", "locale"])
```

Initialises a User instance for getting profile, posts, and comments data from the specified user.

* `username`: Username of the user to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

##### <span class="method-name"><span class="italic">User.</span><strong>profile</strong>(session: aiohttp.ClientSession) -> dict</span>

Returns a user's profile data. This method fetches the profile data of a specified user. It requires
an `aiohttp.ClientSession` to make the asynchronous HTTP request.

##### <span class="method-name"><span class="italic">User.</span><strong>posts</strong>(session: aiohttp.ClientSession, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[dict]</span>

Returns a user's posts. This method retrieves posts from a specified user. You can limit the number of posts returned,
sort them based on a specified criterion, and filter them by a timeframe.

##### <span class="method-name"><span class="italic">User.</span><strong>comments</strong>(session: aiohttp.ClientSession, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[dict]</span>

Returns a user's comments. This method retrieves comments from a specified user. You can limit the number of comments
returned, sort them based on a specified criterion, and filter them by a timeframe.

##### <span class="method-name"><span class="italic">User.</span><strong>overview</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns a user's most recent comments. This method retrieves the most recent comments of a specified user. You can limit
the number of comments returned.

##### <span class="method-name"><span class="italic">User.</span><strong>search_posts</strong>(session: aiohttp.ClientSession, keyword: str, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[dict]</span>

Returns a user's posts that contain the specified keywords. This method searches for posts from a specified user that
contain the specified keywords. You can limit the number of posts returned, sort them based on a specified criterion,
and filter them by a timeframe.

##### <span class="method-name"><span class="italic">User.</span><strong>search_comments</strong>(session: aiohttp.ClientSession, keyword: str, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[dict]</span>

Returns a user's comments that contain the specified keyword. This method searches for comments from a specified user
that contain the specified keyword. You can limit the number of comments returned, sort them based on a specified
criterion, and filter them by a timeframe.

##### <span class="method-name"><span class="italic">User.</span><strong>moderated_subreddits</strong>(session: aiohttp.ClientSession) -> list[dict]</span>

Returns subreddits moderated by the user. This method fetches the subreddits moderated by a specified user.

##### <span class="method-name"><span class="italic">User.</span><strong>top_subreddits</strong>(session: aiohttp.ClientSession, top_n: int, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[tuple]</span>

Returns a user's top n subreddits based on subreddit frequency in n posts. This method retrieves the top n subreddits
that a specified user is most active in. You can limit the number of posts considered, sort them based on a specified
criterion, and filter them by a timeframe.

#### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Users</strong></span>

Represents Reddit users and provides methods for getting related data.

### Initialisation

```python
Users(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple users.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

##### <span class="method-name"><span class="italic">Users.</span><strong>all</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns all users. This method retrieves all users. You can limit the number of users returned.

##### <span class="method-name"><span class="italic">Users.</span><strong>new</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns new users. This method retrieves new users. You can limit the number of users returned.

##### <span class="method-name"><span class="italic">Users.</span><strong>popular</strong>(limit: int, session: aiohttp.ClientSession) -> list[dict]</span>

Returns popular users. This method retrieves popular users. You can limit the number of users returned.

## Timeframes and Sorting

When fetching posts or comments, you can specify timeframes ("`hour`", "`day`", "`month`", "`year`") and sorting
criteria ("`controversial`", "`new`", "`top`", "`best`", "`hot`", "`rising`"). Leaving these parameters unspecified
defaults to retrieving data across all timeframes and sort criteria.

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
Use "`concise`" for relative times (e.g., "*5 minutes ago*") or "`locale`" for locale-based formatting. Here's how to
apply it:
R

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
which is specifically designed for retrieving large volumes of historical data, including posts, comments, and other
Reddit activity.
