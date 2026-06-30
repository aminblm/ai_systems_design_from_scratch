import argparse


def test_modules():
    """Example testing module: 
    python test.py --test slug_generator"""

    parser = argparse.ArgumentParser(description="Test AI Systems Design")
    parser.add_argument("--test", required=True)
    args = parser.parse_args()

    match args.test:
        # Frontend
        case "reactive_frontend": 
            from ai_system_design.modules.reactive_frontend import TestReactiveFrontent
            TestReactiveFrontent().test_reactive_frontend()

        # Load Balancing
        case "round_robin_load_balancer": 
            from ai_system_design.modules.round_robin_load_balancer import TestRoundRobinLoadBalancer
            TestRoundRobinLoadBalancer().test_round_robin_load_balancer()

        # Sockets
        case "socket_server": 
            from ai_system_design.kernel.socket_server import TestSocketServer
            TestSocketServer().test_socket_server()
        case "socket_client": 
            from ai_system_design.kernel.socket_client import TestSocketClient
            TestSocketClient().test_socket_client()

        # REST APIs
        case "rest_api_client": 
            from ai_system_design.modules.rest_api_client import TestRESTAPIClient
            TestRESTAPIClient().test_rest_api_client()
        case "rest_api_server": 
            from ai_system_design.modules.rest_api_server import TestRESTAPIServer
            TestRESTAPIServer().test_rest_api_server()

        # Git RPC
        case "git_rpc_client": 
            from ai_system_design.modules.git_rpc_client import TestGitRPCClient
            TestGitRPCClient().test_git_rpc_client()
        case "git_rpc_server": 
            from ai_system_design.modules.git_rpc_server import TestGitRPCServer
            TestGitRPCServer().test_git_rpc_server()

        # Container Management
        case "container_manager_client": 
            from ai_system_design.modules.container_manager_client import TestContainerManagerClient
            TestContainerManagerClient().test_container_manager_client()
        case "container_manager_server": 
            from ai_system_design.modules.container_manager_server import TestContainerManagerServer
            TestContainerManagerServer().test_container_manager_server()

        # Databases
        case "scalable_index": 
            from ai_system_design.modules.scalable_index import TestScalableIndex
            TestScalableIndex().test_scalable_index()
        case "distributed_no_sql_database": 
            from ai_system_design.modules.distributed_no_sql_database import TestDistributedNoSQLDatabase
            TestDistributedNoSQLDatabase().test_distributed_no_sql_database()
        
        # Caching
        case "realtime_redis_engine": 
            from ai_system_design.modules.realtime_redis_engine import TestRealtimeRedisEngine
            TestRealtimeRedisEngine().test_realtime_redis_engine()

        # AI - Intent matching enging
        case "intent_matching_engine": 
            from ai_system_design.modules.intent_matching_engine import TestIntentMatchingEngine
            TestIntentMatchingEngine().test_intent_matching_engine()

        # Tasks Scheduler
        case "engine_scheduler": 
            from ai_system_design.modules.engine_scheduler import TestEngineScheduler
            TestEngineScheduler().test_engine_scheduler()

        # Site / Blog Posts / Internet Content Generator
        case "generate_site": 
            from ai_system_design.modules.site_generator.site_generator import TestGenerateSite 
            TestGenerateSite().test_generate_site()
        case "slug_generator": 
            from ai_system_design.modules.slug_generator import TestSlugGenerator
            TestSlugGenerator().test_slug_generator()
        case "safe_yaml_parser": 
            from ai_system_design.modules.safe_yaml_parser import TestSafeYAMLParser
            TestSafeYAMLParser().test_safe_yaml_parser()
        case "architecture_renderer": 
            from ai_system_design.modules.architecture_renderer import TestArchitectureRenderer
            TestArchitectureRenderer().test_architecture_renderer()
        case "process_posts": 
            from ai_system_design.modules.process_posts import TestProcessPosts
            TestProcessPosts().test_process_posts()

        # Deugger
        case "debugger": 
            from ai_system_design.kernel.debugger import TestDebugger
            TestDebugger().test_debugger()

        # Edge-cases
        case _:
            # TODO Edge-case proper handling 
            # logger.warning("Enter a valid test case.") 
            pass
    pass