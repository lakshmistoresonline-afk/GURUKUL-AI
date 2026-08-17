import json
from typing import Any, Dict, Optional, List

import httpx

from ..ai.ai_provider import AIProvider
from ..config.app_config import settings
from ..utils.ai_utils import normalize_structured_response


class OllamaCloudProvider(AIProvider):

    def __init__(self):
        self.base_url = (settings.OLLAMA_CLOUD_URL or "").rstrip("/")
        self.api_key = settings.OLLAMA_API_KEY
        self.model = settings.OLLAMA_CLOUD_MODEL
        self.timeout = 120.0

    def get_name(self) -> str:
        return "Ollama Cloud"

    def is_enabled(self) -> bool:
        return bool(
            settings.OLLAMA_CLOUD_ENABLED
            and self.base_url
            and self.api_key
        )

    def _headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def _raise_response_error(
        self,
        response: httpx.Response,
        operation: str,
    ) -> None:
        body = response.text.strip()

        if len(body) > 2000:
            body = body[:2000] + "...[truncated]"

        raise RuntimeError(
            f"Ollama Cloud {operation} failed: "
            f"HTTP {response.status_code}; "
            f"model={self.model}; "
            f"response={body}"
        )

    async def generate(
        self,
        prompt: str,
        model_override: Optional[str] = None,
    ) -> str:

        model = model_override or self.model
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": 0,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._headers(),
                )

            if response.status_code != 200:
                self._raise_response_error(response, "generation")

            data = response.json()
            result = data.get("response", "")

            if not result:
                raise RuntimeError(
                    f"Ollama Cloud generation returned an empty response; "
                    f"model={model}"
                )

            return result

        except httpx.TimeoutException as exc:
            raise RuntimeError(
                f"Ollama Cloud generation timeout after "
                f"{self.timeout}s; model={model}"
            ) from exc

        except httpx.HTTPError as exc:
            raise RuntimeError(
                f"Ollama Cloud HTTP error; model={model}; error={exc}"
            ) from exc

    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        model_override: Optional[str] = None,
    ) -> Dict[str, Any]:

        model = model_override or self.model
        url = f"{self.base_url}/api/generate"

        full_prompt = (
            f"{prompt}\n\n"
            "Return ONLY one valid JSON object matching this schema:\n"
            f"{json.dumps(schema, ensure_ascii=False)}"
        )

        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            "format": "json",
            "keep_alive": 0,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._headers(),
                )

            if response.status_code != 200:
                self._raise_response_error(
                    response,
                    "structured generation",
                )

            data = response.json()
            raw = data.get("response", "")

            if not raw:
                raise RuntimeError(
                    f"Ollama Cloud structured generation returned empty "
                    f"response; model={model}"
                )

            try:
                parsed = normalize_structured_response(raw)
            except Exception as exc:
                raise RuntimeError(
                    f"Ollama Cloud returned invalid JSON; model={model}; "
                    f"response={raw[:1000]}"
                ) from exc

            if not isinstance(parsed, (dict, list)):
                raise RuntimeError(
                    f"Ollama Cloud structured response is neither an object nor an array; "
                    f"model={model}"
                )

            return parsed

        except httpx.TimeoutException as exc:
            raise RuntimeError(
                f"Ollama Cloud structured generation timeout after "
                f"{self.timeout}s; model={model}"
            ) from exc

        except httpx.HTTPError as exc:
            raise RuntimeError(
                f"Ollama Cloud structured HTTP error; "
                f"model={model}; error={exc}"
            ) from exc

    async def generate_embeddings(self, text: str) -> List[float]:
        url = f"{self.base_url}/api/embeddings"

        payload = {
            "model": "mxbai-embed-large",
            "prompt": text,
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    url,
                    json=payload,
                    headers=self._headers(),
                )

            if response.status_code != 200:
                self._raise_response_error(
                    response,
                    "embedding generation",
                )

            data = response.json()
            return data.get("embedding", [])

        except httpx.TimeoutException as exc:
            raise RuntimeError(
                f"Ollama Cloud embedding timeout after {self.timeout}s"
            ) from exc

        except httpx.HTTPError as exc:
            raise RuntimeError(
                f"Ollama Cloud embedding HTTP error: {exc}"
            ) from exc

    async def check_health(self) -> Dict[str, Any]:

        if not self.is_enabled():
            return {
                "status": "disabled",
                "provider": self.get_name(),
            }

        tags_url = f"{self.base_url}/api/tags"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:

                tags_response = await client.get(
                    tags_url,
                    headers=self._headers(),
                )

                if tags_response.status_code != 200:
                    self._raise_response_error(
                        tags_response,
                        "health check",
                    )

                tags_data = tags_response.json()
                models = tags_data.get("models", [])

                model_names = {
                    str(m.get("name", ""))
                    for m in models
                    if isinstance(m, dict)
                }

                if self.model not in model_names:
                    # Ollama Cloud may expose aliases or a model that is
                    # not listed by /api/tags. Verify by a tiny generation.
                    try:
                        response = await client.post(
                            f"{self.base_url}/api/generate",
                            json={
                                "model": self.model,
                                "prompt": "Reply with exactly: PASS",
                                "stream": False,
                                "keep_alive": 0,
                            },
                            headers=self._headers(),
                        )

                        if response.status_code != 200:
                            self._raise_response_error(
                                response,
                                "model health check",
                            )

                        data = response.json()

                        if not data.get("response"):
                            raise RuntimeError(
                                f"Ollama Cloud model {self.model} "
                                "returned an empty health response"
                            )

                    except httpx.TimeoutException as exc:
                        raise RuntimeError(
                            f"Ollama Cloud model health check timeout; "
                            f"model={self.model}"
                        ) from exc

                return {
                    "status": "available",
                    "provider": self.get_name(),
                    "model": self.model,
                }

        except Exception as exc:
            return {
                "status": "unavailable",
                "provider": self.get_name(),
                "error": str(exc),
            }
