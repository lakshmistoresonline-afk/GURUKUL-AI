import time
import logging
from .firebase_utils import verify_firebase_token

logger = logging.getLogger(__name__)

# In-memory cache: token -> (uid, expiry)
_token_cache = {}
CACHE_TTL = 300 # 5 minutes

async def verify_and_get_uid(token: str) -> str:
    """
    Verifies a token and returns the UID.
    Results are cached to prevent repeated Firebase Admin calls on every navigation.
    """
    now = time.time()

    # 1. Check Cache
    if token in _token_cache:
        uid, expiry = _token_cache[token]
        if now < expiry:
            return uid
        else:
            del _token_cache[token]

    # 2. Verify with Firebase
    decoded = await verify_firebase_token(token)
    if decoded:
        uid = decoded.get('uid')
        # Cache for 5 mins
        _token_cache[token] = (uid, now + CACHE_TTL)
        return uid

    return None
