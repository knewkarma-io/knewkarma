# Knew Karma

[![Read the Docs](https://img.shields.io/readthedocs/knewkarma?logo=readthedocs)](https://knewkarma.readthedocs.io) [![CodeQL](https://github.com/bellingcat/knewkarma/actions/workflows/codeql.yml/badge.svg)](https://github.com/bellingcat/knewkarma/actions/workflows/codeql.yml) [![Upload PyPI Package](https://github.com/bellingcat/knewkarma/actions/workflows/python-publish.yml/badge.svg)](https://github.com/bellingcat/knewkarma/actions/workflows/python-publish.yml) [![PyPI - Version](https://img.shields.io/pypi/v/knewkarma?logo=pypi&link=https%3A%2F%2Fpypi.org%2Fproject%2Fknewkarma)](https://pypi.org/project/knewkarma) [![Release Snap Package](https://github.com/bellingcat/knewkarma/actions/workflows/snapstore-publish.yml/badge.svg)](https://github.com/bellingcat/knewkarma/actions/workflows/snapstore-publish.yml) [![Snap version](https://img.shields.io/snapcraft/v/knewkarma/latest/stable?logo=snapcraft&color=%23BB431A)](https://snapcraft.io/knewkarma) [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/rly0nheart)

**Knew Karma** (/nuː ‘kɑːrmə/) is a **Reddit** Data Analysis Toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a **Command-Line Interface (CLI)** (_Snap/PyPI
Package_), and an
**Application Programming Interface (API)** (_PyPI Package_) to enable an easy integration in other Python Projects.

## Feature Overview

Knew Karma provides detailed access to Reddit data across various categories. Refer to the table below for a
complete overview of the features available:

| Category       | Feature                | Description                                                     |
|----------------|------------------------|-----------------------------------------------------------------|
| **Post**       | `Data`                 | Retrieves an individual post's data.                            |
|                | `Comments`             | Retrieves an individual post's comments.                        |
| **Posts**      | `New`                  | Retrieves new posts.                                            |
|                | `Reddit Front-Page`    | Retrieves front-page posts.                                     |
|                | `Listing`              | Retrieves posts from specified Reddit listings.                 |
| **Search**     | `Users`                | Searches for users.                                             |
|                | `Subreddits`           | Searches for subreddits.                                        |
|                | `Posts`                | Searches for posts.                                             |
| **Subreddit**  | `Profile`              | Retrieves subreddit profile information.                        |
|                | `Posts`                | Retrieves posts from a specified subreddit.                     |
|                | `Search Posts`         | Returns a subreddit's posts that contain the specified keyword. |
|                | `Wiki Pages`           | Lists wiki pages in a subreddit.                                |
|                | `Wiki Page`            | Retrieves content from specific wiki pages.                     |
| **Subreddits** | `All`                  | Retrieves all subreddits.                                       |
|                | `Default`              | Retrieves default subreddits.                                   |
|                | `New`                  | Retrieves new subreddits.                                       |
|                | `Popular`              | Retrieves popular subreddits.                                   |
| **User**       | `Profile`              | Retrieves user profile information.                             |
|                | `Posts`                | Retrieves user posts.                                           |
|                | `Comments`             | Retrieves user comments.                                        |
|                | `Overview`             | Retrieves user's most recent comment activity.                  |
|                | `Search Posts`         | Returns a user's posts that contain the specified keyword.      |
|                | `Search Comments`      | Returns a user's comments that contain the specified keyword.   |
|                | `Top n Subreddits`     | Identifies top subreddits based on user activity.               |
|                | `Moderated Subreddits` | Lists subreddits moderated by the user.                         |
| **Users**      | `All`                  | Retrieves all users.                                            |
|                | `New`                  | Retrieves new users.                                            |
|                | `Popular`              | Retrieves popular users.                                        |

# Documentation

[Refer to the Docs](https://knewkarma.readthedocs.io) for the **Installation**, **Integration** and **Usage** guide.

## Important Note on Data Fetching

Knew Karma is designed to fetch recent data from Reddit. It directly interacts with the Reddit API to access up-to-date
information, including the latest posts, comments, and user activity.

If you need to access historical Reddit data, I recommend using the [Pushshift API](https://api.pushshift.io/docs),
which is
specifically designed for retrieving large volumes of historical data, including posts, comments, and
other Reddit activity.

## Star History

<a href="https://star-history.com/#bellingcat/knewkarma&Date">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=bellingcat/knewkarma&type=Date&theme=dark" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=bellingcat/knewkarma&type=Date" />
   <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=bellingcat/knewkarma&type=Date" />
 </picture>
</a>

## License

MIT License © [Richard Mwewa](https://rly0nheart.github.io)

