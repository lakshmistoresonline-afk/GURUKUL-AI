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
from src.data.repositories.database.orm_models import UserORM


async def provision_admin(firebase_uid: str, username: str) -> None:
    initialize_firebase()

    firebase_user = firebase_auth.get_user(firebase_uid)

    print(f"Firebase UID : {firebase_user.uid}")
    print(f"Firebase email: {firebase_user.email or '(none)'}")

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(UserORM).where(UserORM.firebase_uid == firebase_uid)
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = UserORM(
                id=f"user_{firebase_uid}",
                firebase_uid=firebase_uid,
                username=username,
                hashed_password=None,
                role="admin",
                student_profile_id=None,
                is_active=True,
            )
            db.add(user)
            action = "CREATED"
        else:
            user.role = "admin"
            user.is_active = True
            action = "UPDATED"

        await db.commit()
        await db.refresh(user)

        print("")
        print(f"ADMIN_PROVISION_{action}")
        print(f"Database ID : {user.id}")
        print(f"Firebase UID: {user.firebase_uid}")
        print(f"Username    : {user.username}")
        print(f"Role        : {user.role}")
        print(f"Active      : {user.is_active}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Provision an existing Firebase user as a Gurukul administrator."
    )
    parser.add_argument(
        "--firebase-uid",
        required=True,
        help="Firebase Authentication UID",
    )
    parser.add_argument(
        "--username",
        required=True,
        help="Gurukul administrator username",
    )

    args = parser.parse_args()

    asyncio.run(init_db())
    asyncio.run(
        provision_admin(
            firebase_uid=args.firebase_uid,
            username=args.username,
        )
    )


if __name__ == "__main__":
    main()