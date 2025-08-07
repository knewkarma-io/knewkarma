import os
import subprocess
import typing as t

import packaging.version
import requests
from karmakrate.everything.human_things import HumanThings
from knewkarma.core.client import USER_AGENT
from knewkarma.meta.about import Project
from knewkarma.meta.version import Version
from rich.status import Status

from ..riches import rich_colours
from ..riches.rich_logging import console

__all__ = ["RuntimeThings"]


class RuntimeThings:
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

    def check_status(
        self,
        session: requests.Session,
        status: Status,
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
                console.print(
                    f"{rich_colours.BOLD_GREEN}✔{rich_colours.BOLD_GREEN_RESET} {description}"
                )
            else:
                console.log(
                    f"{rich_colours.BOLD_YELLOW}✘{rich_colours.BOLD_YELLOW_RESET} {description} ({rich_colours.YELLOW}{indicator}{rich_colours.YELLOW_RESET})"
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
        status: Status,
    ):
        package_name = Project.package
        local_version = Version.full_version

        if isinstance(status, Status):
            status.update("Checking for updates...")

        response = self.send_request(
            url=f"https://pypi.org/pypi/{package_name}/json", session=session
        )

        latest_version = response.get("info").get("version")
        release_date = response.get("releases")[latest_version][0]["upload_time"]

        local_ver = packaging.version.parse(local_version)
        latest_ver = packaging.version.parse(latest_version)

        if local_ver < latest_ver:
            message = (
                f"🡅 Update available: v{local_version} → v{latest_version} "
                f"(released {HumanThings.human_datetime(inhuman_datetime=release_date)})"
            )
        elif local_ver > latest_ver:
            message = (
                f"You are running a newer version of {package_name} (v{local_version}) "
                f"than what's on PyPI (v{latest_version}, "
                f"released {HumanThings.human_datetime(inhuman_datetime=release_date, show_clock=False)}). "
                f"This may be an internal or unreleased build."
            )
        else:
            message = f"{rich_colours.BOLD_GREEN}✔{rich_colours.BOLD_GREEN_RESET} up to date (v{local_version})."

        console.print(message, justify="center" if local_ver > latest_ver else "left")

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
