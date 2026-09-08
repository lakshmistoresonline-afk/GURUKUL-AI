import time
import os
from fastapi import Request, HTTPException
from typing import Dict

class RateLimiter:
    def __init__(self, limit: int, window: int):
        self.limit = limit
        self.window = window
        self.requests: Dict[str, list] = {}

    def is_allowed(self, client_id: str) -> bool:
        # Bypass for testing
        if os.getenv("TESTING") == "True":
            return True

        now = time.time()
        if client_id not in self.requests:
            self.requests[client_id] = [now]
            return True

        # Filter requests within the window
        self.requests[client_id] = [t for t in self.requests[client_id] if now - t < self.window]

        if len(self.requests[client_id]) < self.limit:
            self.requests[client_id].append(now)
            return True

        return False

# Global rate limiters
auth_limiter = RateLimiter(limit=20, window=60) # 20 requests per minute for final validation

async def rate_limit_auth(request: Request):
    client_ip = request.client.host if request.client else "127.0.0.1"
    if not auth_limiter.is_allowed(client_ip):
        raise HTTPException(status_code=429, detail="Too many attempts. Please try again later.")
