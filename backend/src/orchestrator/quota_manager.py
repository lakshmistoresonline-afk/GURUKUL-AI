import time
import logging
import json
import os
from enum import Enum
from typing import Dict, Any, Optional
from ..config.app_config import settings

logger = logging.getLogger(__name__)

class ProviderStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    COOLDOWN = "COOLDOWN"
    QUOTA_EXHAUSTED = "QUOTA_EXHAUSTED"
    RATE_LIMITED = "RATE_LIMITED"
    TIMEOUT_UNSTABLE = "TIMEOUT_UNSTABLE"
    AUTH_FAILED = "AUTH_FAILED"
    CONTENT_GENERATION_FAILURE = "CONTENT_GENERATION_FAILURE"
    DISABLED = "DISABLED"

class QuotaManager:
    def __init__(self):
        # provider -> metadata
        self.stats = {}
        self.persistence_path = os.path.join(settings.STORAGE_PATH, "provider_health.json")
        self._load_state()

    def report_success(self, provider: str):
        if provider not in self.stats:
            self._init_stats(provider)

        # Recover from temporary states on success
        if self.stats[provider]["status"] in [ProviderStatus.COOLDOWN, ProviderStatus.TIMEOUT_UNSTABLE, ProviderStatus.RATE_LIMITED]:
            logger.info(f"Provider {provider} recovered to AVAILABLE.")

        self.stats[provider]["last_success"] = time.time()
        self.stats[provider]["status"] = ProviderStatus.AVAILABLE
        self.stats[provider]["failure_count"] = 0
        self._save_state()

    def report_error(self, provider: str, error_msg: str):
        if provider not in self.stats:
            self._init_stats(provider)

        now = time.time()
        self.stats[provider]["last_failure"] = now
        self.stats[provider]["failure_count"] += 1

        error_msg_str = str(error_msg)

        if "429" in error_msg_str:
            logger.warning(f"Provider {provider} reported RATE_LIMITED (429).")
            self.stats[provider]["status"] = ProviderStatus.RATE_LIMITED
            # 5 minute cooldown for 429
            self.stats[provider]["cooldown_until"] = now + 300
        elif "402" in error_msg_str:
            logger.error(f"Provider {provider} reported QUOTA_EXHAUSTED (402).")
            self.stats[provider]["status"] = ProviderStatus.QUOTA_EXHAUSTED
            # Long cooldown or manual intervention required
            self.stats[provider]["cooldown_until"] = now + 3600
        elif "401" in error_msg_str or "403" in error_msg_str:
            logger.error(f"Provider {provider} reported AUTH_FAILED (401/403).")
            self.stats[provider]["status"] = ProviderStatus.AUTH_FAILED
        elif "Timeout" in error_msg_str:
            logger.warning(f"Provider {provider} reported TIMEOUT_UNSTABLE.")
            self.stats[provider]["status"] = ProviderStatus.TIMEOUT_UNSTABLE
            # 2 minute cooldown for timeouts
            self.stats[provider]["cooldown_until"] = now + 120
        elif "VALIDATION" in error_msg_str.upper() or "SCHEMA" in error_msg_str.upper():
            logger.warning(f"Provider {provider} reported CONTENT_GENERATION_FAILURE.")
            self.stats[provider]["status"] = ProviderStatus.CONTENT_GENERATION_FAILURE
            # Short cooldown for generation errors to try other providers
            self.stats[provider]["cooldown_until"] = now + 30
        else:
            logger.warning(f"Provider {provider} failed with error: {error_msg_str[:100]}...")
            self.stats[provider]["status"] = ProviderStatus.COOLDOWN
            self.stats[provider]["cooldown_until"] = now + 60

        self._save_state()

    def is_available(self, provider: str) -> bool:
        if provider not in self.stats:
            return True

        stat = self.stats[provider]
        status = stat["status"]

        if status in [ProviderStatus.DISABLED, ProviderStatus.AUTH_FAILED, ProviderStatus.QUOTA_EXHAUSTED]:
            return False

        if status in [ProviderStatus.RATE_LIMITED, ProviderStatus.TIMEOUT_UNSTABLE, ProviderStatus.COOLDOWN]:
            if time.time() > stat.get("cooldown_until", 0):
                # Auto-recovery attempt
                return True
            return False

        return True

    def get_status(self, provider: str) -> ProviderStatus:
        if provider not in self.stats:
            return ProviderStatus.AVAILABLE
        return self.stats[provider]["status"]

    def _init_stats(self, provider: str):
        self.stats[provider] = {
            "status": ProviderStatus.AVAILABLE,
            "failure_count": 0,
            "last_success": None,
            "last_failure": None,
            "cooldown_until": 0
        }

    def _save_state(self):
        """Persists non-sensitive health metadata."""
        try:
            os.makedirs(os.path.dirname(self.persistence_path), exist_ok=True)
            with open(self.persistence_path, 'w') as f:
                json.dump(self.stats, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save quota state: {e}")

    def _load_state(self):
        """Loads health metadata from disk."""
        if os.path.exists(self.persistence_path):
            try:
                with open(self.persistence_path, 'r') as f:
                    self.stats = json.load(f)
                # Ensure enums are handled if we were using them as keys/values
                # But json.load returns strings, which match our ProviderStatus(str, Enum)
            except Exception as e:
                logger.error(f"Failed to load quota state: {e}")
                self.stats = {}

quota_manager = QuotaManager()
