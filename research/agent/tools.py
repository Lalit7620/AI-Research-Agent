from agno.tools.duckduckgo import DuckDuckGoTools
from agno.run import RunContext
from documents.services.retriever import retrieve
from documents.services.context_builder import build_context


def search_documents(query:str, run_context:RunContext) ->str:
    """
    Search the user's uploaded documents for information relevant to the query.
    """

    user_id=int(run_context.user_id)
    
    retrieved_chunks = retrieve(
        query=query,
        user_id=user_id
    )

    context = build_context(
        retrieved_chunks
    )

    return context


duckduckgo_tools = DuckDuckGoTools(
    enable_search=True,
    enable_news=False,
    fixed_max_results=5
)


def search_web(query: str, max_results: int = 5) -> str:
    """
    Search the web for current or external information.

    Args:
        query: The search query.
        max_results: Maximum number of results to return.
    """

    return duckduckgo_tools.web_search(
        query=query,
        max_results=max_results
    )