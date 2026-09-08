import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/api/v1';

export const authApi = {
  login: async (username: string, password: string): Promise<string> => {
    const params = new URLSearchParams();
    params.append('username', username);
    params.append('password', password);
    const response = await axios.post(`${BASE_URL}/auth/login`, params);
    return response.data.access_token;
  },

  register: async (data: any) => {
    const response = await axios.post(`${BASE_URL}/auth/register`, data);
    return response.data;
  },

  getMe: async (): Promise<any> => {
    const response = await axios.get(`${BASE_URL}/auth/me`);
    return response.data;
  }
};

// Axios Interceptor for Authorization
axios.interceptors.request.use(
  (config) => {
    const user = localStorage.getItem('gurukul_user');
    if (user) {
      const stored = JSON.parse(user);
      if (stored.token) {
        config.headers.Authorization = `Bearer ${stored.token}`;
      }
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor for Session Expiration
axios.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('gurukul_user');
      // Optional: window.location.href = '/';
      // We'll let the app handle redirection if needed,
      // but clearing storage stops the polling.
    }
    return Promise.reject(error);
  }
);
