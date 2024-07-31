class Version:
    """
    Represents Knew Karma's version in a structured format, providing access
    to the major, minor, and patch components, as well as composite representations
    like the full version string and the release string.

    Attributes:
        major (str): The major version number, indicating major changes and milestones.
        minor (str): The minor version number, representing minor improvements and significant fixes.
        patch (str): The patch version number, typically used for small fixes and updates.
        full (str): A composite string representing the full version, combining major, minor, and patch.
        release (str): A string representing the release version, combining only the major and minor numbers.
    """

    major: str = "5"
    minor: str = "4"
    patch: str = "0"
    full: str = f"{major}.{minor}.{patch}"
    release: str = f"{major}.{minor}"
