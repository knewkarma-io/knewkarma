import typing as t

from praw.models import Submission, Comment
from rich.status import Status

from .client import reddit


class Post:
    def __init__(self, id: str):
        self.id = id
        self._post = reddit.submission(id=id)

    def info(self, status: Status) -> Submission:
        if isinstance(status, Status):
            status.update(f"Getting info from post {self.id}...")
        return self._post

    def comments(self, status: Status) -> t.List[Comment]:
        if isinstance(status, Status):
            status.update(f"Getting comments from post {self.id}...")
        return self._post.comments.list()
