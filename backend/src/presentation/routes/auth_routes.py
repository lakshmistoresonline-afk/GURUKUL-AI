from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.firebase_auth import verify_firebase_token
from ...core.utils.auth import get_current_active_user
from ...data.repositories.database.db_config import get_db
from ...data.repositories.database.orm_models import UserORM, StudentORM


router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

bearer_scheme = HTTPBearer(auto_error=False)


class FirebaseSessionRequest(BaseModel):
    name: Optional[str] = Field(default=None, max_length=200)
    username: Optional[str] = Field(default=None, max_length=100)
    class_id: Optional[str] = Field(default=None, max_length=50)


class FirebaseSessionResponse(BaseModel):
    id: str
    firebase_uid: str
    email: Optional[str]
    username: str
    name: Optional[str]
    role: str
    class_id: Optional[str]
    is_new_user: bool


def _token(
    credentials: Optional[HTTPAuthorizationCredentials],
) -> str:
    if not credentials or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase authentication token is required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return credentials.credentials


@router.post(
    "/firebase/session",
    response_model=FirebaseSessionResponse,
)
async def firebase_session(
    profile: FirebaseSessionRequest,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        bearer_scheme
    ),
    db: AsyncSession = Depends(get_db),
):
    token = _token(credentials)

    decoded = verify_firebase_token(token)

    firebase_uid = decoded.get("uid")
    email = decoded.get("email")

    if not firebase_uid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Firebase token does not contain a valid user ID.",
        )

    result = await db.execute(
        select(UserORM).where(
            UserORM.firebase_uid == firebase_uid
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        student_name = profile.name or "Pilot Student (Class 5)"
        student_class_id = profile.class_id or "class_5"

        username = profile.username

        if not username:
            if email and "@" in email:
                username = email.split("@")[0]
            else:
                username = f"student_{firebase_uid[:8]}"

        username_result = await db.execute(
            select(UserORM).where(
                UserORM.username == username
            )
        )

        if username_result.scalar_one_or_none():
            username = f"{username}_{firebase_uid[:6]}"

        student_id = f"student_{firebase_uid}"

        student = StudentORM(
            id=student_id,
            name=student_name,
            class_id=student_class_id,
        )

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

        await db.commit()
        await db.refresh(user)

        return FirebaseSessionResponse(
            id=user.id,
            firebase_uid=firebase_uid,
            email=email,
            username=user.username,
            name=student.name,
            role="student",
            class_id=student.class_id,
            is_new_user=True,
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This Gurukul account is inactive.",
        )

    student = None

    if user.student_profile_id:
        result = await db.execute(
            select(StudentORM).where(
                StudentORM.id == user.student_profile_id
            )
        )
        student = result.scalar_one_or_none()

    return FirebaseSessionResponse(
        id=user.id,
        firebase_uid=firebase_uid,
        email=email,
        username=user.username,
        name=student.name if student else None,
        role=user.role,
        class_id=student.class_id if student else None,
        is_new_user=False,
    )


@router.get(
    "/me",
    response_model=FirebaseSessionResponse,
)
async def get_me(
    current_user: UserORM = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    student = None

    if current_user.student_profile_id:
        result = await db.execute(
            select(StudentORM).where(
                StudentORM.id == current_user.student_profile_id
            )
        )
        student = result.scalar_one_or_none()

    return FirebaseSessionResponse(
        id=current_user.id,
        firebase_uid=current_user.firebase_uid,
        email=None,
        username=current_user.username,
        name=student.name if student else None,
        role=current_user.role,
        class_id=student.class_id if student else None,
        is_new_user=False,
    )


@router.post("/logout")
async def logout():
    return {
        "success": True,
        "message": "Firebase client handles sign out.",
    }


@router.post("/password/change", status_code=status.HTTP_410_GONE)
async def password_change_disabled():
    raise HTTPException(
        status_code=status.HTTP_410_GONE,
        detail=(
            "Local password management is disabled. "
            "Passwords are managed by Firebase Authentication."
        ),
    )

