import os
import hashlib
import secrets
import base64
from datetime import datetime, timedelta, UTC
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from firebase_admin import auth as firebase_auth

from ...data.repositories.database.db_config import get_db
from ...data.repositories.database.orm_models import UserORM
from ..firebase_admin import initialize_firebase


# ============================================================
# Legacy password support
# ============================================================

ITERATIONS = 600000
HASH_ALGO = "sha256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24


def get_password_hash(password: str) -> str:
    """Securely hash password using PBKDF2-SHA256."""
    salt = secrets.token_bytes(16)

    hash_bytes = hashlib.pbkdf2_hmac(
        HASH_ALGO,
        password.encode(),
        salt,
        ITERATIONS,
    )

    salt_b64 = base64.b64encode(salt).decode()
    hash_b64 = base64.b64encode(hash_bytes).decode()

    return (
        f"pbkdf2:{HASH_ALGO}:{ITERATIONS}"
        f"${salt_b64}${hash_b64}"
    )


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:

    if not hashed_password:
        return False

    if hashed_password.startswith("pbkdf2:"):
        try:
            parts = hashed_password.split("$")

            if len(parts) != 3:
                return False

            meta = parts[0].split(":")

            algo = meta[1]
            iterations = int(meta[2])

            salt = base64.b64decode(parts[1])
            expected_hash = base64.b64decode(parts[2])

            actual_hash = hashlib.pbkdf2_hmac(
                algo,
                plain_password.encode(),
                salt,
                iterations,
            )

            return secrets.compare_digest(
                actual_hash,
                expected_hash,
            )

        except Exception:
            return False

    # Legacy V60 SHA256
    legacy_salt = "v60_salt_"

    legacy_hash = hashlib.sha256(
        (legacy_salt + plain_password).encode()
    ).hexdigest()

    return secrets.compare_digest(
        legacy_hash,
        hashed_password,
    )


# ============================================================
# Firebase Authentication
# ============================================================

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: AsyncSession = Depends(get_db),
) -> UserORM:

    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    if not credentials:
        raise unauthorized

    if credentials.scheme.lower() != "bearer":
        raise unauthorized

    token = credentials.credentials

    try:
        initialize_firebase()

        decoded_token = firebase_auth.verify_id_token(
            token,
            check_revoked=True,
        )

    except (
        firebase_auth.InvalidIdTokenError,
        firebase_auth.ExpiredIdTokenError,
        firebase_auth.RevokedIdTokenError,
    ):
        raise unauthorized

    except Exception:
        raise unauthorized

    firebase_uid = decoded_token.get("uid")

    if not firebase_uid:
        raise unauthorized

    # --------------------------------------------------------
    # Find existing Gurukul user by Firebase UID
    # --------------------------------------------------------

    result = await db.execute(
        select(UserORM).where(
            UserORM.firebase_uid == firebase_uid
        )
    )

    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Firebase account is authenticated but "
                "not linked to a Gurukul user profile"
            ),
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is inactive",
        )

    return user


async def get_current_active_user(
    current_user: UserORM = Depends(get_current_user),
) -> UserORM:

    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user",
        )

    return current_user


async def get_current_student(
    current_user: UserORM = Depends(
        get_current_active_user
    ),
) -> UserORM:

    if current_user.role not in [
        "STUDENT",
        "ADMIN",
        "SYSTEM",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return current_user


async def get_current_admin(
    current_user: UserORM = Depends(
        get_current_active_user
    ),
) -> UserORM:

    if current_user.role not in [
        "ADMIN",
        "SYSTEM",
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return current_user


# ============================================================
# Legacy functions retained temporarily for compatibility
# ============================================================

async def authenticate_user(
    db: AsyncSession,
    username: str,
    password: str,
):
    result = await db.execute(
        select(UserORM).where(
            UserORM.username == username
        )
    )

    user = result.scalar_one_or_none()

    if not user:
        return False

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return False

    return user


def create_access_token(
    data: dict,
    expires_delta: Optional[timedelta] = None,
):
    """
    Legacy JWT helper retained so unrelated imports do not break.

    Firebase authentication is now the authoritative authentication
    mechanism and this function must not be used for normal login.
    """

    raise RuntimeError(
        "Local JWT authentication is disabled. "
        "Use Firebase Authentication."
    )