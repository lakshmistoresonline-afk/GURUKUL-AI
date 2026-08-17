import sys
import os

sys.path.insert(0, os.getcwd())

from src.providers.ollama_cloud import _parse_structured_json


tests = [
    (
        '[{"question":"Q"}]',
        list,
    ),
    (
        '''```json
[{"question":"Q"}]
```''',
        list,
    ),
    (
        '{"question":"Q"}',
        dict,
    ),
]


for number, (raw, expected) in enumerate(tests, 1):

    result = _parse_structured_json(raw)

    print(
        f"TEST {number}: "
        f"expected={expected.__name__} "
        f"actual={type(result).__name__}"
    )

    if not isinstance(result, expected):
        raise AssertionError(
            f"TEST {number} FAILED"
        )

    print(f"TEST {number}: PASS")


print()
print("OLLAMA STRUCTURED PARSER: PASS")
