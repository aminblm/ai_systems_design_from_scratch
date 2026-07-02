# test_file_watcher.py

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.file_system_watcher import FileSystemWatcher

class TestFileSystemWatcher(TestMixin):
    """TestFileSystemWatcher Class."""
    def __init__(self):
        """TestFileSystemWatcher Constructor."""
        super().__init__()

    def test(self):
        """TestFileSystemWatcher Test."""
        super().test()
        PATH_TO_WATCH = "ai_system_design/kernel"
        def on_change(file_path):
            self.logger.info(f"Change detected: {file_path}. Triggering build...")

        watcher = FileSystemWatcher(PATH_TO_WATCH)
        watcher.watch(on_change)
        