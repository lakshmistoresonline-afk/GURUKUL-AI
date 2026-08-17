import unittest
import asyncio
from unittest.mock import MagicMock, AsyncMock, patch
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.orchestrator.ai_orchestrator import AIOrchestrator, AllProvidersUnavailableError
from src.orchestrator.quota_manager import QuotaManager
from src.ai.ai_provider import AIProvider

class VerifyOrchestratorBehavior(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Fresh quota manager for testing
        self.quota_manager = QuotaManager()

        # Create mocks for each provider
        self.ollama = MagicMock(spec=AIProvider)
        self.ollama.get_name.return_value = "Ollama Cloud"
        self.ollama.is_enabled.return_value = True
        self.ollama.generate = AsyncMock(return_value="Ollama Response")

        self.openrouter = MagicMock(spec=AIProvider)
        self.openrouter.get_name.return_value = "OpenRouter"
        self.openrouter.is_enabled.return_value = True
        self.openrouter.generate = AsyncMock(return_value="OpenRouter Response")

        self.gemini = MagicMock(spec=AIProvider)
        self.gemini.get_name.return_value = "Gemini"
        self.gemini.is_enabled.return_value = True
        # Simulate 429
        self.gemini.generate = AsyncMock(side_effect=Exception("Gemini error: 429 - Quota exceeded"))

        self.groq = MagicMock(spec=AIProvider)
        self.groq.get_name.return_value = "Groq"
        self.groq.is_enabled.return_value = True
        # Simulate 401
        self.groq.generate = AsyncMock(side_effect=Exception("Groq error: 401 - Invalid API Key"))

        self.cerebras = MagicMock(spec=AIProvider)
        self.cerebras.get_name.return_value = "Cerebras"
        self.cerebras.is_enabled.return_value = False # DISABLED

        self.ollama_local = MagicMock(spec=AIProvider)
        self.ollama_local.get_name.return_value = "Ollama Local"
        self.ollama_local.is_enabled.return_value = False # DISABLED

        # Initialize Orchestrator with these mocks
        with patch('src.orchestrator.ai_orchestrator.quota_manager', self.quota_manager):
            self.orchestrator = AIOrchestrator()
            self.orchestrator.providers = [
                self.ollama, self.gemini, self.groq, self.cerebras, self.openrouter, self.ollama_local
            ]

    async def test_uses_available_provider(self):
        """1. Uses an available provider (Ollama Cloud is first in list)."""
        with patch('src.orchestrator.ai_orchestrator.quota_manager', self.quota_manager):
            result = await self.orchestrator.generate("test")
            self.assertTrue(result["success"])
            self.assertEqual(result["provider"], "Ollama Cloud")
            print("PASS: Uses available provider")

    async def test_fallback_logic(self):
        """2. Falls back from a temporary provider failure to another available provider."""
        # Make Ollama fail once with a generic error
        self.ollama.generate.side_effect = Exception("Temporary Network Error")

        with patch('src.orchestrator.ai_orchestrator.quota_manager', self.quota_manager):
            result = await self.orchestrator.generate("test")
            self.assertTrue(result["success"])
            # Should skip gemini (429), groq (401), cerebras (disabled) and hit OpenRouter
            self.assertEqual(result["provider"], "OpenRouter")
            print("PASS: Fallback logic")

    async def test_gemini_429_retryable(self):
        """3 & 4. Treats Gemini 429 as retryable and does not permanently fail chapter if others available."""
        # If we skip Ollama and OpenRouter, and Gemini is next...
        self.ollama.is_enabled.return_value = False
        self.openrouter.is_enabled.return_value = False

        with patch('src.orchestrator.ai_orchestrator.quota_manager', self.quota_manager):
            result = await self.orchestrator.generate("test")
            self.assertFalse(result["success"])
            self.assertTrue(result.get("is_all_failed"))

            # Check quota manager status for Gemini
            self.assertEqual(self.quota_manager.stats["Gemini"]["status"], "RATE_LIMITED")
            print("PASS: Gemini 429 treated as retryable/rate-limited")

    async def test_disabled_providers_ignored(self):
        """5. Does not unnecessarily wait for disabled providers."""
        with patch('src.orchestrator.ai_orchestrator.quota_manager', self.quota_manager):
            active = self.orchestrator.active_providers
            provider_names = [p.get_name() for p in active]
            self.assertNotIn("Cerebras", provider_names)
            self.assertNotIn("Ollama Local", provider_names)
            print("PASS: Disabled providers ignored")

    async def test_paused_logic_when_all_fail(self):
        """6. Preserves the new is_all_failed flag when ALL providers fail."""
        # All enabled providers return error
        self.ollama.generate.side_effect = Exception("Fail")
        self.openrouter.generate.side_effect = Exception("Fail")
        # Gemini and Groq are already failing in SetUp

        with patch('src.orchestrator.ai_orchestrator.quota_manager', self.quota_manager):
            result = await self.orchestrator.generate("test")
            self.assertFalse(result["success"])
            self.assertTrue(result.get("is_all_failed"), "is_all_failed flag missing")
            print("PASS: is_all_failed logic preserved")

if __name__ == "__main__":
    unittest.main()
