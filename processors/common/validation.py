from typing import Any

def validate_canonical_record(record: dict[str, Any]) -> tuple[bool, list[str]]:
    errors = []
    required_fields = ["record_id", "chapter_id", "pillar", "type", "text", "status"]
    for field in required_fields:
        if field not in record or record[field] is None:
            errors.append(f"Missing required field: {field}")
    return len(errors) == 0, errors
