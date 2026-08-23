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
    <div className="space-y-8">
      <AnimatePresence mode="wait">
        {!activeSubject ? (
          <motion.div
            key="subjects"
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.95 }}
            className="grid grid-cols-1 md:grid-cols-2 gap-6"
          >
            {subjects.map((sub) => (
              <button
                key={sub}
                onClick={() => setSubject(sub)}
                className="group p-8 bg-white border border-slate-200 rounded-[48px] hover:border-primary/40 hover:shadow-xl transition-all text-left flex flex-col gap-6"
              >
                <div className="w-14 h-14 rounded-2xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-inner border border-slate-50">
                  <Layout size={28} />
                </div>
                <div>
                  <h3 className="text-2xl font-black text-slate-900 group-hover:text-primary transition-colors capitalize leading-none">{sub.replace(/_/g, ' ')}</h3>
                  <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mt-2">
                    {hierarchy[classKey][sub].length} Chapters
                  </p>
                </div>
                <div className="flex items-center justify-between pt-6 border-t border-slate-50 mt-auto">
                   <span className="text-[10px] font-black text-primary uppercase tracking-widest">Explore</span>
                   <ChevronRight size={18} className="text-slate-300 group-hover:text-primary group-hover:translate-x-1 transition-all" />
                </div>
              </button>
            ))}
          </motion.div>
        ) : (
          <motion.div
            key="chapters"
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            className="space-y-6"
          >
            <div className="flex items-center justify-between px-2">
                <div className="flex items-center gap-3">
                    <button
                        onClick={() => setSubject(null)}
                        className="text-[10px] font-black text-slate-400 uppercase tracking-widest hover:text-primary transition-colors flex items-center gap-2"
                    >
                        Subjects
                    </button>
                    <ChevronRight size={12} className="text-slate-300" />
                    <span className="text-[10px] font-black text-slate-900 uppercase tracking-widest capitalize">{activeSubject.replace('_', ' ')}</span>
                </div>
            </div>

            <div className="grid grid-cols-1 gap-4">
              {hierarchy[classKey][activeSubject].map((chap: any) => (
                <button
                  key={chap.id}
                  onClick={() => setChapter({ id: chap.id, name: chap.name })}
                  className="group p-5 bg-white border border-slate-200 rounded-[32px] hover:border-primary/40 hover:shadow-lg transition-all text-left flex items-center gap-6"
                >
                  <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-inner shrink-0 border border-slate-50">
                    <BookOpen size={18} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <h4 className="font-black text-slate-900 line-clamp-1 group-hover:text-primary transition-colors text-lg">{chap.name}</h4>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-0.5">Chapter {chap.number || chap.id}</p>
                  </div>
                  <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-300 group-hover:bg-primary group-hover:text-white transition-all shadow-sm">
                    <ChevronRight size={18} />
                  </div>
                </button>
              ))}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
