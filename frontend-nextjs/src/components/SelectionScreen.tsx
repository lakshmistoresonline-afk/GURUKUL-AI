'use client';

import React, { useEffect, useState } from 'react';
import { useLearning } from '@/context/LearningContext';
import { chapterService } from '@/services/api';
import { normalizeClassName } from '@/utils/chapter';
import { useAuth } from '@/context/AuthContext';
import { BookOpen, GraduationCap, ChevronRight, Layout, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SelectionScreen() {
  const { profile } = useAuth();
  const { setSubject, setChapter, activeSubject } = useLearning();
  const [hierarchy, setHierarchy] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHierarchy = async () => {
      try {
        const h = await chapterService.getHierarchy();
        setHierarchy(h);
      } catch (e) {
        console.error("Failed to fetch hierarchy", e);
      } finally {
        setLoading(false);
      }
    };
    fetchHierarchy();
  }, []);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center py-12 gap-6">
        <div className="w-8 h-8 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
        <p className="font-black text-slate-400 uppercase tracking-[0.4em] text-[8px]">Curriculum Discovery...</p>
      </div>
    );
  }

  if (!hierarchy) return null;

  // Use normalized lookup for classKey
  const normUserClass = profile?.className ? normalizeClassName(profile.className) : 'class_5';
  const classKey = Object.keys(hierarchy).find(k => normalizeClassName(k) === normUserClass) || Object.keys(hierarchy)[0];
  const classHierarchy = hierarchy[classKey] || {};
  const subjects = Object.keys(classHierarchy);

  return (
    <div className="space-y-6">
      <AnimatePresence mode="wait">
        {!activeSubject ? (
          <motion.div
            key="subjects"
            initial={{ opacity: 0, scale: 0.98 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.98 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"
          >
            {subjects.map((sub) => (
              <button
                key={sub}
                onClick={() => setSubject(sub)}
                className="group p-6 bg-white border border-slate-200 rounded-3xl hover:border-primary/40 hover:shadow-lg transition-all text-left flex flex-col gap-4"
              >
                <div className="w-12 h-12 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-inner border border-slate-50">
                  <Layout size={24} />
                </div>
                <div>
                  <h3 className="text-xl font-black text-slate-900 group-hover:text-primary transition-colors capitalize leading-none">{sub.replace(/_/g, ' ')}</h3>
                  <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-1.5">
                    {hierarchy[classKey][sub].length} Units
                  </p>
                </div>
              </button>
            ))}
          </motion.div>
        ) : (
          <motion.div
            key="chapters"
            initial={{ opacity: 0, x: 10 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -10 }}
            className="space-y-4"
          >
            <div className="flex items-center justify-between px-2">
                <div className="flex items-center gap-2">
                    <button
                        onClick={() => setSubject(null)}
                        className="text-[9px] font-black text-slate-400 uppercase tracking-widest hover:text-primary transition-colors flex items-center gap-1.5"
                    >
                        Subjects
                    </button>
                    <ChevronRight size={10} className="text-slate-300" />
                    <span className="text-[9px] font-black text-slate-900 uppercase tracking-widest capitalize">{activeSubject.replace('_', ' ')}</span>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {hierarchy[classKey][activeSubject].map((chap: any) => (
                <button
                  key={chap.id}
                  onClick={() => setChapter({ id: chap.id, name: chap.name })}
                  className="group p-4 bg-white border border-slate-200 rounded-2xl hover:border-primary/40 hover:shadow-md transition-all text-left flex items-center gap-4"
                >
                  <div className="w-8 h-8 rounded-lg bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shrink-0">
                    <BookOpen size={16} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-bold text-slate-900 line-clamp-1 group-hover:text-primary transition-colors text-sm">{chap.name}</h4>
                    <p className="text-[8px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">Unit {chap.number || chap.id}</p>
                  </div>
                  <ChevronRight size={14} className="text-slate-300 group-hover:text-primary transition-all" />
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
