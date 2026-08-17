from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class AIProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, model_override: Optional[str] = None) -> str:
        """Generates a text response based on a prompt."""
        pass

    @abstractmethod
    async def generate_structured(self, prompt: str, schema: Dict[str, Any], model_override: Optional[str] = None) -> Dict[str, Any]:
        """Generates a structured JSON response based on a schema."""
        pass

    @abstractmethod
    async def generate_embeddings(self, text: str) -> List[float]:
        """Generates embeddings for a given text."""
        pass

    @abstractmethod
    async def check_health(self) -> Dict[str, Any]:
        """Checks the health of the provider."""
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Returns the provider name."""
        pass

    @abstractmethod
    def is_enabled(self) -> bool:
        """Returns True if the provider is enabled in config."""
        pass
