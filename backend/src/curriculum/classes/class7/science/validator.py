from typing import Dict, Any
class Class7ScienceValidator:
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        return isinstance(data, (dict, list))
