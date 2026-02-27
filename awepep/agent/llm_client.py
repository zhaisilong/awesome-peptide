from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import requests


@dataclass(frozen=True)
class LlmResponse:
    content: str
    raw: dict[str, Any]


class OpenAICompatibleClient:
    def __init__(self, *, base_url: str, api_key: str, model: str, timeout_s: float = 30.0):
        self._base_url = base_url.rstrip("/")
        self._api_key = api_key
        self._model = model
        self._timeout_s = timeout_s

    def chat_json(self, *, system: str, user: str, temperature: float = 0.2) -> LlmResponse:
        if not self._api_key:
            raise RuntimeError("Missing LLM API key. Set `AWEPEP_LLM_API_KEY` or `llm.api_key` in awepep-agent.toml.")

        url = f"{self._base_url}/chat/completions"
        payload: dict[str, Any] = {
            "model": self._model,
            "temperature": temperature,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "response_format": {"type": "json_object"},
        }
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }

        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=self._timeout_s)
        except requests.RequestException as e:
            raise RuntimeError(f"Failed to call LLM endpoint: {url}") from e

        if resp.status_code >= 400:
            raise RuntimeError(f"LLM request failed ({resp.status_code}): {resp.text[:500]}")

        data: dict[str, Any] = resp.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except Exception as e:  # noqa: BLE001
            raise RuntimeError("Unexpected LLM response format") from e

        if not isinstance(content, str) or not content.strip():
            raise RuntimeError("LLM returned empty content")
        return LlmResponse(content=content, raw=data)

