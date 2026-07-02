from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.doc_engine import DocEngine


class TestDocEngine(TestMixin):
    """TestDocEngine Class."""

    def __init__(self) -> None:
        """TestDocEngine `__init__(self) -> None` Constructor."""
        super().__init__()

    def test(self) -> None:
        """TestDocEngine `test(self) -> None` test method."""
        super().test()
        SRC_PATH = "ai_system_design"
        DOCUMENTATION_PATH = "docs/ARCHITECTURE.md"
        DOCUMENTATION_PATH_TEST = "test/sg_input/ARCHITECTURE.md"

        DocEngine().generate_manifest(SRC_PATH, DOCUMENTATION_PATH)
        DocEngine().generate_manifest(SRC_PATH, DOCUMENTATION_PATH_TEST)
