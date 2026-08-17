import json
import re
import logging
from typing import Any, Optional

logger = logging.getLogger(__name__)

def normalize_structured_response(response: Any) -> Any:
    """
    Robustly normalizes AI provider responses that should be structured data (list or dict).

    Handles:
    - Direct dict/list
    - Stringified JSON (with or without markdown fences)
    - Enveloped responses like {"value": [...]} or {"data": [...]}
    - Schema-wrapped responses where the actual value is in a sub-field
    - JSON embedded in other text
    """
    if response is None:
        return None

    # 1. If it's already a dict or list, try to unwrap common envelopes
    if isinstance(response, (dict, list)):
        return _unwrap_envelope(response)

    # 2. If it's a string, try to parse it as JSON
    if isinstance(response, str):
        raw = response.strip()
        if not raw:
            return None

        # Remove markdown fences
        raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
        raw = re.sub(r"\s*```$", "", raw).strip()

        # Try direct parsing
        try:
            parsed = json.loads(raw)
            return _unwrap_envelope(parsed)
        except json.JSONDecodeError:
            pass

        # Try to find an embedded JSON array or object
        # Finding [ first
        array_start = raw.find("[")
        array_end = raw.rfind("]")

        object_start = raw.find("{")
        object_end = raw.rfind("}")

        # Prefer the one that starts earlier and looks like a valid block
        candidates = []
        if array_start != -1 and array_end > array_start:
            candidates.append(raw[array_start:array_end + 1])
        if object_start != -1 and object_end > object_start:
            candidates.append(raw[object_start:object_end + 1])

        # Sort candidates by length (longest first, likely to be the full data)
        candidates.sort(key=len, reverse=True)

        for candidate in candidates:
            try:
                parsed = json.loads(candidate)
                return _unwrap_envelope(parsed)
            except json.JSONDecodeError:
                continue

    return response

def _unwrap_envelope(data: Any) -> Any:
    """Recursively unwraps common JSON envelopes used by AI providers."""
    if not isinstance(data, dict):
        return data

    # 1. If it's a small dict with just one key and that value is a list/dict, unwrap it.
    # This handles {"flashcards": [...]} or {"quiz": [...]} or {"result": [...]}
    if len(data) == 1:
        key = list(data.keys())[0]
        val = data[key]
        if isinstance(val, (list, dict)):
            return _unwrap_envelope(val)

    # 2. Known common keys even if there are other metadata keys
    unwrap_keys = ["value", "data", "result", "items", "response", "content"]

    for key in unwrap_keys:
        if key in data:
            # If it's the only key, or there are only few other metadata-like keys
            other_keys = set(data.keys()) - {key, "type", "schema", "metadata", "status"}
            if not other_keys:
                val = data[key]
                if isinstance(val, (list, dict)):
                    return _unwrap_envelope(val)

    # 3. Handle schema envelopes like {"type": "array", "items": ..., "value": [...]}
    if "type" in data and "value" in data and isinstance(data["value"], (list, dict)):
        return _unwrap_envelope(data["value"])

    return data
