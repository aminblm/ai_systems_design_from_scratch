# intent_provider.py
from abc import ABC, abstractmethod
from typing import Any

class IntentProvider(ABC):
    """The modular contract for AI providers."""

    @abstractmethod
    def classify(self, text: str) -> Any:
        pass


class IntentMatchingEngine:
    """Orchestrator is now decoupled from the AI."""
    def __init__(self, provider: IntentProvider):
        self.provider = provider

    def get_intent(self, user_input: str) -> Any:
        return self.provider.classify(user_input)


# Example usage
class LocalLLMProvider(IntentProvider):
    def classify(self, text: str) -> str:
        # Here load local model weights
        return "MATCHED_INTENT_FROM_LOCAL_MODEL"