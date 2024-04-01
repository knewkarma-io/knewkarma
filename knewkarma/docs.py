from datetime import date

from .version import Version


class Docs:
    """
    Container for documentation-related data for Knew Karma.

    Attributes:
          copyright (str): Copyright notice for the current year, including the author's details.
          license (str): The MIT license under which the Knew Karma software is distributed.
          description (str): A brief description of Knew Karma as a CLI tool for Reddit data analysis.
          examples (dict): Usage examples for different operations within Knew Karma.
    """

    copyright: str = (
        f"© 2023-{date.today().year} [Richard Mwewa](https://rly0nheart.github.io)"
    )

    license: str = f"""# License
MIT License

Copyright {copyright}
    
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
"""
    description: str = f"""
# Knew Karma {Version.release}
> **Reddit Data Analysis Toolkit.**"""

    examples: dict = {
        "user": """
    # Examples
    ## Get user profile
    ```
    knewkarma user  AutoModerator --profile
    ```
    ***
    ## Get user comments
    ```
    knewkarma user  AutoModerator --comments
    ```
    ***
    ## Get user comments
    ```
    knewkarma user  AutoModerator --posts
    ```
    ***
    ## Get user's most recent comment activity
    ```
    knewkarma user AutoModerator --overview
    ```
    ***
    ## Get a user's posts that contain the specified keyword
    ```
    knewkarma user AutoModerator --search-posts rules
    ```
    ***
    ## Get a user's comment that contain the specified keyword
    ```
    knewkarma user AutoModerator --search-comments banned
    ```
    ***
    ## Get subreddits moderated by user
    ```
    knewkarma user TheRealKSi --moderated-subreddits
    ```
    ***
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
    ***
    ## Get subreddit posts
    ```
    knewkarma subreddit MachineLearning --posts
    ```
    ***
    ## Search a subreddit for posts that contain a specified keyword
    ```
    knewkarma subreddit MachineLearning --search "artificial intelligence"
    ```
    ***
    ## Get subreddit's wiki pages
    ```
    knewkarma subreddit MachineLearning --wiki-pages
    ```
    ***
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
    ***
    ## Get default subreddits
    ```
    knewkarma subreddits --default
    ```
    ***
    ## Get new subreddits
    ```
    knewkarma subreddits --new
    ```
    ***
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
    ***
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
    ***
    ## Get posts from Reddit Front-Page
    ```
    knewkarma posts --front-page
    ```
    ***
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
    ***
    ## Search subreddits
    ```
    knewkarma search ask --subreddits
    ```
    ***
    ## Search posts
    ```
    knewkarma search covid-19 --posts
    ```
    """,
    }
