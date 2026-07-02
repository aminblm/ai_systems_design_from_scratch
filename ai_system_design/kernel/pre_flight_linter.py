
"""Blocks code that violates architectural standards."""

import ast


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
    