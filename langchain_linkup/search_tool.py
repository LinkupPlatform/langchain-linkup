from typing import Any, Literal, Optional, Type, Union

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from linkup import LinkupClient
from pydantic import BaseModel, Field


class LinkupSearchInput(BaseModel):
    query: str = Field(description="The query for the Linkup API search.")


class LinkupSearchTool(BaseTool):
    """A tool to query the Linkup API search in natural language.

    This tool is a wrapper around the Linkup API search entrypoint, making possible to perform
    search queries based on the Linkup API sources, that is the web and the Linkup Premium Partner
    sources, using natural language.
    """

    depth: Literal["standard", "deep"]
    """The depth of the search. Can be either "standard", for a straighforward and
    fast search, or "deep" for a more powerful agentic workflow."""
    output_type: Literal["searchResults", "sourcedAnswer", "structured"]
    """The type of output which is expected: "searchResults" will output raw
    search results, "sourcedAnswer" will output the answer to the query and sources
    supporting it, and "structured" will base the output on the format provided in
    structured_output_schema."""
    linkup_api_key: Optional[str] = None
    """The API key for the Linkup API. If None, the API key will be read from the environment
    variable `LINKUP_API_KEY`."""
    structured_output_schema: Union[Type[BaseModel], str, None] = None
    """If output_type is "structured", specify the schema of the
    output. Supported formats are a pydantic.BaseModel or a string representing a
    valid object JSON schema."""

    # Fields used by the agent to describe how to use the tool under the hood
    name: str = "linkup"
    description: str = (
        "A tool to perform search queries based on the Linkup API sources, that is the web and the "
        "Linkup Premium Partner sources, using natural language."
    )
    args_schema: Type[BaseModel] = LinkupSearchInput
    return_direct: bool = False

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> Any:
        client = LinkupClient(api_key=self.linkup_api_key)
        return client.search(
            query=query,
            depth=self.depth,
            output_type=self.output_type,
            structured_output_schema=self.structured_output_schema,
        )

    async def _arun(
        self,
        query: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
    ) -> Any:
        client = LinkupClient(api_key=self.linkup_api_key)
        return await client.async_search(
            query=query,
            depth=self.depth,
            output_type=self.output_type,
            structured_output_schema=self.structured_output_schema,
        )
