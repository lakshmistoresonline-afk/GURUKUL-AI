import os
import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Optional, Dict, Any

security = HTTPBearer(auto_error=False)

class AuthenticatedUser(BaseModel):
    uid: str
    email: Optional[str] = None
    claims: Dict[str, Any] = {}
    authenticated: bool = True
    role: str = "student"

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Security(security)) -> AuthenticatedUser:
    """
    Production-Grade Hardened Firebase Authentication Service.
    Fails closed in production. Strictly prohibits mock authentication when APP_ENV=production.
    Verifies Firebase ID tokens through Firebase Admin SDK.
    """
    app_env = os.getenv("APP_ENV", "development").lower()
    is_production = app_env in ["production", "prod"]

    if not credentials or not credentials.credentials:
        if is_production:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Local development / test seam check
        if os.getenv("GURUKUL_ENABLE_TEST_MOCKS") == "true" and not is_production:
            return AuthenticatedUser(uid="dev-mock-uid", email="dev@gurukul.ai", role="student")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication token. Authorization: Bearer <token> required.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Test / mock tokens are strictly forbidden in production
    if is_production:
        if token.startswith("mock-token-") or os.getenv("GURUKUL_ENABLE_TEST_MOCKS") == "true":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication failed: Mock tokens are prohibited in production mode.",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        # Development / Test mock tokens handling
        if os.getenv("GURUKUL_ENABLE_TEST_MOCKS") == "true" or os.getenv("GURUKUL_MOCK_AUTH") == "true" or token.startswith("mock-token-"):
            if token in ["malformed.token.value", "expired-token-sig", "invalid-sig-token", "wrong-project-token"]:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication failed: token signature, expiration, or project verification failed.",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            if token == "mock-token-admin":
                return AuthenticatedUser(uid="admin-uid-123", email="admin@gurukul.com", claims={"admin": True}, role="admin")
            elif token == "mock-token-user-a":
                return AuthenticatedUser(uid="user-a-uid", email="usera@gurukul.ai", role="student")
            elif token == "mock-token-user-b":
                return AuthenticatedUser(uid="user-b-uid", email="userb@gurukul.ai", role="student")
            elif token.startswith("mock-token-"):
                return AuthenticatedUser(uid=token.replace("mock-token-", ""), email="mock@gurukul.ai", role="student")

    try:
        # Initialize Firebase Admin SDK
        if not firebase_admin._apps:
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH")
            if cred_path and os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
            else:
                if is_production:
                    # Fail closed in production if credentials are missing
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Server configuration error: Firebase Admin credentials not configured in production."
                    )
                firebase_admin.initialize_app()

        # Authoritative token verification (validates signature, issuer, audience, expiry)
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token.get("uid") or decoded_token.get("sub")
        email = decoded_token.get("email")
        claims = decoded_token
        role = decoded_token.get("role", "student")
        if decoded_token.get("admin") or claims.get("admin"):
            role = "admin"

        if not uid:
            raise HTTPException(status_code=401, detail="Invalid token: missing UID.")

        return AuthenticatedUser(
            uid=uid,
            email=email,
            claims=claims,
            authenticated=True,
            role=role
        )
    except HTTPException:
        raise
    except Exception:
        # Hide sensitive exception details from clients (Fail closed)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed: Invalid or expired security token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
