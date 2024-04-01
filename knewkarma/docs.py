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
        "© Copyright 2023-{date.today().year} {author}. All Rights Reserved"
    )

    about: str = f"**Knew Karma**: *Reddit Data Analysis Toolkit.* — by {author}"
    description: str = """
**Knew Karma** (/nuː ‘kɑːrmə/) is a **Reddit** Data Analysis Toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a **Command-Line Interface (CLI)**, an
**Application Programming Interface (API)** to enable an easy integration in other Python Projects and a **Graphical
User
Interface (GUI)** for Windows machines, making it adaptable for various user preferences.
"""

    examples: dict = {
        "user": """
# Examples
## Get user profile
```
knewkarma user  AutoModerator --profile
```

## Get user comments
```
knewkarma user  AutoModerator --comments
```

## Get user comments
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
# Examples
## Get a post's 'profile'
```
knewkarma post 12csg48 OSINT --profile
```

## Get a post's comments
```
knewkarma post 12csg48 OSINT --comments
```
""",
        "posts": """
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
