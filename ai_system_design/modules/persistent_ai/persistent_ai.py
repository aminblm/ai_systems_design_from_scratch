# persistent_ai.py
import os, uuid
from typing import Callable, Dict, Any

from ai_system_design.kernel.mixins import JSONSerializableMixin

BASE_PATH = "ai_system_design/modules/persistent_ai/"

class PersistentScheduler(JSONSerializableMixin):
    """Ensures task state survives system reboots."""
    def __init__(self, state_file=f"{BASE_PATH}system_state.json") -> None:
        super().__init__()
        self.state_file = state_file
        self.tasks = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            with open(self.state_file, 'r') as f:
                return self.load(f)
        return {}
    
    def _save_state(self) -> None:
        with open(self.state_file, 'w') as f:
            self.dump(self.tasks, f)

    def schedule_task(self, model_id: str, payload: Any) -> str:
        task_id = str(uuid.uuid4())
        self.tasks[task_id] = {"model": model_id, "data": payload, "status": "PENDING"}
        self._save_state()
        return task_id
    
    def update_status(self, task_id: str, status: str) -> None:
        if task_id in self.tasks:
            self.tasks[task_id]["status"] = status
            self._save_state()


class DurableStorage:
    """Ensures binary data survives ephemeral AI runs."""
    def __init__(self, base_path=f"{BASE_PATH}data"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)

    def persist(self, key: str, data: bytes):
        with open(os.path.join(self.base_path, key), 'wb') as f:
            f.write(data)


class AIHost:
    def __init__(self, scheduler: PersistentScheduler, storage: DurableStorage) -> None:
        self.scheduler = scheduler
        self.storage = storage

    def run_inference(self, model_func: Callable, data: bytes) -> None:
        # 1. State: Log Task Entry persistently
        task_id = self.scheduler.schedule_task("model_v1", "processed_bytes")

        # 2. Ephemeral: Run Model
        try: 
            result = model_func(data)
            # 3. Durable: Persist output
            self.storage.persist(f"{task_id}.out", result)
            self.scheduler.update_status(task_id, "COMPLETED")
        except Exception:
            self.scheduler.update_status(task_id, "FAILED")


# Example execution
storage = DurableStorage()
scheduler = PersistentScheduler()
host = AIHost(scheduler, storage)
host.run_inference(lambda x: x.upper(), b"inference_result")