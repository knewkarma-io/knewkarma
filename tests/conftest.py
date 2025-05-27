import json
import os
from typing import Union, List, Dict


def open_response_file(filename: str) -> Union[List[Dict], Dict]:
    with open(os.path.join("tests", "test_files", filename), "r") as file:
        data: dict = json.load(file)

    return data


RAW_COMMENTS: List[Dict] = open_response_file(filename="comments.json")
RAW_POST: List[Dict] = open_response_file(filename="post.json")
RAW_POSTS: Dict = open_response_file(filename="posts.json")
RAW_SUBREDDIT: Dict = open_response_file(filename="subreddit.json")
RAW_SUBREDDITS: Dict = open_response_file(filename="subreddits.json")
RAW_USER: Dict = open_response_file(filename="user.json")
RAW_USERS: Dict = open_response_file(filename="users.json")
RAW_WIKI_PAGE: Dict = open_response_file(filename="wiki_page.json")
