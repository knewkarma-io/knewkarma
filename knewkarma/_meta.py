# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

import os
from typing import Literal

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

author: str = "Richard Mwewa"
about_author: str = "https://rly0nheart.github.io"
version: str = "4.0.0.0"

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

description: str = f"""
# Knew Karma CLI {version}
> A **Reddit** Data Analysis Toolkit."""
epilog: str = f"""
# Copyright © 2023-2024 [{author}]({about_author})
```
MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of Knew Karma and associated documentation files (the "Software"), to deal
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

## Get communities moderated by user
```
knewkarma user TheRealKSi --moderated-communities
```

## Get user's top n communities based on community frequency in n posts
```
knewkarma --limit 500 user TheRealKSi --top-communities 10
```
"""

community_examples: str = """
# Examples
## Get community profile
```
knewkarma community MachineLearning --profile
```

## Get community posts
```
knewkarma community MachineLearning --posts
```
"""

posts_examples: str = """
# Examples
## Get posts from Reddit Front-Page
```
knewkarma posts --front-page
```

## Search posts
```
knewkarma posts --search "covid-19"
```

## Get posts from specified listing
```
knewkarma posts --listing best
```
"""

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #

# Construct path to the program's directory
PROGRAM_DIRECTORY: str = os.path.expanduser(os.path.join("~", "knewkarma-data"))

DATA_SORT_CRITERION = Literal[
    "controversial",
    "new",
    "top",
    "best",
    "hot",
    "rising",
]
POSTS_LISTINGS = Literal["best", "controversial", "popular", "rising"]
DATA_TIMEFRAME = Literal["hour", "day", "week", "month", "year"]

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++ #
