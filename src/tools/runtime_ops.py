import os
import subprocess
import typing as t
from logging import Logger

import requests
from rich.status import Status

from knewkarma.core.client import USER_AGENT
from knewkarma.meta.version import Version
from . import colours

__all__ = ["RuntimeOps"]


class RuntimeOps:
    ENDPOINTS = {
        "status": "https://www.redditstatus.com/api/v2/status.json",
        "components": "https://www.redditstatus.com/api/v2/components.json",
        "releases": "https://api.github.com/repos/knewkarma-io/knewkarma/releases/latest",
    }

    def __init__(self, package_name: str, version_cls: t.Type[Version]):
        self.package_name = package_name
        self.version_cls = version_cls

    @staticmethod
    def send_request(
        url: str,
        session: requests.Session,
    ) -> t.Union[t.Dict, t.List, str, None]:
        with session.get(
            url=url,
            headers={"User-Agent": USER_AGENT},
        ) as response:
            return response.json()

    @classmethod
    def clear_screen(cls):
        subprocess.run(["cls" if os.name == "nt" else "clear"])

    def infra_status(
        self,
        session: requests.Session,
        logger: t.Optional[Logger] = None,
        status: t.Optional[Status] = None,
    ) -> t.Union[t.List[t.Dict], None]:

        if isinstance(status, Status):
            status.update(f"Checking server status...")

        status_response: dict = self.send_request(
            url=self.ENDPOINTS["status"], session=session
        )

        indicator = status_response.get("status").get("indicator")
        description = status_response.get("status").get("description")
        if description:
            if indicator == "none":
                description = (
                    f"{colours.BOLD_GREEN}✔{colours.BOLD_GREEN_RESET} {description}"
                )
                (
                    logger.info(description)
                    if isinstance(logger, Logger)
                    else print(description.strip("[,]./,bold,green"))
                )
            else:
                status_message = f"{colours.BOLD_YELLOW}✘{colours.BOLD_YELLOW_RESET} {description} ({colours.YELLOW}{indicator}{colours.YELLOW_RESET})"
                (
                    logger.warning(status_message)
                    if isinstance(logger, Logger)
                    else print(status_message.strip("[,],/,bold,yellow"))
                )

                if isinstance(status, Status):
                    status.update("Getting status components...")

                status_components: t.Dict = self.send_request(
                    url=self.ENDPOINTS["components"],
                    session=session,
                )

                if isinstance(status_components, t.Dict):
                    components: t.List[t.Dict] = status_components.get("components")

                    return components
        return None

    def check_updates(
        self,
        session: requests.Session,
        status: t.Optional[Status] = None,
    ):
        from .log_config import logger

        if isinstance(status, Status):
            status.update("Checking for updates")

        # Make a GET request to GitHub to get the project's latest release.
        response = self.send_request(
            url=self.ENDPOINTS["releases"],
            session=session,
        )

        if response.get("tag_name"):
            remote_version_str = response.get("tag_name")

            # Splitting the version strings into components
            local_version_parts = [
                self.version_cls.major[0],
                self.version_cls.minor[0],
                self.version_cls.patch[0],
            ]
            remote_version_parts: t.List = remote_version_str.split(".")

            local_major: int = local_version_parts[0]
            local_minor: int = local_version_parts[1]
            local_patch: int = local_version_parts[2]

            remote_major = int(remote_version_parts[0])
            remote_minor = int(remote_version_parts[1])
            remote_patch = int(remote_version_parts[2])

            update_level = ""

            # Check for differences in version parts
            if remote_major != local_major:
                update_level = f"{colours.BOLD_RED}{self.version_cls.major[1]}{colours.BOLD_RED_RESET}"

            elif remote_minor != local_minor:
                update_level = f"{colours.BOLD_YELLOW}{self.version_cls.minor[1]}{colours.BOLD_YELLOW_RESET}"

            elif remote_patch != local_patch:
                update_level = f"{colours.BOLD_GREEN}{self.version_cls.patch[1]}{colours.BOLD_GREEN_RESET}"

            if update_level:
                logger.info(
                    f"🔄 {update_level} update is available [{colours.CYAN}{remote_version_str}{colours.CYAN_RESET}]"
                )

    @staticmethod
    def is_docker_container() -> bool:
        return os.environ.get("IS_DOCKER_CONTAINER") == "1"

    @staticmethod
    def is_snap_package() -> bool:
        return True if os.getenv("SNAP") else False

    def is_pypi_package(self) -> bool:
        try:
            __import__(name=self.package_name)
            return True
        except ImportError:
            return False


# -------------------------------- END ----------------------------------------- #
