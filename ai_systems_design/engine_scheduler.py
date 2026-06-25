# engine_scheduler.py
import time, logging
from dataclasses import dataclass, field
from typing import Callable, Set, Dict

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class Task:
    name: str
    execute_func: Callable[[], None]
    interval_seconds: int = 5
    # Keep track of names of tasks that MUST run before this one
    upstream_dependencies: Set[str] = field(default_factory=set)


class DAG:
    """Represents a Directed Acyclic Graph of tasks and enforces structural integrity."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.downstream_edges: Dict[str, Set[str]] = {}

    def add_task(self, task: Task) -> None:
        if task.name in self.tasks:
            raise ValueError(f"Task '{task.name} already exists in DAG '{self.name}'.")
        
        self.tasks[task.name] = task
        if task.name not in self.downstream_edges:
            self.downstream_edges[task.name] = set()

        # Link dependencies structurally
        for upstream in task.upstream_dependencies:
            if upstream not in self.downstream_edges:
                self.downstream_edges[upstream] = set()
            self.downstream_edges[upstream].add(task.name)

    def validate_graph(self) -> bool:
        """Simple cycle detection via DFS to guarantee the graph is acyclic."""
        visited = set()
        rec_stack = set()

        def has_cycle(node: str) -> bool:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.downstream_edges.get(node, set()):
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
            return False
        
        for task_name in self.tasks:
            if task_name not in visited:
                if has_cycle(task_name):
                    raise ValueError(f"Cyclic dependency detected in DAG '{self.name}'!")
        return True


class EngineScheduler:
    """Orchestrates DAG tasks using non-blocking structural evaluations."""

    def __init__(self, dag: DAG) -> None:
        dag.validate_graph()
        self.dag = dag
        self.completed_tasks: Set[str] = set()
        self.last_run_times: Dict[str, float] = {}

    def _is_run_due(self, task: Task, current_timestamp: float) -> bool:
        """Determines if a task is chronologically due for evaluation."""
        last_run = self.last_run_times.get(task.name, 0.0)
        return (current_timestamp - last_run) >=  task.interval_seconds
    
    def _dependencies_satisfied(self, task: Task) -> bool:
        """Verifies if all upstream constrains have completed successfully."""
        return task.upstream_dependencies.issubset(self.completed_tasks)

    def step(self) -> None:
        """A single non-blocking evaluation pass over all tasks."""
        now = time.time()

        for task in self.dag.tasks.values():
            if not self._is_run_due(task, now):
                continue

            if not self._dependencies_satisfied(task):
                logger.debug(f"Task '{task.name}' skipped; upstream deps not met.")
                continue

            # Execute the workload safely
            logger.info(f"Executing Task: {task.name}")
            try:
                task.execute_func()
                self.completed_tasks.add(task.name)
                self.last_run_times[task.name] = now
            except Exception as e:
                logger.error(f"Task '{task.name}' failed with error: {e}")

    def run_forever(self, tick_rate_seconds: float = 1.0) -> None:
        """Runs the loop without causing a single task execution to block the cycle clock."""
        logger.info(f"Scheduler started for DAG: {self.dag.name}")
        try:
            while True:
                self.step()
                time.sleep(tick_rate_seconds)
        except KeyboardInterrupt:
            logger.info("Scheduler stopped cleanly.")

