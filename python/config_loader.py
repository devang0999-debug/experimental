"""Load a JSON config file with environment-variable overrides."""

from __future__ import annotations

import json
import os
from typing import Any


def _coerce(raw: str, template: Any) -> Any:
    """Coerce an env-var string to the type of the existing config value."""
    if isinstance(template, bool):
        return raw.strip().lower() in {"1", "true", "yes", "on"}
    if isinstance(template, int):
        return int(raw)
    if isinstance(template, float):
        return float(raw)
    return raw


def load_config(path: str, prefix: str = "APP_") -> dict[str, Any]:
    """Load ``path`` as JSON, then override top-level keys from the environment.

    An env var ``{prefix}{KEY}`` overrides config key ``key`` (case-insensitive),
    coerced to the type of the value already present in the file.
    """
    with open(path, "r", encoding="utf-8") as f:
        config: dict[str, Any] = json.load(f)

    lookup = {key.upper(): key for key in config}
    for env_key, raw in os.environ.items():
        if not env_key.startswith(prefix):
            continue
        name = env_key[len(prefix):].upper()
        if name in lookup:
            key = lookup[name]
            config[key] = _coerce(raw, config[key])

    return config


if __name__ == "__main__":
    import tempfile

    sample = {"host": "localhost", "port": 8000, "debug": False}
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as tmp:
        json.dump(sample, tmp)
        tmp_path = tmp.name

    os.environ["APP_PORT"] = "9090"
    os.environ["APP_DEBUG"] = "true"
    print(load_config(tmp_path))
