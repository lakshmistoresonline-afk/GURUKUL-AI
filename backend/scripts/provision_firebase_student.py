import argparse
import asyncio
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND_DIR))

from firebase_admin import auth as firebase_auth
from sqlalchemy import select

from src.core.firebase_admin import initialize_firebase
from src.data.repositories.database.db_config import AsyncSessionLocal, init_db
from src.data.repositories.database.orm_models import UserORM, StudentORM


async def provision_student(
    firebase_uid: str,
    name: str,
    class_id: str,
    username: str | None = None,
) -> None:
    initialize_firebase()

    firebase_user = firebase_auth.get_user(firebase_uid)

    print(f"Firebase UID  : {firebase_user.uid}")
    print(f"Firebase email: {firebase_user.email or '(none)'}")

    async with AsyncSessionLocal() as db:

        # Find existing Gurukul user by Firebase UID.
        result = await db.execute(
            select(UserORM).where(
                UserORM.firebase_uid == firebase_uid
            )
        )
        user = result.scalar_one_or_none()

        if user is not None:

            if user.role == "admin":
                raise RuntimeError(
                    "This Firebase UID is already provisioned as an admin."
                )

            # Existing user: make sure student profile exists.
            student = None

            if user.student_profile_id:
                result = await db.execute(
                    select(StudentORM).where(
                        StudentORM.id == user.student_profile_id
                    )
                )
                student = result.scalar_one_or_none()

            if student is None:
                student_id = f"student_{firebase_uid}"

                student = StudentORM(
                    id=student_id,
                    name=name,
                    class_id=class_id,
                )

                db.add(student)
                user.student_profile_id = student_id
                action = "UPDATED_WITH_STUDENT"

            else:
                student.name = name
                student.class_id = class_id
                action = "UPDATED"

            user.role = "student"
            user.is_active = True

        else:
            # Create a new student profile.
            student_id = f"student_{firebase_uid}"

            student = StudentORM(
                id=student_id,
                name=name,
                class_id=class_id,
            )

            if not username:
                if firebase_user.email and "@" in firebase_user.email:
                    username = firebase_user.email.split("@")[0]
                else:
                    username = f"student_{firebase_uid[:8]}"

            # Avoid username collision.
            username_result = await db.execute(
                select(UserORM).where(
                    UserORM.username == username
                )
            )

            if username_result.scalar_one_or_none():
                username = f"{username}_{firebase_uid[:6]}"

            user = UserORM(
                id=f"user_{firebase_uid}",
                firebase_uid=firebase_uid,
                username=username,
                hashed_password=None,
                role="student",
                student_profile_id=student_id,
                is_active=True,
            )

            db.add(student)
            db.add(user)

            action = "CREATED"

        await db.commit()
        await db.refresh(user)
        await db.refresh(student)

        print("")
        print(f"STUDENT_PROVISION_{action}")
        print(f"Database ID     : {user.id}")
        print(f"Firebase UID    : {user.firebase_uid}")
        print(f"Username        : {user.username}")
        print(f"Role            : {user.role}")
        print(f"Student ID      : {student.id}")
        print(f"Student Name    : {student.name}")
        print(f"Class ID        : {student.class_id}")
        print(f"Active          : {user.is_active}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Provision an existing Firebase user as a Gurukul student."
    )

    parser.add_argument(
        "--firebase-uid",
        required=True,
        help="Firebase Authentication UID",
    )

    parser.add_argument(
        "--name",
        required=True,
        help="Student name",
    )

    parser.add_argument(
        "--class-id",
        required=True,
        help="Gurukul class ID, for example class_5",
    )

    parser.add_argument(
        "--username",
        default=None,
        help="Optional Gurukul username",
    )

    args = parser.parse_args()

    asyncio.run(init_db())

    asyncio.run(
        provision_student(
            firebase_uid=args.firebase_uid,
            name=args.name,
            class_id=args.class_id,
            username=args.username,
        )
    )


if __name__ == "__main__":
    main()
