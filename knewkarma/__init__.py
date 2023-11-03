__author__ = "Richard Mwewa"
__about__ = "https://about.me/rly0nheart"
__version__ = "1.6.0.0"
__description__ = """
# Knew Karma
> A **Reddit** Data Analysis Toolkit."""
__epilog__ = f"# by [{__author__}]({__about__})"

__operations_description__ = "# **{}** Operations"
__user_examples__ = """
# Examples
## Get User Profile
```
knewkarma user automoderator
```

## Get User Comments (not sorted or limited)
```
knewkarma user automoderator ---comments
```

## Get User Posts (not sorted or limited)
```
knewkarma user automoderator --posts
```

## Get User Posts/Comments (sorted and limited)
```
knewkarma --sort top --limit 20 user automoderator --comments/--posts
```
"""

__subreddit_examples__ = """
# Examples
## Get Subreddit Profile
```
knewkarma subreddit OSINT
```

## Get Subreddit Posts (not sorted or limited)
```
knewkarma subreddit OSINT --posts
```

## Get Subreddit Posts (sorted and limited)
```
knewkarma --sort new --limit 20 subreddit OSINT
```
"""

__post_examples__ = """
# Examples
## Get Post Data (without comments)
```
knewkarma post 12csg48 OSINT
```

## Get Post Data (with comments)
```
knewkarma post 12csg48 OSINT --comments
```

## Get Post's Comments (sorted and limited)
```
knewkarma --sort top --limit 10 post 12csg48 OSINT
```
"""

__posts_examples__ = """
# Examples
## Get Posts from Reddit Front-Page (not sorted or limited)
```
knewkarma posts
```

## Get Posts from A Specified Listing (not sorted or limited)
```
knewkarma posts --listing best
```

## Get Posts from Reddit Front-Page (sorted and limited)
```
knewkarma --sort top --limit 20 posts
```

## Get Posts from A Specified Listing (sorted and limited)
```
knewkarma --sort top --limit 20 posts --listing best
```
"""

__search_examples__ = """
# Examples
## Search for Posts (no sorting and limiting)
```
knewkarma search "This is funny"
```

## Search for Posts (sorted and limited)
```
knewkarma --sort top --limit 20 search "This is funny"
```
"""
