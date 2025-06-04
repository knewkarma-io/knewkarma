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
import requests
from knewkarma.core.post import Post

post = Post(id="13ptwzd", subreddit="AskReddit")
with requests.Session() as session:
    post = post.data(session=session)
    print(post.data)

```

***

#### <span class="method-name"><span class="italic">Post.</span><strong>comments</strong></span>

Gets a post's comments.

##### Code Example:

```python
import requests
from knewkarma.core.post import Post

post = Post(id="13ptwzd", subreddit="AskReddit")
with requests.Session() as session:
    comments = post.comments(limit=50, session=session)
    for comment in comments:
        print(comment.body)
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
import requests
from knewkarma.core.posts import Posts

posts = Posts()
with requests.Session() as session:
    best_posts = posts.best(limit=150, session=session)

    for post in best_posts:
        print(post.title)

```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>controversial</strong></span>

Gets posts from the controversial listing.

##### Code Example::

```python
import requests
from knewkarma.core.posts import Posts

posts = Posts()
with requests.Session() as session:
    controversial_posts = posts.controversial(limit=20, session=session)

    for post in controversial_posts:
        print(post.title)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>front_page</strong></span>

Gets posts from the Reddit front-page.

##### Code Example:

```python
import requests
from knewkarma.core.posts import Posts

posts = Posts()
with requests.Session() as session:
    frontpage_posts = posts.front_page(limit=10, session=session)

    for post in frontpage_posts:
        print(post.title)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>new</strong></span>

Gets new posts.

##### Code Example:

```python
import requests
from knewkarma.core.posts import Posts

posts = Posts()
with requests.Session() as session:
    new_posts = posts.new(limit=10, session=session)

    for post in new_posts:
        print(post.title)

```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>popular</strong></span>

Gets posts from the popular listing.

##### Code Example:

```python
import requests
from knewkarma.core.posts import Posts

posts = Posts()
with requests.Session() as session:
    popular_posts = posts.popular(limit=50, session=session)

    for post in popular_posts:
        print(post.title)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>rising</strong></span>

Gets posts from the rising listing.

##### Code Example:

```python
import requests
from knewkarma.core.posts import Posts

posts = Posts()
with requests.Session() as session:
    rising_posts = posts.rising(limit=100, session=session)

    for post in rising_posts:
        print(post.title)

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
import requests
from knewkarma.core.search import Search

search = Search(query="Something about data science")
with requests.Session() as session:
    posts = search.posts(limit=200, session=session)

    for post in posts:
        print(post.title)

```

***

#### <span class="method-name"><span class="italic">Search.</span><strong>subreddits</strong></span>

Search subreddits.

##### Code Example:

```python
import requests
from knewkarma.core.search import Search

search = Search(query="ask")
with requests.Session() as session:
    subreddits = search.subreddits(limit=200, session=session)

    for subreddit in subreddits:
        print(subreddit.name)
```

***

#### <span class="method-name"><span class="italic">Search.</span><strong>users</strong></span>

Search users.

##### Code Example:

```python
import requests
from knewkarma.core.search import Search

search = Search(query="john")
with requests.Session() as session:
    users = search.users(limit=200, session=session)

    for user in users:
        print(user.name)
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
import requests
from knewkarma.core.subreddit import Subreddit

subreddit = Subreddit(name="AskScience")
with requests.Session() as session:
    profile = subreddit.profile(session=session)
    print(profile.description)
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_pages</strong></span>

Gets a subreddit's wiki pages.

##### Code Example:

```python
import requests
from knewkarma.core.subreddit import Subreddit

subreddit = Subreddit(name="MachineLearning")
with requests.Session() as session:
    wiki_pages = subreddit.wikipages(session=session)
    print(wiki_pages)
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_page</strong></span>

Gets a subreddit's specified wiki page data.

##### Code Example:

```python
import requests
from knewkarma.core.subreddit import Subreddit

subreddit = Subreddit(name="MachineLearning")
with requests.Session() as session:
    wiki_page = subreddit.wikipage(page_name="rules", session=session)
    print(wiki_page.content_markdown)
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>posts</strong></span>

Gets a subreddit's posts.

##### Code Example:

```python
import requests
from knewkarma.core.subreddit import Subreddit

subreddit = Subreddit(name="MachineLearning")
with requests.Session() as session:
    posts = subreddit.posts(limit=500, session=session)

    for post in posts:
        print(post.title)
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>search_posts</strong></span>

Gets posts that contain a specified keyword from a subreddit.

##### Code Example:

```python
import requests
from knewkarma.core.subreddit import Subreddit

subreddit = Subreddit(name="AskScience")
with requests.Session() as session:
    posts = subreddit.search(query="multiverse", limit=100, session=session)

    for post in posts:
        print(post.title)
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
import requests
from knewkarma.core.subreddits import Subreddits

subreddits = Subreddits()
with requests.Session() as session:
    all_subreddits = subreddits.all(limit=500, session=session)

    for subreddit in all_subreddits:
        print(subreddit.description)
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>default</strong></span>

Gets default subreddits.

##### Code Example:

```python
import requests
from knewkarma.core.subreddits import Subreddits

subreddits = Subreddits()
with requests.Session() as session:
    default_subreddits = subreddits.default(limit=20, session=session)

    for subreddit in default_subreddits:
        print(subreddit.description)
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>new</strong></span>

Gets new subreddits.

##### Code Example:

```python
import requests
from knewkarma.core.subreddits import Subreddits

subreddits = Subreddits()
with requests.Session() as session:
    new_subreddits = subreddits.new(limit=50, session=session)

    for subreddit in new_subreddits:
        print(subreddit.description)

```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>popular</strong></span>

Gets popular subreddits.

##### Code Example:

```python
import requests
from knewkarma.core.subreddits import Subreddits

subreddits = Subreddits()
with requests.Session() as session:
    popular_subreddits = subreddits.popular(limit=100, session=session)

    for subreddit in popular_subreddits:
        print(subreddit.description)
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
import requests
from knewkarma.core.user import User

user = User(name="AutoModerator")
with requests.Session() as session:
    profile = user.profile(session=session)
    print(profile.created)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>posts</strong></span>

Gets a user's posts.

##### Code Example:

```python
import requests
from knewkarma.core.user import User

user = User(name="AutoModerator")
with requests.Session() as session:
    posts = user.posts(limit=100, session=session)

    for post in posts:
        print(post.title)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>comments</strong></span>

Gets a user's comments.

##### COde Example:

```python
import requests
from knewkarma.core.user import User

user = User(name="AutoModerator")
with requests.Session() as session:
    comments = user.comments(limit=100, session=session)

    for comment in comments:
        print(comment.id)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>overview</strong></span>

Gets a user's most recent comments.

##### Code Example:

```python
import requests
from knewkarma.core.user import User

user = User(name="AutoModerator")
with requests.Session() as session:
    comments = user.overview(limit=100, session=session)

    for comment in comments:
        print(comment.body)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>moderated_subreddits</strong></span>

Gets subreddits moderated by the user.

##### Code Example:

```python
import requests
from knewkarma.core.user import User

user = User(name="JanelleMonae")
with requests.Session() as session:
    moderated_subreddits = user.moderated_subreddits(session=session)

    for subreddit in moderated_subreddits:
        print(subreddit.name)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>top_subreddits</strong></span>

Gets a user's top n subreddits based on subreddit frequency in *n* posts.

##### Code Example:

```python
import requests
from knewkarma.core.user import User

user = User(name="JanelleMonae")
with requests.Session() as session:
    top_subreddits = user.top_subreddits(
        top_n=10,
        limit=100,
        session=session
    )

    print(top_subreddits)
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
import requests
from knewkarma.core.users import Users

users = Users()
with requests.Session() as session:
    all_users = users.all(limit=50, session=session)

    for user in all_users:
        print(user.name)
```

***

#### <span class="method-name"><span class="italic">Users.</span><strong>new</strong></span>

Gets new users.

##### Code Example:

```python
import requests
from knewkarma.core.users import Users

users = Users()
with requests.Session() as session:
    new_users = users.new(limit=100, session=session)

    for user in new_users:
        print(user.created)
```

***

#### <span class="method-name"><span class="italic">Users.</span><strong>popular</strong></span>

Gets popular users.

##### Code Example:

```python
import requests
from knewkarma.core.users import Users

users = Users()
with requests.Session() as session:
    popular_users = users.popular(limit=200, session=session)

    for user in popular_users:
        print(user.id)
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
