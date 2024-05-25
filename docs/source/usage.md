# Usage
## CLI (and Docker Container) Usage

After installation, the *cli* instance can be called with the `knewkarma` command (or `docker run [container-name]` for
Docker Containers)


```commandline
knewkarma --help
```
```commandline
docker run -t my-knewkarma-container --help
```

```commandline
Usage: knewkarma [-h] [-t {hour,day,week,month,year}]
                 [-s {controversial,new,top,best,hot,rising}] [-l LIMIT]
                 [--time-format {concise,datetime}] [-e EXPORT] [-u] [-v]
                 {post,posts,search,subreddit,subreddits,user} ...

Knew Karma: A Reddit Data Analysis Toolkit — by Richard Mwewa

Positional Arguments:
  {post,posts,search,subreddit,subreddits,user}
                        module
    post                post module (semi-bulk)
    posts               posts module (bulk)
    search              search module (bulk)
    subreddit           subreddit module (semi-bulk)
    subreddits          subreddits module (bulk)
    user                user module (semi-bulk)

Options:
  -h, --help            show this help message and exit
  -t, --timeframe {hour,day,week,month,year}
                        (bulk/semi-bulk) timeframe to get data from (default:
                        all)
  -s, --sort {controversial,new,top,best,hot,rising}
                        (bulk/semi-bulk) sort criterion (default: all)
  -l, --limit LIMIT     (bulk/semi-bulk) data output limit (default: 100)
  --time-format {concise,datetime}
                        determines the format of the output time (default:
                        datetime)
  -e, --export EXPORT   a comma-separated list of file types to export the
                        output to (supported: csv,html,json,xml)
  -u, --updates         check for updates on run
  -v, --version         show program's version number and exit

Knew Karma (/nuː ‘kɑːrmə/) is a Reddit Data Analysis Toolkit designed to
provide an extensive range of functionalities for exploring and analysing
Reddit data. It includes a Command-Line Interface (CLI), an Application
Programming Interface (API) to enable an easy integration in other Python
Projects and a Graphical User Interface (GUI) for Windows machines, making it
adaptable for various user preferences.
```

You can further view individual operation mode usages by calling `knewkarma` with an operation mode name and
the `-h/--help` flag.

### Subreddit Module Usage

```commandline
knewkarma subreddit --help
```

```commandline
docker run -it my-knewkarma-container subreddit --help
```

```commandline
Usage: knewkarma subreddit [-h] [-p] [-s SEARCH] [-pp] [-wp WIKI_PAGE] [-wps]
                           subreddit

Subreddit: Pull a specified subreddit's data.

Positional Arguments:
  subreddit             subreddit name

Options:
  -h, --help            show this help message and exit
  -p, --profile         get a subreddit's profile
  -s, --search SEARCH   get a subreddit's posts that contain the specified
                        keyword
  -pp, --posts          get a subreddit's posts
  -wp, --wiki-page WIKI_PAGE
                        get a subreddit's specified wiki page data
  -wps, --wiki-pages    get a subreddit's wiki pages

The Subreddit module is used to pull a specified subreddit's data including
profile, posts, wiki pages, or even searching posts that have the specified
keyword.

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                  Examples                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                            Get subreddit profile

 knewkarma subreddit MachineLearning --profile

                             Get subreddit posts

 knewkarma subreddit MachineLearning --posts

        Search a subreddit for posts that contain a specified keyword

 knewkarma subreddit MachineLearning --search "artificial intelligence"

                          Get subreddit's wiki pages

 knewkarma subreddit MachineLearning --wiki-pages

                   Get subreddit's specified wiki page data

 knewkarma subreddit MachineLearning --wiki-page config/description
```

### Subreddits Module Usage
```commandline
knewkarma subreddits --help
```
```commandline
docker run -it knewkarma subreddits --help
```
```commandline
Usage: knewkarma subreddits [-h] [-a] [-d] [-n] [-p]

*Subreddits: Pull subreddits from various sources.

Options:
  -h, --help     show this help message and exit
  -a, --all      get all subreddits
  -d, --default  get default subreddits
  -n, --new      get new subreddits
  -p, --popular  get popular subreddits

The Subreddits module is used to pull subreddits from various sources such as
new, default, or popular.

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                  Examples                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                              Get all subreddits

 knewkarma subreddits --all

                            Get default subreddits

 knewkarma subreddits --default

                              Get new subreddits

 knewkarma subreddits --new

                            Get popular subreddits

 knewkarma subreddits --popular
```

### Post Module Usage
```commandline
knewkarma post --help
```
```commandline
docker run -it knewkarma post --help
```
```commandline
Usage: knewkarma post [-h] [-d] [-c] id subreddit

Post Module: Pull an individual post's data

Positional Arguments:
  id              post id
  subreddit       post source subreddit

Options:
  -h, --help      show this help message and exit
  -d, --data      get post data
  -c, --comments  get post comments

The Post module is used to pull an individual post's data including its
comments, provided the post's id and source subreddit are provided.

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                  Examples                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                              Get a post's data

 knewkarma post 12csg48 OSINT --data

                            Get a post's comments

 knewkarma post 12csg48 OSINT --comments
```
### Posts Module Usage

```commandline
knewkarma posts --help
```

```commandline
docker run -it my-knewkarma-container posts --help
```

```commandline
Usage: knewkarma posts [-h] [-n] [-f] [-l {best,controversial,popular,rising}]

Posts: Pull posts from various sources.

Options:
  -h, --help            show this help message and exit
  -n, --new             get new posts
  -f, --front-page      get posts from the reddit front-page
  -l, --listing {best,controversial,popular,rising}
                        get posts from a specified listing

The Posts is used to pull posts from sources like the front page, a listing,
or new posts.

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                  Examples                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                                Get new posts

 knewkarma posts --new

                       Get posts from Reddit Front-Page

 knewkarma posts --front-page

                       Get posts from specified listing

 knewkarma posts --listing best
```

### Search Module Usage

```commandline
knewkarma search --help
```
```commandline
docker run -it my-knewkarma-container search --help
```
```commandline
Usage: knewkarma search [-h] [-u] [-p] [-s] query

Search: Get search results from various sources.

Positional Arguments:
  query             search query

Options:
  -h, --help        show this help message and exit
  -u, --users       search users
  -p, --posts       search posts
  -s, --subreddits  search subreddits

The Search module is used for search/discovery of targets in users,
subreddits, and posts.

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                  Examples                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                                 Search users

 knewkarma search john --users

                              Search subreddits

 knewkarma search ask --subreddits

                                 Search posts

 knewkarma search covid-19 --posts
```

### User Module Usage

```commandline
knewkarma user --help
```

```commandline
docker run -it my-knewkarma-container user --help
```
```commandline
Usage: knewkarma user [-h] [-p] [-c] [-o] [-pp] [-sp SEARCH_POSTS]
                      [-sc SEARCH_COMMENTS] [-mc] [-tc TOP_N]
                      username

User: Pull a specified user's data.

Positional Arguments:
  username              username

Options:
  -h, --help            show this help message and exit
  -p, --profile         get a user's profile
  -c, --comments        get a user's comments
  -o, --overview        get a user's most recent comment activity
  -pp, --posts          get a user's posts
  -sp, --search-posts SEARCH_POSTS
                        get a user's posts that contain the specified keyword
  -sc, --search-comments SEARCH_COMMENTS
                        get a user's comments that contain the specified
                        keyword
  -mc, --moderated-subreddits
                        get subreddits moderated by the user
  -tc, --top-subreddits TOP_N
                        get a user's top n subreddits based on subreddit
                        frequency in n posts

The User module is used to pull a specified user's data including profile,
comments, posts, searching posts that contain the specified kwyword, or even
searching comments that contain the specified keyword.

┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                  Examples                                  ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

                               Get user profile

 knewkarma user  AutoModerator --profile

                              Get user comments

 knewkarma user  AutoModerator --comments

                                Get user posts

 knewkarma user  AutoModerator --posts

                   Get user's most recent comment activity

 knewkarma user AutoModerator --overview

            Get a user's posts that contain the specified keyword

 knewkarma user AutoModerator --search-posts rules

           Get a user's comment that contain the specified keyword

 knewkarma user AutoModerator --search-comments banned

                       Get subreddits moderated by user

 knewkarma user TheRealKSi --moderated-subreddits

     Get user's top n subreddits based on subreddit frequency in n posts

 knewkarma --limit 500 user TheRealKSi --top-subreddits 10
```



