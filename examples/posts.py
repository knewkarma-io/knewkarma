import asyncio

import aiohttp

from knewkarma import RedditPosts


async def async_posts(timeframe: str, limit: int, sort: str):
    # Initialize RedditPosts with the specified timeframe, limit and sorting criteria
    posts = RedditPosts(timeframe=timeframe, limit=limit, sort=sort)

    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Fetch front page posts
        front_page_posts = await posts.front_page(session=session)
        # Fetch posts from a specified listing ('best')
        listing_posts = await posts.listing(listings_name="best", session=session)
        # Fetch posts that match the specified search query 'covid-19'
        search_results = await posts.search(query="covid-19", session=session)

        print(front_page_posts)
        print(listing_posts)
        print(search_results)


# Run the asynchronous function with a specified limit and sorting parameter
# timeframes: ["all", "hour", "day", "month", "year"]
# sorting: ["all", "controversial", "new", "top", "best", "hot", "rising"]
asyncio.run(async_posts(timeframe="year", limit=100, sort="all"))
