import json
import os


class Broker:
    """
    The Broker class holds methods used to re-restructure the API data in-order to get only the relevant information.
    """

    @staticmethod
    def structure_raw_data(api_data: dict, data_file: str) -> dict:
        """
        Structures API data based on a key mapping from a JSON file.

        :param api_data: Dictionary containing raw data from the API.
        :param data_file: Path to the JSON file that contains the key mapping.

        :returns: A Formatted JSON object with human-readable keys.
        """
        from . import CURRENT_FILE_DIRECTORY

        # Construct path to the mapping data file
        mapping_data_file = os.path.join(CURRENT_FILE_DIRECTORY, "data", data_file)

        # Load the mapping from the specified file
        with open(mapping_data_file, "r", encoding="utf-8") as file:
            mapping_data = json.load(file)

        # Initialize an empty dictionary to hold the formatted data
        formatted_data = {}

        # Map API data to human-readable format using the mapping
        for api_data_key, mapping_data_key in mapping_data.items():
            formatted_data[mapping_data_key] = api_data.get(api_data_key, "N/A")

        return formatted_data

    def user_data(self, raw_data: dict) -> tuple:
        """
        Re-structures raw user data from the API to the structure of the json files in the user directory.

        Data Files
        ----------
        - user/profile.json: Holds the structure for a user profile data.
        - user/subreddit.json: Holds the structure for a user subreddit data
        - user/verified.json: Holds the structure for a user's verified status.
        - user/snoovatar.json: (I don't even why 'snoovatar' is a word😂)
           Holds the structure for a user's snoovatar data.
        - user/karma.json: Holds the structure for a user's karma count.

        :param raw_data: Raw data from API.
        :returns: A tuple Re-formatted data
        """
        profile = self.structure_raw_data(
            api_data=raw_data, data_file="user/profile.json"
        )
        subreddit = self.structure_raw_data(
            api_data=raw_data.get("subreddit"), data_file="user/subreddit.json"
        )
        verification = self.structure_raw_data(
            api_data=raw_data, data_file="user/verified.json"
        )
        snoovatar = self.structure_raw_data(
            api_data=raw_data, data_file="user/snoovatar.json"
        )
        karma = self.structure_raw_data(api_data=raw_data, data_file="user/karma.json")

        return profile, subreddit, verification, snoovatar, karma

    def subreddit_data(self, raw_data: dict) -> tuple:
        """
        Re-structures raw subreddit data from the API to the structure of the json files in the subreddit directory.

        Data Files
        ----------
        - subreddit/profile.json: Holds the structure for a subreddit profile data.
        - subreddit/allows.json: Holds the structure for a subreddit's allowed content policies.
        - subreddit/banner.json: Holds the structure for a subreddit's banner data.
        - subreddit/header.json: Holds the structure for a subreddit's header data.
        - subreddit/flair.json: Holds the structure for a subreddit's flair data.

        :param raw_data: Raw data from API.
        :returns: A tuple of Re-formatted data
        """
        profile = self.structure_raw_data(
            api_data=raw_data, data_file="subreddit/profile.json"
        )
        allows = self.structure_raw_data(
            api_data=raw_data, data_file="subreddit/allows.json"
        )
        banner = self.structure_raw_data(
            api_data=raw_data, data_file="subreddit/banner.json"
        )
        header = self.structure_raw_data(
            api_data=raw_data, data_file="subreddit/header.json"
        )
        flairs = self.structure_raw_data(
            api_data=raw_data, data_file="subreddit/flairs.json"
        )
        return profile, allows, banner, header, flairs

    def post_data(self, raw_post: dict) -> dict:
        """
        Re-structures raw post data from the API to the structure of the json files in the post directory.

        Data Files
        ----------
        - post/profile.json: Holds the structure for a post's profile data.
        - post/award.json: Holds the structure for a post's awards. (not yet implemented)

        :param raw_post: Raw post data from API.
        :returns: A dictionary of Re-formatted post data,
          else a dictionary containing profile data only.
        """
        profile = self.structure_raw_data(
            api_data=raw_post, data_file="post/profile.json"
        )

        return profile

    def comment_data(self, raw_comment: dict) -> dict:
        """
        Re-structures raw comment data from the API to the structure of the JSON file in the shared directory.

        Data File
        ----------
        - shared/comment.json: Holds the structure for a comment's data.
        """
        comment_data = self.structure_raw_data(
            api_data=raw_comment, data_file="shared/comment.json"
        )
        return comment_data
