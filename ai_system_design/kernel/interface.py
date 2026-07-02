
"""The central contract for all system modules."""

from abc import ABC, abstractmethod
from typing import Dict

class ModuleInterface(ABC):
    """The central contract for all system modules."""

    @abstractmethod
    def start(self) -> None:
        """Initializes resources."""
        pass

    @abstractmethod
    def stop(self) -> None:
        """Gracefully releases resources."""
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, str]:
        """Returns operational health data."""
        pass


# Example: Implementing the contract
class EventBusModule(ModuleInterface):
    def start(self): print("Bus starting...")
    def stop(self): print("Bus stopping...")
    def get_status(self) -> Dict[str, str]: return {"status": "running"}