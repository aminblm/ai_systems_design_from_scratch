# intent_matching_engine.py
import re, sys
from typing import Dict, Optional, Any

from ai_system_design.kernel.loggable_mixin import LoggableMixin
from ai_system_design.kernel.test_mixin import TestMixin


class TestIntentMatchingEngine(TestMixin):
    """Test the intent_matching_engine module functionality."""

    def __init__(self) -> None:
        super().__init__()
        self.logger.info("TestIntentMatchingEngine initialized.")

    def test(self):
        super().test()
        INTENT_DATA_REPOS = {
            "greetings": {
                "keywords": ["hello", "hi", "hey", "greetings", "good day"],
                "response": "Hello! How can I assist you today? 👋"
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

        
class IntentMatchingEngine(LoggableMixin):
    """A normalized text processing system that maps raw inputs to structured intents."""

    def __init__(self, intents: Dict[str, Dict[str, Any]]) -> None:
        super().__init__()
        self.intents = intents
        self.logger.info("IntentMatchingEngine initialized.")

    def _normalize_text(self, text: str) -> str:
        """Converts text to lowercase and strips trailing whitespace and basic punctuation."""
        lowered = text.strip().lower()
        # Regex expression clears out string punctuation blocks cleanly
        return re.sub(r'[^\w\s]', '', lowered)

    def extract_response(self, raw_user_input: str) -> str:
        """Evaluates token inclusion maps to select the highest-scoring response intent."""
        normalized_input = self._normalize_text(raw_user_input)
        
        best_intent: Optional[str] = None
        highest_score = 0

        # Basic keyword density matching pass replacing strict exact checks
        for intent_name, data in self.intents.items():
            current_score = 0
            for keyword in data["keywords"]:
                # Check for absolute substring keyword match sequences
                if keyword in normalized_input:
                    current_score += 1
            
            if current_score > highest_score:
                highest_score = current_score
                best_intent = intent_name

        if best_intent and highest_score > 0:
            self.logger.debug(f"Matched intent [{best_intent}] with score allocation weight: {highest_score}")
            return self.intents[best_intent]["response"]

        return "I'm sorry, I couldn't quite catch that. Could you rephrase your question?"