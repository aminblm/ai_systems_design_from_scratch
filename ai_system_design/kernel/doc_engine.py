# doc_engine.py

"""Documentation Engine to Generate documentation automatically."""

import ast, os 

from ai_system_design.kernel.mixins import TestMixin, LoggableMixin, CLIMixin
from ai_system_design.kernel.debugger import Debugger


class DocEngineCLI(CLIMixin):
    """DocEngineCLI Class."""

    def __init__(self) -> None:
        """DocEngineCLI `__init__(self) -> None` Constructor."""
        super().__init__()
        self.parser.add_argument("--source", required=True)
        self.parser.add_argument("--output-path", required=True)
        self.parser.add_argument("--secondary-output-path", required=False)
        self.logger.info("DocEngineCLI initialized.")
    
    def cli(self):
        """Usage: `cli.py [-h] --source SOURCE --output-path OUTPUT_PATH [--secondary-output-path SECONDARY_OUTPUT_PATH]`"""
        super().cli()
        args = self.parser.parse_args()

        DocEngine().generate_manifest(args.source, args.output_path)
        if args.secondary_output_path:
            DocEngine().generate_manifest(args.source,  args.secondary_output_path)


class TestDocEngine(TestMixin):
    """TestDocEngine Class."""

    def __init__(self) -> None:
        """TestDocEngine `__init__(self) -> None` Constructor."""
        super().__init__()
        self.logger.info("TestDocEngine initialized.")

    def test(self) -> None:
        """TestDocEngine `test(self) -> None` test method."""
        super().test()
        SRC_PATH = "ai_system_design"
        DOCUMENTATION_PATH = "docs/ARCHITECTURE.md"
        DOCUMENTATION_PATH_TEST = "test/sg_input/ARCHITECTURE.md"

        DocEngine().generate_manifest(SRC_PATH, DOCUMENTATION_PATH)
        DocEngine().generate_manifest(SRC_PATH, DOCUMENTATION_PATH_TEST)


class DocEngine(LoggableMixin):
    """Extracts metadata from source to build automated docs."""

    def __init__(self) -> None:
        """DocEngine `__init__(self) -> None` Constructor."""
        super().__init__()
        self.logger.info("DocEngine initiated.")

    def generate_manifest(self, folder_path: str, docs_path: str) -> None:
        """DocEngine `generate_manifest(self, folder_path: str, docs_path: str) -> None` method."""
        output = '# System Architecture\n\n'
        for root, _, files, in os.walk(folder_path):
            for file in files:
                if file.endswith(".py"):
                    output += self._parse_file(os.path.join(root, file))

        index = "\n".join(["- [{}]({})".format(line.replace("## File: ", ''), line.lower().replace(":", '').replace("`", '').replace(' ', '-')) for line in output.splitlines() if line.startswith("## ")])
        output = output.replace("# System Architecture\n\n", '# System Architecture\n\n## Table of Contents\n\n' + index + '\n\n')

        with open(docs_path, "w") as f:
            f.write(output)
            self.logger.info(f'System Architecture successfully generated at: {docs_path}')

    def _parse_file(self, file_path: str) -> str:
        """DocEngine `_parse_file(file_path: str) -> str` internal method."""
        summary = ""
        with open(file_path, 'r') as f:
            try:
                tree = ast.parse(f.read())
                summary += f"\n## File: `{os.path.basename(file_path)}`\n\n"
                summary += f"> {ast.get_docstring(tree) or 'Upcoming documentation'}\n\n"

                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        summary += f"### `{node.name}`\n\n"
                        summary += f"> {ast.get_docstring(node) or 'Upcoming documentation'}\n"

                    if isinstance(node, ast.FunctionDef):
                        summary += f"**`{node.name}`**\n\n"
                        summary += f"> {ast.get_docstring(node) or 'Upcoming documentation'}\n"
            except Exception:
                Debugger().debug('file_path', file_path)
        
        return summary