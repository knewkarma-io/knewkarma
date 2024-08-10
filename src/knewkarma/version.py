class Version:
    """
    Represents Knew Karma's version in a structured format, providing access to the
    individual components of the version and composite representations.

    Attributes:
        major (tuple[int, str]): A tuple containing the major version number and its label.
            The major version indicates significant changes or milestones.
        minor (tuple[int, str]): A tuple containing the minor version number and its label.
            The minor version signifies incremental improvements or substantial fixes.
        patch (tuple[int, str]): A tuple containing the patch version number and its label.
            The patch version is used for small fixes and updates.
        full (str): A string that combines the major, minor, and patch version numbers
            to represent the full version (e.g., "6.1.2").
        release (str): A string that combines only the major and minor version numbers
            to represent the release version (e.g., "6.1").
    """

    major: tuple[int, str] = 6, "MAJOR"
    minor: tuple[int, str] = 1, "MINOR"
    patch: tuple[int, str] = 4, "PATCH"
    full: str = f"{major[0]}.{minor[0]}.{patch[0]}"
    release: str = f"{major[0]}.{minor[0]}"
