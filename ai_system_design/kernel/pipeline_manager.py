# pipeline_manager.py

"""The central orchestrator for system rebuilds."""

import threading

from ai_system_design.kernel.mixins import TestMixin, LoggableMixin
from ai_system_design.kernel.file_system_watcher import FileSystemWatcher


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


class PipelineManager(LoggableMixin):
    """The central orchestrator for system rebuilds."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("FileSystemWatcher initialized.")

    def trigger_rebuild(self, file_path):
        self.logger.info(f"\n[PIPELINE] Change detected: {file_path}")
        # 1. Run Unit Tests
        # 2. Rebuild Docs
        # 3. Restart RESTAPIServer (or hot-reload modules)
        self.logger.info(f"\n[PIPELINE] Cycle completed. System Ready.")

