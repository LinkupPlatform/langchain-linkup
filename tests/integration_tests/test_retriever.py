import pytest
from langchain_core.documents import Document

from langchain_linkup import LinkupRetriever

# NOTE: there is no retriever integration in langchain-tests to this date (version 0.3.4), so we
# need to implement tests manually


def test_get_relevant_document(linkup_api_key: str) -> None:
    retriever = LinkupRetriever(linkup_api_key=linkup_api_key, depth="standard")
    documents: list[Document] = retriever.invoke(input="What is Linkup, the new French AI startup?")

    assert isinstance(documents, list) and documents
    assert isinstance(documents[0], Document)
    assert isinstance(documents[0].metadata, dict) and documents[0].metadata
    assert isinstance(documents[0].metadata["name"], str) and documents[0].metadata["name"]
    assert isinstance(documents[0].metadata["url"], str) and documents[0].metadata["url"]
    assert isinstance(documents[0].page_content, str) and documents[0].page_content


@pytest.mark.asyncio
async def test_aget_relevant_documents(linkup_api_key: str) -> None:
    retriever = LinkupRetriever(linkup_api_key=linkup_api_key, depth="standard")
    documents: list[Document] = await retriever.ainvoke(
        input="What is Linkup, the new French AI startup?"
    )

    assert isinstance(documents, list) and documents
    assert isinstance(documents[0], Document)
    assert isinstance(documents[0].metadata, dict) and documents[0].metadata
    assert isinstance(documents[0].metadata["name"], str) and documents[0].metadata["name"]
    assert isinstance(documents[0].metadata["url"], str) and documents[0].metadata["url"]
    assert isinstance(documents[0].page_content, str) and documents[0].page_content
