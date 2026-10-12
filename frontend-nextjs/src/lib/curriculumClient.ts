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
  grade: string | number;
  subject: string;
  book?: string;
  part?: string;
  unit?: string;
  chapter_id?: string;
}): string {
  const enc = (v: any) => encodeURIComponent(String(v || '').trim());
  const grade = enc(identity.grade);
  const subject = enc((identity.subject || '').toLowerCase());
  const book = enc(identity.book || identity.subject || 'main');
  const part = enc(identity.part || 'main');
  const unit = enc(identity.unit || 'U01');
  const chapterId = enc(identity.chapter_id || '');
  return `/curriculum/${grade}/${subject}/${book}/${part}/${unit}/${chapterId}`;
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
      grade: String(identity.grade || ''),
      subject: String(identity.subject || ''),
      book: String(identity.book || ''),
      part: String(identity.part || ''),
      unit: String(identity.unit || ''),
      chapter_id: String(identity.chapter_id || ''),
      content_type: String(identity.content_type || '')
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
