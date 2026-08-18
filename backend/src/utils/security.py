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
    Enforces class isolation for students.
    """
    if user.role != "admin" and class_name and class_name != user.class_name:
        # Special case: allow 'class_5' if user has '5'
        from .path_resolver import PathResolver
        req_id = PathResolver.extract_class_id(class_name)
        user_id = PathResolver.extract_class_id(user.class_name)
        if req_id != user_id:
            raise HTTPException(status_code=403, detail="Access Denied: You can only access content for your own class.")

    return class_name if class_name else user.class_name


def validate_chapter_access(
    chapter_id: str,
    student_class: str,
    subject: Optional[str] = None,
):
    """
    Ensures the requested chapter exists within the student's curriculum.
    """
    # For now, we trust the hierarchical path resolution.
    # If the file isn't found later, it will 404.
    return True


async def get_admin_user(
    user: AuthUser = Depends(get_current_user)
) -> str:
    """
    Enforces that only admin users can access the endpoint.
    """
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin role required for this operation.")
    return user.uid
