import httpx
import json
from typing import Any, Dict, Optional, List
from ..ai.ai_provider import AIProvider
from ..config.app_config import settings
from ..utils.ai_utils import normalize_structured_response

class OpenRouterProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY
        self.model = settings.OPENROUTER_MODEL
        self.base_url = "https://openrouter.ai/api/v1"

    def get_name(self) -> str:
        return "OpenRouter"

    def is_enabled(self) -> bool:
        return settings.OPENROUTER_ENABLED and self.api_key is not None

    async def generate(self, prompt: str, model_override: Optional[str] = None) -> str:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://gurukul-ai.local", # Optional
            "X-Title": "Gurukul AI"
        }

        payload = {
            "model": model_override or self.model,
            "messages": [{"role": "user", "content": prompt}]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content']
            else:
                raise Exception(f"OpenRouter error: {response.status_code} - {response.text}")

    async def generate_structured(self, prompt: str, schema: Dict[str, Any], model_override: Optional[str] = None) -> Dict[str, Any]:
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": model_override or self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that outputs ONLY valid JSON."},
                {"role": "user", "content": f"{prompt}\n\nReturn ONLY a JSON object matching this schema: {json.dumps(schema)}"}
            ],
            "response_format": {"type": "json_object"}
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return normalize_structured_response(data['choices'][0]['message']['content'])
            else:
                raise Exception(f"OpenRouter structured error: {response.status_code} - {response.text}")

    async def generate_embeddings(self, text: str) -> List[float]:
        raise NotImplementedError("OpenRouter does not support embeddings directly")

    async def check_health(self) -> Dict[str, Any]:
        if not self.api_key:
            return {"status": "disabled"}
        try:
            await self.generate("hi")
            return {"status": "available", "provider": self.get_name()}
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}
