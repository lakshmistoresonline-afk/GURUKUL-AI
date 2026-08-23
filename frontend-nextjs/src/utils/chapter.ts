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
  if (!id) {
    return {
      id: '',
      number: '',
      name: 'Unknown Chapter',
      fullName: 'Unknown Chapter',
      subject: 'General',
      className: 'Class'
    };
  }
  const parts = id.split('_');
  const code = parts[parts.length - 1] || id;

  // Try to infer subject from code prefix (V3 style: eemm, eeev, ehve, eesa, fepr, fegp, gegp, etc.)
  let inferredSubject = 'General';
  if (code.startsWith('eemm') || code.startsWith('fegp') || code.startsWith('gegp')) inferredSubject = 'Mathematics';
  else if (code.startsWith('eeev') || code.startsWith('fecu') || code.startsWith('gecu')) inferredSubject = 'Science';
  else if (code.startsWith('ehve') || code.startsWith('fhml') || code.startsWith('ghml')) inferredSubject = 'Hindi';
  else if (code.startsWith('eesa') || code.startsWith('fepr') || code.startsWith('gepr')) inferredSubject = 'English';
  else if (code.startsWith('fees') || code.startsWith('gees')) inferredSubject = 'Social Science';

  const subject = parts[parts.length - 2] || inferredSubject;
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
    const { content, metadata, chapter, components } = pkg;
    const comps = components || pkg.components || {};

    // Priority 1: chapter object (V3 Root)
    if (chapter?.chapter_title) {
      chapterName = chapter.chapter_title;
    } else if (chapter?.title) {
      chapterName = chapter.title;
    }
    // Priority 2: components.chapter_metadata (V3 Component)
    else if (comps.chapter_metadata?.content?.title) {
      chapterName = comps.chapter_metadata.content.title;
    } else if (comps.chapter_metadata?.chapter_title) {
      chapterName = comps.chapter_metadata.chapter_title;
    }
    // Priority 3: original_data (Migration Metadata)
    else if (pkg.original_data?.curriculum?.displayName) {
      chapterName = pkg.original_data.curriculum.displayName;
    } else if (metadata?.chapter_name) {
      chapterName = metadata.chapter_name;
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

    // Resolve chapter number from V3 metadata if available
    if (chapter?.chapter_number) {
        chapterNumber = chapter.chapter_number.toString();
    } else if (comps.chapter_metadata?.content?.chapter_number) {
        chapterNumber = comps.chapter_metadata.content.chapter_number.toString();
    }
  }

  // Cleanup: If chapterName is still a code (no spaces, contains numbers and letters)
  if (chapterName === code.toUpperCase() && /^[A-Z0-9]+$/.test(chapterName)) {
      chapterName = `${subject.charAt(0).toUpperCase() + subject.slice(1)} Module ${chapterNumber || 'Core'}`;
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
