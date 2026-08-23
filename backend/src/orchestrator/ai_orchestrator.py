import asyncio
import logging
from typing import Any, Dict, List, Optional

from ..ai.ai_provider import AIProvider
from ..providers.ollama_cloud import OllamaCloudProvider
from ..providers.gemini import GeminiProvider
from ..providers.groq import GroqProvider
from ..providers.cerebras import CerebrasProvider
from ..providers.openrouter import OpenRouterProvider
from ..providers.ollama_local import OllamaLocalProvider
from ..config.app_config import settings
from .quota_manager import quota_manager


logger = logging.getLogger(__name__)


class AllProvidersUnavailableError(Exception):
    """Raised when no AI providers are currently available or all failed."""
    pass


class AIOrchestrator:

    def __init__(self):
        self.providers: List[AIProvider] = [
            OllamaLocalProvider(),
            GeminiProvider(),
            OllamaCloudProvider(),
            GroqProvider(),
            CerebrasProvider(),
            OpenRouterProvider(),
        ]

    @property
    def active_providers(self):
        return [
            p
            for p in self.providers
            if p.is_enabled()
            and quota_manager.is_available(p.get_name())
        ]

    async def generate(
        self,
        prompt: str,
        task_type: str = "general",
    ) -> Dict[str, Any]:

        last_error = None
        attempt_history = []

        active_providers = self._get_ordered_providers(task_type)
        if not active_providers:
            raise AllProvidersUnavailableError("No AI providers are currently enabled or available.")

        for provider in active_providers:

            provider_name = provider.get_name()
            model = self._get_model_for_task(
                provider_name,
                task_type,
            )

            try:
                logger.info(
                    "Routing request to %s for task %s",
                    provider_name,
                    task_type,
                )

                start_time = asyncio.get_event_loop().time()

                response = await provider.generate(
                    prompt,
                    model_override=model,
                )

                duration = (
                    asyncio.get_event_loop().time()
                    - start_time
                )

                quota_manager.report_success(provider_name)

                logger.info(
                    "Provider %s succeeded for task %s",
                    provider_name,
                    task_type,
                )

                return {
                    "success": True,
                    "provider": provider_name,
                    "model": model,
                    "response": response,
                    "duration": duration,
                    "attempts": attempt_history,
                }

            except Exception as exc:

                error_text = str(exc) or repr(exc)

                logger.warning(
                    "Provider %s failed for task %s: %s",
                    provider_name,
                    task_type,
                    error_text,
                )

                quota_manager.report_error(
                    provider_name,
                    error_text,
                )

                attempt_history.append(
                    {
                        "provider": provider_name,
                        "error": error_text,
                        "model": model,
                    }
                )

                last_error = exc

        return {
            "success": False,
            "error": "All providers failed",
            "last_error": str(last_error) if last_error else None,
            "attempts": attempt_history,
            "is_all_failed": True
        }

    async def generate_structured(
        self,
        prompt: str,
        schema: Dict[str, Any],
        task_type: str = "structured",
    ) -> Dict[str, Any]:

        last_error = None
        attempt_history = []

        active_providers = self._get_ordered_providers(task_type)
        if not active_providers:
            raise AllProvidersUnavailableError("No AI providers are currently enabled or available for structured output.")

        for provider in active_providers:

            provider_name = provider.get_name()
            model = self._get_model_for_task(
                provider_name,
                task_type,
            )

            try:
                logger.info(
                    "Routing structured request to %s for task %s",
                    provider_name,
                    task_type,
                )

                response = await provider.generate_structured(
                    prompt,
                    schema,
                    model_override=model,
                )

                return {
                    "success": True,
                    "provider": provider_name,
                    "model": model,
                    "response": response,
                    "attempts": attempt_history,
                }

            except Exception as exc:

                error_text = str(exc) or repr(exc)

                logger.warning(
                    "Structured provider %s failed for task %s: %s",
                    provider_name,
                    task_type,
                    error_text,
                )

                quota_manager.report_error(
                    provider_name,
                    error_text,
                )

                attempt_history.append(
                    {
                        "provider": provider_name,
                        "error": error_text,
                        "model": model,
                    }
                )

                last_error = exc

        return {
            "success": False,
            "error": "All providers failed for structured output",
            "last_error": (
                str(last_error)
                if last_error
                else None
            ),
            "attempts": attempt_history,
            "is_all_failed": True
        }

    def _get_ordered_providers(
        self,
        task_type: str,
    ) -> List[AIProvider]:
        """Returns active providers ordered by priority for the given task type."""
        active = self.active_providers

        if task_type == "complex":
            # Gemini has priority for complex tasks
            return sorted(
                active,
                key=lambda p: p.get_name() != "Gemini",
            )
        else:
            # Local first for simple and normal tasks
            return sorted(
                active,
                key=lambda p: p.get_name() != "Ollama Local",
            )

    def _get_model_for_task(
        self,
        provider_name: str,
        task_type: str,
    ) -> Optional[str]:

        if provider_name == "Gemini":
            return (
                settings.GEMINI_FAST_MODEL
                if task_type == "simple"
                else settings.GEMINI_MODEL
            )

        if provider_name == "Ollama Local":
            if task_type == "simple":
                return settings.OLLAMA_QWEN_MODEL
            # Default to Gemma for normal/complex (failover logic in orchestrator will move to Gemini if needed)
            return settings.OLLAMA_GEMMA_MODEL

        return None

    async def get_health_status(
        self,
    ) -> Dict[str, Any]:

        results = {}

        for provider in self.providers:

            if provider.is_enabled():

                try:
                    results[provider.get_name()] = (
                        await provider.check_health()
                    )

                except Exception as exc:

                    results[provider.get_name()] = {
                        "status": "unavailable",
                        "error": str(exc) or repr(exc),
                    }

            else:

                results[provider.get_name()] = {
                    "status": "disabled"
                }

        return results
