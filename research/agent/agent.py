import os

from agno.agent import Agent
from agno.models.groq import Groq
from .tools import search_documents,web_search_tools


class ResearchAgent:

    def __init__(self,user_id):
        
        self.user_id=user_id

        self.agent = Agent(
            model=Groq(
                id=os.getenv(
                    "GROQ_MODEL",
                    "openai/gpt-oss-120b"
                )
            ),

            tools=[
                web_search_tools,
                search_documents
            ],

            instructions=[
                "You are an AI research assistant.",
                "Use browser search whenever the question requires "
                "current, recent, or external information.",
                "Use the information found through web search to "
                "produce an accurate and well-structured answer.",
            ],

            markdown=True,
        )

    def run(self, query: str):

        response = self.agent.run(
            query,
            user_id=str(self.user_id)
        )

        return response.content