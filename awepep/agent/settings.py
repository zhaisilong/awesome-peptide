from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AgentSettings:
    llm_base_url: str
    llm_api_key: str
    llm_model: str
    request_timeout_s: float

    output_dir: Path
    auto_high_venues: tuple[str, ...]


def _read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    import tomllib

    with path.open("rb") as f:
        return tomllib.load(f)


def load_settings(config_path: str | None = None) -> AgentSettings:
    import os

    config_file = Path(config_path) if config_path else Path("awepep-agent.toml")
    cfg = _read_toml(config_file)

    llm_cfg = cfg.get("llm", {})
    quality_cfg = cfg.get("quality", {})
    output_cfg = cfg.get("output", {})

    base_url = (
        os.getenv("AWEPEP_LLM_BASE_URL")
        or llm_cfg.get("base_url")
        or "https://api.openai.com/v1"
    )
    api_key = os.getenv("AWEPEP_LLM_API_KEY") or llm_cfg.get("api_key") or ""
    model = os.getenv("AWEPEP_LLM_MODEL") or llm_cfg.get("model") or "gpt-4o-mini"
    timeout_s = float(
        os.getenv("AWEPEP_LLM_TIMEOUT_S")
        or llm_cfg.get("timeout_s")
        or 30.0
    )

    output_dir = Path(os.getenv("AWEPEP_AGENT_OUTPUT_DIR") or output_cfg.get("dir") or "out")

    venues = quality_cfg.get(
        "auto_high_venues",
        [
            "Nature",
            "Science",
            "Cell",
            "Nature Communications",
            "NeurIPS",
            "ICML",
            "ICLR",
        ],
    )
    auto_high_venues = tuple(str(v).strip() for v in venues if str(v).strip())

    return AgentSettings(
        llm_base_url=str(base_url).rstrip("/"),
        llm_api_key=str(api_key),
        llm_model=str(model),
        request_timeout_s=timeout_s,
        output_dir=output_dir,
        auto_high_venues=auto_high_venues,
    )

