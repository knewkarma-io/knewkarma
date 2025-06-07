import typing as t
from types import SimpleNamespace

__all__ = ["RedditSanitiser"]

from engines.karmakaze.schemas import (
    Comment,
    Post,
    Subreddit,
    User,
    WikiPage,
    ModeratedSubreddit,
)


class RedditSanitiser:
    """
    A class to sanitise and parse Reddit API response data, converting it into a
    SimpleNamespace format for easier attribute-based access.
    """

    @staticmethod
    def get_after(response: t.Dict) -> t.Union[str, None]:
        if (
            isinstance(response, dict)
            and isinstance(response.get("data"), dict)
            and isinstance(response.get("data").get("after"), (str, None))
        ):
            return response.get("data").get("after")

        return None

    @staticmethod
    def comment(response: dict) -> t.Optional[Comment]:
        """
        Sanitises and converts a single Reddit comment response to a SimpleNamespace.

        :param response: The dictionary representing the comment.
        :return: A SimpleNamespace object for the comment, or None if invalid.
        """
        if (
            isinstance(response, dict)
            and response.get("kind") == "t1"
            and isinstance(response.get("data"), dict)
        ):
            return Comment(**response["data"])

        return None

    def comments(
        self, response: t.Union[t.List[t.Dict], t.Dict]
    ) -> t.Optional[t.List[Comment]]:
        """
        Sanitises and converts multiple Reddit comments to a list of SimpleNamespace objects.

        :param response: Either a dict with 'data > children', or a list of comment dicts.
        :return: A list of SimpleNamespace objects representing comments.
        """
        # Case 1: Raw Reddit listing response (dict with children)
        if isinstance(response, dict):
            data = response.get("data")
            if isinstance(data, dict):
                children = data.get("children")
                if isinstance(children, list):
                    sane_comments: list[Comment] = []

                    for child in children:
                        comment = self.comment(child)
                        if comment is not None:
                            sane_comments.append(comment)

                    return sane_comments if sane_comments else None

        # Case 2: A pre-extracted list of comment dicts (e.g., from saved data)
        elif isinstance(response, list):
            sane_comments: list[Comment] = []

            for raw_comment in response:
                comment = self.comment(raw_comment)
                if comment is not None:
                    sane_comments.append(comment)

            return sane_comments if sane_comments else None

        return None

    @staticmethod
    def post(response: t.List[t.Dict]) -> t.Optional[Post]:
        """
        Sanitises and converts a single post response (from e.g. comments endpoint) to a SimpleNamespace.

        :param response: A list of two dicts, first containing post data.
        :return: A SimpleNamespace object representing the post, or None if invalid.
        """
        if (
            isinstance(response, list)
            and len(response) >= 1
            and isinstance(response[0], dict)
        ):
            data = response[0].get("data")
            if isinstance(data, dict):
                children = data.get("children")
                if (
                    isinstance(children, list)
                    and len(children) > 0
                    and isinstance(children[0], dict)
                    and children[0].get("kind") == "t3"
                    and isinstance(children[0].get("data"), dict)
                ):
                    return Post(**children[0]["data"])

        return None

    @staticmethod
    def posts(response: t.Dict) -> t.Optional[t.List[Post]]:
        """
        Sanitises and converts multiple post results to SimpleNamespace objects.

        :param response: A dictionary containing post search results.
        :return: A list of SimpleNamespace objects representing posts, or None if invalid.
        """
        data = response.get("data")
        if not isinstance(data, dict):
            return None

        children = data.get("children")
        if not isinstance(children, list):
            return None

        sane_children: list[Post] = []

        for child in children:
            if (
                isinstance(child, dict)
                and child.get("kind") == "t3"
                and isinstance(child.get("data"), dict)
            ):
                sane_children.append(Post(**child["data"]))

        return sane_children if sane_children else None

    @staticmethod
    def subreddit(response: t.Dict) -> t.Optional[Subreddit]:
        """
        Sanitises and converts a single subreddit response to a SimpleNamespace object.

        :param response: A dictionary containing a single subreddit.
        :return: A SimpleNamespace object or None if invalid.
        """
        if (
            isinstance(response, dict)
            and response.get("kind") == "t5"
            and isinstance(response.get("data"), dict)
        ):
            return Subreddit(**response["data"])

        return None

    def subreddits(
        self, response: t.Dict
    ) -> t.Optional[t.List[t.Union[Subreddit, ModeratedSubreddit]]]:
        """
        Sanitises and converts multiple subreddit responses to a list of SimpleNamespace objects.

        :param response: A dictionary containing multiple subreddits.
        :return: A list of SimpleNamespace objects or None if invalid.
        """
        data = response.get("data")
        kind = response.get("kind")

        sane_children: list[t.Union[Subreddit, ModeratedSubreddit]] = []
        if kind == "ModeratedList":
            return [ModeratedSubreddit(**child) for child in data]

        children = data.get("children")
        if not isinstance(data, dict):
            return None

        if not isinstance(children, list):
            return None

        for child in children:
            subreddit = self.subreddit(child)
            if subreddit is not None:
                sane_children.append(subreddit)

        return sane_children if sane_children else None

    @staticmethod
    def user(response: t.Dict) -> t.Union[User, Subreddit, None]:
        """
        Sanitises and converts a single Reddit user response to a SimpleNamespace object.
        """
        if (
            isinstance(response, dict)
            and response.get("kind") == "t2"
            and isinstance(response.get("data"), dict)
        ):
            return User(**response["data"])
        elif (
            isinstance(response, dict)
            and response.get("kind")
            == "t5"  # Edge-case only applies to users (top, new, all)... Reddit data is a damn mess!
            and isinstance(response.get("data"), dict)
        ) and response.get("data", {}).get("subreddit_type") == "user":
            return Subreddit(**response["data"])

        return None

    def users(self, response: t.Dict) -> t.Optional[t.List[User]]:
        """
        Sanitises and converts a list of Reddit user search results to SimpleNamespace objects.
        """
        data = response.get("data")
        if not isinstance(data, dict):
            return None

        children = data.get("children")
        if not isinstance(children, list):
            return None

        sane_users: t.List[User] = []

        for child in children:
            user = self.user(child)
            if user is not None:
                sane_users.append(user)

        return sane_users if sane_users else None

    @staticmethod
    def wiki_page(response: t.Dict) -> t.Union[WikiPage, None]:
        """
        Converts a single wiki page response to a SimpleNamespace object.

        :param response: A dictionary containing wiki page data.
        :type response: Dict
        :return: A SimpleNamespace object for the wiki page data.
        :rtype: SimpleNamespace
        """
        if "data" in response:
            return WikiPage(**response.get("data"))

        return None


# -------------------------------- END ----------------------------------------- #
