![knewkarma-cli](https://github.com/bellingcat/knewkarma/assets/74001397/77e603a3-6830-464c-a7db-da8a724bde2d)

A **Reddit** Data Analysis Toolkit.

[![.Net](https://img.shields.io/badge/Visual%20Basic%20.NET-5C2D91?style=flat&logo=.net&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3A%22Visual+Basic+.NET%22&type=code) [![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3APython&type=code) [![Docker](https://img.shields.io/badge/Dockefile-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3ADockerfile&type=code) [![PyPI - Version](https://img.shields.io/pypi/v/knewkarma?style=flat&logo=pypi&logoColor=ffdd54&label=PyPI&labelColor=3670A0&color=3670A0)](https://pypi.org/project/knewkarma)  [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/_rly0nheart)
***

# Feature Overview

## Knew Karma CLI/GUI

- [x] **<ins>Knew Karma can get the following Reddit data from individual targets</ins>**:
    * **User**: *Profile*, *Posts*, *Comments*
    * **Subreddit**: *Profile*, *Posts*
- [x] **<ins>It can also get posts from various sources, such as</ins>**:
    * **Searching**: Allows getting posts that match the user-provided query from all over Reddit
    * **Reddit Front-Page**: Allows getting posts from the Reddit Front-Page
    * **Listing**: Allows getting posts from a user-specified Reddit Listing
- [x] **<ins>Bonus Features</ins>**
    * **Fully Async (both in the CLI and GUI)**
    * **Dark Mode** (*GUI Automatic/Manual*)
    * **Write data to files** (*JSON/CSV*)

## Knew Karma Python Library

<details>
    <summary style="text-decoration: underline;">Code Examples</summary>

### Get User Data

```python
import asyncio
import aiohttp
from knewkarma import RedditUser


# Define an asynchronous function to fetch User
async def async_user(username: str):
    # Initialize RedditUser with the specified username
    user = RedditUser(username=username)

    # Establish an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Fetch user's profile
        profile = await user.profile(session=session)

        # timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
        # sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.

        # Fetch user's posts
        posts = await user.posts(limit=200, sort="top", timeframe="year",
                                 session=session)

        # Fetch user's comments
        comments = await user.comments(limit=200, sort="top", timeframe="year",
                                       session=session)

        print(profile)
        print(posts)
        print(comments)


asyncio.run(async_user(username="automoderator"))
```

### Get Subreddit Data

````python
import asyncio
import aiohttp
from knewkarma import RedditSub


async def async_subreddit(subreddit_name: str):
    # Initialize RedditSub with the specified subreddit
    subreddit = RedditSub(
        subreddit=subreddit_name)

    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Fetch subreddit's profile
        profile = await subreddit.profile(session=session)

        # Fetch subreddit's posts
        # timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
        # sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.
        posts = await subreddit.posts(limit=100, sort="top", timeframe="month", session=session)

        print(profile)
        print(posts)


asyncio.run(
    async_subreddit(subreddit_name="MachineLearning")
)
````

### Get Posts

```python
import asyncio
import aiohttp
from knewkarma import RedditPosts


async def async_posts():
    # Initialize RedditPosts
    posts = RedditPosts()

    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # timeframes: ["hour", "day", "month", "year"]. Leave parameter unspecified to get from all timeframes.
        # sorting: ["controversial", "new", "top", "best", "hot", "rising"]. Leave parameter unspecified to get from all sort criteria.

        # Fetch front page posts
        front_page_posts = await posts.front_page(limit=50, sort="top", timeframe="hour", session=session)

        # Fetch posts from a specified listing ('best')
        listing_posts = await posts.listing(listings_name="best", limit=50, sort="best", timeframe="month",
                                            session=session)

        # Fetch posts that match the specified search query 'covid-19'
        search_results = await posts.search(query="covid-19", limit=300, session=session)

        print(front_page_posts)
        print(listing_posts)
        print(search_results)


asyncio.run(async_posts())
```

</details>

# Documentation

*[Refer to the Wiki](https://github.com/bellingcat/knewkarma/wiki) for Installation, Usage and Uninstallation
instructions.*
***
[![me](https://github.com/bellingcat/knewkarma/assets/74001397/efd19c7e-9840-4969-b33c-04087e73e4da)](https://rly0nheart.github.io)

