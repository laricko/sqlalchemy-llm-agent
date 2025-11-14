from typing import Any, Sequence, Type

from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import Inspector, Engine


class SqlalchemyAgentConfig(BaseModel):
    """
    Args:
        api_key (str): Your openai api key
        model (str, optional): By default is gpt-5 
        tables (list of str): You can leave ["*"] to declare that agent has access to every table 
        row_limit (int, optional): By default - 100
        inspector (sqlalchemy.inspect object) - required
    """
    api_key: str = Field(..., description="LLM API key (for example, an OpenAI API key).")
    model: str = Field(
        "gpt-5",
        description="Name of the LLM model used by the agent.",
    )
    tables: Sequence[str] = Field(
        ...,
        description=(
            "List of SQLAlchemy declarative classes that the agent can use "
            "to build SQL queries."
        ),
    )
    row_limit: int = Field(
        100,
        ge=1,
        description="Maximum number of rows the agent may return per request.",
    )
    inspector: Inspector = Field(..., description="Inspector object used to introspect tables.")
    engine: Engine = Field(..., description="Engine object used to execute queries.")
    model_config = ConfigDict(arbitrary_types_allowed=True)
