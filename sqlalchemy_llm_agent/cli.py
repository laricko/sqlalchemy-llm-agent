"""Command-line interface for sqlalchemy-llm-agent."""
from __future__ import annotations

import argparse
import json
import runpy
import sys
from pathlib import Path

from .agent import SqlalchemyAgent
from .config import SqlalchemyAgentConfig


def load_config_from_path(config_path: str | Path) -> SqlalchemyAgentConfig:
    """Load a ``SqlalchemyAgentConfig`` named ``sqlalchemy_llm_agent_config``.

    Args:
        config_path: Filesystem path to a Python file that defines a variable
            named ``sqlalchemy_llm_agent_config``.

    Raises:
        FileNotFoundError: If the provided path cannot be found.
        ValueError: If the expected variable is missing or has a wrong type.

    Returns:
        The ``SqlalchemyAgentConfig`` instance defined in the given file.
    """

    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file '{config_path}' does not exist.")

    namespace = runpy.run_path(config_path)
    if "sqlalchemy_llm_agent_config" not in namespace:
        raise ValueError(
            "Config file must define a 'sqlalchemy_llm_agent_config' variable."
        )

    config = namespace["sqlalchemy_llm_agent_config"]
    if not isinstance(config, SqlalchemyAgentConfig):
        raise ValueError(
            "'sqlalchemy_llm_agent_config' must be a SqlalchemyAgentConfig instance."
        )

    return config


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Run natural-language SQL queries against your database."
    )
    parser.add_argument(
        "query",
        help="The natural-language request for the agent, e.g. 'List all payments'.",
    )
    parser.add_argument(
        "-c",
        "--config",
        required=True,
        help=(
            "Path to a Python file that defines a 'sqlalchemy_llm_agent_config' "
            "instance."
        ),
    )

    args = parser.parse_args(argv)

    try:
        config = load_config_from_path(args.config)
        agent = SqlalchemyAgent(config)
        rows = agent.query(args.query)
    except Exception as exc:  # pragma: no cover - CLI level safeguard
        parser.exit(1, f"Error: {exc}\n")

    json_output = json.dumps(rows, indent=2, default=str)
    print(json_output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
