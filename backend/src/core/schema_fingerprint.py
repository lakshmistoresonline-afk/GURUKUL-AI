from typing import Dict, Any, List, Set

class SchemaFingerprinter:
    """
    Deeply inspects source content package structure and generates a comprehensive schema fingerprint.
    Identifies root type, nested paths, array types, object types, primitive types, and content patterns.
    Does NOT depend on filenames.
    """

    @staticmethod
    def fingerprint(data: Any) -> Dict[str, Any]:
        if not isinstance(data, dict):
            return {
                "rootType": type(data).__name__,
                "topLevelKeys": [],
                "nestedPaths": [],
                "arrayTypes": [],
                "objectTypes": [],
                "primitiveTypes": [type(data).__name__],
                "keyCount": 0
            }

        top_level_keys: List[str] = sorted(list(data.keys()))
        nested_paths: Set[str] = set()
        array_types: Set[str] = set()
        object_types: Set[str] = set()
        primitive_types: Set[str] = set()

        def traverse(node: Any, current_path: str, depth: int = 0):
            if depth > 5:  # Prevent excessive recursion
                return

            if isinstance(node, dict):
                object_types.add(current_path if current_path else "root")
                for key, val in node.items():
                    child_path = f"{current_path}.{key}" if current_path else key
                    nested_paths.add(child_path)
                    traverse(val, child_path, depth + 1)
            elif isinstance(node, list):
                array_types.add(current_path)
                if node:
                    # Sample first element
                    traverse(node[0], f"{current_path}[]", depth + 1)
            else:
                primitive_types.add(type(node).__name__)

        traverse(data, "")

        return {
            "rootType": "dict",
            "topLevelKeys": top_level_keys,
            "nestedPaths": sorted(list(nested_paths)),
            "arrayTypes": sorted(list(array_types)),
            "objectTypes": sorted(list(object_types)),
            "primitiveTypes": sorted(list(primitive_types)),
            "keyCount": len(top_level_keys)
        }
