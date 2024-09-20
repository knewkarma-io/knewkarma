import pytest

from knewkarma.api import Api
from knewkarma.meta import about

api = Api(
    headers={
        "User-Agent": f"{about.name.replace(' ', '-')}/Test-1.0 "
        f"(PyTest {pytest.__version__}; +{about.documentation})"
    }
)

TEST_USERNAME: str = "AutoModerator"
TEST_SUBREDDIT_1: str = "AskScience"
TEST_SUBREDDIT_2: str = "AskReddit"
