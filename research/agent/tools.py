from agno.tools.websearch import WebSearchTools
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


web_search_tools=WebSearchTools(
    backend="duckduckgo",
    enable_search=True,
    enable_news=False,
    fixed_max_results=5
)