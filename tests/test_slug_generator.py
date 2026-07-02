from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.slug_generator import JekyllFilenameController


class TestSlugGenerator(TestMixin):
    """Test the slug_generator module functionality."""

    def __init__(self) -> None:
        super().__init__()

    def test(self):
        super().test()
        JekyllFilenameController().start_generator_interface()