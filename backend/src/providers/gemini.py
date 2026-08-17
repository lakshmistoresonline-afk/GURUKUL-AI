import httpx
import json
from typing import Any, Dict, Optional, List
from ..ai.ai_provider import AIProvider
from ..config.app_config import settings
from ..utils.ai_utils import normalize_structured_response

class GeminiProvider(AIProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model = settings.GEMINI_MODEL

    def get_name(self) -> str:
        return "Gemini"

    def is_enabled(self) -> bool:
        return settings.GEMINI_ENABLED and self.api_key is not None

    async def generate(self, prompt: str, model_override: Optional[str] = None) -> str:
        model = model_override or self.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                try:
                    return data['candidates'][0]['content']['parts'][0]['text']
                except (KeyError, IndexError):
                    raise Exception("Invalid response format from Gemini")
            else:
                raise Exception(f"Gemini error: {response.status_code} - {response.text}")

    async def generate_structured(self, prompt: str, schema: Dict[str, Any], model_override: Optional[str] = None) -> Dict[str, Any]:
        model = model_override or self.model
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.api_key}"

        # Gemini supports response_mime_type: application/json for some models
        payload = {
            "contents": [{
                "parts": [{"text": f"{prompt}\n\nReturn ONLY a JSON object matching this schema: {json.dumps(schema)}"}]
            }],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                try:
                    text = data['candidates'][0]['content']['parts'][0]['text']
                    return normalize_structured_response(text)
                except (KeyError, IndexError):
                    raise Exception("Failed to parse structured response from Gemini")
            else:
                raise Exception(f"Gemini structured error: {response.status_code} - {response.text}")

    async def generate_embeddings(self, text: str) -> List[float]:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/text-embedding-004:embedContent?key={self.api_key}"

        payload = {
            "content": {
                "parts": [{"text": text}]
            }
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                return data['embedding']['values']
            else:
                raise Exception(f"Gemini embedding error: {response.status_code}")

    async def check_health(self) -> Dict[str, Any]:
        if not self.api_key:
            return {"status": "disabled", "reason": "No API Key"}

        # Simple test call
        try:
            await self.generate("hi", model_override=self.model)
            return {"status": "available", "provider": self.get_name()}
        except Exception as e:
            return {"status": "unavailable", "error": str(e)}
