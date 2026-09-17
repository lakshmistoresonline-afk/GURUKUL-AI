from pathlib import Path
import json
import firebase_admin
from firebase_admin import credentials

PROJECT_ID = "com-ncert-projectgurukul-e5e60"

BASE_DIR = Path(__file__).resolve().parents[2]
CREDENTIAL_PATH = BASE_DIR / "secrets" / "firebase-admin.json"


def initialize_firebase() -> None:
    """Initialize Firebase Admin exactly once."""
    if firebase_admin._apps:
        return

    if not CREDENTIAL_PATH.exists():
        raise FileNotFoundError(
            f"Firebase Admin credential not found: {CREDENTIAL_PATH}"
        )

    with CREDENTIAL_PATH.open("r", encoding="utf-8") as fh:
        service_account = json.load(fh)

    if service_account.get("project_id") != PROJECT_ID:
        raise RuntimeError(
            "Firebase credential project_id does not match "
            f"{PROJECT_ID}"
        )

    cred = credentials.Certificate(service_account)

    firebase_admin.initialize_app(
        cred,
        {
            "projectId": PROJECT_ID,
        },
    )