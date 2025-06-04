__all__ = ["Author", "Project"]


class Author:
    name: str = "Ritchie Mwewa"
    username: str = "rly0nheart"
    gravatar: str = f"https://gravatar.com/{username}"


class Project:
    name: str = "Knew Karma"
    package: str = "knewkarma"
    open_collective: str = f"https://opencollective.com/{package}"
    documentation: str = f"https://{package}.readthedocs.io"
    summary: str = f"A zero-auth toolkit for Reddit data analysis — by {Author.name}"
    description: str = f"""
{name} (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a Command-Line Interface (CLI), and an
Application Programming Interface (API) to enable an easy integration in other Python Projects.
"""


# -------------------------------- END ----------------------------------------- #
