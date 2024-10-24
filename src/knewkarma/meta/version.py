class Version:
    major: tuple[int, str] = 7, "MAJOR"
    minor: tuple[int, str] = 1, "MINOR"
    patch: tuple[int, str] = 2, "PATCH"
    full_version: str = f"{major[0]}.{minor[0]}.{patch[0]}"
    release: str = f"{major[0]}.{minor[0]}"
