from datetime import date


class Docs:
    """
    Container for documentation-related data for Knew Karma.

    Attributes:
          copyright (str): Copyright notice for the current year, including the author's details.
          description (str): A brief description of Knew Karma as a CLI tool for Reddit data analysis.
          examples (dict): Usage examples for different operations within Knew Karma.
    """

    author: str = "[Richard Mwewa](https://rly0nheart.github.io)"
    copyright: str = (
        f"© Copyright 2023-{date.today().year} {author}. All Rights Reserved"
    )

    about: str = f"**Knew Karma**: *A Reddit Data Analysis Toolkit* — by {author}"
    description: str = """
**Knew Karma** (/nuː ‘kɑːrmə/) is a **Reddit** Data Analysis Toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a **Command-Line Interface (CLI)**, an
**Application Programming Interface (API)** to enable an easy integration in other Python Projects and a **Graphical
User
Interface (GUI)** for Windows machines, making it adaptable for various user preferences.
"""

    examples: dict = {
        "user": """
The **User** module is used to pull a specified user's data including profile, comments, posts, 
searching posts that contain the specified kwyword, or even searching comments that contain the specified keyword.

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
knewkarma user AutoModerator --search-posts rules
```

## Get a user's comment that contain the specified keyword
```
knewkarma user AutoModerator --search-comments banned
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
        "post": """
The **Post** module is used to pull an individual post's data including its comments, 
provided the post's **id** and source **subreddit** are provided.

# Examples
### Get a post's data
```
knewkarma post 12csg48 OSINT --data
```

### Get a post's comments
```
knewkarma post 12csg48 OSINT --comments
```
""",
        "posts": """
The **Posts** is used to pull posts from sources like the front page, a listing, or new posts.

# Examples
## Get new posts
```
knewkarma posts --new
```

## Get posts from Reddit Front-Page
```
knewkarma posts --front-page
```

## Get posts from specified listing
```
knewkarma posts --listing best
```
    """,
        "search": """
The **Search** module is used for search/discovery of targets in users, subreddits, and posts.

# Examples
## Search users
```
knewkarma search john --users
```

## Search subreddits
```
knewkarma search ask --subreddits
```

## Search posts
```
knewkarma search covid-19 --posts
```
    """,
    }
