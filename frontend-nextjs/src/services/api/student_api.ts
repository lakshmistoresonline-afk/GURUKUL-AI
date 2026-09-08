import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000/api/v1/student';

export interface Class {
    id: string;
    name: string;
    subjects: Subject[];
}

export interface Subject {
    id: string;
    name: string;
    chapters: ChapterSummary[];
}

export interface ChapterSummary {
    id: string;
    chapter_id: string;
    title: string;
    counts: Record<string, number>;
}

export interface ContentBlock {
    id: string;
    type: string;
    title?: string;
    text?: string;
    answer?: string;
    explanation?: string;
    structuredData?: any;
    source: {
        file: string;
        page?: number;
    };
    order: number;
}

export interface ChapterFull {
    id: string;
    chapter_id: string;
    classId: string;
    subjectId: string;
    title: string;
    counts: Record<string, number>;
    learn: ContentBlock[];
    practice: ContentBlock[];
    assess: ContentBlock[];
    revise: ContentBlock[];
    resources: ContentBlock[];
    traceability?: any[];
}

export const studentApi = {
    getCatalog: async (): Promise<{classes: Class[]}> => {
        const response = await axios.get(`${API_BASE_URL}/catalog`);
        return response.data;
    },

    getClasses: async (): Promise<Class[]> => {
        const response = await axios.get(`${API_BASE_URL}/classes`);
        return response.data;
    },

    getClass: async (classId: string): Promise<Class> => {
        const response = await axios.get(`${API_BASE_URL}/classes/${classId}`);
        return response.data;
    },

    getSubjects: async (classId: string): Promise<Subject[]> => {
        const response = await axios.get(`${API_BASE_URL}/classes/${classId}/subjects`);
        return response.data;
    },

    getSubject: async (subjectId: string): Promise<Subject> => {
        const response = await axios.get(`${API_BASE_URL}/subjects/${subjectId}`);
        return response.data;
    },

    getChapterFull: async (chapterUid: string): Promise<ChapterFull> => {
        const response = await axios.get(`${API_BASE_URL}/chapters/${chapterUid}/full`);
        return response.data;
    },

    getDashboardSummary: async () => {
        const response = await axios.get(`${API_BASE_URL}/dashboard/summary`);
        return response.data;
    },

    search: async (query: string, classId?: string): Promise<any[]> => {
        const params: any = { q: query };
        if (classId) params.classId = classId;
        const response = await axios.get(`${API_BASE_URL}/search`, { params });
        return response.data;
    },

    logEvent: async (eventType: string, eventData?: any) => {
        // Placeholder for analytics ingestion
        try {
            const response = await axios.post(`${API_BASE_URL}/analytics/event?event_type=${eventType}`, eventData || {});
            return response.data;
        } catch (e) {
            console.warn('Analytics event failed', e);
            return null;
        }
    }
};
