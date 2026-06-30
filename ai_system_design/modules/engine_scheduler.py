# engine_scheduler.py
import time
from dataclasses import dataclass, field
from typing import Callable, Set, Dict

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestEngineScheduler(TestMixin):
    """Test the engine_scheduler module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestGenerateSite initialized.")

    def test(self):
        super().test()
        # Define clean decoupled topology
        sample_dag = DAG("Production_pipeline")

        def extract(): self.logger.info("[DB] Extracting raw ingestion assets...")
        def transform(): self.logger.info("[Spark] Normalizing structural records...")
        def load(): self.logger.info("[Warehouse] Committing target delta changes...")

        task_a = Task("Extract_Data", execute_func=extract, interval_seconds=3)
        task_b = Task("Transform_Data", execute_func=transform, interval_seconds=3, upstream_dependencies={"Extract_Data"})
        task_c = Task("Load_Data", execute_func=load, interval_seconds=3, upstream_dependencies={"Transform_Data"})

        sample_dag.add_task(task_a)
        sample_dag.add_task(task_b)
        sample_dag.add_task(task_c)

        scheduler = EngineScheduler(sample_dag)
        # Run the execution agent loop
        scheduler.run_forever(tick_rate_seconds=0.5)


@dataclass
class Task(LoggableMixin):
    """Task classe to instanciate classes."""
    def __init__(self, name: str, execute_func: Callable[[], None], interval_seconds: int, upstream_dependencies: Set[str] = set()) -> None:
        super().__init__()
        self.name = name
        self.execute_func = execute_func
        self.interval_seconds = interval_seconds
        self.upstream_dependencies = upstream_dependencies
        self.logger.info("Task initialized.")    


class DAG(LoggableMixin):
    """Represents a Directed Acyclic Graph of tasks and enforces structural integrity."""

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.tasks: Dict[str, Task] = {}
        self.downstream_edges: Dict[str, Set[str]] = {}
        self.logger.info("DAG initialized.")

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


class EngineScheduler(LoggableMixin):
    """Orchestrates DAG tasks using non-blocking structural evaluations."""

    def __init__(self, dag: DAG) -> None:
        super().__init__()
        dag.validate_graph()
        self.dag = dag
        self.completed_tasks: Set[str] = set()
        self.last_run_times: Dict[str, float] = {}
        self.logger.info("EngineScheduler initialized.")

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
                self.logger.debug(f"Task '{task.name}' skipped; upstream deps not met.")
                continue

            # Execute the workload safely
            self.logger.info(f"Executing Task: {task.name}")
            try:
                task.execute_func()
                self.completed_tasks.add(task.name)
                self.last_run_times[task.name] = now
            except Exception as e:
                self.logger.error(f"Task '{task.name}' failed with error: {e}")

    def run_forever(self, tick_rate_seconds: float = 1.0) -> None:
        """Runs the loop without causing a single task execution to block the cycle clock."""
        self.logger.info(f"Scheduler started for DAG: {self.dag.name}")
        try:
            while True:
                self.step()
                time.sleep(tick_rate_seconds)
        except KeyboardInterrupt:
            self.logger.info("Scheduler stopped cleanly.")

