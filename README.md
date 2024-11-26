# ⚡ Langchain Linkup

[![PyPI version](https://badge.fury.io/py/langchain-linkup.svg)](https://pypi.org/project/langchain-linkup/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A [LangChain](https://www.langchain.com/) integration for the
[Linkup API](https://linkup-api.readme.io/reference/getting-started), allowing easy integration with
Linkup's services. 🔗

## 🌟 Features

- 🔗 **Simple LangChain components to cover all Linkup API use cases.**
- 🔍 **Supports both standard and deep search queries.**
- ⚡ **Supports synchronous and asynchronous requests.**
- 🔒 **Handles authentication and request management.**

## 📦 Installation

Simply install the LangChain integration using `pip`:

```bash
pip install langchain-linkup
```

## 🛠️ Usage

### Setting Up Your Environment

1. **🔑 Obtain an API Key:**

   Sign up on Linkup to get your API key.

2. **⚙️ Set-up the API Key:**

   Option 1: Export the `LINKUP_API_KEY` environment variable in your shell before using the Linkup
   LangChain component.

   ```bash
   export LINKUP_API_KEY='YOUR_LINKUP_API_KEY'
   ```

   Option 2: Set the `LINKUP_API_KEY` environment variable directly within Python, using for
   instance `os.environ` or [python-dotenv](https://github.com/theskumar/python-dotenv) with a
   `.env` file (`python-dotenv` needs to be installed separately in this case), before creating the
   Linkup LangChain component.

   ```python
   import os
   from langchain_linkup import LinkupSearchRetriever

   os.environ["LINKUP_API_KEY"] = "YOUR_LINKUP_API_KEY"
   # or dotenv.load_dotenv()
   retriever = LinkupSearchRetriever(...)
   ...
   ```

   Option 3: Pass the Linkup API key to the Linkup LangChain component when creating it.

   ```python
   from langchain_linkup import LinkupSearchRetriever

   retriever = LinkupSearchRetriever(api_key="YOUR_LINKUP_API_KEY", ...)
   ...
   ```

## 📋 Example

All search queries can be used with two very different modes:

- with `depth="standard"`, the search will be straightforward and fast, suited for relatively simple
  queries (e.g. "What's the weather in Paris today?")
- with `depth="deep"`, the search will use an agentic workflow, which makes it in general slower,
  but it will be able to solve more complex queries (e.g. "What is the company profile of LangChain
  accross the last few years, and how does it compare to its concurrents?")

### 🔍 Linkup Search Retriever

A retriever is a LangChain component which simply retrieves documents based on a query. It is
typically the first step of a RAG (Retrival Augmented Generation) pipeline. See
[this page](https://python.langchain.com/docs/concepts/retrievers/) for more information. The
`LinkupSearchRetriever` makes available the Linkup API search as a LangChain retriever.

```python
from langchain_linkup import LinkupSearchRetriever

# Initialize the LangChain component (API key can be read from the environment variable or passed as
# an argument)
retriever = LinkupSearchRetriever(
    depth="deep",  # "standard" or "deep"
)

# Perform a search query
documents = retriever.invoke(input="What is Linkup, the new French AI startup?")
print(documents)
```

### ⚒️ Linkup Search Tool

A tool is a LangChain component which enables agents to perform a specific task, like a web search.
Tools are designed to be called autonomously by the agent, and their output is fed back to the
agent, allowing them to perform some kind of reasoning based on the tool usage. See
[this page](https://python.langchain.com/docs/integrations/tools/) for more information. The
`LinkupSearchTool` makes available the Linkup API search as a LangChain tool.

```python
from langchain_linkup import LinkupSearchTool

# Initialize the LangChain component (API key can be read from the environment variable or passed as
# an argument)
tool = LinkupSearchTool(
    depth="deep",  # "standard" or "deep"
    output_type="searchResults",  # "searchResults", "sourcedAnswer" or "structured"
)

# Perform a search query
search_results = tool.invoke(input="What is Linkup, the new French AI startup?")
print(search_results)
```

### 📚 More Examples

See the `examples/` directory for more contextualized examples and documentation, for instance on
how to use the Linkup Search Retriever in a simple RAG pipeline.
