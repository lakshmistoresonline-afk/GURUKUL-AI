import axios from 'axios';

const API_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_URL,
});

// Helper to set security context from AuthContext
export const setSecurityContext = (profile: any, token?: string) => {
  if (token) {
    console.log("API: Security context initialized");
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    console.log("API: Clearing Authorization header");
    delete api.defaults.headers.common['Authorization'];
  }
};

// Request interceptor to catch missing tokens before they hit the wire
api.interceptors.request.use(config => {
  if (!config.headers['Authorization']) {
    console.warn(`API: Missing Authorization header for ${config.url}`);
  }
  return config;
});

// Response interceptor to handle specialized errors
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      console.error("API: 401 Unauthorized - Token may be expired or invalid");
    } else if (error.response?.status === 403) {
      console.error("API: 403 Forbidden - Access denied to this resource");
    } else if (error.response?.status === 404) {
       // Only log warning for 404 as it might be an expected "not found" state for optional data
       console.warn(`API: 404 Not Found - ${error.config.url}`);
    } else if (error.code === 'ERR_CANCELED') {
       console.log("API: Request canceled");
    } else {
      console.error(`API Error (${error.response?.status || 'Network'}):`, error.message);
    }
    return Promise.reject(error);
  }
);

// Lightweight Client-Side Cache
const chapterCache: Record<string, { data: any, timestamp: number }> = {};
const CACHE_TTL = 5 * 60 * 1000; // 5 minutes

export const chapterService = {
  processChapter: async (formData: FormData) => {
    const response = await api.post('/api/chapters/process', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  getJobStatus: async (jobId: string) => {
    const response = await api.get(`/api/chapters/status/${jobId}`);
    return response.data;
  },
  getPackage: async (className: string, subject: string, chapterId: string, signal?: AbortSignal) => {
    const cacheKey = `pkg:${className}:${subject}:${chapterId}`;
    if (chapterCache[cacheKey] && (Date.now() - chapterCache[cacheKey].timestamp < CACHE_TTL)) {
       return chapterCache[cacheKey].data;
    }

    const response = await api.get(`/api/chapters/package/${className}/${subject}/${chapterId}`, { signal });
    chapterCache[cacheKey] = { data: response.data, timestamp: Date.now() };
    return response.data;
  },
  getHierarchy: async () => {
    const cacheKey = 'hierarchy';
    if (chapterCache[cacheKey] && (Date.now() - chapterCache[cacheKey].timestamp < CACHE_TTL)) {
       return chapterCache[cacheKey].data;
    }
    const response = await api.get('/api/chapters/explorer/hierarchy');
    chapterCache[cacheKey] = { data: response.data, timestamp: Date.now() };
    return response.data;
  },
  invalidateCache: () => {
    Object.keys(chapterCache).forEach(key => delete chapterCache[key]);
  }
};

export const mediaService = {
  generateMedia: async (chapterId: string, className: string, subject: string, type = 'animation') => {
    const response = await api.post('/api/media/generate', { chapter_id: chapterId, class_name: className, subject, type });
    return response.data;
  },
  getStatus: async (jobId: string) => {
    const response = await api.get(`/api/media/status/${jobId}`);
    return response.data;
  },
  getChapterMedia: async (chapterId: string, signal?: AbortSignal) => {
    const cacheKey = `media:${chapterId}`;
    if (chapterCache[cacheKey] && (Date.now() - chapterCache[cacheKey].timestamp < CACHE_TTL)) {
       return chapterCache[cacheKey].data;
    }
    const response = await api.get(`/api/media/chapter/${chapterId}`, { signal });
    chapterCache[cacheKey] = { data: response.data, timestamp: Date.now() };
    return response.data;
  },
  discoverMedia: async (params: { class_name?: string, subject?: string, limit?: number }) => {
    const response = await api.get('/api/media/discover', { params });
    return response.data;
  },
  getExternalResources: async (params: {
    class_name?: string,
    subject?: string,
    chapter_id?: string,
    resource_type?: string,
    search?: string,
    limit?: number
  }, signal?: AbortSignal) => {
    const response = await api.get('/api/media/external', { params, signal });
    return response.data;
  },
  getExternalStats: async () => {
    const response = await api.get('/api/media/external/stats');
    return response.data;
  },
  getClassSummary: async (className: string) => {
    const response = await api.get(`/api/media/summary/${className}`);
    return response.data;
  },
  getHubData: async () => {
    const response = await api.get('/api/media/hub');
    return response.data;
  },
  getAdminAllExternal: async (params: {
    class_name?: string,
    subject?: string,
    status?: string
  }) => {
    const response = await api.get('/api/media/admin/external/all', { params });
    return response.data;
  },
  getAdminPending: async (params: {
    class_name?: string,
    subject?: string,
    provider?: string
  }) => {
    const response = await api.get('/api/media/admin/external/pending', { params });
    return response.data;
  },
  verifyExternal: async (resourceId: string) => {
    const response = await api.post(`/api/media/admin/external/${resourceId}/verify`);
    return response.data;
  },
  rejectExternal: async (resourceId: string) => {
    const response = await api.post(`/api/media/admin/external/${resourceId}/reject`);
    return response.data;
  },
  reloadExternalCatalogs: async () => {
    const response = await api.post('/api/media/admin/external/reload');
    return response.data;
  }
};

export const resourceService = {
  getChapterResources: async (chapterId: string, signal?: AbortSignal) => {
    const cacheKey = `res:${chapterId}`;
    if (chapterCache[cacheKey] && (Date.now() - chapterCache[cacheKey].timestamp < CACHE_TTL)) {
       return chapterCache[cacheKey].data;
    }
    const response = await api.get(`/api/resources/${chapterId}`, { signal });
    chapterCache[cacheKey] = { data: response.data, timestamp: Date.now() };
    return response.data;
  },
  verifyResource: async (chapterInfo: any, candidate: any) => {
    const response = await api.post('/api/resources/verify', { chapter_info: chapterInfo, candidate });
    return response.data;
  },
  analyzeCollection: async (providerId: string, collectionId: string) => {
    const response = await api.post(`/api/resources/analyze-collection?provider_id=${providerId}&collection_id=${collectionId}`);
    return response.data;
  },
  runIntegrityCheck: async () => {
    const response = await api.post('/api/resources/check-integrity');
    return response.data;
  },
  getCollections: async () => {
    const response = await api.get('/api/resources/collections');
    return response.data;
  },
};

export const aiService = {
  generate: async (prompt: string, taskType = 'general') => {
    const response = await api.post('/api/ai/generate', { prompt, task_type: taskType });
    return response.data;
  },
  generateStructured: async (prompt: string, schema: any, taskType = 'structured') => {
    const response = await api.post('/api/ai/generate-structured', { prompt, schema, task_type: taskType });
    return response.data;
  },
};

export const quizService = {
  generateDynamic: async (className: string, subject: string, chapterId: string, count = 5, difficulty = 'Medium') => {
    const response = await api.post('/api/quiz/generate-dynamic', {
      class_name: className,
      subject,
      chapter_id: chapterId,
      count,
      difficulty
    });
    return response.data;
  },
  getDiagnostic: async (className: string, subject: string, chapterId: string) => {
    const response = await api.get(`/api/quiz/diagnostic/${className}/${subject}/${chapterId}`);
    return response.data;
  },
  processDiagnostic: async (className: string, subject: string, chapterId: string, results: any[]) => {
    const response = await api.post('/api/quiz/process-diagnostic', {
      class_name: className,
      subject,
      chapter_id: chapterId,
      results
    });
    return response.data;
  },
  getBankStats: async () => {
    const response = await api.get('/api/quiz/bank/stats');
    return response.data;
  },
  getSession: async (params: {
    type: 'quick' | 'chapter' | 'concept' | 'mastery' | 'full' | 'remediation',
    classId?: number,
    subject?: string,
    chapterId?: string,
    conceptId?: string,
    count?: number
  }) => {
    const response = await api.get('/api/quiz/session', { params });
    return response.data;
  },
  getInterleaved: async (className: string, subject: string, count: number, studentMastery: any[]) => {
    const response = await api.post('/api/quiz/interleaved', {
      uid: 'current_user', // Auth service handles this on backend if needed, but we pass UID
      class_name: className,
      subject,
      count,
      student_mastery: studentMastery
    });
    return response.data;
  }
};

export const feynmanService = {
  getChallenge: async (className: string, subject: string, chapterId: string, level = 1) => {
    const response = await api.post('/api/feynman/challenge', {
      class_name: className,
      subject,
      chapter_id: chapterId,
      level
    });
    return response.data;
  },
  evaluate: async (className: string, subject: string, chapterId: string, concept: string, explanation: string, level = 1) => {
    const response = await api.post('/api/feynman/evaluate', {
      class_name: className,
      subject,
      chapter_id: chapterId,
      concept,
      explanation,
      level
    });
    return response.data;
  }
};

export const srsService = {
  getDueItems: async (studentId: string, contentType?: string, limit = 10) => {
    const response = await api.get(`/api/srs/due/${studentId}`, {
      params: { content_type: contentType, limit }
    });
    return response.data;
  },
  recordReview: async (studentId: string, contentId: string, contentType: string, rating: number) => {
    const response = await api.post('/api/srs/review', {
      student_id: studentId,
      content_id: contentId,
      content_type: contentType,
      rating
    });
    return response.data;
  },
  getSession: async (studentId: string, contentType?: string) => {
    const response = await api.get(`/api/srs/session/${studentId}`, {
      params: { content_type: contentType }
    });
    return response.data;
  }
};

export const masteryService = {
  getConfig: async (className: string, subject: string, chapterId: string) => {
    const response = await api.get(`/api/mastery/${className}/${subject}/${chapterId}`);
    return response.data;
  },
  calculateState: async (className: string, subject: string, chapterId: string, studentRecord: any) => {
    const response = await api.post(`/api/mastery/calculate-state`, {
      class_name: className,
      subject,
      chapter_id: chapterId,
      student_record: studentRecord
    });
    return response.data;
  },
  getRemediation: async (className: string, subject: string, chapterId: string, conceptId: string) => {
    const response = await api.get(`/api/mastery/remediation/${className}/${subject}/${chapterId}/${conceptId}`);
    return response.data;
  }
};

export const generalLearningService = {
  getHome: async (uid: string) => {
    const response = await api.get('/api/general-learning/home', { params: { uid } });
    return response.data;
  },
  getToday: async (uid: string) => {
    const response = await api.get('/api/general-learning/today', { params: { uid } });
    return response.data;
  },
  getCategory: async (category: string) => {
    const response = await api.get(`/api/general-learning/category/${category}`);
    return response.data;
  },
  getContent: async (id: string) => {
    const response = await api.get(`/api/general-learning/content/${id}`);
    return response.data;
  },
  recordProgress: async (uid: string, contentId: string, rating: number) => {
    const response = await api.post('/api/general-learning/progress', { uid, content_id: contentId, rating });
    return response.data;
  }
};

export default api;
