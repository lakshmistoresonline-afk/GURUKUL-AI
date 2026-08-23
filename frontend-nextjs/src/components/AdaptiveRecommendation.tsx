'use client';

import React, { useEffect, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, ArrowRight, Brain, Zap, Target, BookOpen, RotateCcw, Library } from 'lucide-react';
import { useRouter } from 'next/navigation';
import api from '@/services/api';
import { progressService } from '@/services/progress';

interface Recommendation {
  action: string;
  target_id: string;
  reason: string;
  context: string;
}

export default function AdaptiveRecommendation({ profile, currentChapter }: { profile: any, currentChapter?: any }) {
  const [recommendation, setRecommendation] = useState<Recommendation | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    if (!profile) return;

    const class_name = profile.className || `class_${profile.classId}`;
    if (!class_name) return;

    const fetchRecommendation = async () => {
      setLoading(true);
      try {
        let student_record: any = { conceptPerformance: {} };
        let chapterId = currentChapter?.id;
        let subject = (currentChapter?.subject || 'general').toLowerCase().replace(/ /g, '_');

        if (chapterId) {
          const record = await progressService.getMastery(chapterId);
          if (record) student_record = record;
        } else {
          // If no current chapter, fetch the first one from hierarchy to suggest starting
          try {
              const h = await api.get('/api/chapters/explorer/hierarchy');
              const classKey = Object.keys(h.data).find(k => k.includes(profile.classId)) || Object.keys(h.data)[0];
              if (classKey && h.data[classKey]) {
                  const firstSub = Object.keys(h.data[classKey])[0];
                  const firstChap = h.data[classKey][firstSub][0];
                  if (firstChap) {
                      setRecommendation({
                        action: 'LEARN_CONCEPT',
                        target_id: firstChap.id,
                        reason: `Start your journey with ${firstChap.name}`,
                        context: 'INITIAL'
                      });
                      setLoading(false);
                      return;
                  }
              }
          } catch (e) {
              console.warn("Recommendation: Fallback fetch failed", e);
          }

          setRecommendation({
            action: 'EXPLORE_LIBRARY',
            target_id: '',
            reason: 'Start your learning journey by exploring the curriculum.',
            context: 'INITIAL'
          });
          setLoading(false);
          return;
        }

        const res = await api.post('/api/adaptive/next-step', {
          uid: profile.uid,
          class_name,
          subject,
          chapter_id: chapterId,
          student_record
        });

        setRecommendation(res.data);
      } catch (err: any) {
        if (err.response?.status === 404) {
           console.warn("Adaptive system: No path mapped for this chapter yet.");
        } else if (err.code === 'ERR_CANCELED') {
           // Ignore silent cancellation
        } else {
           console.error("Failed to fetch adaptive recommendation", err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendation();
  }, [profile?.uid, currentChapter?.id, currentChapter?.subject, profile?.className, profile]);

  if (loading) return <div className="h-40 bg-slate-100 rounded-[40px] animate-pulse" />;
  if (!recommendation) return null;

  const getActionConfig = (action: string) => {
    const chapterId = currentChapter?.id;
    const subject = currentChapter?.subject || 'mathematics';
    const className = profile?.className;
    const queryParams = `?class=${className}&subject=${subject}`;

    switch (action) {
      case 'LEARN_CONCEPT': return { icon: BookOpen, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-100', label: 'Recommended Study', path: `/learn/${chapterId}${queryParams}` };
      case 'PRACTICE_CONCEPT': return { icon: Target, color: 'text-emerald-600', bg: 'bg-emerald-50', border: 'border-emerald-100', label: 'Practice Session', path: `/quiz/${chapterId}${queryParams}` };
      case 'REMEDIATE_CONCEPT': return { icon: RotateCcw, color: 'text-amber-600', bg: 'bg-amber-50', border: 'border-amber-100', label: 'Neural Repair', path: `/quiz/interleaved?mode=remediation&conceptId=${recommendation.target_id}&class=${className}&subject=${subject}` };
      case 'RETENTION_REVIEW': return { icon: Brain, color: 'text-indigo-600', bg: 'bg-indigo-50', border: 'border-indigo-100', label: 'Daily Retrieval', path: `/quiz/interleaved?type=quick&class=${className}&subject=${subject}` };
      case 'EXPLORE_LIBRARY': return { icon: Library, color: 'text-primary', bg: 'bg-blue-50', border: 'border-blue-100', label: 'Curriculum Hub', path: `/library` };
      default: return { icon: Sparkles, color: 'text-blue-600', bg: 'bg-blue-50', border: 'border-blue-100', label: 'Next Step', path: '/library' };
    }
  };

  const config = getActionConfig(recommendation.action);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white border border-slate-200/60 rounded-[40px] p-8 flex flex-col md:flex-row items-center justify-between gap-8 group hover:bg-slate-50 transition-all shadow-sm"
    >
       <div className="flex items-center gap-6 text-center md:text-left">
          <div className={`w-16 h-16 rounded-3xl ${config.bg} flex items-center justify-center ${config.color} border ${config.border} shadow-sm`}>
             <config.icon size={32} />
          </div>
          <div className="space-y-1">
             <p className={`text-[10px] font-black uppercase tracking-[0.2em] ${config.color}`}>{config.label}</p>
             <h4 className="text-2xl font-black text-slate-900">{recommendation.reason}</h4>
             <p className="text-slate-500 text-xs font-bold uppercase tracking-widest">{recommendation.context} PHASE</p>
          </div>
       </div>

       <button
         onClick={() => router.push(config.path)}
         className="bg-slate-900 text-white px-10 py-5 rounded-2xl font-black text-sm uppercase tracking-widest flex items-center gap-3 shadow-md hover:bg-blue-600 active:scale-95 transition-all"
       >
          Initialize <ArrowRight size={18} />
       </button>
    </motion.div>
  );
}
