# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import os

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

author: str = "Richard Mwewa"
about_author: str = "https://about.me/rly0nheart"
version: str = "3.2.0.0"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

description: str = f"""
# Knew Karma CLI {version}
> A **Reddit** Data Analysis Toolkit."""
epilog: str = f"""
# by [{author}]({about_author})
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
knewkarma user automoderator --profile
```

## Get User Comments
```
knewkarma user automoderator --comments
```

## Get User Posts
```
knewkarma user automoderator --posts
```
"""

subreddit_examples: str = """
# Examples
## Get Subreddit Profile
```
knewkarma subreddit MachineLearning --profile
```

## Get Subreddit Posts
```
knewkarma subreddit MachineLearning --posts
```
"""

posts_examples: str = """
# Examples
## Get Posts from Reddit Front-Page
```
knewkarma posts --front-page
```

## Search posts
```
knewkarma posts --search "covid-19"
```

## Get Posts from A Specified Listing
```
knewkarma posts --listing best
```
"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# Construct path to the program's directory
PROGRAM_DIRECTORY: str = os.path.expanduser(os.path.join("~", "knewkarma-data"))

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
