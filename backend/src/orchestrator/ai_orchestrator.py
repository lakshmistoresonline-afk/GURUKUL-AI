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
from ..providers.nvidia import NvidiaProvider
from ..config.app_config import settings
from .quota_manager import quota_manager


logger = logging.getLogger(__name__)


class AllProvidersUnavailableError(Exception):
    """Raised when no AI providers are currently available or all failed."""
    pass


class AIOrchestrator:

    def __init__(self):
        self.providers: List[AIProvider] = [
            GroqProvider(),
            NvidiaProvider(),
            OpenRouterProvider(),
            GeminiProvider(),
            OllamaCloudProvider(),
            OllamaLocalProvider(),
            CerebrasProvider(),
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
        active = {p.get_name(): p for p in self.active_providers}

        # Priority mapping
        priorities = {
            "simple": ["Groq", "OpenRouter", "NVIDIA", "Gemini"],
            "general": ["Groq", "OpenRouter", "NVIDIA", "Gemini"],
            "normal_coding": ["Groq", "NVIDIA", "OpenRouter", "Gemini"],
            "complex": ["NVIDIA", "OpenRouter", "Gemini"],
            "reasoning": ["NVIDIA", "OpenRouter", "Gemini"],
            "large_context": ["NVIDIA", "OpenRouter", "Gemini"],
            "agentic_coding": ["OpenRouter", "NVIDIA", "Gemini"],
            "vision": ["OpenRouter", "Gemini"],
            "advanced_reasoning": ["OpenRouter", "NVIDIA", "Gemini"],
            "agentic_reasoning": ["NVIDIA", "OpenRouter", "Gemini"],
            "android": ["Gemini", "Groq", "NVIDIA", "OpenRouter"]
        }

        order = priorities.get(task_type, ["Groq", "NVIDIA", "OpenRouter", "Gemini"])

        # Build final list based on order, appending any remaining active providers
        result = []
        seen = set()
        for name in order:
            if name in active:
                result.append(active[name])
                seen.add(name)

        for name, provider in active.items():
            if name not in seen:
                result.append(provider)

        return result

    def _get_model_for_task(
        self,
        provider_name: str,
        task_type: str,
    ) -> Optional[str]:

        if provider_name == "Groq":
            # Groq is prioritized for speed/efficiency
            return settings.GROQ_MODEL

        if provider_name == "NVIDIA":
            if task_type in ["complex", "reasoning", "agentic_coding"]:
                return settings.NVIDIA_GPT_OSS_MODEL
            if task_type in ["large_context", "advanced_reasoning"]:
                return settings.NVIDIA_DEEPSEEK_MODEL
            if task_type == "agentic_reasoning":
                return settings.NVIDIA_MINIMAX_MODEL
            return settings.NVIDIA_GPT_OSS_MODEL

        if provider_name == "OpenRouter":
            if task_type == "vision":
                return settings.OPENROUTER_KIMI_K26_MODEL
            if task_type in ["advanced_reasoning", "complex", "reasoning", "agentic_reasoning", "large_context"]:
                return settings.OPENROUTER_KIMI_K3_MODEL
            if task_type == "agentic_coding":
                return settings.OPENROUTER_KIMI_CODE_MODEL
            return settings.OPENROUTER_MODEL

        if provider_name == "Gemini":
            if task_type == "simple":
                return settings.GEMINI_FAST_MODEL
            return settings.GEMINI_MODEL

        if provider_name == "Ollama Local":
            if task_type == "simple":
                return settings.OLLAMA_QWEN_MODEL
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
