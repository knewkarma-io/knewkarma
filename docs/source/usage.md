# Usage

## CLI (and Docker Container) Usage

After installation, the *cli* instance can be called with the `knewkarma` command (or `docker run -it [container-name]`
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


> E.g., you can run `knewkarma subreddit --help` to see the `subreddit` module's help message.
>> Or, run `knewkarma user --help` to see the `user` module's help message**, e.t.c.


