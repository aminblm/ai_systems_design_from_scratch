
"""Decompose deep functions following the Rule of Three"""

class DeepFeatureEngine:
    """Decomposes complex logic into a chain of shallow primitives."""

    def process(self, data: dict) -> dict:
        """Transformation pipeline (The Rule of Three)"""
        clean_data = self._step_one_sanitize(data)
        result = self._step_two__transform(clean_data)
        return self._strep_three_format(result)
    
    def _step_one_sanitize(self, data: dict) -> dict:
        """Primitive 1: Filter and validate."""
        return {k: v for k, v in data.items() if v is not None}
    
    def _step_two__transform(self, data: dict) -> dict:
        """Primitive 2: Core Business Logic."""
        return {k: v * 2 for k, v in data.items() if isinstance(v, int)}
    
    def _strep_three_format(self, data: dict) -> dict:
        """Primitive 3: Output structural mapping."""
        return {"result": list(data.values()), "status": "ok"}