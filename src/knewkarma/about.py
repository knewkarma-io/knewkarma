from .version import Version

__all__ = ["About"]


class About:
    """
    Container for metadata about Knew Karma.

    Attributes:
        package (str): The package name for Knew Karma.
        name (str): The full name of the project.
        author (tuple[str, str, str]): A tuple containing the author's name, username and URL to gravatar profile.
        copyright (str): Copyright notice including the project name, release version, and author's name.
        documentation (str): URL to the official documentation for Knew Karma.
        summary (str): A brief summary of the project, including the author's name and URL.
        description (str): A detailed description of Knew Karma, its purpose, and functionality, including
            links to further documentation and usage examples.
    """

    package: str = "knewkarma"
    name: str = "Knew Karma"
    author: tuple[str, str, str] = (
        "Richard Mwewa",
        "rly0nheart",
        "https://gravatar.com/rly0nheart",
    )
    sponsor: str = f"https://opencollective.com/{package}"
    copyright: str = f"{name} {Version.release} © {author[0]}. All rights reserved."
    documentation: str = "https://knewkarma.readthedocs.io"
    summary: str = f"A Reddit data analysis toolkit — by {author[0]} <{author[2]}>"
    description: str = f"""
{name} (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a Command-Line Interface (CLI), and an
Application Programming Interface (API) to enable an easy integration in other Python Projects.



🕮  Refer to the documentation <{documentation}> for usage examples and integration guide.

❤️  Become a sponsor <{sponsor}>
"""


# -------------------------------- END ----------------------------------------- #
