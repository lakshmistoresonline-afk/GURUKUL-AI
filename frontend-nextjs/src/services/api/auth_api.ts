import axios from 'axios';
import {
  createUserWithEmailAndPassword,
  sendEmailVerification,
  sendPasswordResetEmail,
  signInWithEmailAndPassword,
  signOut,
} from 'firebase/auth';
import { firebaseAuth } from '@/lib/firebase';

const BASE_URL =
  process.env.NEXT_PUBLIC_API_URL_BASE ||
  `${process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000'}/api/v1`;

export const apiClient = axios.create({
  baseURL: BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(
  async (config) => {
    if (typeof window !== 'undefined') {
      const currentUser = firebaseAuth.currentUser;

      if (currentUser) {
        const token = await currentUser.getIdToken();

        config.headers = config.headers ?? {};
        config.headers.Authorization = `Bearer ${token}`;
      }
    }

    return config;
  },
  (error) => Promise.reject(error)
);

export const authApi = {
  login: async (email: string, password: string) => {
    const credential = await signInWithEmailAndPassword(
      firebaseAuth,
      email.trim(),
      password
    );

    const token = await credential.user.getIdToken();

    const response = await apiClient.post(
      '/auth/firebase/session',
      {},
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data;
  },

  register: async (data: {
    email: string;
    password: string;
    name: string;
    username?: string;
    class_id: string;
  }) => {
    const credential = await createUserWithEmailAndPassword(
      firebaseAuth,
      data.email.trim(),
      data.password
    );

    await sendEmailVerification(credential.user);

    const token = await credential.user.getIdToken();

    const response = await apiClient.post(
      '/auth/firebase/session',
      {
        name: data.name.trim(),
        username: data.username?.trim() || undefined,
        class_id: data.class_id,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    return response.data;
  },

  resetPassword: async (email: string) => {
    await sendPasswordResetEmail(
      firebaseAuth,
      email.trim()
    );
  },

  getMe: async () => {
    const response = await apiClient.get('/auth/me');
    return response.data;
  },

  logout: async () => {
    try {
      await apiClient.post('/auth/logout');
    } finally {
      await signOut(firebaseAuth);
    }
  },
};