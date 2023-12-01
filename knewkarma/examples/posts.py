import asyncio

import aiohttp

from knewkarma import RedditPosts


async def async_posts(limit: int, sort: str):
    posts = RedditPosts(limit=limit, sort=sort)
    async with aiohttp.ClientSession() as session:
        front_page_posts = await posts.front_page(session=session)
        listing_posts = await posts.listing(listings_name="best", session=session)
        search_results = await posts.search(query="covid-19", session=session)

        print(front_page_posts)
        print(listing_posts)
        print(search_results)


asyncio.run(async_posts(limit=100, sort="all"))
