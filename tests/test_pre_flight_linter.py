# test_pre_flight_linter.py

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.pre_flight_linter import PreFlightLinter


class TestPreFlightLinter(TestMixin):
    """TestPreFlightLinter Class."""

    def __init__(self):
        """TestPreFlightLinter Constructor."""
        super().__init__()
        self.logger.info("TestPreFlightLinter initialized.")

    def test(self):
        """TestPreFlightLinter Test."""
        super().test()
        MODULE_PATH = "ai_system_design/kernel/test_mixin.py"

        linter = PreFlightLinter()
        status = linter.check_file(MODULE_PATH)

        if status != "PASS":
            raise SystemError(status)
