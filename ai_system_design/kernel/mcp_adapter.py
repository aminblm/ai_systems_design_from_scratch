# mcp_adapter.py
"""Adapts existing Registry tools to MCP Specification."""

from typing import Dict

class MCPAdapter:
    """Adapts existing Registry tools to MCP Specification."""
    def __init__(self, registry):
        self.registry = registry

    def handle_request(self, json_rpc_payload: Dict):
        method = json_rpc_payload.get('method')
        params = json_rpc_payload.get('params', {})

        # MCP: tools/list
        if method == "tools/list":
            return self._list_tools()
        
        # MCP: tools/call
        if method == "tools/call":
            return self._execute_tool(params)
        
        #TODO
        # MCP: resources/read
        if method == "resources/read":
            self._read_resource()

        #TODO
        # MCP: prompts/list
        if method == "resources/read":
            self._list_prompts()
        
        return {"error": "Method not found"}
    
    def _list_tools(self):
        tools = [{"name": name, "description": meta["doc"]}
                 for name, meta in self.registry._registry.items()]
        return {"tools": tools}
    
    def _execute_tool(self, params):
        name = params.get('name')
        args = params.get("arguments", {})
        func = self.registry._registry[name]["func"]
        return {"content": [{"type": "text", "text": str(func(**args))}]}
    
    def _read_resource(self):
        pass

    def _list_prompts(self):
        pass