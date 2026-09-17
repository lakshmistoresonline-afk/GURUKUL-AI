'use client';

import React, {
  createContext,
  useContext,
  useEffect,
  useState,
} from 'react';

import {
  onAuthStateChanged,
  signOut,
  User as FirebaseUser,
} from 'firebase/auth';

import { firebaseAuth } from '@/lib/firebase';
import { authApi } from '@/services/api/auth_api';

export interface User {
  id: string;
  firebase_uid: string;
  email?: string | null;
  username: string;
  name?: string | null;
  class_id?: string | null;
  role: string;
}

interface RegisterData {
  email: string;
  password: string;
  name: string;
  username?: string;
  class_id: string;
}

interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  register: (data: RegisterData) => Promise<void>;
  resetPassword: (email: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

function normalizeRole(
  role: string | undefined | null
): string {
  return (role || 'student').toLowerCase();
}

function profileToUser(profile: any): User {
  return {
    id: profile.id,
    firebase_uid: profile.firebase_uid,
    email: profile.email ?? null,
    username: profile.username,
    name: profile.name ?? null,
    class_id: profile.class_id ?? null,
    role: normalizeRole(profile.role),
  };
}

async function establishExistingSession(
  firebaseUser: FirebaseUser
): Promise<any> {
  const token = await firebaseUser.getIdToken();

  const baseUrl =
    process.env.NEXT_PUBLIC_API_URL_BASE ||
    'http://127.0.0.1:8000/api/v1';

  const response = await fetch(
    `${baseUrl}/auth/firebase/session`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({}),
    }
  );

  if (!response.ok) {
    const body = await response.json().catch(() => ({}));

    throw new Error(
      body.detail ||
        'Unable to establish the Gurukul session.'
    );
  }

  return response.json();
}

export const AuthProvider: React.FC<{
  children: React.ReactNode;
}> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(
      firebaseAuth,
      async (firebaseUser) => {
        if (!firebaseUser) {
          setUser(null);
          setLoading(false);
          return;
        }

        try {
          const profile =
            await establishExistingSession(firebaseUser);

          setUser(profileToUser(profile));
        } catch (error) {
          console.error(
            'Existing Gurukul session restoration failed:',
            error
          );

          try {
            await signOut(firebaseAuth);
          } catch (signOutError) {
            console.error(
              'Firebase sign-out failed:',
              signOutError
            );
          }

          setUser(null);
        } finally {
          setLoading(false);
        }
      }
    );

    return () => unsubscribe();
  }, []);

  const login = async (
    email: string,
    password: string
  ): Promise<void> => {
    setLoading(true);

    try {
      const profile = await authApi.login(
        email,
        password
      );

      setUser(profileToUser(profile));

      if (
        normalizeRole(profile.role) === 'admin'
      ) {
        window.location.href = '/admin/dashboard';
      } else {
        window.location.href = '/';
      }
    } finally {
      setLoading(false);
    }
  };

  const register = async (
    data: RegisterData
  ): Promise<void> => {
    setLoading(true);

    try {
      const profile = await authApi.register(data);

      setUser(profileToUser(profile));

      window.location.href = '/';
    } finally {
      setLoading(false);
    }
  };

  const resetPassword = async (
    email: string
  ): Promise<void> => {
    await authApi.resetPassword(email);
  };

  const logout = async (): Promise<void> => {
    try {
      await authApi.logout();
    } finally {
      setUser(null);
      window.location.href = '/';
    }
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        login,
        register,
        resetPassword,
        logout,
        loading,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      'useAuth must be used within an AuthProvider'
    );
  }

  return context;
};