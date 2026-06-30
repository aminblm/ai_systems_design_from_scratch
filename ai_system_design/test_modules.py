# test_modules.py
import argparse
from ai_system_design.kernel.test_mixin import TestMixin


class TestModules(TestMixin):
    """Test all modules implemented."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestModules initialized.")

    def test(self):
        super().test()
        """Example testing module: 
        python test.py --test slug_generator"""

        parser = argparse.ArgumentParser(description="Test AI Systems Design")
        parser.add_argument("--test", required=True)
        args = parser.parse_args()

        match args.test:
            # Frontend
            case "reactive_frontend": 
                from ai_system_design.modules.reactive_frontend import TestReactiveFrontent
                TestReactiveFrontent().test()

            # Load Balancing
            case "round_robin_load_balancer": 
                from ai_system_design.modules.round_robin_load_balancer import TestRoundRobinLoadBalancer
                TestRoundRobinLoadBalancer().test()

            # Sockets
            case "socket_server": 
                from ai_system_design.kernel.socket_server import TestSocketServer
                TestSocketServer().test()
            case "socket_client": 
                from ai_system_design.kernel.socket_client import TestSocketClient
                TestSocketClient().test()

            # REST APIs
            case "rest_api_client": 
                from ai_system_design.modules.rest_api_client import TestRESTAPIClient
                TestRESTAPIClient().test()
            case "rest_api_server": 
                from ai_system_design.modules.rest_api_server import TestRESTAPIServer
                TestRESTAPIServer().test()

            # Git RPC
            case "git_rpc_client": 
                from ai_system_design.modules.git_rpc_client import TestGitRPCClient
                TestGitRPCClient().test()
            case "git_rpc_server": 
                from ai_system_design.modules.git_rpc_server import TestGitRPCServer
                TestGitRPCServer().test()

            # Container Management
            case "container_manager_client": 
                from ai_system_design.modules.container_manager_client import TestContainerManagerClient
                TestContainerManagerClient().test()
            case "container_manager_server": 
                from ai_system_design.modules.container_manager_server import TestContainerManagerServer
                TestContainerManagerServer().test()

            # Databases
            case "scalable_index": 
                from ai_system_design.modules.scalable_index import TestScalableIndex
                TestScalableIndex().test()
            case "distributed_no_sql_database": 
                from ai_system_design.modules.distributed_no_sql_database import TestDistributedNoSQLDatabase
                TestDistributedNoSQLDatabase().test()
            
            # Caching
            case "realtime_redis_engine": 
                from ai_system_design.modules.realtime_redis_engine import TestRealtimeRedisEngine
                TestRealtimeRedisEngine().test()

            # AI - Intent matching enging
            case "intent_matching_engine": 
                from ai_system_design.kernel.intent_matching_engine import TestIntentMatchingEngine
                TestIntentMatchingEngine().test()

            # Tasks Scheduler
            case "engine_scheduler": 
                from ai_system_design.modules.engine_scheduler import TestEngineScheduler
                TestEngineScheduler().test()

            # Site / Blog Posts / Internet Content Generator
            case "generate_site": 
                from ai_system_design.modules.site_generator.site_generator import TestGenerateSite 
                TestGenerateSite().test()
            case "slug_generator": 
                from ai_system_design.modules.slug_generator import TestSlugGenerator
                TestSlugGenerator().test()
            case "safe_yaml_parser": 
                from ai_system_design.modules.safe_yaml_parser import TestSafeYAMLParser
                TestSafeYAMLParser().test()
            case "architecture_renderer": 
                from ai_system_design.modules.architecture_renderer import TestArchitectureRenderer
                TestArchitectureRenderer().test()
            case "process_posts": 
                from ai_system_design.modules.process_posts import TestProcessPosts
                TestProcessPosts().test()

            # Deugger
            case "debugger": 
                from ai_system_design.kernel.debugger import TestDebugger
                TestDebugger().test()

            # File System Watcher
            case "file_system_watcher":
                from ai_system_design.kernel.file_system_watcher import TestFileSystemWatcher
                TestFileSystemWatcher().test()
            case "pipeline_manager":
                from ai_system_design.kernel.pipeline_manager import TestPipelineManager
                TestPipelineManager().test()

            # Linter
            case "pre_flight_linter":
                from ai_system_design.kernel.pre_flight_linter import TestPreFlightLinter
                TestPreFlightLinter().test()

            # Edge-cases
            case _: self.logger.warning("Enter a valid test case.") 
