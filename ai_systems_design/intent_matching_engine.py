# intent_matching_engine.py
import re
from typing import Dict, Optional, Any

from ai_systems_design.utils import logger


class IntentMatchingEngine:
    """A normalized text processing system that maps raw inputs to structured intents."""

    def __init__(self, intents: Dict[str, Dict[str, Any]]) -> None:
        self.intents = intents

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
            logger.debug(f"Matched intent [{best_intent}] with score allocation weight: {highest_score}")
            return self.intents[best_intent]["response"]

        return "I'm sorry, I couldn't quite catch that. Could you rephrase your question?"