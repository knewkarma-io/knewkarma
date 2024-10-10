__all__ = ["Author", "Project"]


class Author:
    name: str = "Richard Mwewa"
    username: str = "rly0nheart"
    gravatar: str = f"https://gravatar.com/{username}"


class Project:
    name: str = "Knew Karma"
    package: str = "knewkarma"
    opencollective: str = f"https://opencollective.com/{package}"
    documentation: str = f"https://{package}.readthedocs.io"
    summary: str = f"A Reddit data analysis toolkit — by {Author.name}"
    description: str = f"""
{name} (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a Command-Line Interface (CLI), and an
Application Programming Interface (API) to enable an easy integration in other Python Projects.
"""


# -------------------------------- END ----------------------------------------- #
