import uvicorn
from src.main import app
from src.config.app_config import settings

if __name__ == "__main__":
    print(f"Starting server on port {settings.PORT}...")
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
