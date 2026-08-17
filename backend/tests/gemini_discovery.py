import httpx
import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.app_config import settings

async def discover_gemini():
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        print("Gemini API Key missing")
        return

    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                data = response.json()
                print("Available Gemini Models:")
                for model in data.get('models', []):
                    print(f"- {model['name']} (Supports: {model['supportedGenerationMethods']})")
            else:
                print(f"Failed to list models: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(discover_gemini())
