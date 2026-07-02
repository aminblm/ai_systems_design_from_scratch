# test_pipeline_manager.py

"""The central orchestrator for system rebuilds."""

import threading

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.file_system_watcher import FileSystemWatcher
from ai_system_design.kernel.pipeline_manager import PipelineManager


class TestPipelineManager(TestMixin):
    """TestPipelineManager Class."""

    def __init__(self):
        """TestPipelineManager Constructor."""
        super().__init__()
        self.logger.info("TestPipelineManager initialized.")

    def test(self):
        """TestPipelineManager Test."""
        super().test()
        PATH_TO_WATCH = "ai_system_design/kernel"
        def start_dev_loop(path_to_watch):
            manager = PipelineManager()
            watcher = FileSystemWatcher(path_to_watch)

            # Run watcher in a background thread to keep kernel responsive
            thread = threading.Thread(target=watcher.watch, args=(manager.trigger_rebuild,), daemon=True)
            thread.start()
            self.logger.info(f"[KERNEL] Development loop active on: {path_to_watch}")

        start_dev_loop(PATH_TO_WATCH)

