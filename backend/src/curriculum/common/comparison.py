from typing import Optional, Any

class StructuralComparison:
    @staticmethod
    def deep_compare(source_obj: Any, api_obj: Any, path: str = "root") -> Optional[str]:
        if type(source_obj) != type(api_obj):
            return f"Type mismatch at {path}: source is {type(source_obj)}, api is {type(api_obj)}"

        if isinstance(source_obj, dict):
            s_keys = set(source_obj.keys())
            a_keys = set(api_obj.keys())
            missing = s_keys - a_keys
            for k in missing:
                return f"Missing key '{k}' at {path}"
            for k in s_keys:
                res = StructuralComparison.deep_compare(source_obj[k], api_obj[k], f"{path}.{k}")
                if res:
                    return res
        elif isinstance(source_obj, list):
            if len(source_obj) != len(api_obj):
                return f"Array length mismatch at {path}: source len {len(source_obj)}, api len {len(api_obj)}"
            for idx, (s_item, a_item) in enumerate(zip(source_obj, api_obj)):
                res = StructuralComparison.deep_compare(s_item, a_item, f"{path}[{idx}]")
                if res:
                    return res
        else:
            if source_obj != api_obj:
                return f"Value mismatch at {path}: source '{source_obj}' != api '{api_obj}'"

        return None
