from typing import Literal, Optional

from langchain_core.callbacks import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from linkup import LinkupClient, LinkupSearchResults


class LinkupRetriever(BaseRetriever):
    """A retriever which using the Linkup API to retrieve documents.

    This retriever is a wrapper around the Linkup API, allowing you to search for documents from
    the Linkup API sources, that is the web and the Linkup Premium Partner sources.
    """

    linkup_api_key: Optional[str] = None
    """The API key for the Linkup API."""
    depth: Literal["standard", "deep"] = "standard"
    """The depth of the search. Can be either "standard" or "deep"."""

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
