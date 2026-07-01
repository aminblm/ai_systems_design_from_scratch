# doc_engine.py

"""Generates documentation automatically."""

import ast, os 

from ai_system_design.kernel.test_mixin import TestMixin
from ai_system_design.kernel.debugger import Debugger


class TestDocEngine(TestMixin):
    def __init__(self):
        super().__init__()
        self.logger.info("TestDocEngine initialized.")

    def test(self):
        super().test()
        SRC_PATH = "ai_system_design"
        DOCUMENTATION_PATH = "docs/ARCHITECTURE.md"
        DOCUMENTATION_PATH_TEST = "test/sg_input/ARCHITECTURE.md"

        DocEngine().generate_manifest(SRC_PATH, DOCUMENTATION_PATH)
        DocEngine().generate_manifest(SRC_PATH, DOCUMENTATION_PATH_TEST)


class DocEngine:
    """Extracts metadata from source to build automated docs."""

    def generate_manifest(self, folder_path, docs_path):
        output = '# System Architecture\n\n'
        for root, _, files, in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    output += self._parse_file(os.path.join(root, file))

        index = "\n".join(["- [{}]({})".format(line.replace("## File: ", ''), line.lower().replace(":", '').replace("`", '').replace(' ', '-')) for line in output.splitlines() if line.startswith("##")])
        
        # Debugger().debug('index', index)

        output = output.replace("# System Architecture\n\n", '# System Architecture\n\n## Table of Contents\n\n' + index + '\n\n')

        with open(docs_path, "w") as f:
            f.write(output)

    def _parse_file(self, file_path: str):
        summary = ""
        with open(file_path, 'r') as f:
            try:
                tree = ast.parse(f.read())
                summary += f"\n## File: `{os.path.basename(file_path)}`\n\n"
                summary += f"> {ast.get_docstring(tree) or 'Upcoming documentation'}\n\n"

                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        summary += f"**`{node.name}`**\n\n"
                        summary += f"> {ast.get_docstring(node) or 'Upcoming documentation'}\n"
            except Exception:
                Debugger().debug('file_path', file_path)
        
        return summary