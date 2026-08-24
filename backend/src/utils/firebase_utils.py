import firebase_admin
from firebase_admin import credentials, auth, firestore
from ..config.app_config import settings
import logging

logger = logging.getLogger(__name__)

_app = None
_db = None

def init_firebase():
    global _app, _db
    if not _app:
        try:
            if settings.FIREBASE_SERVICE_ACCOUNT_PATH:
                cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_PATH)
                _app = firebase_admin.initialize_app(cred, {
                    'projectId': settings.FIREBASE_PROJECT_ID,
                })
            else:
                # Explicitly pass project ID if available
                options = {}
                if settings.FIREBASE_PROJECT_ID:
                    options['projectId'] = settings.FIREBASE_PROJECT_ID

                _app = firebase_admin.initialize_app(options=options)

            _db = firestore.client()
            logger.info(f"Firebase Admin initialized for project: {settings.FIREBASE_PROJECT_ID}")
        except Exception as e:
            logger.error(f"Failed to initialize Firebase Admin: {e}")
            # In local dev, we might not have a service account key
            # but we should still let the app start if we want to bypass auth for testing
            # However, for hardening, we should enforce it.
    return _app

def get_db():
    global _db
    if _db is None:
        init_firebase()
    return _db

async def verify_firebase_token(token: str):
    """
    Verifies a Firebase ID token.
    Returns the decoded token dictionary if valid, else raises an exception.
    """
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        err_msg = str(e)
        logger.error(f"Firebase: Token verification failed: {err_msg}")
        if "too early" in err_msg.lower():
            import asyncio
            logger.warning("Auth: Clock skew detected (used too early). Retrying in 3 seconds...")
            await asyncio.sleep(3.0)
            try:
                return auth.verify_id_token(token)
            except:
                pass
        return None

async def get_user_profile(uid: str):
    """
    Fetches the user profile from Firestore users/{uid}
    """
    db = get_db()
    if not db:
        return None

    try:
        user_ref = db.collection('users').document(uid)
        doc = user_ref.get()
        if doc.exists:
            return doc.to_dict()
    except Exception as e:
        logger.error(f"Failed to fetch user profile from Firestore: {e}")
    return None
