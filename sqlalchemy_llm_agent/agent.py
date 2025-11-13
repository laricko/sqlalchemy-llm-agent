from typing import Sequence

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI

from .config import SqlalchemyAgentConfig
from .tools import execute_query, inspect_table


class SqlalchemyAgent:
    def __init__(self, config: SqlalchemyAgentConfig):
        self.config = config

        self.model = ChatOpenAI(
            model="gpt-5",
            temperature=0.1,
            max_tokens=1000,
            timeout=30,
            api_key=config.api_key
        )
        self.agent = create_agent(
            self.model,
            [inspect_table, execute_query]
        )

    def query(self, q: str) -> Sequence[dict]:
        pass
