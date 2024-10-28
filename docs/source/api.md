# Developer Interface

## Overview

The Knew Karma API offers a seamless way to interact with Reddit data, providing asynchronous access to user profiles,
subreddit information, posts, comments, and more.

> This API is designed for developers with a basic understanding of asynchronous programming.

To help you get started, I've included detailed examples showcasing how to utilise various
API features effectively.

The API exposes 7 primary classes, each tailored for different types of data retrieval:

### <span style="font-size: 140%;"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Post</strong></span>

Represents a Reddit post and provides method(s) for getting data from the specified post.

### Initialisation

```text
post = Post(id: str, subreddit: str, )
```

Initialises an instance for getting data from a specified post.

* `post_id`: ID of the post to get data from.
* `subreddit`: Name of the subreddit where the post is located.

### Methods

#### <span class="method-name"><span class="italic">Post.</span><strong>data</strong></span>

Gets a post's data.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Post


async def get_post_data(post_id, post_subreddit):
    post = Post(id=post_id, subreddit=post_subreddit)
    async with aiohttp.ClientSession() as session:
        post = await post.data(session=session)
        print(post.data)


asyncio.run(get_post_data(post_id="13ptwzd", post_subreddit="AskReddit"))
```

***

#### <span class="method-name"><span class="italic">Post.</span><strong>comments</strong></span>

Gets a post's comments.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Post


async def get_post_comments(post_id, post_subreddit, comments_limit):
    post = Post(id=post_id, subreddit=post_subreddit)
    async with aiohttp.ClientSession() as session:
        comments = await post.comments(limit=comments_limit, session=session)

        for comment in comments:
            print(comment.data.body)


asyncio.run(get_post_comments(post_id="13ptwzd", post_subreddit="AskReddit", comments_limit=50))
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Posts</strong></span>

Represents Reddit posts and provides methods for getting posts from various sources.

### Initialisation

```text
posts = Posts()
```

Initialises an instance for getting data from multiple posts.

### Methods

#### <span class="method-name"><span class="italic">Posts.</span><strong>best</strong></span>

Gets posts from the best listing.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Posts


async def get_best_posts(posts_limit):
    posts = Posts()
    async with aiohttp.ClientSession() as session:
        best_posts = await posts.best(limit=posts_limit, session=session)

        for post in best_posts:
            print(post.data.title)


asyncio.run(get_best_posts(posts_limit=120))
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>controversial</strong></span>

Gets posts from the controversial listing.

##### Code Example::

```python
import asyncio
import aiohttp
from knewkarma import Posts


async def get_controversial_posts(posts_limit):
    posts = Posts()
    async with aiohttp.ClientSession() as session:
        controversial_posts = await posts.controversial(limit=posts_limit, session=session)

        for post in controversial_posts:
            print(post.data.title)


asyncio.run(get_controversial_posts(posts_limit=50))
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>front_page</strong></span>

Gets posts from the Reddit front-page.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Posts


async def get_frontpage_posts(posts_limit):
    posts = Posts()
    async with aiohttp.ClientSession() as session:
        frontpage_posts = await posts.front_page(limit=posts_limit, session=session)

        for post in frontpage_posts:
            print(post.data.title)


asyncio.run(get_frontpage_posts(posts_limit=10))
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>new</strong></span>

Gets new posts.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Posts


async def get_new_posts(posts_limit):
    posts = Posts()
    async with aiohttp.ClientSession() as session:
        new_posts = await posts.new(limit=posts_limit, session=session)

        for post in new_posts:
            print(post.data.title)


asyncio.run(get_new_posts(posts_limit=10))
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>popular</strong></span>

Gets posts from the popular listing.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Posts


async def get_popular_posts(posts_limit):
    posts = Posts()
    async with aiohttp.ClientSession() as session:
        popular_posts = await posts.popular(limit=posts_limit, session=session)

        for post in popular_posts:
            print(post.data.title)


asyncio.run(get_popular_posts(posts_limit=50))
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>rising</strong></span>

Gets posts from the rising listing.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Posts


async def get_rising_posts(posts_limit):
    posts = Posts()
    async with aiohttp.ClientSession() as session:
        rising_posts = await posts.rising(limit=posts_limit, session=session)

        for post in rising_posts:
            print(post.data.title)


asyncio.run(get_rising_posts(posts_limit=100))
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Search</strong></span>

Represents Reddit search functionality and provides methods for getting search results from
different entities.

### Initialisation

```text
search = Search(query: str, )
```

Initialises an instance for performing searches across Reddit.

* `query`: Search query.

### Methods

#### <span class="method-name"><span class="italic">Search.</span><strong>posts</strong></span>

Search posts.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Search


async def search_posts(query, results_limit):
    search = Search(query=query)
    async with aiohttp.ClientSession() as session:
        posts = await search.posts(limit=results_limit, session=session)

        for post in posts:
            print(post.data.title)


asyncio.run(search_posts(query="something in data science", results_limit=200))
```

***

#### <span class="method-name"><span class="italic">Search.</span><strong>subreddits</strong></span>

Search subreddits.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Search


async def search_subreddits(query, results_limit):
    search = Search(query=query)
    async with aiohttp.ClientSession() as session:
        subreddits = await search.subreddits(limit=results_limit, session=session)

        for subreddit in subreddits:
            print(subreddit.data.name)


asyncio.run(search_subreddits(query="questions", results_limit=200))
```

***

#### <span class="method-name"><span class="italic">Search.</span><strong>users</strong></span>

Search users.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Search


async def search_users(query, results_limit):
    search = Search(query=query)
    async with aiohttp.ClientSession() as session:
        users = await search.users(limit=results_limit, session=session)

        for user in users:
            print(user.data.name)


asyncio.run(search_users(query="john", results_limit=200))
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Subreddit</strong></span>

Represents a Reddit subreddit and provides methods for getting data from it.

### Initialisation

```text
subreddit = Subreddit(name: str, )
```

Initialises a Subreddit instance for getting profile and posts from the specified subreddit.

* `name`: Name of the subreddit to get data from.

### Methods

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>profile</strong></span>

Gets a subreddit's profile data.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddit


async def get_subreddit_profile(subreddit):
    subreddit = Subreddit(name=subreddit)
    async with aiohttp.ClientSession() as session:
        profile = await subreddit.profile(session=session)
        print(profile.data.description)


asyncio.run(get_subreddit_profile(subreddit="AskScience"))
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_pages</strong></span>

Gets a subreddit's wiki pages.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddit


async def get_subreddit_wiki_pages(subreddit):
    subreddit = Subreddit(name=subreddit)
    async with aiohttp.ClientSession() as session:
        wiki_pages = await subreddit.wikipages(session=session)
        print(wiki_pages)


asyncio.run(get_subreddit_wiki_pages(subreddit="MachineLearning"))
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_page</strong></span>

Gets a subreddit's specified wiki page data.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddit


async def get_subreddit_wiki_page(page, subreddit):
    subreddit = Subreddit(name=subreddit)
    async with aiohttp.ClientSession() as session:
        wiki_page_data = await subreddit.wikipage(page_name=page, session=session)
        print(wiki_page_data.data.content_markdown)


asyncio.run(get_subreddit_wiki_page(page="rules", subreddit="MachineLearning"))
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>posts</strong></span>

Gets a subreddit's posts.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddit


async def get_subreddit_posts(subreddit, posts_limit):
    subreddit = Subreddit(name=subreddit)
    async with aiohttp.ClientSession() as session:
        posts = await subreddit.posts(limit=posts_limit, session=session)

        for post in posts:
            print(post.data.title)


asyncio.run(get_subreddit_posts(posts_limit=500, subreddit="MachineLearning"))
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>comments</strong></span>

Gets a subreddit's comments.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddit


async def get_subreddit_comments(subreddit, posts_limit, comments_per_post):
    subreddit = Subreddit(name=subreddit)
    async with aiohttp.ClientSession() as session:
        comments = await subreddit.comments(
            posts_limit=posts_limit,
            comments_per_post=comments_per_post,
            session=session
        )

        for comment in comments:
            print(comment.data.body)


asyncio.run(get_subreddit_comments(subreddit="AskScience", posts_limit=100, comments_per_post=20))
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>search_posts</strong></span>

Gets posts that contain a specified keyword from a subreddit.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddit


async def search_subreddit_posts(search_query, subreddit, posts_limit):
    subreddit = Subreddit(name=subreddit)
    async with aiohttp.ClientSession() as session:
        posts = await subreddit.search(query=search_query, limit=posts_limit, session=session)

        for post in posts:
            print(post.data.title)


asyncio.run(search_subreddit_posts(search_query="multiverse theory", posts_limit=100, subreddit="AskScience"))
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Subreddits</strong></span>

Represents subreddits and provides methods for getting related data.

### Initialisation

```text
subreddits = Subreddits()
```

Initialises an instance for getting data from multiple subreddits.

### Methods

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>all</strong></span>

Gets all subreddits.

##### implementation

```python
import asyncio
import aiohttp
from knewkarma import Subreddits


async def get_all_subreddits(subreddits_limit):
    subreddits = Subreddits()
    async with aiohttp.ClientSession() as session:
        all_subreddits = await subreddits.all(limit=subreddits_limit, session=session)

        for subreddit in all_subreddits:
            print(subreddit.data.description)


asyncio.run(get_all_subreddits(subreddits_limit=500))
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>default</strong></span>

Gets default subreddits.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddits


async def get_default_subreddits(subreddits_limit):
    subreddits = Subreddits()
    async with aiohttp.ClientSession() as session:
        default_subreddits = await subreddits.default(limit=subreddits_limit, session=session)

        for subreddit in default_subreddits:
            print(subreddit.data.description)


asyncio.run(get_default_subreddits(subreddits_limit=20))
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>new</strong></span>

Gets new subreddits.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddits


async def get_new_subreddits(subreddits_limit):
    subreddits = Subreddits()
    async with aiohttp.ClientSession() as session:
        new_subreddits = await subreddits.new(limit=subreddits_limit, session=session)

        for subreddit in new_subreddits:
            print(subreddit.data.description)


asyncio.run(get_new_subreddits(subreddits_limit=50))
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>popular</strong></span>

Gets popular subreddits.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Subreddits


async def get_popular_subreddits(subreddits_limit):
    subreddits = Subreddits()
    async with aiohttp.ClientSession() as session:
        popular_subreddits = await subreddits.popular(limit=subreddits_limit, session=session)

        for subreddit in popular_subreddits:
            print(subreddit.data.description)


asyncio.run(get_popular_subreddits(subreddits_limit=100))
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>User</strong></span>

Represents a Reddit user and provides methods for getting data from the specified user.

### Initialisation

```text
user = User(username: str, )
```

Initialises a User instance for getting profile, posts, and comments data from the specified user.

* `username`: Username of the user to get data from.

### Methods

#### <span class="method-name"><span class="italic">User.</span><strong>profile</strong></span>

Gets a user's profile data.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import User


async def get_user_profile(username):
    user = User(name=username)
    async with aiohttp.ClientSession() as session:
        profile = await user.profile(session=session)
        print(profile.data.created)


asyncio.run(get_user_profile(username="AutoModerator"))
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>posts</strong></span>

Gets a user's posts.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import User


async def get_user_posts(username, posts_limit):
    user = User(name=username)
    async with aiohttp.ClientSession() as session:
        posts = await user.posts(limit=posts_limit, session=session)

        for post in posts:
            print(post.data.title)


asyncio.run(get_user_posts(username="AutoModerator", posts_limit=100))
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>comments</strong></span>

Gets a user's comments.

##### COde Example:

```python
import asyncio
import aiohttp
from knewkarma import User


async def get_user_comments(username, comments_limit):
    user = User(name=username)
    async with aiohttp.ClientSession() as session:
        comments = await user.comments(limit=comments_limit, session=session)

        for comment in comments:
            print(comment.data.id)


asyncio.run(get_user_comments(username="AutoModerator", comments_limit=100))
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>overview</strong></span>

Gets a user's most recent comments.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import User


async def get_user_overview(username, comments_limit):
    user = User(name=username)
    async with aiohttp.ClientSession() as session:
        comments = await user.overview(limit=comments_limit, session=session)

        for comment in comments:
            print(comment.data.body)


asyncio.run(get_user_overview(username="AutoModerator", comments_limit=100))
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>moderated_subreddits</strong></span>

Gets subreddits moderated by the user.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import User


async def get_user_moderated_subreddits(username):
    user = User(name=username)
    async with aiohttp.ClientSession() as session:
        moderated_subreddits = await user.moderated_subreddits(session=session)

        for subreddit in moderated_subreddits:
            print(subreddit.data.name)


asyncio.run(get_user_moderated_subreddits(username="TheRealKSI"))
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>top_subreddits</strong></span>

Gets a user's top n subreddits based on subreddit frequency in *n* posts.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import User


async def get_user_top_subreddits(username, top_number, subreddits_limit):
    user = User(name=username)
    async with aiohttp.ClientSession() as session:
        top_subreddits = await user.top_subreddits(
            top_n=top_number,
            limit=subreddits_limit,
            session=session
        )

        print(top_subreddits)


asyncio.run(
    get_user_top_subreddits(
        username="TheRealKSI",
        top_number=10,
        subreddits_limit=100
    )
)
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Users</strong></span>

Represents Reddit users and provides methods for getting related data.

### Initialisation

```text
users = Users()
```

Initialises an instance for getting users from multiple sources.

### Methods

#### <span class="method-name"><span class="italic">Users.</span><strong>all</strong></span>

Gets all users.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Users


async def get_all_users(users_limit):
    users = Users()
    async with aiohttp.ClientSession() as session:
        all_users = await users.all(limit=users_limit, session=session)

        for user in all_users:
            print(user.data.name)


asyncio.run(get_all_users(users_limit=1000))
```

***

#### <span class="method-name"><span class="italic">Users.</span><strong>new</strong></span>

Gets new users.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Users


async def get_new_users(users_limit):
    users = Users()
    async with aiohttp.ClientSession() as session:
        new_users = await users.new(limit=users_limit, session=session)

        for user in new_users:
            print(user.data.created)


asyncio.run(get_new_users(users_limit=500))
```

***

#### <span class="method-name"><span class="italic">Users.</span><strong>popular</strong></span>

Gets popular users.

##### Code Example:

```python
import asyncio
import aiohttp
from knewkarma import Users


async def get_popular_users(users_limit):
    users = Users()
    async with aiohttp.ClientSession() as session:
        popular_users = await users.popular(limit=users_limit, session=session)

        for user in popular_users:
            print(user.data.id)


asyncio.run(get_popular_users(users_limit=100))
```

***

## Timeframes and Sorting

When fetching posts or comments, you can specify timeframes ("`hour`", "`day`", "`month`", "`year`") and sorting
criteria ("`controversial`", "`new`", "`top`", "`best`", "`hot`", "`rising`"). Leaving these parameters unspecified
defaults to retrieving data across all timeframes and sort criteria.

## Random Cool-Down for Bulk Results

To avoid hitting rate limits, Knew Karma includes a random cool-down or sleep timer ranging from 1 to 10 seconds for
bulk results that exceed 100. This feature ensures smooth and uninterrupted data retrieval while adhering to Reddit's
API usage.

That's pretty much it. You've completed the Knew Karma API crash course!
