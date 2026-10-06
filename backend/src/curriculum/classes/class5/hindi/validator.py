from typing import Dict, Any
class Class5HindiValidator:
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        return isinstance(data, (dict, list))
