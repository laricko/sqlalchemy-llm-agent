from typing import Sequence

from langchain.tools import tool
from sqlalchemy import text

from .config import SqlalchemyAgentConfig
from .errors import UnsupportedTable


def create_tools(config: SqlalchemyAgentConfig):
    """
    Factory function to create LangChain tools bound to a specific config.

    Args:
        config (SqlalchemyAgentConfig): Configuration object containing the inspector
            and allowed table list.

    Returns:
        list: A list of LangChain tools ready to be used with agents.
    """

    @tool
    def inspect_tables(tables: Sequence[str]) -> dict:
        """
        Inspect columns for the given tables, validating access against the agent config.

        This function uses the agent's `SqlalchemyAgentConfig` to determine which tables
        are allowed to be inspected. If the config restricts tables (i.e. `config.tables[0] != "*"`),
        any table not listed in `config.tables` will cause an `UnsupportedTable` exception.

        Args:
            tables (Sequence[str]): Sequence of table names to inspect.

        Raises:
            UnsupportedTable: If any requested table is not permitted by `config.tables`.

        Returns:
            dict: A mapping from table name (as provided in `tables`) to the list of
                column metadata returned by `config.inspector.get_columns(table)`.
        """
        if config.tables[0] != "*":
            allowed_tables = {table.lower() for table in config.tables}
            for table in tables:
                if table.lower() not in allowed_tables:
                    raise UnsupportedTable

        res = {}
        for table in tables:
            res[table] = config.inspector.get_columns(table)

        return res

    @tool
    def execute_query(query: str) -> Sequence[dict]:
        """
        Execute a SQL query and return the resulting rows as a sequence of dictionaries.

        Args:
            query (str): The SQL query string to execute.

        Returns:
            Sequence[dict]: A sequence of row dictionaries, where each dictionary maps
                column names to their values.

        Example:
            >>> execute_query("SELECT id, name FROM users")
            [{"id": 1, "name": "larry", "email": "lari@lari.ru", "password": "..."}]
        """
        with config.engine.connect() as conn:
            result = conn.execute(text(query))
            rows = result.fetchall()

        return [dict(row._mapping) for row in rows]

    return [inspect_tables, execute_query]
