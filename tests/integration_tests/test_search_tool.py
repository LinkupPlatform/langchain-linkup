import os
from typing import Any, Optional, Type

from dotenv import load_dotenv
from langchain_tests.integration_tests import ToolsIntegrationTests

from langchain_linkup import LinkupSearchTool


class TestLinkupSearchToolIntegration(ToolsIntegrationTests):
    @property
    def tool_constructor(self) -> Type[LinkupSearchTool]:
        return LinkupSearchTool

    @property
    def tool_constructor_params(self) -> dict[str, Any]:
        # Due to the way the tests are set up (with properties), we can't use the `linkup_api_key`
        # fixture
        load_dotenv()  # Load environment variables from .env file if it exists
        linkup_api_key: Optional[str] = os.environ.get("LINKUP_API_KEY")
        if linkup_api_key is None:
            raise ValueError("LINKUP_API_KEY environment variable is not set.")
        return dict(
            depth="standard",
            output_type="searchResults",
            api_key=linkup_api_key,
        )

    @property
    def tool_invoke_params_example(self) -> dict[str, Any]:
        return dict(
            query="What's the weather like in Paris, London and Berlin?",
        )
