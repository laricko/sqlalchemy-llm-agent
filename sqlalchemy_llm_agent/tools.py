from typing import Sequence

from langchain.tools import tool

from .config import SqlalchemyAgentConfig
from .errors import UnsupportedTable


@tool
def inspect_table(config: SqlalchemyAgentConfig, table: str) -> str:
    """Inspects a table, if table is not presented in user's config then throws an error, overwise returns a table schema"""
    if table not in config.tables:
        raise UnsupportedTable

    return "User table has such fields as id, name, email, password"


@tool
def execute_query(query: str) -> Sequence[dict]:
    """Executes a sql query to database, then returns a dict of fields and values"""
    return [{"id": 1, "name": "larry", "email": "lari@lari.ru", "password": "qweqweqwe"}]
