import os
import typing as t

from dotenv import load_dotenv
from rich.prompt import Prompt

from .io_handlers import FileHandler
from ..riches import rich_colours
from ..riches.rich_logging import console


class AuthHandler:
    ENV_CLIENT_ID = "REDDIT_CLIENT_ID"
    ENV_CLIENT_SECRET = "REDDIT_CLIENT_SECRET"
    ENV_FILE = os.path.join(FileHandler.AUTH_DIR, ".env")

    @classmethod
    def read(cls) -> t.Dict[str, str]:
        FileHandler.pathfinder(directories=[FileHandler.AUTH_DIR])

        if os.path.exists(cls.ENV_FILE):
            console.print(
                f"{rich_colours.BOLD_GREEN}✔{rich_colours.BOLD_GREEN_RESET} Found .env file at {cls.ENV_FILE}, attempting to load."
            )
            load_dotenv(dotenv_path=cls.ENV_FILE)
        else:
            console.log(
                f"{rich_colours.BOLD_YELLOW}⚠{rich_colours.BOLD_YELLOW_RESET} .env file not found at {cls.ENV_FILE}. Triggering credential prompt."
            )
            return cls.write()

        client_id = os.getenv(cls.ENV_CLIENT_ID)
        client_secret = os.getenv(cls.ENV_CLIENT_SECRET)

        if client_id and client_secret:
            console.print(
                f"{rich_colours.BOLD_BLUE}＊{rich_colours.BOLD_BLUE_RESET} Successfully loaded credentials from environment."
            )
            return {"client_id": client_id, "client_secret": client_secret}
        else:
            console.log(
                f"{rich_colours.BOLD_YELLOW}⚠{rich_colours.BOLD_YELLOW_RESET} Credentials missing or incomplete in .env file. Prompting for new input."
            )
            return cls.write()

    @classmethod
    def write(
        cls, client_id: t.Optional[str] = None, client_secret: t.Optional[str] = None
    ) -> t.Dict[str, str]:
        console.print("Prompting for Reddit API credentials.")

        client_id = client_id or Prompt.ask("Enter your Reddit API Client ID")
        client_secret = client_secret or Prompt.ask(
            "Enter your Reddit API Client Secret"
        )

        FileHandler.pathfinder(directories=[FileHandler.AUTH_DIR])

        try:
            with open(cls.ENV_FILE, "w") as env_file:
                env_file.write(f"{cls.ENV_CLIENT_ID}={client_id}\n")
                env_file.write(f"{cls.ENV_CLIENT_SECRET}={client_secret}\n")
            console.print(
                f"{rich_colours.BOLD_GREEN}✔{rich_colours.BOLD_GREEN_RESET} Credentials written to .env file at {cls.ENV_FILE}."
            )
        except Exception as e:
            console.log(
                f"{rich_colours.BOLD_RED}⚠{rich_colours.BOLD_RED_RESET} Failed to write credentials to {cls.ENV_FILE}: {e}"
            )
            raise

        os.environ[cls.ENV_CLIENT_ID] = client_id
        os.environ[cls.ENV_CLIENT_SECRET] = client_secret

        console.print(
            f"{rich_colours.GREEN}✔{rich_colours.GREEN_RESET} Credentials added to runtime environment."
        )

        return {"client_id": client_id, "client_secret": client_secret}
