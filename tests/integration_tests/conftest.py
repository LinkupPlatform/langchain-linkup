import os
from typing import Optional

import pytest
from dotenv import load_dotenv


@pytest.fixture(scope="session")
def linkup_api_key() -> str:
    load_dotenv()  # Load environment variables from .env file if it exists

    linkup_api_key: Optional[str] = os.environ.get("LINKUP_API_KEY")
    if linkup_api_key is None:
        raise ValueError("LINKUP_API_KEY environment variable is not set.")

    return linkup_api_key
