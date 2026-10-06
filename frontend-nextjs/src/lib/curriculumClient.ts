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
  static async fetchHierarchy(): Promise<any[]> {
    try {
      const res = await fetch(`${API_BASE}/api/v1/curriculum/hierarchy`);
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      return await res.json();
    } catch (err) {
      console.warn('Failed to fetch authoritative curriculum hierarchy from backend:', err);
      return [];
    }
  }

  static async fetchContent(identity: CurriculumIdentity): Promise<ChapterContentResponse> {
    const params = new URLSearchParams({
      grade: identity.grade,
      subject: identity.subject,
      book: identity.book,
      part: identity.part,
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
