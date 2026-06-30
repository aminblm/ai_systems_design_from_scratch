from abc import ABC, abstractmethod
from typing import Dict

class BaseTool(ABC):
    """Standardized interface for all platform modules."""
    
    @abstractmethod
    def execute(self, params: Dict):
        pass