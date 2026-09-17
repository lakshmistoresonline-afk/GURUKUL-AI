import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base


# ------------------------------------------------------------
# Backend directory
# ------------------------------------------------------------

BACKEND_DIR = Path(__file__).resolve().parents[4]

ENV_FILE = BACKEND_DIR / ".env"

load_dotenv(ENV_FILE, override=True)


# ------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------

DEFAULT_DATABASE_PATH = BACKEND_DIR / "gurukul_v60.db"

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = (
        f"sqlite+aiosqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"
    )


# ------------------------------------------------------------
# SQLAlchemy
# ------------------------------------------------------------

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
