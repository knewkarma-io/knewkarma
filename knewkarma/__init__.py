import os

OPERATION_MODES: list = ["user", "subreddit", "post", "posts", "search", "quit"]
DATA_SORT_CRITERION: list = ["all", "controversial", "new", "top", "best", "hot", "rising"]
POST_LISTINGS: list = ["all", "best", "controversial", "popular", "rising"]

# Construct path to the program's directory
PROGRAM_DIRECTORY: str = os.path.expanduser(os.path.join("~", "knewkarma"))

# Construct path to the current file's directory
CURRENT_FILE_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))

# Construct paths to directories of CSV and JSON files.
CSV_DIRECTORY: str = os.path.join(PROGRAM_DIRECTORY, "csv")
JSON_DIRECTORY: str = os.path.join(PROGRAM_DIRECTORY, "json")

__author__: str = "Richard Mwewa"
__about__: str = "https://about.me/rly0nheart"
__version__: str = "2.4.0.0"
__pypi_project_endpoint__: str = "https://pypi.org/pypi/knewkarma/json"
__description__: str = """
# Knew Karma
> A **Reddit** Data Analysis Toolkit."""
__epilog__: str = f"""
> Call `knewkarma` without command-line arguments to invoke an interactive command-line interface.
>> Calling it with only the `-d/--debug` flag will invoke an interactive command-line interface in debug mode.

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

__operations_description__: str = "# **{}** Operations"
__user_examples__: str = """
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

__subreddit_examples__: str = """
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

__post_example__: str = """
# Example
```
knewkarma post POST_ID SUBREDDIT_NAME
```
"""

__posts_examples__: str = """
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

__search_examples__: str = """
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
