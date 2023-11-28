import asyncio
from pprint import pprint

from knewkarma import api

username = "automoderator"

if __name__ == "__main__":
    user_profile = asyncio.run(
        api.get_profile(profile_type="user_profile", profile_source=username)
    )
    user_posts = asyncio.run(
        api.get_posts(posts_type="user_posts", posts_source=username)
    )
    user_comments = asyncio.run(
        api.get_posts(posts_type="user_comments", posts_source=username)
    )

    pprint(user_profile)
    pprint(user_posts)
    pprint(user_comments)
