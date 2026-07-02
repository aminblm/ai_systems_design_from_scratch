import sys

from ai_system_design.kernel.mixins import TestMixin
from ai_system_design.kernel.intent_matching_engine import IntentMatchingEngine


class TestIntentMatchingEngine(TestMixin):
    """Test the intent_matching_engine module functionality."""

    def __init__(self) -> None:
        """TestIntentMatchingEngine Constructor."""
        super().__init__()
        self.logger.info("TestIntentMatchingEngine initialized.")

    def test(self):
        """TestIntentMatchingEngine Test."""
        super().test()
        INTENT_DATA_REPOS = {
            "greetings": {
                "keywords": ["hello", "hi", "hey", "greetings", "good day"],
                "response": "Hello! How can I assist you today?"
            },
            "state_of_being": {
                "keywords": ["how are you", "hows it going", "how are things"],
                "response": "I am operating optimally. How can I help you build today?"
            },
            "identity": {
                "keywords": ["what is your name", "who are you", "your name"],
                "response": "I am a refactored automation agent running on Python."
            },
            "capabilities": {
                "keywords": ["what can you do", "help", "features", "options"],
                "response": "I can process commands, normalize inputs, and route intents."
            },
            "farewells": {
                "keywords": ["bye", "goodbye", "exit", "quit", "see ya"],
                "response": "Goodbye! Have an excellent day."
            }
        }
        # Instantiate engine cleanly parsing external mapping values
        engine = IntentMatchingEngine(intents=INTENT_DATA_REPOS)

        print("\n=== Robust Intent Processing Bot Interface Enabled ===")
        print("Ask questions smoothly. Type 'exit' to terminate the runtime cycle.")

        while True:
            try:
                print("\nUser> ", end="", flush=True)
                user_raw_string = sys.stdin.readline().strip()

                if user_raw_string.lower() in ("exit", "quit"):
                    print("Bot: Goodbye!")
                    break

                if not user_raw_string:
                    continue

                bot_reply = engine.extract_response(user_raw_string)
                print(f"Bot: {bot_reply}")

            except (KeyboardInterrupt, SystemExit):
                print("\nSession killed via hardware interrupt signal.")
                break
