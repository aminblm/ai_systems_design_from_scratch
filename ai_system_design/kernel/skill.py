
"""Universal contract for an executable capability."""

from abc import ABC, abstractmethod
from typing import Any, Dict

class Skill(ABC):
    """Universal contract for an executable capability."""

    @abstractmethod
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardized skill execution.
        Must always return a status and result payload.
        """
        pass


# Example of a specialized Skill implementation
class DataFetchSkill(Skill):
    def execute(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Example Execute
        """
        try:
            # 1. Validation logic
            if "query" not in params:
                return {"status": "error", "message": "Missing required param: query"}
            
            # 2. Perform logic
            result = f"Data for {params['query']}"

            # 3. Return structured status
            return {"status": "success", "data": result}
        except Exception as e:
            return {"status": "error", "message": str(e)}