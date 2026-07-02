from ai_system_design.use_cases.agents.agentic_hello_world import ToolRegistry, HelloWorldAgent, append_log, query_db

if __name__ == "__main__":
    # Agentic execution
    agent = HelloWorldAgent(ToolRegistry())
    agent.run_cycle("Fetch User: 101")