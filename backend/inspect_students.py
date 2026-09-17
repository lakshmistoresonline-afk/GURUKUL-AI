import sys
import asyncio

sys.path.insert(0, "backend")

from src.data.repositories.database.db_config import AsyncSessionLocal
from src.data.repositories.database.orm_models import StudentORM


async def main():
    async with AsyncSessionLocal() as db:
        result = await db.execute(StudentORM.__table__.select())
        rows = result.fetchall()

        print("STUDENT_COUNT:", len(rows))

        for row in rows:
            print(dict(row._mapping))


asyncio.run(main())
