# test_process_posts.py

import argparse

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.process_posts import run_pipeline


class TestProcessPosts(TestMixin):
    """Test the process_posts module functionality."""

    def __init__(self) -> None:
        super().__init__()

    def test(self):
        super().test()
        """Example usage> python test.py --input _posts/20260623-in --output _posts/20260623-out"""
        parser = argparse.ArgumentParser(description="Inject metadata and links into Markdown posts.")
        parser.add_argument("--input", required=True, help="Input directory containing markdown files")
        parser.add_argument("--output", required=True, help="Output directory for processed files")
        
        args = parser.parse_args()
        run_pipeline(args.input, args.output)

    