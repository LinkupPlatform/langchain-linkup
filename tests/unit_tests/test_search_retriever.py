import pytest
from httpx import Response
from langchain_core.documents import Document
from pytest_mock import MockerFixture

from langchain_linkup import LinkupSearchRetriever

# NOTE: there is no retriever integration in langchain-tests to this date (version 0.3.4), so we
# need to implement tests manually


def test_get_relevant_document(mocker: MockerFixture, linkup_api_key: str) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=b"""
              {
                "results": [
                  {
                    "type": "text",
                    "name": "foo",
                    "url": "http://foo",
                    "content": "foo"
                  }
                ]
              }
            """,
        ),
    )

    retriever = LinkupSearchRetriever(linkup_api_key=linkup_api_key, depth="standard")
    documents: list[Document] = retriever.invoke(input="This is a query")

    assert len(documents) == 1
    assert documents[0].metadata["name"] == "foo"
    assert documents[0].metadata["url"] == "http://foo"
    assert documents[0].page_content == "foo"


@pytest.mark.asyncio
async def test_aget_relevant_documents(mocker: MockerFixture, linkup_api_key: str) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=b"""
              {
                "results": [
                  {
                    "type": "text",
                    "name": "foo",
                    "url": "http://foo",
                    "content": "foo"
                  }
                ]
              }
            """,
        ),
    )

    retriever = LinkupSearchRetriever(linkup_api_key=linkup_api_key, depth="standard")
    documents: list[Document] = await retriever.ainvoke(input="This is a query")

    assert len(documents) == 1
    assert documents[0].metadata["name"] == "foo"
    assert documents[0].metadata["url"] == "http://foo"
    assert documents[0].page_content == "foo"
