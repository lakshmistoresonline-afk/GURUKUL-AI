'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { authApi } from '@/services/api/auth_api';

interface User {
  id: string;
  username: string;
  name: string;
  class_id: string; // 'class_5' or 'class_6'
  role: string;
  token: string;
}

interface AuthContextType {
  user: User | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const savedUser = localStorage.getItem('gurukul_user');
    if (savedUser) {
      try {
        setUser(JSON.parse(savedUser));
      } catch (e) {
        localStorage.removeItem('gurukul_user');
      }
    }
    setLoading(false);
  }, []);

  const login = async (username: string, password: string) => {
    try {
        const token = await authApi.login(username, password);

        const partialUser = { token };
        localStorage.setItem('gurukul_user', JSON.stringify(partialUser));

        const profile = await authApi.getMe();

        const fullUser: User = {
          id: profile.id,
          username: profile.username,
          name: profile.name || (profile.class_id === 'class_6' ? 'Class 6 Student' : 'Pilot Student'),
          class_id: profile.class_id || (username.toLowerCase().includes('6') ? 'class_6' : 'class_5'),
          role: profile.role,
          token: token
        };

        setUser(fullUser);
        localStorage.setItem('gurukul_user', JSON.stringify(fullUser));

        if (fullUser.role === 'ADMIN') {
            window.location.href = '/admin/dashboard';
        } else {
            window.location.href = '/';
        }
    } catch (e) {
        console.error("Login failed", e);
        localStorage.removeItem('gurukul_user');
        throw e;
    }
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('gurukul_user');
    window.location.href = '/';
  };

  return (
    <AuthContext.Provider value={{ user, login, logout, loading }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
