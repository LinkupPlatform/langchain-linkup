import pytest
from httpx import Response
from langchain_core.documents import Document
from pytest_mock import MockerFixture

from langchain_linkup import LinkupRetriever

# NOTE: there is no retriever integration in langchain-tests to this date (version 0.3.4), so we
# need to implement tests manually


def test_get_relevant_document(mocker: MockerFixture, linkup_api_key: str) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._request",
        return_value=Response(
            status_code=200,
            content=b'{"results":[{"name":"Paris-based Linkup raises \xe2\x82\xac3 million aiming '
            b'to revolutionise ethical ...","url":"https://www.eu-startups.com/2024/11/paris-'
            b"based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-"
            b'access-for-ai/","content":"Linkup, a French startup providing AI with fast, ethical '
            b"access to online content, has secured \xe2\x82\xac3 million supported by leading "
            b"investors, including Seedcamp, Axeleo Capital, MotierVentures, and a network of "
            b"prominent tech and media industry angels to further develop its sustainable "
            b"alternative to web scraping and address the challenges posed by AI-driven web "
            b'traffic."},{"name":"Linkup raises \xe2\x82\xac3 million to offer a new gateway to '
            b'the \xe2\x80\x9cInternet of AIs\xe2\x80\x9d","url":"https://seedcamp.com/views/'
            b'linkup-raises-e3-million-to-offer-a-new-gateway-to-the-internet-of-ais/","content":'
            b'"News Linkup raises \xe2\x82\xac3 million to offer a new gateway to the \xe2\x80\x9c'
            b"Internet of AIs\xe2\x80\x9d 18.11.2024 AI is fundamentally anging the nature of the "
            b"Internet and its traditional business models. Developing an ethical, sustainable and "
            b"efficient ecosystem for the web of AI agents is a priority. We are excited to "
            b"partner with Linkup, a French startup on a mission to build new pathways for AIs "
            b'to access ..."}]}',
        ),
    )

    retriever = LinkupRetriever(linkup_api_key=linkup_api_key, depth="standard")
    documents: list[Document] = retriever.invoke(input="What is Linkup, the new French AI startup?")

    assert len(documents) == 2
    assert (
        documents[0].metadata["name"]
        == "Paris-based Linkup raises €3 million aiming to revolutionise ethical ..."
    )
    assert (
        documents[0].metadata["url"]
        == "https://www.eu-startups.com/2024/11/paris-based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-for-ai/"
    )
    assert (
        documents[0].page_content
        == "Linkup, a French startup providing AI with fast, ethical access to online content, "
        "has secured €3 million supported by leading investors, including Seedcamp, Axeleo "
        "Capital, MotierVentures, and a network of prominent tech and media industry angels to "
        "further develop its sustainable alternative to web scraping and address the challenges "
        "posed by AI-driven web traffic."
    )


@pytest.mark.asyncio
async def test_aget_relevant_documents(mocker: MockerFixture, linkup_api_key: str) -> None:
    mocker.patch(
        "linkup.client.LinkupClient._async_request",
        return_value=Response(
            status_code=200,
            content=b'{"results":[{"name":"Paris-based Linkup raises \xe2\x82\xac3 million aiming '
            b'to revolutionise ethical ...","url":"https://www.eu-startups.com/2024/11/paris-'
            b"based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-"
            b'access-for-ai/","content":"Linkup, a French startup providing AI with fast, ethical '
            b"access to online content, has secured \xe2\x82\xac3 million supported by leading "
            b"investors, including Seedcamp, Axeleo Capital, MotierVentures, and a network of "
            b"prominent tech and media industry angels to further develop its sustainable "
            b"alternative to web scraping and address the challenges posed by AI-driven web "
            b'traffic."},{"name":"Linkup raises \xe2\x82\xac3 million to offer a new gateway to '
            b'the \xe2\x80\x9cInternet of AIs\xe2\x80\x9d","url":"https://seedcamp.com/views/'
            b'linkup-raises-e3-million-to-offer-a-new-gateway-to-the-internet-of-ais/","content":'
            b'"News Linkup raises \xe2\x82\xac3 million to offer a new gateway to the \xe2\x80\x9c'
            b"Internet of AIs\xe2\x80\x9d 18.11.2024 AI is fundamentally anging the nature of the "
            b"Internet and its traditional business models. Developing an ethical, sustainable and "
            b"efficient ecosystem for the web of AI agents is a priority. We are excited to "
            b"partner with Linkup, a French startup on a mission to build new pathways for AIs "
            b'to access ..."}]}',
        ),
    )

    retriever = LinkupRetriever(linkup_api_key=linkup_api_key, depth="standard")
    documents: list[Document] = await retriever.ainvoke(
        input="What is Linkup, the new French AI startup?"
    )

    assert len(documents) == 2
    assert (
        documents[0].metadata["name"]
        == "Paris-based Linkup raises €3 million aiming to revolutionise ethical ..."
    )
    assert (
        documents[0].metadata["url"]
        == "https://www.eu-startups.com/2024/11/paris-based-linkup-raises-e3-million-aiming-to-revolutionise-ethical-and-efficient-web-access-for-ai/"
    )
    assert (
        documents[0].page_content
        == "Linkup, a French startup providing AI with fast, ethical access to online content, "
        "has secured €3 million supported by leading investors, including Seedcamp, Axeleo "
        "Capital, MotierVentures, and a network of prominent tech and media industry angels to "
        "further develop its sustainable alternative to web scraping and address the challenges "
        "posed by AI-driven web traffic."
    )
