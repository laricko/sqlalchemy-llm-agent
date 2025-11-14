from typing import Sequence

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .config import SqlalchemyAgentConfig
from .tools import create_tools


class Result(BaseModel):
    rows_as_list_of_dict: list[dict]


class SqlalchemyAgent:
    def __init__(self, config: SqlalchemyAgentConfig):
        self.config = config

        self.model = ChatOpenAI(
            model="gpt-5",
            temperature=0,
            timeout=30,
            api_key=config.api_key
        )
        all_tables = self.config.inspector.get_table_names()
        allowed_tables = "all" if self.config.tables[0] == "*" else ", ".join(self.config.tables)

        system_prompt = f"""You are making sql queries for user.
You allowed only make safe queries, no inserts or updates.
You have access to {allowed_tables} tables from these tables {all_tables}.
Do not touch other tables if you don't have access to it.
        """
        tools = create_tools(self.config)
        self.agent = create_agent(
            self.model,
            tools,
            system_prompt=system_prompt,
            response_format=Result
        )

    def query(self, query: str) -> Sequence[dict]:
        result = self.agent.invoke(
            {"messages": [{"role": "user", "content": query}]}
        )
        return result["structured_response"].rows_as_list_of_dict
