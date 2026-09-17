from typing import Any, Dict

from firebase_admin import auth as firebase_auth

from ..core.firebase_admin import initialize_firebase


def verify_token(token: str) -> Dict[str, Any]:
    initialize_firebase()
    return firebase_auth.verify_id_token(
        token,
        check_revoked=True,
    )


def get_firebase_user(uid: str) -> Any:
    initialize_firebase()
    return firebase_auth.get_user(uid)
