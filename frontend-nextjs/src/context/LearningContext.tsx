'use client';

import React, { createContext, useContext, useEffect, useState } from 'react';
import { useAuth } from './AuthContext';

interface ActiveChapter {
  id: string;
  name: string;
}

interface LearningContextType {
  activeSubject: string | null;
  activeChapter: ActiveChapter | null;
  setSubject: (subject: string | null) => void;
  setChapter: (chapter: ActiveChapter | null) => void;
  clearContext: () => void;
  isContextComplete: boolean;
}

const LearningContext = createContext<LearningContextType>({
  activeSubject: null,
  activeChapter: null,
  setSubject: () => {},
  setChapter: () => {},
  clearContext: () => {},
  isContextComplete: false,
});

export const useLearning = () => useContext(LearningContext);

export const LearningProvider = ({ children }: { children: React.ReactNode }) => {
  const { profile } = useAuth();
  const [activeSubject, setActiveSubject] = useState<string | null>(null);
  const [activeChapter, setActiveChapter] = useState<ActiveChapter | null>(null);

  // Load from localStorage on mount or profile change
  useEffect(() => {
    if (profile) {
      const savedSubject = localStorage.getItem(`subject:${profile.uid}`);
      const savedChapter = localStorage.getItem(`chapter:${profile.uid}`);

      if (savedSubject) setActiveSubject(savedSubject);
      if (savedChapter) {
        try {
          setActiveChapter(JSON.parse(savedChapter));
        } catch (e) {
          console.error("Failed to parse saved chapter", e);
        }
      }
    }
  }, [profile]);

  // Sync to localStorage
  useEffect(() => {
    if (profile) {
      if (activeSubject) {
        localStorage.setItem(`subject:${profile.uid}`, activeSubject);
      } else {
        localStorage.removeItem(`subject:${profile.uid}`);
      }

      if (activeChapter) {
        localStorage.setItem(`chapter:${profile.uid}`, JSON.stringify(activeChapter));
      } else {
        localStorage.removeItem(`chapter:${profile.uid}`);
      }
    }
  }, [activeSubject, activeChapter, profile]);

  const setSubject = (subject: string | null) => {
    setActiveSubject(subject);
    if (subject !== activeSubject) {
        setActiveChapter(null);
    }
  };

  const setChapter = (chapter: ActiveChapter | null) => {
    setActiveChapter(chapter);
  };

  const clearContext = () => {
    setActiveSubject(null);
    setActiveChapter(null);
  };

  const isContextComplete = !!(activeSubject && activeChapter);

  return (
    <LearningContext.Provider value={{
        activeSubject,
        activeChapter,
        setSubject,
        setChapter,
        clearContext,
        isContextComplete
    }}>
      {children}
    </LearningContext.Provider>
  );
};
