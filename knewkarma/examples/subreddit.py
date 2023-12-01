import asyncio

import aiohttp

from knewkarma import RedditSub


async def async_subreddit(
    subreddit_name: str, data_timeframe: str, data_limit: int, data_sort: str
):
    # Initialize a RedditSub object with the specified subreddit, data timeframe,  limit, and sorting criteria
    subreddit = RedditSub(
        subreddit=subreddit_name,
        data_timeframe=data_timeframe,
        data_limit=data_limit,
        data_sort=data_sort,
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
# timeframes: ["all", "hour", "day", "month", "year"]
# sorting: ["all", "controversial", "new", "top", "best", "hot", "rising"]
asyncio.run(
    async_subreddit(
        subreddit_name="MachineLearning",
        data_timeframe="year",
        data_limit=100,
        data_sort="top",
    )
)
