/**
 * Formats internal technical identifiers into human-readable display names.
 * E.g. "social_science" -> "Social Science", "class_5" -> "Class 5"
 */
export function formatDisplayName(id: string): string {
  if (!id) return "";

  // Handle class names explicitly if they follow class_XX pattern
  if (id.toLowerCase().startsWith("class_")) {
    const num = id.split("_").pop();
    return `Class ${num}`;
  }

  if (id.toLowerCase().startsWith("class")) {
    const num = id.replace(/class/i, "");
    if (num) return `Class ${num}`;
  }

  // General underscore to space and title case conversion
  return id
    .split(/[_-]/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(" ");
}

/**
 * Returns a short motivational phrase for each class level.
 */
export function getClassMotto(classId: string): string {
  const id = classId.toLowerCase();
  if (id.includes("5")) return "Explore & Discover";
  if (id.includes("6")) return "Understand & Connect";
  if (id.includes("7")) return "Think & Master";
  return "Learn & Grow";
}
