import httpx
import json
import logging
from typing import Any, Dict, Optional, List
from ..ai.ai_provider import AIProvider
from ..config.app_config import settings
from ..utils.ai_utils import normalize_structured_response

logger = logging.getLogger(__name__)

class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1"
        self.timeout_cfg = httpx.Timeout(
            connect=10.0,
            read=60.0,
            write=30.0,
            pool=10.0
        )

    def get_name(self) -> str:
        return "OpenRouter"

    def is_enabled(self) -> bool:
        return settings.OPENROUTER_ENABLED and self.api_key is not None

    def _create_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            timeout=self.timeout_cfg,
            follow_redirects=True
        )

    async def generate(self, prompt: str, model_override: Optional[str] = None) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://gurukul-ai.local",
            "X-Title": "Gurukul AI"
        }

        model = model_override or self.model
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": settings.OPENROUTER_MAX_TOKENS
        }

        try:
            async with self._create_client() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                return data['choices'][0]['message']['content']
        except httpx.HTTPStatusError as e:
            error_msg = f"OpenRouter API Error ({model}): {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.RequestError) as e:
            error_msg = f"OpenRouter Network Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"OpenRouter Unexpected Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    async def generate_structured(self, prompt: str, schema: Dict[str, Any], model_override: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        model = model_override or self.model
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that outputs ONLY valid JSON."},
                {"role": "user", "content": f"{prompt}\n\nReturn ONLY a JSON object matching this schema: {json.dumps(schema)}"}
            ],
            "response_format": {"type": "json_object"},
            "max_tokens": settings.OPENROUTER_MAX_TOKENS
        }

        try:
            async with self._create_client() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content']
                return normalize_structured_response(content)
        except httpx.HTTPStatusError as e:
            error_msg = f"OpenRouter Structured API Error ({model}): {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except (httpx.TimeoutException, httpx.ConnectError, httpx.RequestError) as e:
            error_msg = f"OpenRouter Structured Network Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"OpenRouter Structured Unexpected Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    async def generate_embeddings(self, text: str) -> List[float]:
        raise NotImplementedError("OpenRouter does not support embeddings directly")

    async def check_health(self) -> Dict[str, Any]:
        if not self.api_key:
            return {"status": "disabled", "reason": "API key missing"}

        return {
            "status": "available",
            "provider": self.get_name(),
            "configured": True,
            "base_url": self.base_url,
            "note": "Health check verified configuration. Inference test not performed to save quota."
        }
