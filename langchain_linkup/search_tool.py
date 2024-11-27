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
    """LinkupSearchTool tool.

    The LinkupSearchTool uses the Linkup API search entrypoint, making possible to perform
    search queries based on the Linkup API sources, that is the web and the Linkup Premium Partner
    sources, using natural language.

    Setup:
        Install ``langchain_linkup`` and set environment variable ``LINKUP_API_KEY``.

        .. code-block:: bash

            pip install -U langchain_linkup
            export LINKUP_API_KEY="your-api-key"

    Key init args:
        depth: Literal["standard", "deep"]
            The depth of the Linkup search. Can be either "standard", for a straighforward and fast
            search, or "deep" for a more powerful agentic workflow.
        output_type: Literal["searchResults", "sourcedAnswer", "structured"]
            The type of output which is expected from the Linkup API search: "searchResults" will
            output raw search results, "sourcedAnswer" will output the answer to the query and
            sources supporting it, and "structured" will base the output on the format provided in
            structured_output_schema.
        linkup_api_key: Optional[str] = None
            The API key for the Linkup API. If None (the default), the API key will be read from
            the environment variable `LINKUP_API_KEY`.
        structured_output_schema: Union[Type[BaseModel], str, None] = None
            If output_type is "structured", specify the schema of the output. Supported formats are
            a pydantic.BaseModel or a string representing a valid object JSON schema.

    Instantiate:
        .. code-block:: python

            from langchain_linkup import LinkupSearchTool

            tool = LinkupSearchTool(
                depth="deep",  # "standard" or "deep"
                output_type="sourcedAnswer",  # "searchResults", "sourcedAnswer" or "structured"
                linkup_api_key=None,
                structured_output_schema=None,
            )

    Usage:
        .. code-block:: python

            query = "Who won the latest US presidential elections?"

            tool.invoke(query)

        .. code-block:: python

            LinkupSourcedAnswer(answer='Donald Trump has won the 2024 presidential election by securing more than the 270 Electoral College votes needed for the presidency.', sources=[LinkupSource(name='NBC News', url='https://www.nbcnews.com/politics/2024-elections

    Use within an agent:
        .. code-block:: python

            from langchain_core.messages import HumanMessage
            from langchain_openai import ChatOpenAI
            from langgraph.prebuilt import create_react_agent

            model = ChatOpenAI(model="gpt-4o-mini")
            agent_executor = create_react_agent(model=model, tools=[tool])

            # Use the agent
            for chunk in agent_executor.stream(input=dict(messages=[HumanMessage(content=query)])):
                print(chunk)

        .. code-block:: python

            {'agent': {'messages': [AIMessage(content='', additional_kwargs={'tool_calls': [{'id': 'call_9q6zsP8hRyGHyOsf0FYLLYJQ', 'function': {'arguments': '{"query":"latest US presidential elections winner 2024"}', 'name': 'linkup'}, 'type': 'function'}], 'refusa
            l': None}, response_metadata={'token_usage': {'completion_tokens': 21, 'prompt_tokens': 85, 'total_tokens': 106, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'p
            rompt_tokens_details': {'audio_tokens': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_0705bf87c0', 'finish_reason': 'tool_calls', 'logprobs': None}, id='run-f61f4081-30e4-4130-8823-c161c25d22af-0', tool_calls=
            [{'name': 'linkup', 'args': {'query': 'latest US presidential elections winner 2024'}, 'id': 'call_9q6zsP8hRyGHyOsf0FYLLYJQ', 'type': 'tool_call'}], usage_metadata={'input_tokens': 85, 'output_tokens': 21, 'total_tokens': 106, 'input_token_details': {'au
            dio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}}
            {'tools': {'messages': [ToolMessage(content="answer='The latest results from the 2024 US presidential election indicate that Donald Trump has won against Kamala Harris. Trump secured approximately 49.9% of the vote, while Harris received around 48.3%.' s
            ources=[LinkupSource(name='Election 2024: Presidential results - CNN', url='https://www.cnn.com/election/2024/results/president', snippet='View maps and real-time results for the 2024 US presidential election matchup between former President Donald Trump
             and Vice President Kamala Harris.'), LinkupSource(name='NBC News - Presidential Election 2024 Live Results', url='https://www.nbcnews.com/politics/2024-elections/president-results', snippet='View live election results from the 2024 presidential race as
            Kamala Harris and Donald Trump face off.'), LinkupSource(name='Los Angeles Times - Trump wins 2024 U.S. presidential election, defeats Harris', url='https://www.latimes.com/politics/story/2024-11-06/trump-defeats-harris-47th-president-election-2024', sni
            ppet='2024 U.S. elections results See how the latest national vote counts for the President, Senate, Congress and Governors races change the balance of power.'), LinkupSource(name='The New York Times - Presidential Election Results: Trump Wins', url='htt
            ps://www.nytimes.com/interactive/2024/11/05/us/elections/results-president.html', snippet='Donald J. Trump has won the presidency, improving upon his 2020 performance in both red and blue states.'), LinkupSource(name='BBC News - US Presidential Election
            Results 2024', url='https://www.bbc.com/news/election/2024/us/results', snippet='Kamala Harris of the Democrat party has 74,498,303 votes (48.3%) Donald Trump of the Republican party has 76,989,499 votes (49.9%).')]", name='linkup', id='c9a53419-b6fe-486
            9-b57d-ac26083e5342', tool_call_id='call_9q6zsP8hRyGHyOsf0FYLLYJQ')]}}
            {'agent': {'messages': [AIMessage(content='The latest results from the 2024 US presidential election indicate that Donald Trump has won against Kamala Harris. Trump secured approximately 49.9% of the vote, while Harris received around 48.3%.\n\nHere are
            some sources for more details:\n- [CNN - Election 2024: Presidential results](https://www.cnn.com/election/2024/results/president)\n- [NBC News - Presidential Election 2024 Live Results](https://www.nbcnews.com/politics/2024-elections/president-results)\
            n- [Los Angeles Times - Trump wins 2024 U.S. presidential election, defeats Harris](https://www.latimes.com/politics/story/2024-11-06/trump-defeats-harris-47th-president-election-2024)\n- [The New York Times - Presidential Election Results: Trump Wins](h
            ttps://www.nytimes.com/interactive/2024/11/05/us/elections/results-president.html)\n- [BBC News - US Presidential Election Results 2024](https://www.bbc.com/news/election/2024/us/results)', additional_kwargs={'refusal': None}, response_metadata={'token_u
            sage': {'completion_tokens': 229, 'prompt_tokens': 519, 'total_tokens': 748, 'completion_tokens_details': {'accepted_prediction_tokens': 0, 'audio_tokens': 0, 'reasoning_tokens': 0, 'rejected_prediction_tokens': 0}, 'prompt_tokens_details': {'audio_token
            s': 0, 'cached_tokens': 0}}, 'model_name': 'gpt-4o-mini-2024-07-18', 'system_fingerprint': 'fp_3de1288069', 'finish_reason': 'stop', 'logprobs': None}, id='run-3c2962e2-bae7-47e3-92c5-b7725314254a-0', usage_metadata={'input_tokens': 519, 'output_tokens':
             229, 'total_tokens': 748, 'input_token_details': {'audio': 0, 'cache_read': 0}, 'output_token_details': {'audio': 0, 'reasoning': 0}})]}}
    """  # noqa: E501

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
