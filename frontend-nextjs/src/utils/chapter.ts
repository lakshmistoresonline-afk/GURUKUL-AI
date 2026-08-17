import manifest from '@/data/manifest.json';

/**
 * Gurukul AI Chapter Display Utilities
 */

export interface ChapterDisplayData {
  id: string;
  number: string;
  name: string;
  fullName: string;
  subject: string;
  className: string;
}

/**
 * Extracts chapter number and name from internal ID and optional package content.
 */
export function getChapterDisplayData(id: string, pkg?: any): ChapterDisplayData {
  const parts = id.split('_');
  const code = parts[parts.length - 1] || id;
  const subject = parts[parts.length - 2] || 'General';
  const className = parts[parts.length - 3] || 'Class';

  // 1. Extract Number: assumes last 2 digits of the code are the chapter number (e.g. eemm110 -> 10)
  const numMatch = code.match(/\d+$/);
  const numPart = numMatch ? numMatch[0] : '';
  let chapterNumber = '';
  if (numPart.length >= 2) {
    chapterNumber = parseInt(numPart.slice(-2)).toString();
  } else if (numPart.length === 1) {
    chapterNumber = numPart;
  }

  // 2. Extract Name
  let chapterName = code.toUpperCase();

  // Try to find in manifest first if pkg is not provided
  if (!pkg) {
    const manifestItem = manifest.find((c: any) => c.id === id);
    if (manifestItem) {
      chapterName = manifestItem.title;
    }
  }

  if (pkg) {
    const { content, metadata, original_data } = pkg;

    // Priority: curriculum.displayName → curriculum.chapterTitle → metadata.chapter_name → content.topic
    if (original_data?.curriculum?.displayName) {
      chapterName = original_data.curriculum.displayName;
    } else if (original_data?.curriculum?.chapterTitle) {
      chapterName = original_data.curriculum.chapterTitle;
    } else if (metadata?.chapter_name) {
      chapterName = metadata.chapter_name;
    } else if (metadata?.chapterTitle) {
      chapterName = metadata.chapterTitle;
    } else if (content?.topic && content.topic !== 'N/A') {
      chapterName = content.topic;
    } else if (content?.title) {
      chapterName = content.title;
    } else {
      const intro = content?.introduction || '';
      // Improved regex for NCERT titles
      const match = intro.match(/Chapter .*?\*\*[“"'](.+?)[”"']\*\*/i) ||
                    intro.match(/\*\*[“"'](.+?)[”"']\*\*/) ||
                    intro.match(/#+\s+(.+)/) ||
                    intro.match(/\*\*(.+?)\*\*/);

      if (match) {
        chapterName = match[1].replace(/\*/g, '').trim();
      }
    }
  }

  const numberPrefix = chapterNumber ? `Chapter ${chapterNumber}` : '';
  const fullName = numberPrefix ? `${numberPrefix} — ${chapterName}` : chapterName;

  return {
    id,
    number: chapterNumber,
    name: chapterName,
    fullName,
    subject,
    className
  };
}

/**
 * Normalizes a class name to a canonical format (e.g. 'Class 5' -> 'class_5').
 */
export function normalizeClassName(name: string): string {
  if (!name) return "";
  // Extract number
  const match = name.match(/\d+/);
  if (match) {
    return `class_${match[0]}`;
  }
  return name.toLowerCase().replace(' ', '_');
}
