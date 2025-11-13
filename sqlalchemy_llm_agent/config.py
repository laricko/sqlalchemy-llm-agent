from typing import Any, Sequence, Type

from pydantic import BaseModel, Field


class SqlalchemyAgentConfig(BaseModel):
    api_key: str = Field(..., description="LLM API key (например, OpenAI API key).")
    model: str = Field(
        "gpt-5",
        description="Имя модели LLM, используемой агентом.",
    )
    tables: Sequence[Type[Any]] = Field(
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
