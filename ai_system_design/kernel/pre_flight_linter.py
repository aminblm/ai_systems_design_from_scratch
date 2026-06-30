# pre_flight_linter.py


import ast

from ai_system_design.kernel.test_mixin import TestMixin


class TestPreFlightLinter(TestMixin):
    def __init__(self):
        super().__init__()
        self.logger.info("TestPreFlightLinter initialized.")

    def test(self):
        super().test()
        MODULE_PATH = "ai_system_design/kernel/test_mixin.py"

        linter = PreFlightLinter()
        status = linter.check_file(MODULE_PATH)

        if status != "PASS":
            raise SystemError(status)


class PreFlightLinter:
    """Blocks code that violates architectural standards."""

    def check_file(self, file_path: str):
        with open(file_path, 'r') as f:
            tree = ast.parse(f.read())

        # Rule: prevent direct imports bypassing the ai_system_design
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if "os" in alias.name or "subprocess" in alias.name:
                        return f"Architectural violation: Direct use of {alias.name} prohibited."
                    
        # Rule: Enforce Docstrings
        if not ast.get_docstring(tree):
            return "Quality violation: Missing module docstring."
        
        return "PASS"
    