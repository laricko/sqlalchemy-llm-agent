import os

from sqlalchemy_llm_agent import SqlalchemyAgent, SqlalchemyAgentConfig

openai_api_key = os.environ["openai_api_key"]

config = SqlalchemyAgentConfig(
    api_key=openai_api_key
)
