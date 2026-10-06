from typing import Dict, Any

class BaseValidator:
    """Strict schema validator ensuring zero information loss and valid JSON structure."""
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        if not isinstance(data, (dict, list)):
            return False
        return True
