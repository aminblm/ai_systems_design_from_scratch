import logging

from ai_systems_design.site_generator.site_generator import SiteGenerator 
from ai_systems_design.py_slug_generator import SlugGenerator, TerminalInterface
from ai_systems_design.engine_scheduler import Task, DAG, EngineScheduler

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def test_generate_site():
    base_path = 'ai_systems_design/site_generator/'
    test_path = 'test/'
    SiteGenerator(f'{base_path}layout.html', f'{base_path}config.yaml').generate_site(f'{test_path}input')

def test_generate_slugs():
    slug_engine = SlugGenerator()
    interface = TerminalInterface(generator=slug_engine)
    interface.run()

def test_start_engine_scheduler():
    # Define clean decoupled topology
    sample_dag = DAG("Production_pipeline")

    def extract(): logger.info("[DB] Extracting raw ingestion assets...")
    def transform(): logger.info("[Spark] Normalizing structural records...")
    def load(): logger.info("[Warehouse] Committing target delta changes...")

    task_a = Task("Extract_Data", execute_func=extract, interval_seconds=3)
    task_b = Task("Transform_Data", execute_func=transform, interval_seconds=3, upstream_dependencies={"Extract_Data"})
    task_c = Task("Load_Data", execute_func=load, interval_seconds=3, upstream_dependencies={"Transform_Data"})

    sample_dag.add_task(task_a)
    sample_dag.add_task(task_b)
    sample_dag.add_task(task_c)

    scheduler = EngineScheduler(sample_dag)
    # Run the execution agent loop
    scheduler.run_forever(tick_rate_seconds=0.5)

if __name__ == "__main__":
    test_generate_site()
    #test_generate_slugs()
    #test_start_engine_scheduler()