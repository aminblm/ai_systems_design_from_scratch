from abc import ABC, abstractmethod
from typing import Any

class InferenceEngine(ABC):
    """The formal contract for any ML/math model."""

    @abstractmethod
    def preprocess(self, raw_data: bytes) -> Any:
        """Converts raw data to mathematical tensors/arrays."""
        pass

    @abstractmethod
    def predict(self, tensor) -> Any:
        """Performs the heavy computation."""
        pass

    @abstractmethod
    def run(self, raw_data: bytes) -> Any:
        """Unified entry point for inference."""
        tensor = self.preprocess(raw_data)
        prediction = self.predict(tensor)
        return self.format_results(prediction)

    @abstractmethod
    def format_results(self, prediction) -> Any:
        """Translates raw model output into usable data."""
        pass
