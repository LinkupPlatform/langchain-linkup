"""Simple RAG example using the Linkup API and LangChain's LCEL (LangChain Expression Language).

For this example to work, you need few additional dependencies, all specified in the
`requirements-dev.txt` file (you can run `pip install -r requirements-dev.txt` to install them).

Additionally, you need an API key for Linkup, and another one for OpenAI (for the final generation),
which you can set manually as the LINKUP_API_KEY and OPENAI_API_KEY environment variables, or you
can duplicate the file `.env.example` in a `.env` file, fill the missing values, and the environment
variables will be automatically loaded from it, or you can replace the corresponding variables
below.
"""

from typing import Any, Literal

from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable, RunnableLambda, RunnablePassthrough
from langchain_openai import ChatOpenAI

from langchain_linkup import LinkupRetriever

# You can change the RAG query and parameters here. If you prefer not to use environment variables
# you can fill them here.
query: str = "What is Linkup, the new French AI startup?"
linkup_depth: Literal["standard", "deep"] = "standard"
linkup_api_key = None
open_ai_model: str = "gpt-4o-mini"
openai_api_key = None

load_dotenv()  # Load environment variables from .env file if there is one


retriever = LinkupRetriever(linkup_api_key=linkup_api_key, depth=linkup_depth)


def format_retrieved_documents(docs: list[Document]) -> str:
    """Format the documents retrieved by the Linkup API as a text."""

    return "\n\n".join(
        [
            f"{document.metadata['name']} ({document.metadata['url']}):\n{document.page_content}"
            for document in docs
        ]
    )


def inspect_context(state: dict[str, Any]) -> dict[str, Any]:
    """Print the context retrieved by the retriever."""
    print(f"Context: {state['context']}\n\n")
    return state


generation_prompt_template = """Answer the question based only on the following context:

{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(generation_prompt_template)
model = ChatOpenAI(model=open_ai_model, api_key=openai_api_key)


chain: Runnable[Any, str] = (
    {"context": retriever | format_retrieved_documents, "question": RunnablePassthrough()}
    | RunnableLambda(inspect_context)
    | prompt
    | model
    | StrOutputParser()
)
response = chain.invoke(input=query)
print(f"Response: {response}")
