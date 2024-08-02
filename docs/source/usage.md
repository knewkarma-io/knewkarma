# Usage

## Getting Started

After installation, the *command-line interface* instance can be called with the `knewkarma` command (
or `docker run -it [container-name]`
for Docker Containers):

```shell
knewkarma --help
```

```shell
docker run -t my-knewkarma-container --help
```

You can further view individual module usages by calling `knewkarma` with a module name and
the `-h/--help` flag [see table below]:

| Command                        |                      Description                      |
|--------------------------------|:-----------------------------------------------------:|
| `knewkarma post --help`        |      Print help message for post data retrieval       |
| `knewkarma posts --help`       |     Print help message for posts' data retrieval      |
| `knewkarma search -- help`     | Print help message for search results' data retrieval |
| `knewkarma subreddit -- help`  |    Print help message for subreddit data retrieval    |
| `knewkarma subreddits -- help` |   Print help message for subreddits' data retrieval   |
| `knewkarma user -- help`       |      Print help message for user data retrieval       |
| `knewkarma users -- help`      |     Print help message for users' data retrieval      |

## Basic Usage Examples

### Post Command

Use this command to get an individual post's data including its comments, provided the post's `id` and
source `subreddit` are specified.

| Command                                       | Description           |
|-----------------------------------------------|-----------------------|
| `knewkarma post 13ptwzd AskReddit --data`     | Get a post's data     |
| `knewkarma post 13ptwzd AskReddit --comments` | Get a post's comments |

### Posts Command

Use this command get best, controversial, popular, new and/or front-page posts.

| Command                           | Description                            |
|-----------------------------------|----------------------------------------|
| `knewkarma posts --best`          | Get posts from *best* listing          |
| `knewkarma posts --controversial` | Get posts from *controversial* listing |
| `knewkarma posts --front-page`    | Get posts from Reddit Front-Page       |
| `knewkarma posts --new`           | Get new posts                          |
| `knewkarma posts --popular`       | Get posts from *popular* listing       |
| `knewkarma posts --rising`        | Get posts from *rising* listing        |

### Search Command

Use this command search/discovery of targets in users, subreddits, and posts.

| Command                                           | Description       |
|---------------------------------------------------|-------------------|
| `knewkarma search "this is automated" --comments` | Search comments   |
| `knewkarma search coronavirus --posts`            | Search posts      |
| `knewkarma search ask --subreddits`               | Search subreddits |
| `knewkarma search john --users`                   | Search users      |

### Subreddit Command

Use this command to get a subreddit's data, such as comments, posts, wiki-pages, wiki-page data, and more...

| Command                                                                        | Description                                                      |
|--------------------------------------------------------------------------------|------------------------------------------------------------------|
| `knewkarma subreddit MachineLearning --profile`                                | Get subreddit profile                                            |
| `knewkarma subreddit MachineLearning --comments`                               | Get subreddit comments                                           |
| `knewkarma subreddit MachineLearning --posts`                                  | Get subreddit posts                                              |
| `knewkarma subreddit MachineLearning --search-comments "something"`            | Search a subreddit for comments that contain a specified keyword |
| `knewkarma subreddit MachineLearning --search-posts "artificial intelligence"` | Search a subreddit for posts that contain a specified keyword    |
| `knewkarma subreddit MachineLearning --wiki-pages`                             | Get subreddit's wiki pages                                       |
| `knewkarma subreddit MachineLearning --wiki-page config/description`           | Get subreddit's specified wiki page data                         |

### Subreddits Command

Use this command to get new, popular, default and/or all subreddits.

| Command                          | Description            |
|----------------------------------|------------------------|
| `knewkarma subreddits --all`     | Get all subreddits     |
| `knewkarma subreddits --default` | Get default subreddits |
| `knewkarma subreddits --new`     | Get new subreddits     |
| `knewkarma subreddits --popular` | Get popular subreddits |

### User Command

Use this command to get user data, such as profile, posts, comments, top subreddits, moderated subreddits, and more...

| Command                                                                        | Description                                                         |
|--------------------------------------------------------------------------------|---------------------------------------------------------------------|
| `knewkarma user AutoModerator --profile`                                       | Get user profile                                                    |
| `knewkarma user AutoModerator --comments`                                      | Get user comments                                                   |
| `knewkarma user AutoModerator --posts`                                         | Get user posts                                                      |
| `knewkarma user AutoModerator --overview`                                      | Get user's most recent comment activity                             |
| `knewkarma user AutoModerator --search-posts "banned"`                         | Get a user's posts that contain the specified keyword               |
| `knewkarma user AutoModerator --search-comments "this is an automated action"` | Get a user's comment that contain the specified keyword             |
| `knewkarma user TheRealKSi --moderated-subreddits`                             | Get subreddits moderated by user                                    |
| `knewkarma --limit 500 user TheRealKSi --top-subreddits 10`                    | Get user's top n subreddits based on subreddit frequency in n posts |

### Users Command

Use this command to get new, popular, and/or all users.

| Command                     | Description       |
|-----------------------------|-------------------|
| `knewkarma users --all`     | Get all users     |
| `knewkarma users --new`     | Get new users     |
| `knewkarma users --popular` | Get popular users |
