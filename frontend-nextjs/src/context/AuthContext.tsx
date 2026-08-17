'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { onAuthStateChanged, User } from 'firebase/auth';
import { auth, db } from '../lib/firebase';
import { doc, getDoc } from 'firebase/firestore';
import { setSecurityContext } from '../services/api';

interface UserProfile {
  uid: string;
  email: string;
  name: string;
  role: string;
  classId: string;
  className: string;
  xp: number;
}

interface AuthContextType {
  user: User | null;
  profile: UserProfile | null;
  loading: boolean;
  mustOnboard: boolean;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  profile: null,
  loading: true,
  mustOnboard: false,
  refreshProfile: async () => {},
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [mustOnboard, setMustOnboard] = useState(false);

  const fetchProfile = async (u: User) => {
    try {
      const token = await u.getIdToken();
      const userRef = doc(db, 'users', u.uid);
      const userSnap = await getDoc(userRef);
      if (userSnap.exists()) {
        const data = userSnap.data();
        const p = {
          uid: u.uid,
          email: u.email!,
          name: data.name,
          role: data.role,
          classId: data.classId,
          className: data.classId ? `class_${data.classId}` : '',
          xp: data.xp || 0,
        };
        setProfile(p);
        setMustOnboard(!data.classId);
        setSecurityContext(p, token);
      } else {
        setMustOnboard(true);
      }
    } catch (err) {
      console.error("Auth profile fetch error:", err);
    }
  };

  const refreshProfile = async () => {
    if (user) {
      await fetchProfile(user);
    }
  };

  useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (u) => {
      setUser(u);
      if (u) {
        await fetchProfile(u);
      } else {
        setProfile(null);
        setMustOnboard(false);
        setSecurityContext(null);
      }
      setLoading(false);
    });

    return () => unsubscribe();
  }, []);

  return (
    <AuthContext.Provider value={{ user, profile, loading, mustOnboard, refreshProfile }}>
      {children}
    </AuthContext.Provider>
  );
};
