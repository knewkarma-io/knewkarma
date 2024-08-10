from .version import Version

__all__ = ["About"]


class About:
    """
    Container for about data for Knew Karma.

    Attributes:
          author (str): A markdown-formatted string of author name and url.
          copyright (str): Copyright notice for license and the author's details.
          summary (str): A brief description of Knew Karma as a tool for Reddit data analysis.
          description (str): A full description of Knew Karma as a CLI, and Library program for Reddit data analysis.
    """

    name: str = "Knew Karma"
    author: str = "Richard Mwewa"
    author_link: str = "https://gravatar.com/rly0nheart"
    copyright: str = f"{name} {Version.release} © {author}. All rights reserved."
    documentation: str = "https://knewkarma.readthedocs.io"
    summary: str = f"A Reddit data analysis toolkit — by {author} <{author_link}>"
    description: str = f"""
{name} (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a Command-Line Interface (CLI), and an
Application Programming Interface (API) to enable an easy integration in other Python Projects.



Refer to the documentation <{documentation}> for usage examples and integration guide.
"""


# -------------------------------- END ----------------------------------------- #
