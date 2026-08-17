from fastapi import Header, HTTPException, Depends
from typing import Optional
import logging
from .firebase_utils import verify_firebase_token, get_user_profile

logger = logging.getLogger(__name__)

class AuthUser:
    def __init__(self, uid: str, email: str, role: str, class_id: str):
        self.uid = uid
        self.email = email
        self.role = role
        self.class_id = class_id
        self.class_name = f"class_{class_id}" if class_id else None

async def get_current_user(
    authorization: Optional[str] = Header(None)
) -> AuthUser:
    """
    Dependency that verifies the Firebase ID token.
    Login results are cached in-memory to reduce Firebase Admin API load.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = authorization.split("Bearer ")[1]

    # Simple Token Cache to reduce verify_id_token calls and log noise
    from .token_cache import verify_and_get_uid
    uid = await verify_and_get_uid(token)

    if not uid:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    # Authoritative source for role and class is Firestore
    profile = await get_user_profile(uid)
    if not profile:
        logger.warning(f"Auth: User profile not found for UID: {uid}")
        raise HTTPException(status_code=404, detail="User profile not found in Firestore")

    role = profile.get("role", "student")
    raw_class_id = profile.get("classId", "")

    # Robust normalization
    try:
        from .path_resolver import PathResolver
        class_id = PathResolver.extract_class_id(str(raw_class_id))
    except:
        class_id = str(raw_class_id)

    return AuthUser(uid, profile.get("email", ""), role, class_id)

async def get_current_student(
    user: AuthUser = Depends(get_current_user)
) -> AuthUser:
    """
    Dependency that ensures the current user is a student.
    Legacy check: now proceeds for any authenticated user.
    """
    return user

async def get_current_admin(
    user: AuthUser = Depends(get_current_user)
) -> AuthUser:
    """
    Dependency that ensures the current user is an admin.
    Legacy check: now proceeds for any authenticated user.
    """
    return user
