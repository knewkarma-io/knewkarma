class Help:
    """
    Container for help-related data for Knew Karma.

    Attributes:
          author (str): A markdown-formatted string of author name and url.
          copyright (str): Copyright notice for license and the author's details.
          summary (str): A brief description of Knew Karma as a tool for Reddit data analysis.
          description (str): A full description of Knew Karma as a CLI, Library,
                and GUI program for Reddit data analysis.
          examples (dict): Usage examples for different operations within Knew Karma.
    """

    author: str = "[Richard Mwewa](https://gravatar.com/rly0nheart)"
    copyright: str = f"© MIT License {author}. All rights reserved."
    documentation: str = "https://knewkarma.readthedocs.io"

    summary: str = f"**Knew Karma**: *A Reddit data analysis toolkit* — by {author}"
    description: str = f"""
**Knew Karma** (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a **Command-Line Interface (CLI)**, and an
**Application Programming Interface (API)** to enable an easy integration in other Python Projects.

Refer to the [documentation]({documentation}) for *usage* and *integration* guide.
"""

    examples: dict = {
        "post": """
The **Post** module is used to pull an individual post's data including its comments, 
provided the post's **id** and source **subreddit** are provided.

# Examples
### Get a post's data
```
knewkarma post 13ptwzd AskReddit --data
```

### Get a post's comments
```
knewkarma post 13ptwzd AskReddit --comments
```
""",
        "posts": """
The **Posts** is used to pull posts from sources like the front page, a listing, or new posts.

# Examples
## Get posts from *best* listing
```
knewkarma posts --best
```

## Get posts from *controversial* listing
```
knewkarma posts --controversial
```

## Get posts from Reddit Front-Page
```
knewkarma posts --front-page
```

## Get new posts
```
knewkarma posts --new
```

## Get posts from *popular* listing
```
knewkarma posts --popular
```

## Get posts from *rising* listing
```
knewkarma posts --rising
```
""",
        "search": """
The **Search** module is used for search/discovery of targets in users, subreddits, and posts.

# Examples
## Search comments
```
knewkarma search "this is automated" --comments
```

## Search posts
```
knewkarma search coronavirus --posts
```

## Search subreddits
```
knewkarma search ask --subreddits
```

## Search users
```
knewkarma search john --users
```
""",
        "subreddit": """
The **Subreddit** module is used to pull a specified subreddit's data including profile, posts, wiki pages,
or even searching posts that have the specified keyword.

# Examples
## Get subreddit profile
```
knewkarma subreddit MachineLearning --profile
```

## Get subreddit posts
```
knewkarma subreddit MachineLearning --posts
```

## Search a subreddit for posts that contain a specified keyword
```
knewkarma subreddit MachineLearning --search "artificial intelligence"
```

## Get subreddit's wiki pages
```
knewkarma subreddit MachineLearning --wiki-pages
```

## Get subreddit's specified wiki page data
```
knewkarma subreddit MachineLearning --wiki-page config/description
```
""",
        "subreddits": """
The **Subreddits** module is used to pull subreddits from various sources such as new, default, or popular.

# Examples
## Get all subreddits
```
knewkarma subreddits --all
```

## Get default subreddits
```
knewkarma subreddits --default
```

## Get new subreddits
```
knewkarma subreddits --new
```

## Get popular subreddits
```
knewkarma subreddits --popular
```
""",
        "user": """
The **User** module is used to pull a specified user's data including profile, comments, posts, 
searching posts that contain the specified keyword, or even searching comments that contain the specified keyword.

# Examples
## Get user profile
```
knewkarma user  AutoModerator --profile
```

## Get user comments
```
knewkarma user  AutoModerator --comments
```

## Get user posts
```
knewkarma user  AutoModerator --posts
```

## Get user's most recent comment activity
```
knewkarma user AutoModerator --overview
```

## Get a user's posts that contain the specified keyword
```
knewkarma user AutoModerator --search-posts "banned"
```

## Get a user's comment that contain the specified keyword
```
knewkarma user AutoModerator --search-comments "this is an automated action"
```

## Get subreddits moderated by user
```
knewkarma user TheRealKSi --moderated-subreddits
```

## Get user's top n subreddits based on subreddit frequency in n posts
```
knewkarma --limit 500 user TheRealKSi --top-subreddits 10
```
""",
        "users": """
The **Users** module is used to pull users from various sources such as new, all or popular.

# Examples
## Get all users
```
knewkarma users --all
```

## Get new users
```
knewkarma users --new
```

## Get popular users
```
knewkarma users --popular
```
""",
    }
