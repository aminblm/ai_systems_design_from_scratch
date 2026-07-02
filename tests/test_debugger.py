# test_debugger.py

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.debugger import Debugger


class TestDebugger(TestMixin):
    """Test the debugger module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestDebugger initialized.")

    def test(self):
        super().test()
        debugger = Debugger()
        debugger.debug("debugger", debugger)