import httpx
import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.app_config import settings

async def discover_groq():
    api_key = settings.GROQ_API_KEY
    if not api_key:
        print("Groq API Key missing")
        return

    url = "https://api.groq.com/openai/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                print("Available Groq Models:")
                for model in data.get('data', []):
                    print(f"- {model['id']}")
            else:
                print(f"Failed to list models: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(discover_groq())
