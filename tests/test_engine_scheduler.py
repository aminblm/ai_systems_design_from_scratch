# engine_scheduler.py

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.modules.engine_scheduler import EngineScheduler, Task, DAG

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
