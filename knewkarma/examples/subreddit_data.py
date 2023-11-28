import asyncio
from pprint import pprint

from knewkarma import api

subreddit = "OSINT"

if __name__ == "__main__":
    user_profile = asyncio.run(
        api.get_profile(profile_type="subreddit_profile", profile_source=subreddit)
    )
    user_posts = asyncio.run(
        api.get_posts(posts_type="subreddit_posts", posts_source=subreddit)
    )

    pprint(user_profile)
    pprint(user_posts)
