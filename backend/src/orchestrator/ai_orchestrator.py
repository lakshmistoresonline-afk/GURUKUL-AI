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

        routing = self._get_task_routing(task_type)
        if not routing:
            raise AllProvidersUnavailableError("No AI providers are currently enabled or available for this task.")

        for entry in routing:
            provider = entry["provider"]
            provider_name = provider.get_name()
            model = entry["model"]

            try:
                logger.info(
                    "Routing request to %s (%s) for task %s",
                    provider_name,
                    model,
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

        routing = self._get_task_routing(task_type)
        if not routing:
            raise AllProvidersUnavailableError("No AI providers are currently enabled or available for structured output.")

        for entry in routing:
            provider = entry["provider"]
            provider_name = provider.get_name()
            model = entry["model"]

            try:
                logger.info(
                    "Routing structured request to %s (%s) for task %s",
                    provider_name,
                    model,
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

    def _get_task_routing(self, task_type: str) -> List[Dict[str, Any]]:
        """Returns a list of (provider, model) pairs for the given task type, respecting priority and availability."""

        # Get enabled and available providers
        providers = {p.get_name(): p for p in self.providers if p.is_enabled() and quota_manager.is_available(p.get_name())}

        # Model Shortcuts
        groq_model = settings.GROQ_MODEL
        nv_gpt_oss = settings.NVIDIA_GPT_OSS_MODEL
        nv_minimax = settings.NVIDIA_MINIMAX_MODEL
        or_kimi_k3 = settings.OPENROUTER_KIMI_K3_MODEL
        or_kimi_k26 = settings.OPENROUTER_KIMI_K26_MODEL
        or_kimi_code = settings.OPENROUTER_KIMI_CODE_MODEL
        or_nemotron_lightning = settings.OPENROUTER_NEMOTRON_LIGHTNING_MODEL
        or_nemotron_ultra = settings.OPENROUTER_NEMOTRON_ULTRA_MODEL
        gemini_model = settings.GEMINI_MODEL
        gemini_fast = settings.GEMINI_FAST_MODEL

        # Task specific sequences (Provider Name, Model ID)
        task_map = {
            "simple": [
                ("Groq", groq_model),
                ("OpenRouter", or_kimi_k3),
                ("Gemini", gemini_fast)
            ],
            "general": [
                ("Groq", groq_model),
                ("OpenRouter", or_kimi_k3),
                ("Gemini", gemini_model)
            ],
            "normal_coding": [
                ("Groq", groq_model),
                ("NVIDIA", nv_gpt_oss),
                ("OpenRouter", or_kimi_code)
            ],
            "complex": [
                ("NVIDIA", nv_gpt_oss),
                ("OpenRouter", or_kimi_k3),
                ("Groq", groq_model)
            ],
            "reasoning": [
                ("NVIDIA", nv_gpt_oss),
                ("OpenRouter", or_kimi_k3),
                ("OpenRouter", or_nemotron_ultra)
            ],
            "large_context": [
                ("OpenRouter", or_nemotron_lightning),
                ("OpenRouter", or_kimi_k3),
                ("NVIDIA", nv_gpt_oss),
                ("Groq", groq_model)
            ],
            "agentic_coding": [
                ("OpenRouter", or_kimi_code),
                ("NVIDIA", nv_gpt_oss),
                ("Groq", groq_model)
            ],
            "vision": [
                ("OpenRouter", or_kimi_k26),
                ("Gemini", gemini_model)
            ],
            "advanced_reasoning": [
                ("OpenRouter", or_nemotron_ultra),
                ("OpenRouter", or_kimi_k3),
                ("NVIDIA", nv_gpt_oss)
            ],
            "agentic_reasoning": [
                ("NVIDIA", nv_minimax),
                ("OpenRouter", or_nemotron_ultra),
                ("OpenRouter", or_kimi_k3),
                ("NVIDIA", nv_gpt_oss)
            ],
            "android": [
                ("Gemini", gemini_model),
                ("Groq", groq_model),
                ("NVIDIA", nv_gpt_oss),
                ("OpenRouter", or_kimi_code)
            ]
        }

        sequence = task_map.get(task_type, [("Groq", groq_model), ("NVIDIA", nv_gpt_oss), ("OpenRouter", or_kimi_k3)])

        routing = []
        for p_name, model_id in sequence:
            if p_name in providers:
                routing.append({
                    "provider": providers[p_name],
                    "model": model_id
                })

        return routing

    def _get_ordered_providers(
        self,
        task_type: str,
    ) -> List[AIProvider]:
        """Deprecated: Use _get_task_routing instead."""
        routing = self._get_task_routing(task_type)
        return [r["provider"] for r in routing]

    def _get_model_for_task(
        self,
        provider_name: str,
        task_type: str,
    ) -> Optional[str]:
        """Deprecated: Use _get_task_routing instead."""
        routing = self._get_task_routing(task_type)
        for r in routing:
            if r["provider"].get_name() == provider_name:
                return r["model"]
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
