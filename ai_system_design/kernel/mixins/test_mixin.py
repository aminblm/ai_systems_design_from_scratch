# test_mixin.py

"""TextMixin class to be inherited as a contract for the testing classes testing the modules."""

from abc import ABC, abstractmethod

from ai_system_design.kernel.mixins import LoggableMixin


class TestMixin(LoggableMixin, ABC):
    """Test Mixin Contract class for all module testing."""

    def __init__(self) -> None:
        """TestMixin Constructor to initialize the test states."""
        super().__init__()
        self.logger.info("TestMixin initialized.")

    @abstractmethod
    def test(self) -> None:
        """Test method for all testing classes."""
        self.logger.info(f"Running {self.__class__.__name__} Tests ...")

    def __repr__(self) -> str:
        """A representation of the TestMixin class."""
        return str(self.__dict__)