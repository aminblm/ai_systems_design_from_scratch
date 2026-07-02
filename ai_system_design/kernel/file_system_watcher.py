# file_watcher.py

"""A recursive, zero-dependency file system monitor."""

import os, time
from typing import Dict, Callable

from ai_system_design.kernel.mixins import LoggableMixin
     

class FileSystemWatcher(LoggableMixin):
    """A recursive, zero-dependency file system monitor."""
    def __init__(self, path_to_watch: str, interval: int = 1) -> None:
        super().__init__()
        self.path = path_to_watch
        self.interval = interval
        self._state = self._scan()

    def _scan(self) -> Dict:
        """Build a snapshot of files and their modification time."""
        snapshot = {}
        for root, _, files in os.walk(self.path):
            for file in files:
                if file.endswith(".py"):
                    full_path = os.path.join(root, file)
                    snapshot[full_path] = os.path.getmtime(full_path)
        return snapshot
    
    def watch(self, callback: Callable) -> Dict:
        """Poll the file system for changes."""
        while True:
            self.logger.info(f"Listening on changes on {self.path}...")
            time.sleep(self.interval)
            current_state = self._scan()

            # Detect changes or new files
            for path, mtime in current_state.items():
                if path not in self._state or mtime > self._state[path]:
                    callback(path)

            self._state = current_state

    
