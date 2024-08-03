# Developer Interface

## Overview

The Knew Karma API offers a seamless way to interact with Reddit data, providing asynchronous access to user profiles,
subreddit information, posts, comments, and more.

To help you get started, I've included detailed examples showcasing how to utilise various
API features effectively.

The API exposes 7 primary classes, each tailored for different types of data retrieval:

### <span style="font-size: 140%;"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Post</strong></span>

Represents a Reddit post and provides method(s) for getting data from the specified post.

### Initialisation

```python
post = Post(post_id: str, post_subreddit: str, time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from a specified post.

* `post_id`: ID of the post to get data from.
* `subreddit`: Name of the subreddit where the post is located.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

#### <span class="method-name"><span class="italic">Post.</span><strong>data</strong>(session: requests.Session)</span>

Returns a post's data. This method fetches the detailed data of a specified Reddit post.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Post
import requests


def get_post_data(post_id, post_subreddit):
    post = Post(post_id=post_id, post_subreddit=post_subreddit)
    with requests.Session() as session:
        data = post.data(session=session)
        pprint(data)


get_post_data(post_id="13ptwzd", post_subreddit="AskReddit")
```

***

#### <span class="method-name"><span class="italic">Post.</span><strong>comments</strong>(session: requests.Session, limit: int, sort: Literal[str] = "all")</span>

Returns a post's comments. This method retrieves comments from the specified post. You can limit the number of comments
returned and sort them based on a specified criterion.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Post
import requests


def get_post_comments(post_id, post_subreddit, comments_limit):
    post = Post(post_id=post_id, post_subreddit=post_subreddit)
    with requests.Session() as session:
        comments = post.comments(limit=comments_limit, session=session)
        pprint(comments)


get_post_comments(post_id="13ptwzd", post_subreddit="AskReddit", comments_limit=50))
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Posts</strong></span>

Represents Reddit posts and provides methods for getting posts from various sources.

### Initialisation

```python
posts = Posts(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple posts.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

#### <span class="method-name"><span class="italic">Posts.</span><strong>best</strong>(limit: int, session: requests.Session)</span>

Returns posts from the best listing. This method retrieves the best posts according to Reddit's algorithm. You can limit
the number of posts returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Posts
import requests


def get_best_posts(posts_limit):
    posts = Posts()
    with requests.Session() as session:
        best = posts.best(limit=posts_limit, session=session)
        pprint(best)


get_best_posts(posts_limit=120)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>controversial</strong>(limit: int, session: requests.Session)</span>

Returns posts from the controversial listing. This method fetches posts that are considered controversial based on
Reddit's algorithm. You can limit the number of posts returned.

##### Code Example::

```python
from pprint import pprint
from knewkarma import Posts
import requests


def get_controversial_posts(posts_limit):
    posts = Posts()
    with requests.Session() as session:
        controversial = posts.controversial(limit=posts_limit, session=session)
        pprint(controversial)


get_controversial_posts(posts_limit=50)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>front_page</strong>(session: requests.Session, limit: int, sort: Literal[str] = "all")</span>

Returns posts from the Reddit front-page. This method retrieves posts from Reddit's front page. You can limit the number
of posts returned and sort them based on a specified criterion.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Posts
import requests


def get_frontpage_posts(posts_limit):
    posts = Posts()
    with requests.Session() as session:
        frontpage = posts.front_page(limit=posts_limit, session=session)
        pprint(frontpage)


get_frontpage_posts(posts_limit=10)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>new</strong>(session: requests.Session, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns new posts. This method fetches new posts. You can limit the number of posts returned, sort them based on a
specified criterion, and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Posts
import requests


def get_new_posts(posts_limit):
    posts = Posts()
    with requests.Session() as session:
        new = posts.new(limit=posts_limit, session=session)
        pprint(new)


get_new_posts(posts_limit=10)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>popular</strong>(limit: int, session: requests.Session)</span>

Returns posts from the popular listing. This method retrieves popular posts. You can limit the number of posts returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Posts
import requests


def get_popular_posts(posts_limit):
    posts = Posts()
    with requests.Session() as session:
        popular = posts.popular(limit=posts_limit, session=session)
        pprint(popular)


get_popular_posts(posts_limit=50)
```

***

#### <span class="method-name"><span class="italic">Posts.</span><strong>rising</strong>(limit: int, session: requests.Session)</span>

Returns posts from the rising listing. This method fetches rising posts. You can limit the number of posts returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Posts
import requests


def get_rising_posts(posts_limit):
    posts = Posts()
    with requests.Session() as session:
        rising = posts.rising(limit=posts_limit, session=session)
        pprint(rising)


get_rising_posts(posts_limit=100)
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Search</strong></span>

Represents Reddit search functionality and provides methods for getting search results from
different entities.

### Initialisation

```python
search = Search(query: str, time_format: Literal["concise", "locale"])
```

Initialises an instance for performing searches across Reddit.

* `query`: Search query.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

#### <span class="method-name"><span class="italic">Search.</span><strong>posts</strong>(timeframe: Literal[str], sort: Literal[str], limit: int, session: requests.Session)</span>

Returns posts matching the search query. This method retrieves posts that match the search query. You can limit the
number of posts returned, sort them based on a specified criterion, and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Search
import requests


def get_search_posts(query, results_limit):
    search = Search(query=query)
    with requests.Session() as session:
        posts = search.posts(limit=results_limit, session=session)
        pprint(posts)


get_search_posts(query="something in data science", results_limit=200)
```

***

#### <span class="method-name"><span class="italic">Search.</span><strong>subreddits</strong>(timeframe: Literal[str], sort: Literal[str], limit: int, session: requests.Session)</span>

Search subreddits. This method searches for subreddits that match the query. You can limit the number of subreddits
returned, sort them based on a specified criterion, and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Search
import requests


def get_search_subreddits(query, results_limit):
    search = Search(query=query)
    with requests.Session() as session:
        subreddits = search.subreddits(limit=results_limit, session=session)
        pprint(subreddits)


get_search_subreddits(query="questions", results_limit=200)
```

***

#### <span class="method-name"><span class="italic">Search.</span><strong>users</strong>(timeframe: Literal[str], sort: Literal[str], limit: int, session: requests.Session)</span>

Search users. This method searches for users that match the query. You can limit the number of users returned, sort them
based on a specified criterion, and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Search
import requests


def get_search_users(query, results_limit):
    search = Search(query=query)
    with requests.Session() as session:
        users = search.users(limit=results_limit, session=session)
        pprint(users)


get_search_users(query="john", results_limit=200)
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Subreddit</strong></span>

Represents a Reddit subreddit and provides methods for getting data from it.

### Initialisation

```python
subreddit = Subreddit(subreddit: str, time_format: Literal["concise", "locale"])
```

Initialises a Subreddit instance for getting profile and posts from the specified subreddit.

* `subreddit`: Name of the subreddit to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>profile</strong>(session: requests.Session)</span>

Returns a subreddit's profile data. This method fetches the profile data of a specified subreddit.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddit
import requests


def get_subreddit_profile(subreddit):
    subreddit = Subreddit(subreddit=subreddit)
    with requests.Session() as session:
        profile = subreddit.profile(session=session)
        pprint(profile)


get_subreddit_profile(subreddit="MachineLearning")
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_pages</strong>(session: requests.Session)</span>

Returns a subreddit's wiki pages. This method retrieves the wiki pages of a specified subreddit.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddit
import requests


def get_subreddit_wiki_pages(subreddit):
    subreddit = Subreddit(subreddit=subreddit)
    with requests.Session() as session:
        wiki_pages = subreddit.wiki_pages(session=session)
        pprint(wiki_pages)


get_subreddit_wiki_pages(subreddit="MachineLearning")
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>wiki_page</strong>(page: str, session: requests.Session)</span>

Returns a subreddit's specified wiki page data. This method fetches the data of a specified wiki page from a subreddit.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddit
import requests


def get_subreddit_wiki_page(page, subreddit):
    subreddit = Subreddit(subreddit=subreddit)
    with requests.Session() as session:
        wiki_page_data = subreddit.wiki_page(page_name=page, session=session)
        pprint(wiki_page_data)


get_subreddit_wiki_page(page="rules", subreddit="MachineLearning")
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>posts</strong>(session: requests.Session, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns a subreddit's posts. This method retrieves posts from a specified subreddit. You can limit the number of posts
returned, sort them based on a specified criterion, and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddit
import requests


def get_subreddit_posts(subreddit, posts_limit):
    subreddit = Subreddit(subreddit=subreddit)
    with requests.Session() as session:
        posts = subreddit.posts(limit=posts_limit, session=session)
        pprint(posts)


get_subreddit_posts(posts_limit=500, subreddit="MachineLearning")
```

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>comments</strong>(session: requests.Session, posts_limit: int, comments_per_post: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns a subreddit's comments. This method retrieves comments from a specified subreddit. You can limit the number of
posts
to get comments from, and the number of comments to get from each post.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddit
import requests


def get_subreddit_comments(subreddit, posts_limit, comments_per_post):
    subreddit = Subreddit(subreddit=subreddit)
    with requests.Session() as request_session:
        comments = subreddit.comments(
            posts_limit=posts_limit,
            comments_per_post=comments_per_post,
            session=request_session
        )
        pprint(comments)


get_subreddit_comments(subreddit="AskScience", posts_limit=100, comments_per_post=20)
```

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>search</strong>(session: requests.Session, keyword: str, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns posts that contain a specified keyword from a subreddit. This method searches for posts in a subreddit that
contain the specified keyword. You can limit the number of posts returned, sort them based on a specified criterion, and
filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddit
import requests


def search_subreddit_comments(search_query, subreddit, limit):
    subreddit = Subreddit(subreddit=subreddit)
    with requests.Session() as session:
        posts = subreddit.search_comments(query=search_query, limit=limit, session=session)
        pprint(posts)


search_subreddit_comments(search_query="ML jobs", limit=100, subreddit="MachineLearning")
```

##### Note:

The limit of posts will be the same as the number of comments that will be returned, e.i., If you specify the limit as
500, then the search will also look through 500 comments for matches of the query (I intend to improve this, but that's
how it'll work for now.)

***

#### <span class="method-name"><span class="italic">Subreddit.</span><strong>search</strong>(session: requests.Session, keyword: str, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns posts that contain a specified keyword from a subreddit. This method searches for posts in a subreddit that
contain the specified keyword. You can limit the number of posts returned, sort them based on a specified criterion, and
filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddit
import requests


def search_subreddit_posts(search_query, subreddit, posts_limit):
    subreddit = Subreddit(subreddit=subreddit)
    with requests.Session() as session:
        posts = subreddit.search_posts(query=search_query, limit=posts_limit, session=session)
        pprint(posts)


search_subreddit_posts(search_query="ML jobs", posts_limit=100, subreddit="MachineLearning")
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Subreddits</strong></span>

Represents subreddits and provides methods for getting related data.

### Initialisation

```python
subreddits = Subreddits(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple subreddits.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>all</strong>(limit: int, timeframe: Literal[str] = "all", session: requests.Session)</span>

Returns all subreddits. This method retrieves all subreddits. You can limit the number of subreddits returned and filter
them by a timeframe.

##### implementation

```python
from pprint import pprint
from knewkarma import Subreddits
import requests


def get_all_subreddits(subreddits_limit):
    subreddits = Subreddits()
    with requests.Session() as session:
        all_subs = subreddits.all(limit=subreddits_limit, session=session)
        pprint(all_subs)


get_all_subreddits(subreddits_limit=500)
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>default</strong>(limit: int, session: requests.Session)</span>

Returns default subreddits. This method fetches the default subreddits. You can limit the number of subreddits returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddits
import requests


def get_default_subreddits(subreddits_limit):
    subreddits = Subreddits()
    with requests.Session() as session:
        default_subs = subreddits.default(limit=subreddits_limit, session=session)
        pprint(default_subs)


get_default_subreddits(subreddits_limit=20)
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>new</strong>(limit: int, session: requests.Session, timeframe: Literal[str] = "all")</span>

Returns new subreddits. This method retrieves new subreddits. You can limit the number of subreddits returned and filter
them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddits
import requests


def get_new_subreddits(subreddits_limit):
    subreddits = Subreddits()
    with requests.Session() as session:
        new_subs = subreddits.new(limit=subreddits_limit, session=session)
        pprint(new_subs)


get_new_subreddits(subreddits_limit=50)
```

***

#### <span class="method-name"><span class="italic">Subreddits.</span><strong>popular</strong>(limit: int, session: requests.Session, timeframe: Literal[str] = "all")</span>

Returns popular subreddits. This method fetches popular subreddits. You can limit the number of subreddits returned and
filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Subreddits
import requests


def get_popular_subreddits(subreddits_limit):
    subreddits = Subreddits()
    with requests.Session() as session:
        popular_subs = subreddits.popular(limit=subreddits_limit, session=session)
        pprint(popular_subs)


get_popular_subreddits(subreddits_limit=100)
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>User</strong></span>

Represents a Reddit user and provides methods for getting data from the specified user.

### Initialisation

```python
user = User(username: str, time_format: Literal["concise", "locale"])
```

Initialises a User instance for getting profile, posts, and comments data from the specified user.

* `username`: Username of the user to get data from.
* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

#### <span class="method-name"><span class="italic">User.</span><strong>profile</strong>(session: requests.Session)</span>

Returns a user's profile data. This method fetches the profile data of a specified user. It requires
an `requests.Session` to make the asynchronous HTTP request.

##### Code Example:

```python
from pprint import pprint
from knewkarma import User
import requests


def get_user_profile(username):
    user = User(username=username)
    with requests.Session() as session:
        profile = user.profile(session=session)
        pprint(profile)


get_user_profile(username="AutoModerator")
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>posts</strong>(session: requests.Session, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns a user's posts. This method retrieves posts from a specified user. You can limit the number of posts returned,
sort them based on a specified criterion, and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import User
import requests


def get_user_posts(username, posts_limit):
    user = User(username=username)
    with requests.Session() as session:
        posts = user.posts(limit=posts_limit, session=session)
        pprint(posts)


get_user_posts(username="AutoModerator", posts_limit=100)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>comments</strong>(session: requests.Session, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns a user's comments. This method retrieves comments from a specified user. You can limit the number of comments
returned, sort them based on a specified criterion, and filter them by a timeframe.

##### COde Example:

```python
from pprint import pprint
from knewkarma import User
import requests


def get_user_comments(username, comments_limit):
    user = User(username=username)
    with requests.Session() as session:
        comments = user.comments(limit=comments_limit, session=session)
        pprint(comments)


get_user_comments(username="AutoModerator", comments_limit=100)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>overview</strong>(limit: int, session: requests.Session)</span>

Returns a user's most recent comments. This method retrieves the most recent comments of a specified user. You can limit
the number of comments returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import User
import requests


def get_user_overview(username, comments_limit):
    user = User(username=username)
    with requests.Session() as session:
        comments = user.overview(limit=comments_limit, session=session)
        pprint(comments)


get_user_overview(username="AutoModerator", comments_limit=100)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>search_posts</strong>(session: requests.Session, keyword: str, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns a user's posts that contain the specified keywords. This method searches for posts from a specified user that
contain the specified keywords. You can limit the number of posts returned, sort them based on a specified criterion,
and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import User
import requests


def get_search_user_posts(username, search_query, posts_limit):
    user = User(username=username)
    with requests.Session() as session:
        posts = user.search_posts(query=search_query,
                                  limit=posts_limit, session=session)
        pprint(posts)


get_search_user_posts(username="AutoModerator",
                      search_query="banned", posts_limit=100)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>search_comments</strong>(session: requests.Session, keyword: str, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all")</span>

Returns a user's comments that contain the specified keyword. This method searches for comments from a specified user
that contain the specified keyword. You can limit the number of comments returned, sort them based on a specified
criterion, and filter them by a timeframe.

##### Code Example:

```python
from pprint import pprint
from knewkarma import User
import requests


def get_search_user_comments(username, search_query, comments_limit):
    user = User(username=username)
    with requests.Session() as session:
        comments = user.search_comments(
            query=search_query,
            limit=comments_limit,
            session=session
        )
        pprint(comments)


get_search_user_comments(
    username="AutoModerator",
    search_query="this is an automated action",
    comments_limit=100
)
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>moderated_subreddits</strong>(session: requests.Session)</span>

Returns subreddits moderated by the user. This method fetches the subreddits moderated by a specified user.

##### Code Example:

```python
from pprint import pprint
from knewkarma import User
import requests


def get_user_moderated_subreddits(username):
    user = User(username=username)
    with requests.Session() as session:
        moderated_subs = user.moderated_subreddits(session=session)
        pprint(moderated_subs)


get_user_moderated_subreddits(username="TheRealKSI")
```

***

#### <span class="method-name"><span class="italic">User.</span><strong>top_subreddits</strong>(session: requests.Session, top_n: int, limit: int, sort: Literal[str] = "all", timeframe: Literal[str] = "all") -> list[tuple]</span>

Returns a user's top n subreddits based on subreddit frequency in n posts. This method retrieves the top n subreddits
that a specified user is most active in. You can limit the number of posts considered, sort them based on a specified
criterion, and filter them by a timeframe.

##### Code Example:

```python
from knewkarma import User
import requests


def get_user_top_subreddits(username, top_number, subreddits_limit):
    user = User(username=username)
    with requests.Session() as session:
        top_subs = user.top_subreddits(
            top_n=top_number,
            limit=subreddits_limit,
            session=session
        )
        pprint(top_subs)

    get_user_top_subreddits(
        username="TheRealKSI",
        top_number=10,
        subreddits_limit=100
    )
```

***

### <span class="class-name"><span class="italic">class</span> <span class="faint">knewkarma.</span><strong>Users</strong></span>

Represents Reddit users and provides methods for getting related data.

### Initialisation

```python
users = Users(time_format: Literal["concise", "locale"])
```

Initialises an instance for getting data from multiple users.

* `time_format`: Determines the format of the output's datetime. Use "concise" for a human-readable time difference,
  or "locale" for a localized datetime string. Defaults to "locale".

### Methods

#### <span class="method-name"><span class="italic">Users.</span><strong>all</strong>(limit: int, session: requests.Session)</span>

Returns all users. This method retrieves all users. You can limit the number of users returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Users
import requests


def get_all_users(users_limit):
    users = Users()
    with requests.Session() as session:
        all_users = users.all(limit=users_limit, session=session)
        pprint(all_users)


get_all_users(users_limit=1000)
```

***

#### <span class="method-name"><span class="italic">Users.</span><strong>new</strong>(limit: int, session: requests.Session)</span>

Returns new users. This method retrieves new users. You can limit the number of users returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Users
import requests


def get_new_users(users_limit):
    users = Users()
    with requests.Session() as session:
        new = users.new(limit=users_limit, session=session)
        pprint(new)


get_new_users(users_limit=500)
```

***

#### <span class="method-name"><span class="italic">Users.</span><strong>popular</strong>(limit: int, session: requests.Session)</span>

Returns popular users. This method retrieves popular users. You can limit the number of users returned.

##### Code Example:

```python
from pprint import pprint
from knewkarma import Users
import requests


def get_popular_users(users_limit):
    users = Users()
    with requests.Session() as session:
        popular = users.popular(limit=users_limit, session=session)
        pprint(popular)


get_popular_users(users_limit=100)
```

***

## Timeframes and Sorting

When fetching posts or comments, you can specify timeframes ("`hour`", "`day`", "`month`", "`year`") and sorting
criteria ("`controversial`", "`new`", "`top`", "`best`", "`hot`", "`rising`"). Leaving these parameters unspecified
defaults to retrieving data across all timeframes and sort criteria.

## Utilising `time_format` Parameter

The `time_format` parameter (or `--time-format` in the CLI) affects how timestamps are displayed in your results.
Use "`concise`" for relative times (e.g., "*5 minutes ago*") or "`locale`" for locale-based formatting.

Here's how to apply it:

```python
from knewkarma import Posts

posts = Posts(time_format="concise")
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
