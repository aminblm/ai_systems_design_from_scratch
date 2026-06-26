# round_robin_load_balancer.py
from typing import Callable, List, Dict, Any

from ai_system_design import logger


class RoundRobinLoadBalancer:
    """A thread-safe, programmatic load balancer distributing homogeneous traffic evenly."""
    
    def __init__(self, backend_servers: List[Callable[[Dict[str, Any]], str]]) -> None:
        if not backend_servers:
            raise ValueError("Load Balancer infrastructure requires at least one upstream backend node.")
            
        self._backends = backend_servers
        self._next_index = 0  # Pointer tracking round-robin sequencing transitions

    def route_request(self, request_context: Dict[str, Any]) -> str:
        """Balances incoming request loads across backend pools monotonically."""
        # Select target node using modulo algorithm to ensure consistent distribution
        selected_index = self._next_index % len(self._backends)
        target_node = self._backends[selected_index]
        
        # Increment sequence tracker
        self._next_index = (selected_index + 1) % len(self._backends)

        logger.info(f"[LB Routing Master] Dispatched request context to Backend Node Cluster #{selected_index}")

        try:
            return target_node(request_context)
        except Exception as backend_err:
            logger.error(f"Backend Node Cluster #{selected_index} faulted during execution: {backend_err}")
            return "HTTP 502: Bad Gateway (Target node exception)"
    

# Refactored Backends: Interchangeable, homogeneous processors accepting generic signatures
def web_node_alpha(context: Dict[str, Any]) -> str:
    return f"Response processed by [Node Alpha]. Payload data: '{context.get('body')}'"

def web_node_beta(context: Dict[str, Any]) -> str:
    return f"Response processed by [Node Beta]. Payload data: '{context.get('body')}'"

def web_node_gamma(context: Dict[str, Any]) -> str:
    return f"Response processed by [Node Gamma]. Payload data: '{context.get('body')}'"
