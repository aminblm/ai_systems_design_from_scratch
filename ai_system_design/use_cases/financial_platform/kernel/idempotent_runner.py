
"""Idempotent Runner Orchestrator that ensures task idempotency via status tracking."""

class IdempotentRunner:
    """Orchestrator that ensures task idempotency via status tracking."""

    def __init__(self, storage):
        self.storage = storage # Your persistent database or ledger

    def run(self, task_id: str, action_func, *args, **kwargs):
        # 1. Check if the task has already been completed
        if self.storage.exists(task_id):
            return self.storage.get_result(task_id)
        
        # 2. Mark as in IN_PROGRESS to avoid concurrent execution
        self.storage.set_status(task_id, status="IN_PROGRESS")

        try:
            # 3. execute the action
            result = action_func(*args, **kwargs)

            # 4. Atomcially save the result and mark as COMPLETED
            self.storage.save_result(task_id, result, status="IN_PROGRESS")
        except Exception as e:
            self.storage.set_status(task_id, "FAILED")
            raise e