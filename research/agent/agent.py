import os

from agno.agent import Agent
from agno.run import RunStatus
from agno.models.groq import Groq
from .tools import search_documents  #search_web
from .prompts import RESEARCH_AGENT_SYSTEM_PROMPT


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
                {"type": "browser_search"},
                search_documents
            ],

            instructions=RESEARCH_AGENT_SYSTEM_PROMPT,

            markdown=True,
        )

    def run(self, query: str):

        response = self.agent.run(
            query,
            user_id=str(self.user_id)
        )

        if response.status != RunStatus.completed:
            raise RuntimeError(
                response.content or "Research run failed."
            )

        return response.content