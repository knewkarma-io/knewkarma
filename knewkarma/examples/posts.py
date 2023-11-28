import asyncio
from pprint import pprint

from knewkarma import api

posts_listing = "all"  # ["best", "controversial", "popular", "rising"]

if __name__ == "__main__":
    front_page_posts = asyncio.run(api.get_posts(posts_type="front_page_posts"))
    listing_posts = asyncio.run(
        api.get_posts(posts_type="listing_posts", posts_source=posts_listing)
    )

    pprint(front_page_posts)
    pprint(listing_posts)
