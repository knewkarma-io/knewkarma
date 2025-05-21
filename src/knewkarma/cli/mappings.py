import typing as t

from knewkarma import Post, Posts, Search, Subreddit, Subreddits
from toolbox.render import Render


class Mappings:

    def __init__(
        self, data_cls: t.Union[Post, Posts, Search, Subreddit, Subreddits], **kwargs
    ):
        self.kwargs = kwargs
        self.data_cls = data_cls

    def subreddit(self) -> t.Tuple[t.Dict, t.Dict[str, t.Callable]]:
        limit = self.kwargs.get("limit")
        comments_per_post = self.kwargs.get("comments_per_post")
        sort = self.kwargs.get("sort")
        timeframe = self.kwargs.get("timeframe")
        query = self.kwargs.get("search")
        wikipage = self.kwargs.get("wikipage")

        methods: t.Dict = {
            "comments": lambda session, status, logger: self.data_cls.comments(
                session=session,
                posts_limit=self.kwargs.get("limit"),
                comments_per_post=comments_per_post,
                sort=sort,
                timeframe=timeframe,
                status=status,
                logger=logger,
            ),
            "posts": lambda session, status, logger=None: self.data_cls.posts(
                limit=limit,
                sort=sort,
                timeframe=timeframe,
                status=status,
                logger=logger,
                session=session,
            ),
            "profile": lambda session, status: self.data_cls.profile(
                status=status, session=session
            ),
            "search": lambda session, status, logger: self.data_cls.search(
                query=query,
                limit=limit,
                sort=sort,
                timeframe=timeframe,
                status=status,
                logger=logger,
                session=session,
            ),
            "wikipages": lambda session, status, logger: self.data_cls.wikipages(
                status=status, session=session
            ),
            "wikipage": lambda session, status, logger: self.data_cls.wikipage(
                page_name=wikipage, status=status, session=session
            ),
        }

        renders = {"profile": Render.subreddit_profile}

        return methods, renders
