# ai_system_component.py

"""The formal AI System Component contract for all platform modules."""


from abc import ABC, abstractmethod
from typing import Dict, Any

class AISystemComponent(ABC):
    """The formal contract for all platform modules."""

    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> bool:
        """Sets up internal state before execution."""
        pass

    @abstractmethod
    def execute(self, task_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Performs the core capability of the module."""
        pass

    @property
    @abstractmethod
    def status(self) -> str:
        """Returns the operational state of the module."""
        pass