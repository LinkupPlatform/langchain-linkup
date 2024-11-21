import pytest


@pytest.fixture(scope="session")
def linkup_api_key() -> str:
    return "api-key"
