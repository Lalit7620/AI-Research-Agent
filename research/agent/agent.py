import os

from agno.agent import Agent
from agno.models.groq import Groq


class ResearchAgent:

    def __init__(self):

        self.agent = Agent(
            model=Groq(
                id=os.getenv(
                    "GROQ_MODEL",
                    "openai/gpt-oss-120b"
                )
            ),

            tools=[
                {
                    "type": "browser_search"
                }
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

        response = self.agent.run(query)

        return response.content