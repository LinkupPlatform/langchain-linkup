from typing import Literal, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from linkup import LinkupClient, LinkupSearchResults


class LinkupSearchRetriever(BaseRetriever):
    """A retriever using the Linkup API search to retrieve documents using natural language.

    This retriever is a wrapper around the Linkup API search entrypoint, making possible to
    retrieve documents from the Linkup API sources, that is the web and the Linkup Premium Partner
    sources, using natural language.
    """

    depth: Literal["standard", "deep"]
    """The depth of the search. Can be either "standard", for a straighforward and fast search, or
    "deep" for a more powerful agentic workflow."""
    linkup_api_key: Optional[str] = None
    """The API key for the Linkup API. If None, the API key will be read from the environment
    variable `LINKUP_API_KEY`."""

    def _get_relevant_documents(
        self,
        query: str,
        *,
        run_manager: CallbackManagerForRetrieverRun,
    ) -> list[Document]:
        client = LinkupClient(api_key=self.linkup_api_key)
        search_results: LinkupSearchResults = client.search(
            query=query,
            depth=self.depth,
            output_type="searchResults",
        )

        return [
            Document(
                page_content=result.content,
                metadata=dict(
                    name=result.name,
                    url=result.url,
                ),
            )
            for result in search_results.results
        ]

    async def _aget_relevant_documents(
        self,
        query: str,
        *,
        run_manager: AsyncCallbackManagerForRetrieverRun,
    ) -> list[Document]:
        client = LinkupClient(api_key=self.linkup_api_key)
        search_results: LinkupSearchResults = await client.async_search(
            query=query,
            depth=self.depth,
            output_type="searchResults",
        )

        return [
            Document(
                page_content=result.content,
                metadata=dict(
                    name=result.name,
                    url=result.url,
                ),
            )
            for result in search_results.results
        ]
