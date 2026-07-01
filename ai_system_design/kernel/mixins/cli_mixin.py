# cli_mixin.py

"""CLIMixin class to be inherited as a contract for the CLI classe interfaces of the modules."""

from abc import ABC, abstractmethod
import argparse

from ai_system_design.kernel.mixins.loggable_mixin import LoggableMixin


class CLIMixin(LoggableMixin, ABC):
    """CLI Mixin Contract class for all module testing."""

    def __init__(self) -> None:
        """CLIMixin `__init__(self) -> None` Constructor to initialize the cli states."""
        super().__init__()
        self.parser = argparse.ArgumentParser(description="CLI Interface for AI Systems Design")
        self.logger.info("CLIMixin initialized.")

    @abstractmethod
    def cli(self) -> None:
        """CLI `cli(self) -> None` method for all CLI Interface classes."""
        self.logger.info(f"[{self.__class__.__name__}] CLI Interface started.")

    def __repr__(self) -> str:
        """A representation `__repr__(self) -> str` of the CLIMixin class."""
        return str(self.__dict__)