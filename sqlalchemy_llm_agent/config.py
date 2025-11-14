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
    api_key: str = Field(..., description="LLM API key (например, OpenAI API key).")
    model: str = Field(
        "gpt-5",
        description="Имя модели LLM, используемой агентом.",
    )
    tables: Sequence[str] = Field(
        ...,
        description=(
            "Список declarative-классов SQLAlchemy, по которым агент может "
            "строить SQL-запросы."
        ),
    )
    row_limit: int = Field(
        100,
        ge=1,
        description="Максимальное количество строк, которое агент может вернуть за один запрос.",
    )
    inspector: Inspector = Field(..., description="Объект inspector для таблиц")
    engine: Engine = Field(..., description="Engine объект чтобы делать запросы")
    model_config = ConfigDict(arbitrary_types_allowed=True)
