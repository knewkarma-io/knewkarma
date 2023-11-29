# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import os

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

author: str = "Richard Mwewa"
about: str = "https://about.me/rly0nheart"
version: str = "3.0.0.0"

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

description: str = f"""
# Knew Karma CLI {version}
> A **Reddit** Data Analysis Toolkit."""
epilog: str = f"""
# by [{author}]({about})
```
MIT License

Copyright © 2023 {author}

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

operations_description: str = "# **{}** Operations"
user_examples: str = """
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

subreddit_examples: str = """
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

post_example: str = """
# Example
```
knewkarma post POST_ID SUBREDDIT_NAME
```
"""

posts_examples: str = """
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

search_examples: str = """
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

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# Construct path to the program's directory
PROGRAM_DIRECTORY: str = os.path.expanduser(os.path.join("~", "knewkarma"))

# Construct path to the current file's directory
CURRENT_FILE_DIRECTORY: str = os.path.dirname(os.path.abspath(__file__))

# Construct paths to directories of CSV and JSON files.
CSV_DIRECTORY: str = os.path.join(PROGRAM_DIRECTORY, "csv")
JSON_DIRECTORY: str = os.path.join(PROGRAM_DIRECTORY, "json")

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
