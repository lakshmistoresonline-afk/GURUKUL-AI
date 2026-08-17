import httpx
import json
from typing import Any, Dict, Optional, List
from ..ai.ai_provider import AIProvider
from ..config.app_config import settings
from ..utils.ai_utils import normalize_structured_response

class OllamaLocalProvider(AIProvider):
    def __init__(self):
        self.base_url = settings.OLLAMA_LOCAL_URL
        self.model = settings.OLLAMA_LOCAL_MODEL

    def get_name(self) -> str:
        return "Ollama Local"

    def is_enabled(self) -> bool:
        return settings.OLLAMA_LOCAL_ENABLED

    async def generate(self, prompt: str, model_override: Optional[str] = None) -> str:
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": model_override or self.model,
            "prompt": prompt,
            "stream": False,
            "keep_alive": 0
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data.get("response", "")
            else:
                raise Exception(f"Ollama Local error: {response.status_code} - {response.text}")

    async def generate_structured(self, prompt: str, schema: Dict[str, Any], model_override: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/api/generate"
        full_prompt = f"{prompt}\n\nReturn the response as a JSON object following this schema: {json.dumps(schema)}"

        payload = {
            "model": model_override or self.model,
            "prompt": full_prompt,
            "stream": False,
            "format": "json",
            "keep_alive": 0
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                return normalize_structured_response(data.get("response", "{}"))
            else:
                raise Exception(f"Ollama Local structured error: {response.status_code} - {response.text}")

    async def generate_embeddings(self, text: str) -> List[float]:
        url = f"{self.base_url}/api/embeddings"
        payload = {
            "model": "mxbai-embed-large",
            "prompt": text
        }
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data.get("embedding", [])
            else:
                raise Exception(f"Ollama Local embedding error: {response.status_code}")

    async def check_health(self) -> Dict[str, Any]:
        url = f"{self.base_url}/api/tags"
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, timeout=2)
                if response.status_code == 200:
                    return {"status": "available", "provider": self.get_name()}
                return {"status": "unhealthy", "code": response.status_code}
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}
