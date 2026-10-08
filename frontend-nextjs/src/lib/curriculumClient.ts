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

export class CurriculumApiError extends Error {
  status: number;
  code?: string;

  constructor(status: number, message: string, code?: string) {
    super(message);
    this.name = 'CurriculumApiError';
    this.status = status;
    this.code = code;
  }
}

export function buildCurriculumUrl(identity: {
  grade: string;
  subject: string;
  book: string;
  part: string;
  unit: string;
  chapter_id: string;
}): string {
  const enc = (v: string) => encodeURIComponent(v.trim());
  return `/curriculum/${enc(identity.grade)}/${enc(identity.subject.toLowerCase())}/${enc(identity.book)}/${enc(identity.part)}/${enc(identity.unit)}/${enc(identity.chapter_id)}`;
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || (process.env.NODE_ENV === 'development' ? 'http://localhost:8080' : '');

export class CurriculumApiClient {
  static async fetchHierarchy(): Promise<any[]> {
    const res = await fetch(`${API_BASE}/api/v1/curriculum/hierarchy`);
    if (!res.ok) {
      throw new CurriculumApiError(res.status, `Authoritative hierarchy fetch failed with HTTP ${res.status}`);
    }
    return await res.json();
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
      const msg = errBody.detail?.error?.message || `Curriculum resolution failed with HTTP ${res.status}`;
      const code = errBody.detail?.error?.code;
      throw new CurriculumApiError(res.status, msg, code);
    }
    return res.json();
  }
}
