# Command-Line Interface

## 🚀 Getting Started

Once installed, you can launch the command-line interface using the knewkarma command.
If you're using Docker, you can run the container interactively like this:

```shell
knewkarma --help
```

```shell
docker run -t knewkarma --help
```

To explore the usage details of individual modules, either:

* Run knewkarma <module> `-h` or `--help`
* Or use the `r<module>` shortcut syntax (refer to the tables below for specifics)

| Command                        | Shortened            | Description                                           |
|--------------------------------|----------------------|-------------------------------------------------------|
| `knewkarma post --help`        | `rpost --help`       | Print help message for post data retrieval            |
| `knewkarma posts --help`       | `rposts --help`      | Print help message for posts' data retrieval          |
| `knewkarma search -- help`     | `rsearch --help`     | Print help message for search results' data retrieval |
| `knewkarma subreddit -- help`  | `rsubreddit --help`  | Print help message for subreddit data retrieval       |
| `knewkarma subreddits -- help` | `rsubreddits --help` | Print help message for subreddits' data retrieval     |
| `knewkarma user -- help`       | `ruser --help`       | Print help message for user data retrieval            |
| `knewkarma users -- help`      | `rusers --help`      | Print help message for users' data retrieval          |

---

## 📋 Basic Usage Examples

### Post Command

Use this command to get an individual post's data including its comments, provided the post's `id` and
source `subreddit` are specified.

| Ccmmand                                       | Shortened                            | Description           |
|-----------------------------------------------|--------------------------------------|-----------------------|
| `knewkarma post 13ptwzd AskReddit --data`     | `rpost 13ptwzd AskReddit --data`     | Get a post's data     |
| `knewkarma post 13ptwzd AskReddit --comments` | `rpost 13ptwzd AskReddit --comments` | Get a post's comments |

---

### Posts Command

Use this command get best, controversial, popular, new and/or front-page posts.

| Command                           | Shortened                | Description                            |
|-----------------------------------|--------------------------|----------------------------------------|
| `knewkarma posts --best`          | `rposts --best`          | Get posts from *best* listing          |
| `knewkarma posts --controversial` | `rposts --controversial` | Get posts from *controversial* listing |
| `knewkarma posts --front-page`    | `rposts --front-page`    | Get posts from Reddit Front-Page       |
| `knewkarma posts --new`           | `rposts --new`           | Get new posts                          |
| `knewkarma posts --top`           | `rposts --top`           | Get posts from *top* listing           |
| `knewkarma posts --rising`        | `rposts --rising`        | Get posts from *rising* listing        |

---

### Search Command

Use this command search/discovery of targets in users, subreddits, and posts.

| Command                                           | Shortened                                | Description       |
|---------------------------------------------------|------------------------------------------|-------------------|
| `knewkarma search "this is automated" --comments` | `rsearch "this is automated" --comments` | Search comments   |
| `knewkarma search coronavirus --posts`            | `rsearch coronavirus --posts`            | Search posts      |
| `knewkarma search ask --subreddits`               | `rsearch ask --subreddits`               | Search subreddits |
| `knewkarma search john --users`                   | `rsearch john --users`                   | Search users      |

---

### Subreddit Command

Use this command to get a subreddit's data, such as comments, posts, wiki-pages, wiki-page data, and more...

| Command                                                                        | Shortened                                                             | Description                                                   |
|--------------------------------------------------------------------------------|-----------------------------------------------------------------------|---------------------------------------------------------------|
| `knewkarma subreddit MachineLearning --profile`                                | `rsubreddit MachineLearning --profile`                                | Get subreddit profile                                         |
| `knewkarma subreddit MachineLearning --posts`                                  | `rsubreddit MachineLearning --posts`                                  | Get subreddit posts                                           |
| `knewkarma subreddit MachineLearning --search-posts "artificial intelligence"` | `rsubreddit MachineLearning --search-posts "artificial intelligence"` | Search a subreddit for posts that contain a specified keyword |
| `knewkarma subreddit MachineLearning --wiki-pages`                             | `rsubreddit MachineLearning --wiki-pages`                             | Get subreddit's wiki pages                                    |
| `knewkarma subreddit MachineLearning --wiki-page config/description`           | `rsubreddit MachineLearning --wiki-page config/description`           | Get subreddit's specified wiki page data                      |

---

### Subreddits Command

Use this command to get new, popular, default and/or all subreddits.

| Command                          | Shortened               | Description            |
|----------------------------------|-------------------------|------------------------|
| `knewkarma subreddits --all`     | `rsubreddits --all`     | Get all subreddits     |
| `knewkarma subreddits --default` | `rsubreddits --default` | Get default subreddits |
| `knewkarma subreddits --new`     | `rsubreddits --new`     | Get new subreddits     |
| `knewkarma subreddits --popular` | `rsubreddits --popular` | Get popular subreddits |

---

### User Command

Use this command to get user data, such as profile, posts, comments, top subreddits, moderated subreddits, and more...

| Command                                                      | Shortened                                           | Description                                                         |
|--------------------------------------------------------------|-----------------------------------------------------|---------------------------------------------------------------------|
| `knewkarma user AutoModerator --profile`                     | `ruser AutoModerator --profile`                     | Get user profile                                                    |
| `knewkarma user AutoModerator --comments`                    | `ruser AutoModerator --comments`                    | Get user comments                                                   |
| `knewkarma user AutoModerator --posts`                       | `ruser AutoModerator --posts`                       | Get user posts                                                      |
| `knewkarma user AutoModerator --overview`                    | `ruser AutoModerator --overview`                    | Get user's most recent comment activity                             |
| `knewkarma user AutoModerator --search-posts "banned"`       | `ruser AutoModerator --search-posts "banned"`       | Get a user's posts that contain the specified keyword               |
| `knewkarma user AutoModerator --search-comments "automated"` | `ruser AutoModerator --search-comments "automated"` | Get a user's comment that contain the specified keyword             |
| `knewkarma user janellemonae --moderated-subreddits`         | `ruser janellemonae --moderated-subreddits`         | Get subreddits moderated by user                                    |
| `knewkarma user TheRealKSi --top-subreddits 10`              | `ruser  TheRealKSi --top-subreddits 10`             | Get user's top n subreddits based on subreddit frequency in n posts |
| `knewkarma user TheRealKSi --does-user-exist`                | `ruser  TheRealKSI --does-user-exist`               | Check user existence                                                |

---

### Users Command

Use this command to get new, popular, and/or all users.

| Command                     | Shortened          | Description       |
|-----------------------------|--------------------|-------------------|
| `knewkarma users --all`     | `rusers --all`     | Get all users     |
| `knewkarma users --new`     | `rusers --new`     | Get new users     |
| `knewkarma users --popular` | `rusers --popular` | Get popular users |
