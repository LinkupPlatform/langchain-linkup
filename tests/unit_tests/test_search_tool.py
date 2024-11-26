from typing import Any, Type

from langchain_tests.unit_tests import ToolsUnitTests

from langchain_linkup import LinkupSearchTool


class TestLinkupSearchToolUnit(ToolsUnitTests):
    @property
    def tool_constructor(self) -> Type[LinkupSearchTool]:
        return LinkupSearchTool

    @property
    def tool_constructor_params(self) -> dict[str, Any]:
        return dict(
            depth="standard",
            output_type="searchResults",
        )

    @property
    def tool_invoke_params_example(self) -> dict[str, Any]:
        return dict(
            query="What's the weather like in Paris, London and Berlin?",
        )
