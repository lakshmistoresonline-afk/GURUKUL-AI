import httpx
import json
import logging
from typing import Any, Dict, Optional, List
from ..ai.ai_provider import AIProvider
from ..config.app_config import settings
from ..utils.ai_utils import normalize_structured_response

logger = logging.getLogger(__name__)

class NvidiaProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.NVIDIA_API_KEY.strip() if settings.NVIDIA_API_KEY else None
        self.base_url = settings.NVIDIA_BASE_URL.rstrip('/')
        self.default_model = settings.NVIDIA_GPT_OSS_MODEL
        # Explicit timeout configuration for large cloud models
        self.timeout_cfg = httpx.Timeout(
            connect=10.0,
            read=300.0,  # Highly generous for heavy reasoning models
            write=60.0,
            pool=10.0
        )

    def get_name(self) -> str:
        return "NVIDIA"

    def is_enabled(self) -> bool:
        return settings.NVIDIA_ENABLED and self.api_key is not None

    def _create_client(self) -> httpx.AsyncClient:
        """Creates a robust HTTP client for NVIDIA API communication."""
        return httpx.AsyncClient(
            timeout=self.timeout_cfg,
            http2=False,           # Ensure HTTP/1.1 for broad compatibility
            follow_redirects=True  # Support API redirects if any
        )

    async def generate(self, prompt: str, model_override: Optional[str] = None) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        model = model_override or self.default_model
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5,
            "top_p": 0.7,
            "max_tokens": 1024,
            "stream": False
        }

        try:
            async with self._create_client() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                # Existing response parsing as requested
                content = data['choices'][0]['message']['content']
                # Note: Some reasoning models might return content=None if using reasoning_content
                return content or ""
        except httpx.HTTPStatusError as e:
            error_msg = f"NVIDIA API Error ({model}): {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.TimeoutException as e:
            error_msg = f"NVIDIA Timeout ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.ConnectError as e:
            error_msg = f"NVIDIA Connection Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.RequestError as e:
            error_msg = f"NVIDIA Request Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"NVIDIA Unexpected Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    async def generate_structured(self, prompt: str, schema: Dict[str, Any], model_override: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        model = model_override or self.default_model
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that outputs only valid JSON."},
                {"role": "user", "content": f"{prompt}\n\nReturn ONLY a JSON object matching this schema: {json.dumps(schema)}"}
            ],
            "temperature": 0.2,
            "stream": False
        }

        try:
            async with self._create_client() as client:
                response = await client.post(url, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                content = data['choices'][0]['message']['content']
                return normalize_structured_response(content)
        except httpx.HTTPStatusError as e:
            error_msg = f"NVIDIA Structured API Error ({model}): {e.response.status_code} - {e.response.text}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.TimeoutException as e:
            error_msg = f"NVIDIA Structured Timeout ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.ConnectError as e:
            error_msg = f"NVIDIA Structured Connection Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except httpx.RequestError as e:
            error_msg = f"NVIDIA Structured Request Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)
        except Exception as e:
            error_msg = f"NVIDIA Structured Unexpected Error ({model}): {type(e).__name__} - {str(e)}"
            logger.error(error_msg)
            raise Exception(error_msg)

    async def generate_embeddings(self, text: str) -> List[float]:
        raise NotImplementedError("NVIDIA embedding implementation pending specific model selection")

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
