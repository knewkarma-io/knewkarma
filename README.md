# Knew Karma

[![.Net](https://img.shields.io/badge/Visual%20Basic%20.NET-5C2D91?style=flat&logo=.net&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3A%22Visual+Basic+.NET%22&type=code) [![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3APython&type=code) [![Docker](https://img.shields.io/badge/Docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3ADockerfile&type=code) [![PyPI - Version](https://img.shields.io/pypi/v/knewkarma?style=flat&logo=pypi&logoColor=ffdd54&label=PyPI&labelColor=3670A0&color=3670A0)](https://pypi.org/project/knewkarma) [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/_rly0nheart)

**Knew Karma** is a Reddit Data Analysis Toolkit designed to provide an extensive range of functionalities for exploring
and analysing Reddit data. It includes both Command-Line Interface (CLI) and Graphical User Interface (GUI) options,
making it adaptable for various user preferences.

## Feature Overview

### Knew Karma CLI/GUI

Knew Karma offers a variety of features for accessing and analyzing Reddit data, including:

#### User Data

- **Profile** — Retrieves user profile information.
- **Posts** — Retrieves posts created by a user.
- **Comments** — Collects comments from users.
- **Top n Communities** — Identifies top communities based on user activity.
- **Moderated Communities** — Lists communities moderated by the user.

#### Community (Subreddit) Data

- **Profile** — Retrieves community profile information.
- **Posts** — Retrieves posts from a specified community.
- **Wiki Pages** — Lists wiki pages in a community.
- **Wiki Page Data** — Retrieves content from specific wiki pages.

#### Communities (Subreddits) Data

- **All** — Retrieves all communities.
- **Default** — Retrieves default communities.
- **New** — Retrieves new communities.
- **Popular** — Retrieves popular communities.

#### Posts Data

- **New** — Retrieves new posts.
- **Reddit Front-Page** — Retrieves front-page posts.
- **Search** — Searches for posts based on queries.
- **Listing** — Retrieves posts from specified Reddit listings.

#### Search/Discovery

- **Users** — Searches for users.
- **Communities** — Searches for communities.
- **Posts** — Searches for posts.

## Knew Karma Library

### Integration with Your Projects

Knew Karma also serves as a Python library for integration into other projects. Below are some code examples
illustrating how to use Knew Karma in different scenarios:

<details>
    <summary style="text-decoration: underline;">Code Examples</summary>

### User Data

```python
import asyncio
import aiohttp
from knewkarma import RedditUser

user = RedditUser(username="TheRealKSi")


# Get user's profile
async def async_profile():
    async with aiohttp.ClientSession() as session:
        profile = await user.profile(session=session)
        print(profile)


# Get user's posts
async def async_posts(limit):
    async with aiohttp.ClientSession() as session:
        # timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
        # sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.
        posts = await user.posts(limit=limit, session=session)
        print(posts)


# Get user's comments
async def async_comments(limit):
    async with aiohttp.ClientSession() as session:
        # timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
        # sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.
        comments = await user.comments(limit=limit, session=session)
        print(comments)


# Get user's top n communities based on n post frequency
async def async_top_communities(top_n, limit):
    async with aiohttp.ClientSession() as session:
        top_communities = await user.top_communities(top_n=top_n, limit=limit, session=session)
        print(top_communities)


# Get communities moderated by user       
async def async_moderated_communities():
    async with aiohttp.ClientSession() as session:
        moderated_communities = await user.moderated_communities(session=session)
        print(moderated_communities)


asyncio.run(async_profile())
asyncio.run(async_posts(limit=5))
asyncio.run(async_comments(limit=100))
asyncio.run(async_top_communities(top_n=10, limit=100))
asyncio.run(async_moderated_communities())

```

### Community (Subreddit) Data

````python
import asyncio
import aiohttp
from knewkarma import RedditCommunity

# Initialize RedditSub with the specified community
community = RedditCommunity(community="MachineLearning")


# Get a community's profile
async def async_profile():
    async with aiohttp.ClientSession() as session:
        profile = await community.profile(session=session)
        print(profile)


# Get a community's posts
async def async_posts(limit):
    async with aiohttp.ClientSession() as session:
        # timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
        # sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.
        posts = await community.posts(limit=limit, session=session)
        print(posts)


# Get a community's wiki pages
async def async_wiki_pages():
    async with aiohttp.ClientSession() as session:
        wiki_pages = await community.wiki_pages(session=session)
        print(wiki_pages)


# Get a community's specified wiki page
async def async_wiki_page(page):
    async with aiohttp.ClientSession() as session:
        wiki_page = await community.wiki_page(page=page, session=session)
        print(wiki_page)


asyncio.run(async_profile())
asyncio.run(async_posts(limit=200))
asyncio.run(async_wiki_pages())
asyncio.run(async_wiki_page(page="config/description"))
````

### Communities (Subreddits) Data

````python
import asyncio
import aiohttp
from knewkarma import RedditCommunities

# Initialize RedditSub with the specified community
communities = RedditCommunities()


# Get all communities
async def async_all(limit):
    async with aiohttp.ClientSession() as session:
        all_communities = await communities.all(limit=limit, session=session)
        print(all_communities)


# Get default communities
async def async_default(limit):
    async with aiohttp.ClientSession() as session:
        default_communities = await communities.default(limit=limit, session=session)
        print(default_communities)


# Get new communities
async def async_new(limit):
    async with aiohttp.ClientSession() as session:
        new_communities = await communities.new(limit=limit, session=session)
        print(new_communities)


# Get popular communities
async def async_popular(limit):
    async with aiohttp.ClientSession() as session:
        popular_communities = await communities.default(limit=limit, session=session)
        print(popular_communities)


asyncio.run(async_all(limit=500))
asyncio.run(async_default(limit=200))
asyncio.run(async_new(limit=100))
asyncio.run(async_popular(limit=150))
````

### Posts Data

```python
import asyncio
import aiohttp
from knewkarma import RedditPosts

# Initialize RedditPosts
posts = RedditPosts()


# Get new posts
async def async_new(limit):
    async with aiohttp.ClientSession() as session:
        new_posts = await posts.new(limit=limit, session=session)
        print(new_posts)


# Get posts from the front-page
async def async_front_page(limit, sort, timeframe):
    async with aiohttp.ClientSession() as session:
        front_page_posts = await posts.front_page(limit=limit, sort=sort, timeframe=timeframe, session=session)
        print(front_page_posts)


# Get posts from a specified listing
async def async_listing(listing, limit, timeframe):
    async with aiohttp.ClientSession() as session:
        listing_posts = await posts.listing(listings_name=listing, limit=limit, timeframe=timeframe,
                                            session=session)
        print(listing_posts)


asyncio.run(async_new(limit=100))

# timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
# sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.
asyncio.run(async_front_page(limit=150, sort="top", timeframe="hour"))
asyncio.run(async_listing(listing="best", limit=200, timeframe="month"))
```

### Search/Discovery

```python
import asyncio
import aiohttp
from knewkarma import RedditSearch

search = RedditSearch()


# Search users
async def async_search_users(query, limit):
    async with aiohttp.ClientSession() as session:
        users = await search.users(query=query, limit=limit, session=session)
        print(users)


# Search communities (subreddits)
async def async_search_communities(query, limit):
    async with aiohttp.ClientSession() as session:
        communities = await search.communities(query=query, limit=limit, session=session)
        print(communities)


# Search posts
async def async_search_posts(query, limit):
    async with aiohttp.ClientSession() as session:
        # timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
        # sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.
        posts = await search.posts(query=query, limit=limit, session=session)
        print(posts)


asyncio.run(async_search_users(query="john", limit=150))
asyncio.run(async_search_communities(query="ask", limit=200))
asyncio.run(async_search_posts(query="cooking", limit=250))
```

</details>

# Documentation

*[Refer to the Wiki](https://github.com/bellingcat/knewkarma/wiki) for Installation, Usage and Uninstallation
instructions.*
***
[![me](https://github.com/bellingcat/knewkarma/assets/74001397/efd19c7e-9840-4969-b33c-04087e73e4da)](https://rly0nheart.github.io)

