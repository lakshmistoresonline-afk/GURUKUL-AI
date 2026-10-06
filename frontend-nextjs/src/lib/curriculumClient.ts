export interface CurriculumIdentity {
  grade: string;
  subject: string;
  book: string;
  part: string;
  unit: string;
  chapter_id: string;
  content_type: string;
}

export interface ChapterContentResponse {
  identity: CurriculumIdentity;
  contentType: string;
  data: any;
  status: string;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';

export class CurriculumApiClient {
  static async fetchClasses(): Promise<{ grade: string; subjects: string[] }[]> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/curriculum/classes`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return data.classes ? data.classes.map((g: string) => ({ grade: g, subjects: [] })) : data;
    } catch (err) {
      console.warn('Failed to fetch classes from backend registry:', err);
      return [];
    }
  }

  static async fetchSubjects(grade: string): Promise<string[]> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/curriculum/classes/${grade}/subjects`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return data.subjects || [];
    } catch (err) {
      console.warn(`Failed to fetch subjects for Class ${grade}:`, err);
      return [];
    }
  }

  static async fetchChapters(grade: string, subject: string, book: string = 'main', unit: string = 'U01'): Promise<string[]> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/curriculum/classes/${grade}/subjects/${subject}/books/${book}/units/${unit}/chapters`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      return data.chapters || [];
    } catch (err) {
      console.warn(`Failed to fetch chapters for Class ${grade} ${subject}:`, err);
      return [];
    }
  }

  static async fetchContent(identity: CurriculumIdentity): Promise<ChapterContentResponse> {
    const params = new URLSearchParams({
      grade: identity.grade,
      subject: identity.subject,
      book: identity.book,
      unit: identity.unit,
      chapter_id: identity.chapter_id,
      content_type: identity.content_type
    });

    const res = await fetch(`${API_BASE}/api/v1/curriculum/resolve?${params.toString()}`);
    if (!res.ok) {
      const errBody = await res.json().catch(() => ({}));
      throw new Error(errBody.detail?.error?.message || `Curriculum resolution failed with HTTP ${res.status}`);
    }
    return res.json();
  }
}
