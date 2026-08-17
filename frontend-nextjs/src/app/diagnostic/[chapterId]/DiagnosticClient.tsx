'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { quizService, chapterService } from '@/services/api';
import { getChapterDisplayData } from '@/utils/chapter';
import {
  Brain,
  ChevronLeft,
  ArrowRight,
  CheckCircle2,
  AlertCircle,
  Zap,
  RefreshCw,
  Info
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';

export default function DiagnosticClient() {
  const { profile, loading: authLoading } = useAuth();
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const chapterId = params.chapterId as string;
  const className = searchParams.get('class') || profile?.className || 'class_5';
  const subject = searchParams.get('subject') || 'mathematics';

  const [questions, setQuestions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [responses, setResponses] = useState<any[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [signals, setSignals] = useState<any>(null);
  const [pkg, setPackage] = useState<any>(null);

  const displayData = getChapterDisplayData(chapterId, pkg);

  useEffect(() => {
    if (authLoading) return;
    const load = async () => {
      try {
        const [qData, pkgData] = await Promise.all([
           quizService.getDiagnostic(className, subject, chapterId),
           chapterService.getPackage(className, subject, chapterId)
        ]);
        setQuestions(qData);
        setPackage(pkgData);
      } catch (e) {
        console.error("Failed to load diagnostic", e);
      } finally {
        setLoading(false);
      }
    };
    load();
  }, [chapterId, className, subject, authLoading]);

  const handleSubmit = () => {
    if (!selectedOption) return;
    const current = questions[currentIndex];
    const isCorrect = selectedOption.toLowerCase().trim() === current.correctAnswer.toLowerCase().trim();

    const newResponses = [...responses, {
      question_id: current.id,
      is_correct: isCorrect,
      concept_id: current.concept_id,
      is_prereq: current.is_prereq || false
    }];
    setResponses(newResponses);

    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelectedOption(null);
    } else {
      process(newResponses);
    }
  };

  const process = async (finalResponses: any[]) => {
    setLoading(true);
    try {
      const res = await quizService.processDiagnostic(className, subject, chapterId, finalResponses);
      setSignals(res.concept_signals);
      setShowResults(true);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="min-h-screen bg-[#0F172A] flex items-center justify-center text-white uppercase font-black tracking-widest text-[10px]">Neural Diagnostic in progress...</div>;

  if (showResults) return (
     <div className="min-h-screen bg-[#0F172A] p-12 flex items-center justify-center">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
          className="bg-slate-900 border border-white/10 rounded-[60px] p-16 max-w-3xl w-full text-center shadow-2xl relative overflow-hidden"
        >
           <div className="relative z-10">
              <Brain className="mx-auto text-primary mb-8 animate-pulse" size={80} />
              <h2 className="text-4xl font-black text-white mb-2 uppercase italic tracking-tight">Diagnostic Mapped</h2>
              <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px] mb-8">{displayData.name}</p>
              <p className="text-slate-500 font-bold uppercase tracking-[0.3em] text-[10px] mb-12">Your Personalized Learning Path is Ready</p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left mb-12">
                 {Object.entries(signals || {}).map(([key, signal]: any) => (
                    <div key={key} className="p-5 bg-white/5 border border-white/5 rounded-3xl flex items-center justify-between group hover:border-primary/30 transition-all">
                       <span className="text-[10px] font-black text-slate-400 uppercase tracking-wider truncate mr-4">{key.replace('PREREQ_', 'PRE: ')}</span>
                       <span className={`px-3 py-1 rounded-full text-[8px] font-black uppercase tracking-widest ${
                          signal === 'STRONG' ? 'bg-emerald-500/20 text-emerald-400' :
                          signal === 'PREREQUISITE_GAP' ? 'bg-red-500/20 text-red-400 border border-red-500/20' :
                          'bg-blue-500/20 text-blue-400'
                       }`}>{signal.replace('_', ' ')}</span>
                    </div>
                 ))}
              </div>

              <button
                onClick={() => router.push(`/learn/${chapterId}?class=${className}&subject=${subject}`)}
                className="w-full py-6 bg-primary text-white rounded-[28px] font-black uppercase tracking-[0.2em] text-sm shadow-glow shadow-primary/20 hover:scale-[1.02] active:scale-95 transition-all flex items-center justify-center gap-3"
              >
                 Initialize Neural Journey <ArrowRight size={20} />
              </button>
           </div>
           <div className="absolute -top-24 -right-24 w-96 h-96 bg-primary/10 rounded-full blur-[120px]" />
        </motion.div>
     </div>
  );

  const current = questions[currentIndex];
  return (
    <div className="min-h-screen bg-[#0F172A] p-8 md:p-24 flex flex-col items-center">
      <div className="max-w-3xl w-full space-y-12">
        <div className="flex items-center justify-between">
           <button onClick={() => router.back()} className="text-slate-500 hover:text-white transition-colors flex items-center gap-2 text-[10px] font-black uppercase tracking-widest text-left">
              <ChevronLeft size={16} />
              <div>
                 <span className="block opacity-50">Abort Analysis</span>
                 <span className="text-white font-bold">{displayData.fullName}</span>
              </div>
           </button>
           <div className="text-[10px] font-black text-primary uppercase tracking-[0.4em]">
              Probe {currentIndex + 1} / {questions.length}
           </div>
        </div>

        <div className="h-1 bg-white/5 rounded-full overflow-hidden">
           <motion.div className="h-full bg-primary shadow-glow shadow-primary/40" animate={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }} />
        </div>

        <motion.div
          key={currentIndex} initial={{ opacity: 0, x: 20 }} animate={{ opacity: 1, x: 0 }}
          className="bg-slate-900 border border-white/5 rounded-[50px] p-16 shadow-2xl relative overflow-hidden"
        >
           {current.is_prereq && (
             <div className="absolute top-8 right-12 px-4 py-1 bg-amber-500/10 text-amber-500 border border-amber-500/20 rounded-full text-[8px] font-black uppercase tracking-widest flex items-center gap-2">
                <Zap size={10} /> Prerequisite Check
             </div>
           )}
           <h3 className="text-2xl md:text-3xl font-black text-white leading-tight mb-12">
              {current.question}
           </h3>

           <div className="grid gap-4">
              {current.options.map((opt: string, i: number) => (
                 <button
                   key={opt}
                   onClick={() => setSelectedOption(opt)}
                   className={`p-8 rounded-[32px] text-left font-bold text-lg transition-all flex items-center gap-6 border-2 ${
                      selectedOption === opt ? 'bg-primary/10 border-primary text-white shadow-glow shadow-primary/5' : 'bg-white/[0.02] border-white/5 text-slate-400 hover:bg-white/[0.04]'
                   }`}
                 >
                    <div className={`w-10 h-10 rounded-2xl flex items-center justify-center font-black text-sm shrink-0 ${
                       selectedOption === opt ? 'bg-primary text-white shadow-glow' : 'bg-slate-800 text-slate-500'
                    }`}>
                       {String.fromCharCode(65 + i)}
                    </div>
                    {opt}
                 </button>
              ))}
           </div>

           <button
             disabled={!selectedOption}
             onClick={handleSubmit}
             className="w-full mt-16 py-6 bg-white text-slate-900 rounded-[28px] font-black uppercase tracking-[0.2em] text-xs shadow-2xl hover:bg-primary hover:text-white transition-all disabled:opacity-20 disabled:grayscale"
           >
              Capture Evidence
           </button>
        </motion.div>
      </div>
    </div>
  );
}
