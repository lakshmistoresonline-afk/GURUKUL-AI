from fastapi import HTTPException, status
from .auth_service import AuthenticatedUser

class AuthorizationService:
    @classmethod
    def require_admin(cls, user: AuthenticatedUser) -> AuthenticatedUser:
        if user.role != "admin" and not user.claims.get("admin"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Administrator privileges required."
            )
        return user

    @classmethod
    def require_owner_or_admin(cls, user: AuthenticatedUser, target_uid: str) -> AuthenticatedUser:
        if user.role == "admin" or user.claims.get("admin") or user.uid == target_uid:
            return user
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You do not have permission to access another user's data."
        )
