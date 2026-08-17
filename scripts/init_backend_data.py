import asyncio
import os
import sys

# Add backend/src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from src.services.external_media_service import ExternalMediaService
from src.services.mastery_service import MasteryService

async def main():
    print("Initializing backend database and loading catalogs...")
    mastery = MasteryService()
    ext_media = ExternalMediaService(mastery)
    await ext_media.init_db()
    print("Backend data initialization COMPLETE.")

if __name__ == "__main__":
    asyncio.run(main())
