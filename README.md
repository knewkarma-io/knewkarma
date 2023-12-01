```
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻
```

A **Reddit** Data Analysis Toolkit.

[![.Net](https://img.shields.io/badge/Visual%20Basic%20.NET-5C2D91?style=flat&logo=.net&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3A%22Visual+Basic+.NET%22&type=code) [![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3APython&type=code) [![Docker](https://img.shields.io/badge/Dockefile-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3ADockerfile&type=code) [![PyPI - Version](https://img.shields.io/pypi/v/knewkarma?style=flat&logo=pypi&logoColor=ffdd54&label=PyPI&labelColor=3670A0&color=3670A0)](https://pypi.org/project/knewkarma)  [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/_rly0nheart)

## Feature Overview

### Knew Karma CLI/GUI

<details>
    <summary style="text-decoration: underline;">Preview </summary>

```commandline
Usage: knewkarma [-h] [--runtime-prof] [-pct {WALL,CPU}]
                 [-pss {ttot,tsub,tavg,ncall,name,lineno,builtin,threadid,tt_perc,tsub_perc}]
                 [-s {controversial,new,top,best,hot,rising}] [-l LIMIT] [-j]
                 [-c] [-d] [-v]
                 {user,subreddit,posts} ...

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                           Knew Karma CLI                                   ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

▌ A Reddit Data Analysis Toolkit.

Positional Arguments:
  {user,subreddit,posts}
                        Operation mode
    user                User operations
    subreddit           Subreddit operations
    posts               Posts operations

Options:
  -h, --help            show this help message and exit
  --runtime-prof        (dev) enable runtime profiler.
  -pct, --prof-clock-type {WALL,CPU}
                        set profiler clock type (default: CPU)
  -pss, --prof-stats-sort {ttot,tsub,tavg,ncall,name,lineno,builtin,threadid,tt_perc,tsub_perc}
                        profiler stats sort criterion (default: ncall)
  -s, --sort {controversial,new,top,best,hot,rising}
                        Bulk data sort criterion
  -l, --limit LIMIT     Bulk data output limit
  -j, --json            Write data to a JSON file.
  -c, --csv             Write data to a CSV file.
  -d, --debug           Run Knew Karma in debug mode.
  -v, --version         show program's version number and exit

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                              by Richard Mwewa                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

 MIT License

 Copyright © 2023 Richard Mwewa

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to dea
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in a
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN TH
 SOFTWARE.
```

</details>

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

### Knew Karma Python Library

<details>
    <summary style="text-decoration: underline;">Code Examples</summary>

#### Get User Data

```python
import asyncio
import aiohttp
from knewkarma import RedditUser


# Define an asynchronous function to fetch User
async def async_user(username: str, data_limit: int, data_sort: str):
    # Initialize a RedditUser object with the specified username, data limit, and sorting criteria
    user = RedditUser(username=username, data_limit=data_limit, data_sort=data_sort)

    # Establish an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Fetch user's profile
        profile = await user.profile(session=session)

        # Fetch user's posts
        posts = await user.posts(session=session)

        # Fetch user's comments
        comments = await user.comments(session=session)

        print(profile)
        print(posts)
        print(comments)


# Run the asynchronous function with a specified username, data limit, and sorting parameter
asyncio.run(async_user(username="automoderator", data_limit=100, data_sort="all"))
```

#### Get Subreddit Data

````python
import asyncio
import aiohttp
from knewkarma import RedditSub


# Define an asynchronous function to fetch Subreddit data
async def async_subreddit(subreddit_name: str, data_limit: int, data_sort: str):
    # Initialize a RedditSub object with the specified subreddit, data limit, and sorting criteria
    subreddit = RedditSub(
        subreddit=subreddit_name, data_limit=data_limit, data_sort=data_sort
    )

    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Fetch subreddit's profile
        profile = await subreddit.profile(session=session)

        # Fetch subreddit's posts
        posts = await subreddit.posts(session=session)

        print(profile)
        print(posts)


# Run the asynchronous function with specified subreddit name, data limit, and sorting criteria
asyncio.run(
    async_subreddit(subreddit_name="MachineLearning", data_limit=100, data_sort="top")
)
````

#### Get Posts

```python
import asyncio
import aiohttp
from knewkarma import RedditPosts


# Define an asynchronous function to fetch Reddit posts
async def async_posts(limit: int, sort: str):
    # Initialize RedditPosts with the specified limit and sorting criteria
    posts = RedditPosts(limit=limit, sort=sort)

    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Fetch front page posts
        front_page_posts = await posts.front_page(session=session)
        # Fetch posts from a specified listing ('best')
        listing_posts = await posts.listing(listings_name="best", session=session)
        # Fetch posts that match the specified search query 'covid-19'
        search_results = await posts.search(query="covid-19", session=session)

        print(front_page_posts)
        print(listing_posts)
        print(search_results)


# Run the asynchronous function with a specified limit and sorting parameter
asyncio.run(async_posts(limit=100, sort="all"))
```

</details>

## Documentation

*[Refer to the Wiki](https://github.com/bellingcat/knewkarma/wiki) for Installation, Usage and Uninstallation
instructions.*
***
[![me](https://github.com/bellingcat/knewkarma/assets/74001397/efd19c7e-9840-4969-b33c-04087e73e4da)](https://about.me/rly0nheart)

