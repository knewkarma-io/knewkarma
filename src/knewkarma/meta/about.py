from knewkarma.meta.version import full as full_version

__all__ = [
    "author",
    "copyright",
    "description",
    "documentation",
    "project_name",
    "package_name",
    "sponsor",
    "summary",
]

package: str = "knewkarma"
name: str = "Knew Karma"
author: tuple[str, str, str] = (
    "Richard Mwewa",
    "rly0nheart",
    "https://gravatar.com/rly0nheart",
)
sponsor: str = f"https://opencollective.com/{name}"
copyright: str = f"{name} {full_version} © {author[0]}. All rights reserved."
documentation: str = "https://knewkarma.readthedocs.io"
summary: str = f"A Reddit data analysis toolkit — by {author[0]} <{author[2]}>"
description: str = f"""
{name} (/nuː ‘kɑːrmə/) is a Reddit data analysis toolkit designed to provide an extensive range of
functionalities for exploring and analysing Reddit data. It includes a Command-Line Interface (CLI), and an
Application Programming Interface (API) to enable an easy integration in other Python Projects.



📚 Refer to the documentation <{documentation}> for usage examples and integration guide.

❤️  Become a sponsor: <{sponsor}>
"""

# -------------------------------- END ----------------------------------------- #
