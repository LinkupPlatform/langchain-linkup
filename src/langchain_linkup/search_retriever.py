from typing import Literal, Optional, cast

from langchain_core.callbacks import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from linkup import LinkupClient, LinkupSearchResults, LinkupSearchTextResult


class LinkupSearchRetriever(BaseRetriever):
    """LinkupSearchRetriever retriever.

    The LinkupSearchRetriever uses the Linkup API search entrypoint, making possible to retrieve
    documents from the Linkup API sources, that is the web and the Linkup Premium Partner sources,
    using natural language.

    Setup:
        Install ``langchain_linkup`` and set environment variable ``LINKUP_API_KEY``.

        .. code-block:: bash

            pip install -U langchain_linkup
            export LINKUP_API_KEY="your-api-key"

    Key init args:
        depth: Literal["standard", "deep"]
            The depth of the Linkup search. Can be either "standard", for a straighforward and fast
            search, or "deep" for a more powerful agentic workflow.
        linkup_api_key: Optional[str] = None
            The API key for the Linkup API. If None (the default), the API key will be read from
            the environment variable `LINKUP_API_KEY`.


    Instantiate:
        .. code-block:: python

            from langchain_linkup import LinkupSearchRetriever

            retriever = LinkupSearchRetriever(
                depth="deep",  # "standard" or "deep"
                linkup_api_key=None,
            )

    Usage:
        .. code-block:: python

            query = "Who won the latest US presidential elections?"

            retriever.invoke(query)

        .. code-block:: python

            [Document(metadata={'name': 'US presidential election results 2024: Harris vs. Trump | Live maps ...', 'url': 'https://www.reuters.com/graphics/USA-ELECTION/R
            ESULTS/zjpqnemxwvx/'}, page_content='Updated results from the 2024 election for the US president. Reuters live coverage of the 2024 US President, Senate, Hous
            e and state governors races.'), Document(metadata={'name': 'Election 2024: Presidential results - CNN', 'url': 'https://www.cnn.com/election/2024/results/pres
            ident'}, page_content='View maps and real-time results for the 2024 US presidential election matchup between former President Donald Trump and Vice President
            Kamala Harris. For more ...'), Document(metadata={'name': 'Presidential Election 2024 Live Results: Donald Trump wins - NBC News', 'url': 'https://www.nbcnews
            .com/politics/2024-elections/president-results'}, page_content='View live election results from the 2024 presidential race as Kamala Harris and Donald Trump f
            ace off. See the map of votes by state as results are tallied.'), Document(metadata={'name': '2024 President Election - Live Results | RealClearPolitics', 'ur
            l': 'https://www.realclearpolitics.com/elections/live_results/2024/president/'}, page_content='Latest Election 2024 Results • President • United States • Tues
            day November 3rd • Presidential Election Details'), Document(metadata={'name': 'US Presidential Election Results 2024 - BBC News', 'url': 'https://www.bbc.com
            /news/election/2024/us/results'}, page_content='Kamala Harris of the Democrat party has 74,498,303 votes (48.3%) Donald Trump of the Republican party has 76,9
            89,499 votes (49.9%) This map of the US states was filled in as presidential results ...'), Document(metadata={'name': '2024 US Presidential Election Results:
             Live Map - Bloomberg.com', 'url': 'https://www.bloomberg.com/graphics/2024-us-election-results/'}, page_content='US Presidential Election Results November 5,
             2024. Bloomberg News is reporting live election results in the presidential race between Democratic Vice President Kamala Harris and her Republican ...'), Do
            cument(metadata={'name': 'Presidential Election Results 2024: Electoral Votes & Map by State ...', 'url': 'https://www.politico.com/2024-election/results/pres
            ident/'}, page_content='Live 2024 Presidential election results, maps and electoral votes by state. POLITICO’s real-time coverage of 2024 races for President,
             Senate, House and Governor.'), Document(metadata={'name': '2024 U.S. Election: Live Results and Maps - USA TODAY', 'url': 'https://www.usatoday.com/elections
            /results/2024-11-05'}, page_content='See who is winning races in the Nov. 5, 2024 U.S. Election with real-time results and state-by-state maps.'), Document(me
            tadata={'name': 'US Presidential Election Results 2024 - BBC News', 'url': 'https://www.bbc.co.uk/news/election/2024/us/results'}, page_content='Follow the 20
            24 US presidential election results as they come in with BBC News. Find out if Trump or Harris is ahead as well as detailed state-by-state results.'), Documen
            t(metadata={'name': '2024 US Presidential Election Results: Live Map - ABC News', 'url': 'https://abcnews.go.com/Elections/2024-us-presidential-election-resul
            ts-live-map/'}, page_content='View live updates on electoral votes by state for presidential candidates Joe Biden and Donald Trump on ABC News. Senate, House,
             and Governor Election results also available at ABCNews.com')]

    Use within a chain:
        .. code-block:: python

            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_core.runnables import RunnablePassthrough
            from langchain_openai import ChatOpenAI

            prompt = ChatPromptTemplate.from_template(
                \"\"\"Answer the question based only on the context provided.

            Context: {context}

            Question: {question}\"\"\"
            )

            llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

            def format_docs(docs):
                return "\n\n".join(doc.page_content for doc in docs)

            chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | llm
                | StrOutputParser()
            )

            chain.invoke("Who won the latest US presidential elections?")

        .. code-block:: python

            'Donald Trump won the latest US presidential elections.'

    """  # noqa: E501

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
            include_images=False,
        )

        return [
            Document(
                page_content=cast(LinkupSearchTextResult, result).content,
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
            include_images=False,
        )

        return [
            Document(
                page_content=cast(LinkupSearchTextResult, result).content,
                metadata=dict(
                    name=result.name,
                    url=result.url,
                ),
            )
            for result in search_results.results
        ]
