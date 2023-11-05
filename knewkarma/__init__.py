import os

DATA_SORT_LISTINGS = ["controversial", "new", "top", "best", "hot", "rising"]
POST_LISTINGS = ["best", "controversial", "popular", "rising"]

# Construct path to the program's directory
PROGRAM_DIRECTORY = os.path.expanduser(os.path.join("~", "knewkarma"))

# Construct path to the current file's directory
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Construct paths to directories of CSV and JSON files.
CSV_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "csv")
JSON_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "json")


__author__ = "Richard Mwewa"
__about__ = "https://about.me/rly0nheart"
__version__ = "2.0.0.0-beta"
__description__ = """
# Knew Karma
> A **Reddit** Data Analysis Toolkit."""
__epilog__ = f"# by [{__author__}]({__about__})"


__operations_description__ = "# **{}** Operations"
__user_examples__ = """
# Examples
## Get User Profile
```
knewkarma user USERNAME
```

## Get User Comments (not sorted or limited)
```
knewkarma user USERNAME ---comments
```

## Get User Posts (not sorted or limited)
```
knewkarma user USERNAME --posts
```

## Get User Posts/Comments (sorted and limited)
```
knewkarma --sort top --limit 20 user USERNAME --comments/--posts
```
"""

__subreddit_examples__ = """
# Examples
## Get Subreddit Profile
```
knewkarma subreddit SUBREDDIT_NAME --profile
```

## Get Subreddit Posts (not sorted or limited)
```
knewkarma subreddit SUBREDDIT_NAME --posts
```

## Get Subreddit Posts (sorted and limited)
```
knewkarma --sort new --limit 20 subreddit SUBREDDIT_NAME
```
"""

__post_examples__ = """
# Examples
## Get Post Data (without comments)
```
knewkarma post POST_ID SUBREDDIT_NAME
```

## Get Post Data (with comments)
```
knewkarma post POST_ID SUBREDDIT_NAME --comments
```

## Get Post's Comments (sorted and limited)
```
knewkarma --sort top --limit 10 post POST_ID SUBREDDIT_NAME
```
"""

__posts_examples__ = """
# Examples
## Get Posts from Reddit Front-Page (not sorted or limited)
```
knewkarma posts --front-page
```

## Get Posts from A Specified Listing (not sorted or limited)
```
knewkarma posts --listing best
```

## Get Posts from Reddit Front-Page (sorted and limited)
```
knewkarma --sort top --limit 20 posts --front-page
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
knewkarma search QUERY_STRING
```

## Search for Posts (sorted and limited)
```
knewkarma --sort top --limit 20 search QUERY_STRING
```
"""
