import os

DATA_SORT_LISTINGS = ["controversial", "new", "top", "best", "hot", "rising"]
POST_LISTINGS = ["all", "best", "controversial", "popular", "rising"]

# Construct path to the program's directory
PROGRAM_DIRECTORY = os.path.expanduser(os.path.join("~", "knewkarma"))

# Construct path to the current file's directory
CURRENT_FILE_DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Construct paths to directories of CSV and JSON files.
CSV_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "csv")
JSON_DIRECTORY = os.path.join(PROGRAM_DIRECTORY, "json")


__author__ = "Richard Mwewa"
__about__ = "https://about.me/rly0nheart"
__version__ = "2.0.0.0"
__description__ = """
# Knew Karma
> A **Reddit** Data Analysis Toolkit."""
__epilog__ = f"""
> Command-Line options can be mixed to get various data with a one-line command

```
knewkarma OPERATION_MODE POSITIONAL_MODE_ARGUMENT -OPTION_1OPTION_2OPTION_3
```

# by [{__author__}]({__about__})

```
MIT License

Copyright © 2023 {__author__}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
"""


__operations_description__ = "# **{}** Operations"
__user_examples__ = """
# Examples
## Get User Profile
```
knewkarma user USERNAME --profile
```

## Get User Comments (unsorted and unlimited)
```
knewkarma user USERNAME --comments
```

## Get User Posts (unsorted and unlimited)
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

## Get Subreddit Posts (unsorted and unlimited)
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
knewkarma post POST_ID SUBREDDIT_NAME --profile
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
## Get Posts from Reddit Front-Page (unsorted and unlimited)
```
knewkarma posts --front-page
```

## Get Posts from A Specified Listing (unsorted and unlimited)
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
## Search for Posts (unsorted and unlimited)
```
knewkarma search QUERY_STRING
```

## Search for Posts (sorted and limited)
```
knewkarma --sort top --limit 20 search QUERY_STRING
```
"""
