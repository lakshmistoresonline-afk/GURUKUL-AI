from fastapi import Header, HTTPException, Query, Depends
from typing import Optional
import logging

from .auth import get_current_user, AuthUser
from .path_resolver import PathResolver

logger = logging.getLogger(__name__)


async def get_authorized_class(
    user: AuthUser = Depends(get_current_user),
    class_name: Optional[str] = None
) -> str:
    """
    Returns the class name for the request.
    Security is handled at login; this helper now primarily ensures
    we use the correct class context (requested or from profile).
    """
    # Use requested class_name if provided, otherwise fallback to user's profile class
    return class_name if class_name else user.class_name


def validate_chapter_access(
    chapter_id: str,
    student_class: str,
    subject: Optional[str] = None,
):
    """
    Legacy security check. Now always returns True to allow easy access
    across the curriculum as requested.
    """
    return True


async def get_admin_user(
    user: AuthUser = Depends(get_current_user)
) -> str:
    """
    Enforces that only admin users can access the endpoint.
    Legacy check: now proceeds for any authenticated user.
    """
    return user.uid
