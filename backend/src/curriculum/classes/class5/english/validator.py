from typing import Dict, Any
class Class5EnglishValidator:
    @classmethod
    def validate(cls, data: Dict[str, Any]) -> bool:
        return isinstance(data, (dict, list))
