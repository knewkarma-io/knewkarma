from pprint import pprint

from knewkarma import api

search_query = "covid-19"

if __name__ == "__main__":
    search_results = api.get_posts(posts_type="search_posts", posts_source=search_query)

    pprint(search_results)
