import time
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class QuotaManager:
    def __init__(self):
        # provider -> metadata
        self.stats = {}

    def report_success(self, provider: str):
        if provider not in self.stats:
            self._init_stats(provider)
        self.stats[provider]["last_success"] = time.time()
        self.stats[provider]["status"] = "AVAILABLE"

    def report_error(self, provider: str, error_type: str):
        if provider not in self.stats:
            self._init_stats(provider)

        self.stats[provider]["last_failure"] = time.time()
        self.stats[provider]["error_count"] += 1

        if "429" in error_type:
            logger.warning(f"Provider {provider} rate limited.")
            self.stats[provider]["status"] = "RATE_LIMITED"
            # Set cooldown for 1 minute by default
            self.stats[provider]["cooldown_until"] = time.time() + 60
        elif "401" in error_type or "403" in error_type:
            self.stats[provider]["status"] = "DISABLED"
            logger.error(f"Provider {provider} auth failed. Disabling.")

    def is_available(self, provider: str) -> bool:
        if provider not in self.stats:
            return True

        stat = self.stats[provider]
        if stat["status"] == "DISABLED":
            return False

        if stat["status"] == "RATE_LIMITED":
            if time.time() > stat["cooldown_until"]:
                stat["status"] = "AVAILABLE"
                return True
            return False

        return True

    def _init_stats(self, provider: str):
        self.stats[provider] = {
            "status": "AVAILABLE",
            "error_count": 0,
            "last_success": None,
            "last_failure": None,
            "cooldown_until": 0
        }

quota_manager = QuotaManager()
