"""Test all modules implemented."""

import argparse, asyncio
from ai_system_design.kernel.mixins import TestMixin


class TestModules(TestMixin):
    """Test all modules implemented."""

    def __init__(self) -> None:
        super().__init__()

    async def test(self):
        super().test()
        
        parser = argparse.ArgumentParser(description="Test AI Systems Design")
        parser.add_argument("--test", required=True)
        args = parser.parse_args()

        match args.test:
            # Deugger
            case "debugger": 
                from tests.test_debugger import TestDebugger
                TestDebugger().test()

            # Frontend
            case "reactive_frontend": 
                from tests.test_reactive_frontend import TestReactiveFrontent
                TestReactiveFrontent().test()

            # Load Balancing
            case "round_robin_load_balancer": 
                from tests.test_round_robin_load_balancer import TestRoundRobinLoadBalancer
                TestRoundRobinLoadBalancer().test()

            # Sockets
            case "socket_server": 
                from tests.test_socket_server import TestSocketServer
                await TestSocketServer().test()
            case "socket_client": 
                from tests.test_socket_client import TestSocketClient
                TestSocketClient().test()

            # REST APIs
            case "rest_api_client": 
                from tests.test_rest_api_client import TestRESTAPIClient
                TestRESTAPIClient().test()
            case "rest_api_server": 
                from tests.test_rest_api_server import TestRESTAPIServer
                await TestRESTAPIServer().test()

            # Git RPC
            case "git_rpc_client": 
                from tests.test_git_rpc_client import TestGitRPCClient
                TestGitRPCClient().test()
            case "git_rpc_server": 
                from tests.test_git_rpc_server import TestGitRPCServer
                await TestGitRPCServer().test()

            # Container Management
            case "container_manager_client": 
                from tests.test_container_manager_client import TestContainerManagerClient
                TestContainerManagerClient().test()
            case "container_manager_server": 
                from tests.test_container_manager_server import TestContainerManagerServer
                await TestContainerManagerServer().test()

            # Databases
            case "scalable_index": 
                from tests.test_scalable_index import TestScalableIndex
                TestScalableIndex().test()
            case "distributed_no_sql_database": 
                from tests.test_distributed_no_sql_database import TestDistributedNoSQLDatabase
                TestDistributedNoSQLDatabase().test()
            
            # Caching
            case "realtime_redis_engine": 
                from tests.test_realtime_redis_engine import TestRealtimeRedisEngine
                TestRealtimeRedisEngine().test()

            # AI - Intent matching enging
            case "intent_matching_engine": 
                from tests.test_intent_matching_engine import TestIntentMatchingEngine
                TestIntentMatchingEngine().test()

            # Tasks Scheduler
            case "engine_scheduler": 
                from tests.test_engine_scheduler import TestEngineScheduler
                TestEngineScheduler().test()

            # Site / Blog Posts / Internet Content Generator
            case "generate_site": 
                from tests.test_site_generator import TestGenerateSite 
                TestGenerateSite().test()
            case "slug_generator": 
                from tests.test_slug_generator import TestSlugGenerator
                TestSlugGenerator().test()
            case "safe_yaml_parser": 
                from tests.test_safe_yaml_parser import TestSafeYAMLParser
                TestSafeYAMLParser().test()
            case "architecture_renderer": 
                from tests.test_architecture_renderer import TestArchitectureRenderer
                TestArchitectureRenderer().test()
            case "process_posts": 
                from tests.test_process_posts import TestProcessPosts
                TestProcessPosts().test()

            # File System Watcher
            case "file_system_watcher":
                from tests.test_file_system_watcher import TestFileSystemWatcher
                TestFileSystemWatcher().test()
            case "pipeline_manager":
                from tests.test_pipeline_manager import TestPipelineManager
                TestPipelineManager().test()

            # Linter
            case "pre_flight_linter":
                from tests.test_pre_flight_linter import TestPreFlightLinter
                TestPreFlightLinter().test()

            # Documentation generation
            case "doc_engine":
                from tests.test_doc_engine import TestDocEngine
                TestDocEngine().test()

            # State Sketcher
            case "state_sketcher":
                from tests.test_state_sketcher import TestStateSketcher
                TestStateSketcher().test()

            # Sockets
            case "sockets":
                from tests.test_sockets import TestSockets
                TestSockets().test()

            # Edge-cases
            case _: self.logger.warning("Enter a valid test case.") 

    def run(self):
        asyncio.run(self.test())