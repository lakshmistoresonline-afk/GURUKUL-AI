import hashlib
import json

class CanonicalHasher:
    @staticmethod
    def hash_payload(payload: Any) -> str:
        s = json.dumps(payload, sort_keys=True, default=str)
        return hashlib.sha256(s.encode("utf-8")).hexdigest()
