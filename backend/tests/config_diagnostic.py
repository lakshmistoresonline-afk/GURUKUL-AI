import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.config.app_config import settings

def run_diagnostic():
    print("==================================================")
    print("      GURUKUL AI CONFIGURATION DIAGNOSTIC        ")
    print("==================================================")

    print(f"Current Working Directory: {os.getcwd()}")
    print(f"Config File Path: {os.path.abspath(__file__)}")

    # Check if .env exists where we expect it
    env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
    print(f"Expected .env path: {env_path}")
    print(f".env exists: {os.path.exists(env_path)}")

    print("\nLOADED MODELS:")
    print(f"GEMINI_MODEL = {settings.GEMINI_MODEL}")
    print(f"GEMINI_FAST_MODEL = {settings.GEMINI_FAST_MODEL}")
    print(f"GROQ_MODEL = {settings.GROQ_MODEL}")
    print(f"CEREBRAS_MODEL = {settings.CEREBRAS_MODEL}")
    print(f"OPENROUTER_MODEL = {settings.OPENROUTER_MODEL}")

    print("\nAPI KEYS STATUS (Presence Check Only):")
    print(f"GEMINI_API_KEY: {'SET' if settings.GEMINI_API_KEY else 'MISSING'}")
    print(f"GROQ_API_KEY: {'SET' if settings.GROQ_API_KEY else 'MISSING'}")
    print(f"CEREBRAS_API_KEY: {'SET' if settings.CEREBRAS_API_KEY else 'MISSING'}")
    print(f"OLLAMA_API_KEY: {'SET' if settings.OLLAMA_API_KEY else 'MISSING'}")

if __name__ == "__main__":
    run_diagnostic()
