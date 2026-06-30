# agent_runner.py
from typing import Dict, Any
from ai_system_design.kernel.base_tool import BaseTool

class AgentRunner:
    """The orchestration loop that binds thought to action."""

    def __init__(self, engine, scheduler, tools: Dict[str, BaseTool]) -> None:
        self.engine = engine            # IntentMatchingEngine
        self.scheduler = scheduler      # EngineScheduler
        self.tools = tools              # {tool_name: BaseTool}

    def step(self, observation: str) -> Any:
        # 1. Think: Determine Intent
        intent = self.engine.get_intent(observation)

        # 2. Plan: Schedule the work
        task_id = self.scheduler.schedule_task(intent, {"observation": observation})

        # 3. Act: Map intent to tool and execution
        if intent in self.tools: 
            result = self.tools[intent].execute({"task_id": task_id})
            self.scheduler.update_status(task_id, "COMPLETED")
            return result
        return "No tool found for the intent"