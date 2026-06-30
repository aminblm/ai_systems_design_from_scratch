# round_robin_load_balancer.py
import sys
from typing import Callable, List, Dict, Any

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestRoundRobinLoadBalancer(TestMixin):
    """Test the round_robin_load_balancer module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestRoundRobinLoadBalancer initialized.")

    def test_round_robin_load_balancer(self):
        # Cluster nodes are registered as uniform units inside the balancing array pool
        cluster_pool = [web_node_alpha, web_node_beta, web_node_gamma]
        load_balancer = RoundRobinLoadBalancer(backend_servers=cluster_pool)

        print("\n=== Enterprise Load Balancer Core Engaged ===")
        print("Submit message payloads below to test distribution loops. Type 'exit' to halt.")

        while True:
            try:
                print("\nclient_payload> ", end="", flush=True)
                user_payload = sys.stdin.readline().strip()

                if user_payload.lower() in ("exit", "quit"):
                    print("Dismantling network configuration infrastructure layers cleanly.")
                    break

                if not user_payload:
                    continue

                # Package transaction argument contexts to simulate web parameters
                mock_request = {"body": user_payload, "protocol": "HTTP/1.1"}
                
                # Dispatch traffic
                gateway_response = load_balancer.route_request(mock_request)
                print(f"Client Receives -> {gateway_response}")

            except (KeyboardInterrupt, SystemExit):
                print("\nSystem execution loop terminated via hardware interrupt signal.")
                break
        
        
class RoundRobinLoadBalancer(LoggableMixin):
    """A thread-safe, programmatic load balancer distributing homogeneous traffic evenly."""
    
    def __init__(self, backend_servers: List[Callable[[Dict[str, Any]], str]]) -> None:
        super().__init__()
        if not backend_servers:
            raise ValueError("Load Balancer infrastructure requires at least one upstream backend node.")
            
        self._backends = backend_servers
        self._next_index = 0  # Pointer tracking round-robin sequencing transitions
        self.logger.info("RoundRobinLoadBalancer initialized.")

    def route_request(self, request_context: Dict[str, Any]) -> str:
        """Balances incoming request loads across backend pools monotonically."""
        # Select target node using modulo algorithm to ensure consistent distribution
        selected_index = self._next_index % len(self._backends)
        target_node = self._backends[selected_index]
        
        # Increment sequence tracker
        self._next_index = (selected_index + 1) % len(self._backends)

        self.logger.info(f"[LB Routing Master] Dispatched request context to Backend Node Cluster #{selected_index}")

        try:
            return target_node(request_context)
        except Exception as backend_err:
            self.logger.error(f"Backend Node Cluster #{selected_index} faulted during execution: {backend_err}")
            return "HTTP 502: Bad Gateway (Target node exception)"
    

# Refactored Backends: Interchangeable, homogeneous processors accepting generic signatures
def web_node_alpha(context: Dict[str, Any]) -> str:
    return f"Response processed by [Node Alpha]. Payload data: '{context.get('body')}'"

def web_node_beta(context: Dict[str, Any]) -> str:
    return f"Response processed by [Node Beta]. Payload data: '{context.get('body')}'"

def web_node_gamma(context: Dict[str, Any]) -> str:
    return f"Response processed by [Node Gamma]. Payload data: '{context.get('body')}'"
