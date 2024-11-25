"""Simple agent example using the Linkup API and LangChain's agent framework.

This example is adapted from:
https://python.langchain.com/docs/tutorials/agents/

For this example to work, you need few additional dependencies, all specified in the
`requirements-dev.txt` file (you can run `pip install -r requirements-dev.txt` to install them).

Additionally, you need an API key for Linkup, and another one for OpenAI (for the base agent model),
which you can set manually as the LINKUP_API_KEY and OPENAI_API_KEY environment variables, or you
can duplicate the file `.env.example` in a `.env` file, fill the missing values, and the environment
variables will be automatically loaded from it, or you can replace the corresponding variables
below.
"""

from typing import Literal

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from langchain_linkup import LinkupTool

# You can change the RAG query and parameters here. If you prefer not to use environment variables
# you can fill them here.
query: str = "What's the weather like in Paris, London and Berlin?"
linkup_depth: Literal["standard", "deep"] = "standard"
linkup_api_key = None
openai_model: str = "gpt-4o-mini"
openai_api_key = None

load_dotenv()  # Load environment variables from .env file if there is one

model = ChatOpenAI(model=openai_model, api_key=openai_api_key)
search_tool = LinkupTool(depth="standard", output_type="searchResults")
agent_executor = create_react_agent(model=model, tools=[search_tool])

# Use the agent
for chunk in agent_executor.stream(input=dict(messages=[HumanMessage(content=query)])):
    print(chunk)
    print("----")
