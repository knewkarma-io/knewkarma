<h2 align="center">Karma Kaze (カルマの風)</h2>

<p align="center">Reddit response sanitation & parsing engine.</p>

<p align="center">
      <img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-000000?logo=github&link=https%3A%2F%2Fgithub.com%2Frly0nheart%2Fkarmakaze">
</p>

```python
from engines.karmakaze import RedditSanitiser
import requests

sanitiser = RedditSanitiser()
username = "AutoModerator"
response = requests.get(f"https://www.reddit.com/user/{username}/about.json").json()

print(sanitiser.user(response=response))
```

