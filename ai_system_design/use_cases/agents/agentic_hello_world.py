# agentic_hello_world.py
from ai_system_design.kernel.tool_registry import ToolRegistry

# 1. The tools registered as capabilities
@ToolRegistry.register
def query_db(query: str): 
    """Queries the distributed database for records."""
    return f"DB_RESULT: {query}"

@ToolRegistry.register
def append_log(data: str): 
    """Appends data to local system log."""
    with open("ai_system_design/use_cases/agents/system_log.txt", 'a') as f:
        f.write(data + "\n")
    return "SUCCESS: Logged."

# 2. The Agent: The Orchestrator
class HelloWorldAgent:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def run_cycle(self, prompt: str):
        print(f"Observing: {prompt}")

        # Simple Decision: Use registry to execute
        result = self.registry._registry['query_db']['func'](prompt)
        log_result = self.registry._registry['append_log']['func'](result)

        print(f"Action complete: {log_result}")

if __name__ == "__main__":
    # 3. Execution
    agent = HelloWorldAgent(ToolRegistry())
    agent.run_cycle("Fetch User: 101")
