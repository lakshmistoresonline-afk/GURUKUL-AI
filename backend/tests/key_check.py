import os
import sys
from dotenv import load_dotenv

# Add root to path to find .env
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(root_dir, ".env"))

def check_keys():
    print(f"CWD: {os.getcwd()}")
    gemini = os.getenv("GEMINI_API_KEY")
    groq = os.getenv("GROQ_API_KEY")

    if gemini:
        print(f"GEMINI_API_KEY: {gemini[:5]}... (Len: {len(gemini)})")
    else:
        print("GEMINI_API_KEY: NOT FOUND")

    if groq:
        print(f"GROQ_API_KEY: {groq[:5]}... (Len: {len(groq)})")
    else:
        print("GROQ_API_KEY: NOT FOUND")

if __name__ == "__main__":
    check_keys()
