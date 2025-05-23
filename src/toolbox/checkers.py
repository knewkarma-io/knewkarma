from types import SimpleNamespace


class Checkers:

    @classmethod
    def is_user(cls, data: SimpleNamespace) -> bool:
        return hasattr(data.kind, "t2")

    @classmethod
    def is_subreddit(cls, data: SimpleNamespace) -> bool:
        return hasattr(data.kind, "t5")

    @classmethod
    def is_post(cls, data: SimpleNamespace) -> bool:
        return hasattr(data.kind, "t3")

    @classmethod
    def is_comment(cls, data: SimpleNamespace) -> bool:
        return hasattr(data.kind, "t1")
