import typing as t
from types import SimpleNamespace

__all__ = ["RedditSanitiser"]


class RedditSanitiser:
    """
    A class to sanitise and parse Reddit API response data, converting it into a
    SimpleNamespace format for easier attribute-based access.
    """

    @classmethod
    def _dict_to_namespace_obj(
        cls, obj: t.Union[t.List[t.Dict], t.Dict]
    ) -> t.Union[t.List[SimpleNamespace], SimpleNamespace, t.List[t.Dict], t.Dict]:
        """
        Recursively converts dictionaries and lists of dictionaries into SimpleNamespace objects.

        :param obj: The object to convert, either a dictionary or a list of dictionaries.
        :type obj: Union[List[Dict], Dict]
        :return: A SimpleNamespace object or list of SimpleNamespace objects.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace, None]
        """
        if isinstance(obj, t.Dict):
            return SimpleNamespace(
                **{
                    key: cls._dict_to_namespace_obj(obj=value)
                    for key, value in obj.items()
                }
            )
        elif isinstance(obj, t.List):
            return [cls._dict_to_namespace_obj(obj=item) for item in obj]
        else:
            return obj

    @classmethod
    def comment(cls, response: t.Dict) -> t.Union[SimpleNamespace, None]:
        """
        Converts a single comment response to a SimpleNamespace object.

        :param response: The dictionary representing the comment.
        :type response: Dict
        :return: A SimpleNamespace object for the comment.
        :rtype: SimpleNamespace
        """
        if isinstance(response, t.Dict):
            return cls._dict_to_namespace_obj(obj=response)

        return None

    @classmethod
    def comments(
        cls, response: t.Union[t.List[t.Dict], t.Dict]
    ) -> t.Union[t.List[SimpleNamespace], SimpleNamespace, None]:
        """
        Converts a list of comments or a single comment to SimpleNamespace objects.

        :param response: A list of dictionaries, each representing a comment, or a single dictionary.
        :type response: Union[List[Dict], Dict]
        :return: A list of SimpleNamespace objects or a single SimpleNamespace object.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        if isinstance(response, t.List) and all(
            isinstance(comment, t.Dict) for comment in response
        ):
            return [cls.comment(response=raw_comment) for raw_comment in response]
        elif isinstance(response, t.Dict):
            return cls._dict_to_namespace_obj(obj=response.get("data", {}))

        return None

    @classmethod
    def post(cls, response: t.List[t.Dict]) -> t.Union[SimpleNamespace, None]:
        """
        Converts a single post response to a SimpleNamespace object.

        :param response: A list containing dictionaries with post data.
        :type response: List[Dict]
        :return: A SimpleNamespace object representing the post.
        :rtype: SimpleNamespace
        """
        if isinstance(response, t.List) and len(response) == 2:
            children = response[0].get("data", {}).get("children")
            return cls._dict_to_namespace_obj(obj=children[0])

        return None

    @classmethod
    def posts(
        cls, response: t.Dict
    ) -> t.Union[t.List[SimpleNamespace], SimpleNamespace, None]:
        """
        Converts post data to SimpleNamespace objects.

        :param response: A dictionary containing post data.
        :type response: Dict
        :return: A SimpleNamespace object or list of SimpleNamespace objects representing posts.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        data = response.get("data", {})
        if isinstance(data, t.Dict):
            return cls._dict_to_namespace_obj(obj=data)

        return None

    @classmethod
    def subreddit(cls, response: t.Dict) -> t.Union[SimpleNamespace, None]:
        """
        Converts a single subreddit response to a SimpleNamespace object.

        :param response: A dictionary containing subreddit data.
        :type response: Dict
        :return: A SimpleNamespace object for the subreddit data.
        :rtype: SimpleNamespace
        """
        if "data" in response:
            return cls._dict_to_namespace_obj(obj=response)

        return None

    @classmethod
    def subreddits(
        cls, response: t.Dict
    ) -> t.Union[t.List[SimpleNamespace], SimpleNamespace, None]:
        """
        Converts subreddit data to SimpleNamespace objects.

        :param response: A dictionary containing subreddit data.
        :type response: Dict
        :return: A SimpleNamespace object or list of SimpleNamespace objects for the subreddits.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        if "data" in response:
            return cls._dict_to_namespace_obj(obj=response.get("data", {}))

        return None

    @classmethod
    def user(cls, response: t.Dict) -> t.Union[SimpleNamespace, None]:
        """
        Converts a single user response to a SimpleNamespace object.

        :param response: A dictionary containing user data.
        :type response: Dict
        :return: A SimpleNamespace object for the user data.
        :rtype: SimpleNamespace
        """
        if "data" in response:
            return cls._dict_to_namespace_obj(obj=response)

        return None

    @classmethod
    def users(
        cls, response: t.Dict
    ) -> t.Union[t.List[SimpleNamespace], SimpleNamespace, None]:
        """
        Converts user data to SimpleNamespace objects.

        :param response: A dictionary containing user data.
        :type response: Dict
        :return: A SimpleNamespace object or list of SimpleNamespace objects for the users.
        :rtype: Union[List[SimpleNamespace], SimpleNamespace]
        """
        if "data" in response:
            return cls._dict_to_namespace_obj(obj=response.get("data", {}))

        return None

    @classmethod
    def wiki_page(cls, response: t.Dict) -> t.Union[SimpleNamespace, None]:
        """
        Converts a single wiki page response to a SimpleNamespace object.

        :param response: A dictionary containing wiki page data.
        :type response: Dict
        :return: A SimpleNamespace object for the wiki page data.
        :rtype: SimpleNamespace
        """
        if "data" in response:
            return cls._dict_to_namespace_obj(obj=response)

        return None


# -------------------------------- END ----------------------------------------- #
