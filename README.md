**Knew Karma** (*/nuː ‘kɑːrmə/*) is a zero-auth data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a **Command-Line Interface (CLI)**, and an
**Application Programming Interface (API)** to enable an easy integration in other Python Projects</p>

<p>
  <a href="https://github.com/knewkarma-io/knewkarma"><img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000?logo=github&link=https%3A%2F%2Fgithub.com%2Frly0nheart%2Fknewkarma"></a>
  <a href="https://pepy.tech/project/knewkarma"><img alt="Downloads" src="https://img.shields.io/pepy/dt/knewkarma?logo=pypi"></a>
  <a href="https://pypi.org/project/knewkarma"><img alt="PyPI - Version" src="https://img.shields.io/pypi/v/knewkarma?logo=pypi&link=https%3A%2F%2Fpypi.org%2Fproject%2Fknewkarma"></a>
  <a href="https://snapcraft.io/knewkarma"><img alt="Snap Version" src="https://img.shields.io/snapcraft/v/knewkarma/latest/stable?logo=snapcraft&color=%23BB431A"></a>
  <!--<a href="https://opencollective.com/knewkarma"><img alt="Open Collective backers and sponsors" src="https://img.shields.io/opencollective/all/knewkarma?logo=open-collective"></a>-->
</p>

```commandline
knewkarma subreddit AskScience --posts --limit 200
```

Or

```commandline
rsubreddit AskScience --posts --limit 200
```

And/Or

```python
import requests

from knewkarma.core.subreddit import Subreddit

subreddit = Subreddit("AskScience")
with requests.Session() as session:
    posts = subreddit.posts(session=session, limit=200)
    for post in posts:
        print(post.title)
```

## Documentation

Refer to the [documentation](https://knewkarma.readthedocs.io) for *Feature Overview*, *Installation*, *API
Integration*, and *Usage* instructions.

## Star History

<a href="https://star-history.com/#knewkarma-io/knewkarma&Date">
   <picture>
      <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/svg?repos=knewkarma-io/knewkarma&type=Date&theme=dark" />
      <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/svg?repos=knewkarma-io/knewkarma&type=Date" />
      <img alt="Star History Chart" src="https://api.star-history.com/svg?repos=knewkarma-io/knewkarma&type=Date" />
   </picture>
</a>

## License

GPL-3.0+ License © [Ritchie Mwewa](https://gravatar.com/rly0nheart)

## Support

If you find Knew Karma useful and would like to support its development, you can sponsor the project through **Open
Collective**.

Your sponsorship will help cover the **costs of ongoing maintenance**, **new feature development**, and **overall
project sustainability**.

### How to Sponsor

You can sponsor the project by visiting Knew Karma's [Open Collective page](https://opencollective.com/knewkarma) and
choosing a sponsorship tier that fits your budget.

Whether you're a company that relies on Knew Karma for data analysis or an individual who appreciates open-source
projects and/or the work put into this project in particular, any sponsorship tier is greatly appreciated.

[Become a Sponsor](https://opencollective.com/knewkarma)
