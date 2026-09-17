import sys
import asyncio

sys.path.insert(0, "backend")

from sqlalchemy import select

from src.data.repositories.database.db_config import AsyncSessionLocal
from src.data.repositories.database.orm_models import UserORM, StudentORM


FIREBASE_UID = "lPbFfSV0b7PgkmQ7x99aEMQjZdH3"


async def main():
    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(UserORM).where(
                UserORM.firebase_uid == FIREBASE_UID
            )
        )

        user = result.scalar_one_or_none()

        if user is None:
            print("USER_NOT_FOUND")
            return

        print("USER_FOUND")
        print("USER_ID:", user.id)
        print("FIREBASE_UID:", user.firebase_uid)
        print("USERNAME:", user.username)
        print("ROLE:", user.role)
        print("STUDENT_PROFILE_ID:", user.student_profile_id)
        print("ACTIVE:", user.is_active)

        if user.student_profile_id:
            result = await db.execute(
                select(StudentORM).where(
                    StudentORM.id == user.student_profile_id
                )
            )

            student = result.scalar_one_or_none()

            if student:
                print("STUDENT_FOUND")
                print("STUDENT_ID:", student.id)
                print("STUDENT_NAME:", student.name)
                print("CLASS_ID:", student.class_id)
            else:
                print("STUDENT_PROFILE_NOT_FOUND")


asyncio.run(main())
