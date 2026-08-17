import asyncio
import os
import sys

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.providers.gemini import GeminiProvider

async def test_gemini():
    print("Testing Gemini...")
    provider = GeminiProvider()
    try:
        res = await provider.generate("Hi, respond with 'PASS'")
        print(f"Result: {res}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
