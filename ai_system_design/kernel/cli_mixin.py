# test_mixin.py

"""TextMixin class to be inherited as a contract for the CLI classe interfaces of the modules."""

from abc import ABC, abstractmethod
import argparse

from ai_system_design.kernel.loggable_mixin import LoggableMixin


class CLIMixin(LoggableMixin, ABC):
    """Test Mixin Contract class for all module testing."""

    def __init__(self) -> None:
        """CLIMixin Constructor to initialize the test states."""
        super().__init__()
        self.parser = argparse.ArgumentParser(description="Test AI Systems Design")
        self.logger.info("CLIMixin initialized.")

    @abstractmethod
    def cli(self) -> None:
        """CLI method for all CLI Interface classes."""
        self.logger.info(f"[{self.__class__.__name__}] CLI Interface started.")

    def __repr__(self) -> str:
        """A representation of the CLIMixin class."""
        return str(self.__dict__)