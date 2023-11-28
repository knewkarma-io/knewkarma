```
┓┏┓         ┓┏┓         
┃┫ ┏┓┏┓┓┏┏  ┃┫ ┏┓┏┓┏┳┓┏┓
┛┗┛┛┗┗ ┗┻┛  ┛┗┛┗┻┛ ┛┗┗┗┻
```

A **Reddit** Data Analysis Toolkit.

[![.Net](https://img.shields.io/badge/Visual%20Basic%20.NET-5C2D91?style=flat&logo=.net&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3A%22Visual+Basic+.NET%22&type=code) [![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3APython&type=code) [![Docker](https://img.shields.io/badge/Dockefile-%230db7ed.svg?style=flat&logo=docker&logoColor=white)](https://github.com/search?q=repo%3Abellingcat%2Fknewkarma++language%3ADockerfile&type=code) [![PyPI - Version](https://img.shields.io/pypi/v/knewkarma?style=flat&logo=pypi&logoColor=ffdd54&label=PyPI&labelColor=3670A0&color=3670A0)](https://pypi.org/project/knewkarma)  [![BuyMeACoffee](https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=flat&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/_rly0nheart)

# Feature Overview

## Knew Karma CLI/GUI

- [x] **<ins>Knew Karma can get the following Reddit data from individual targets</ins>**:
    * **User**: *Profile*, *Posts*, *Comments*
    * **Subreddit**: *Profile*, *Posts*
    * **Post**: *Data*, *Comments* (available only in the CLI)
- [x] **<ins>It can also get posts from various sources, such as</ins>**:
    * **Searching**: Allows getting posts that match the user-provided query from all over Reddit
    * **Reddit Front-Page**: Allows getting posts from the Reddit Front-Page
    * **Listing**: Allows getting posts from a user-specified Reddit Listing
- [x] **<ins>Bonus Features</ins>**
    * **CLI/GUI**
    * **Dark Mode** (*GUI Automatic/Manual*)
    * **Write data to files** (*JSON/CSV*)

## Knew Karma Python Library

```python
from pprint import pprint

from knewkarma import api

# Get user profile
username = "automoderator"
user_profile = api.get_profile(profile_type="user_profile", profile_source=username)
pprint(user_profile)

# Get subreddit profile
subreddit = "OSINT"
subreddit_profile = api.get_profile(profile_type="subreddit_profile", profile_source=subreddit)
pprint(subreddit_profile)

# Get a post's data
post_id = "12csg48"
post_subreddit = "OSINT"
post_data = api.get_post_data(post_id=post_id, subreddit=post_subreddit)
pprint(post_data)
```

> More code examples/implementations are
> available [here](https://github.com/bellingcat/knewkarma/tree/master/knewkarma/examples)

# Documentation

*[Refer to the Wiki](https://github.com/bellingcat/knewkarma/wiki) for Installation, Usage and Uninstallation
instructions.*
***
[![me](https://github.com/bellingcat/knewkarma/assets/74001397/efd19c7e-9840-4969-b33c-04087e73e4da)](https://about.me/rly0nheart)

