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

    author: str = "Richard Mwewa"
    copyright: str = f"Knew Karma {Version.release} © {author}. All rights reserved."
    documentation: str = "https://knewkarma.readthedocs.io"

    summary: str = f"Knew Karma: A Reddit data analysis toolkit — by {author}"
    description: str = f"""
Knew Karma (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a Command-Line Interface (CLI), and an
Application Programming Interface (API) to enable an easy integration in other Python Projects.



Refer to the documentation ({documentation}) for usage examples and integration guide.
"""


# -------------------------------- END ----------------------------------------- #
