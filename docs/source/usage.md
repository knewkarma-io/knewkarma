# Usage

After installation, the *command-line interface* instance can be called with the `knewkarma` command (
or `docker run -it [container-name]`
for Docker Containers)

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

Knew Karma: A Reddit data analysis toolkit — by Richard Mwewa

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

Knew Karma (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a Command-Line Interface (CLI), and an
Application Programming Interface (API) to enable an easy integration in other Python Projects.
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


