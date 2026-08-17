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
    Enforces that student requests are scoped to their verified class.
    """
    student_class = user.class_name

    if class_name and class_name != student_class:
        logger.error(
            "Unauthorized class access attempt by UID %s: Requested %s, authorized for %s",
            user.uid,
            class_name,
            student_class,
        )
        raise HTTPException(
            status_code=403,
            detail="Access Denied: You are not authorized to access content for this class.",
        )

    return student_class


def validate_chapter_access(
    chapter_id: str,
    student_class: str,
    subject: Optional[str] = None,
):
    """
    Validate that a chapter belongs to the authenticated student's
    curriculum using the FINAL MASTER CONTENT index.
    """
    if not student_class:
        raise HTTPException(
            status_code=403,
            detail="Access Denied: Student curriculum is not assigned.",
        )

    if not chapter_id:
        raise HTTPException(
            status_code=400,
            detail="Chapter ID is required.",
        )

    # Canonical master-index membership is the security source of truth.
    master_path = PathResolver.get_chapter_path(
        student_class,
        chapter_id,
        subject=subject,
    )

    if not master_path:
        logger.warning(
            "Chapter access denied: class=%s subject=%s chapter=%s",
            student_class,
            subject,
            chapter_id,
        )
        raise HTTPException(
            status_code=403,
            detail="Access Denied: Requested chapter does not belong to your curriculum.",
        )

    return True


async def get_admin_user(
    user: AuthUser = Depends(get_current_user)
) -> str:
    """
    Enforces that only admin users can access the endpoint.
    """
    if user.role != "admin":
        logger.error(
            "Unauthorized admin access attempt by UID: %s with role: %s",
            user.uid,
            user.role,
        )
        raise HTTPException(
            status_code=403,
            detail="Access Denied: Admin role required.",
        )

    return user.uid
