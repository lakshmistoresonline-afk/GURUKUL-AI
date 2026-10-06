from typing import Dict, Any
class Class6MathematicsValidator:
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        return isinstance(data, (dict, list))
