/**
 * Gurukul AI Student-Safe Content Sanitizer
 *
 * Deterministically removes extraction artifacts while preserving
 * legitimate educational prose.
 */

const ARTIFACT_PATTERNS = [
  /Chapter\s+\d+\.indd\s+\d+\s+\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}/gi, // InDesign markers
  /\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}/g, // Timestamps
  /Grade\s+\d+/gi, // Grade markers
  /Santoor\s+Grade\s+\d+/gi, // Specific book markers
  /\[Concept:\s*Concept\s*\d+\]/gi, // Internal concept bracket tags
];

export function sanitizeStudentContent(text: string): string {
  if (!text) return "";

  let cleaned = text;

  // 1. Apply regex patterns for known artifacts
  ARTIFACT_PATTERNS.forEach(pattern => {
    cleaned = cleaned.replace(pattern, "");
  });

  // 2. Clean up resulting messy whitespace
  cleaned = cleaned.replace(/\s{2,}/g, " ").trim();

  // 3. Handle specific labels like UNSPECIFIED
  if (cleaned.toUpperCase() === "UNSPECIFIED") {
    return "Not specified";
  }

  return cleaned;
}

/**
 * Specifically cleans question stems which often have repetitive metadata framing.
 */
export function sanitizeQuestionStem(stem: string, conceptName?: string): string {
  let cleaned = sanitizeStudentContent(stem);

  // If the stem is a template like "Explain the important information in about...",
  // we try to make it more direct.
  if (conceptName) {
     cleaned = cleaned.replace(new RegExp(`about '${conceptName}'`, 'gi'), "");
     cleaned = cleaned.replace(new RegExp(`about ${conceptName}`, 'gi'), "");
  }

  return cleaned;
}
