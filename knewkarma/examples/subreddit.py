import asyncio

import aiohttp

from knewkarma import RedditSub


# Define an asynchronous function to fetch Subreddit data
async def async_subreddit(subreddit_name: str, data_limit: int, data_sort: str):
    # Initialize a RedditSub object with the specified subreddit, data limit, and sorting criteria
    subreddit = RedditSub(
        subreddit=subreddit_name, data_limit=data_limit, data_sort=data_sort
    )

    # Create an asynchronous HTTP session
    async with aiohttp.ClientSession() as session:
        # Fetch subreddit's profile
        profile = await subreddit.profile(session=session)

        # Fetch subreddit's posts
        posts = await subreddit.posts(session=session)

        print(profile)
        print(posts)


# Run the asynchronous function with specified subreddit name, data limit, and sorting criteria
asyncio.run(
    async_subreddit(subreddit_name="MachineLearning", data_limit=100, data_sort="top")
)
