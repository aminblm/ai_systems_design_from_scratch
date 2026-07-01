# mcp_server.py
"""Exposes internal modules as discoverable MCP tools."""

from typing import Dict, Any

class MCPServer:
    """Exposes internal modules as discoverable MCP tools."""

    def __init__(self, registry: Dict) -> None:
        self.registry = registry # Dict of modules

    def get_capabilities(self) -> Dict[str, Any]:
        """Schema discovery for AI clients."""
        return {
            "tools": [
                {
                    "name": name,
                    "description": module.__doc__,
                    "schema": self._derive_schema(module)
                }
                for name, module in self.registry.items()
            ]
        }
    
    def _derive_schema(self, module) -> Dict[str, Any]:
        # Maps module methods to JSON-Schema parameters
        return {"type": "object", "properties": {"task_id": {"type": "string"}}}
    
    def execute_request(self, tool_name, params):
        """Standardized execution interface for MCP Clients."""
        module = self.registry[tool_name]
        if hasattr(module, 'execute'):
            return module.execute(params)
        return {"error": "Tool execution failed."}