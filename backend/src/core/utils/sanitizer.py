import re

ARTIFACT_PATTERNS = [
    r"Chapter\s+\d+\.indd\s+\d+\s+\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}", # Full InDesign markers
    r"Chapter\s+\d+\.indd\s+\d+", # Short InDesign markers
    r"Chapter\s+\d+\.indd",
    r"\w+\.indd\s+\d+", # Any indd and numbers
    r"\d+\.indd\s+\d+", # Just indd and numbers
    r"\d{2,}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}", # Timestamps with long day/month
    r"\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}", # Standard Timestamps
    r"\d{2,}-\d{2}-\d{4}", # Date sequences
    r"\d{2}:\d{2}:\d{2}", # Time sequences
    r"2\s+3\s+5\s+6\s+4\s+1\s+7\s+8\s+9", # Specific extraction sequence
    r"\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d\s+\d", # Generic long number sequences
    r"Grade\s+\d+",
    r"Santoor\s+Grade\s+\d+",
    r"Unit\s+\d+:\s+Let’s\s+Have\s+Fun",
    r"Let us Recite \d+",
    r"Canonical source evidence",
    r"source-supported points below",
    r"source-supported statement",
    r"supplied source evidence",
    r"important information in evidence",
    r"evidence \d+",
    r"Concept\s+\d+", # Remove generic 'Concept X' text from strings
]

def sanitize_student_content(text: str) -> str:
    if not text:
        return ""

    cleaned = text
    for pattern in ARTIFACT_PATTERNS:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)

    # Clean up messy whitespace
    cleaned = re.sub(r"\s{2,}", " ", cleaned).strip()

    if cleaned.upper() == "UNSPECIFIED":
        return "Not specified"

    return cleaned

def sanitize_question_stem(stem: str, concept_name: str = None) -> str:
    cleaned = sanitize_student_content(stem)
    if concept_name:
        cleaned = cleaned.replace(f"about '{concept_name}'", "")
        cleaned = cleaned.replace(f"about {concept_name}", "")
    return cleaned
