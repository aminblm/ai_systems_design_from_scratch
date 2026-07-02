from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.site_generator.site_generator import SiteGenerator


class TestGenerateSite(TestMixin):
    """Test the site_generator module functionality."""

    def __init__(self) -> None:
        """TestGenerateSite `__init__(self) -> None` Constructor."""
        super().__init__()
    
    def test(self) -> None:
        """TestGenerateSite `test(self) -> None` test."""
        super().test()

        BASE_PATH = 'ai_system_design/modules/site_generator/'
        DEFAULT_LAYOUT = f'{BASE_PATH}layout.html'
        DEFAULT_CONFIG = f'{BASE_PATH}config.yaml'
        TEST_INPUT_PATH = 'test/sg_input'

        SiteGenerator(DEFAULT_LAYOUT, DEFAULT_CONFIG).generate_site(TEST_INPUT_PATH)
