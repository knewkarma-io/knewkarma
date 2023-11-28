from pprint import pprint

from knewkarma import api

post_id = "12csg48"
post_subreddit = "OSINT"

if __name__ == "__main__":
    post_data = api.get_post_data(post_id=post_id, subreddit=post_subreddit)

    pprint(post_data)
