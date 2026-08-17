'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { generalLearningService } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import {
  ArrowLeft,
  ArrowRight,
  Book,
  Globe,
  Brain,
  CheckCircle2,
  RefreshCw,
  Zap,
  Volume2,
  Sparkles,
  Trophy,
  X,
  ChevronRight
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import FormattedText from '@/components/FormattedText';

export default function LearnClient() {
  const { id } = useParams() as { id: string };
  const { profile, loading: authLoading } = useAuth();
  const router = useRouter();

  const [item, setItem] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [mode, setMode] = useState<'learn' | 'practice' | 'result'>('learn');
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isCorrect, setIsCorrect] = useState<boolean | null>(null);

  useEffect(() => {
    if (authLoading || !profile) return;

    const fetchItem = async () => {
      try {
        const data = await generalLearningService.getContent(id);
        setItem(data);
      } catch (err) {
        console.error("Failed to load learning item", err);
        router.push('/general-learning');
      } finally {
        setLoading(false);
      }
    };
    fetchItem();
  }, [authLoading, profile, id, router]);

  const handlePractice = () => {
    if (!profile) return;
    if (selectedOption === (item.answer || item.practice?.answer)) {
      setIsCorrect(true);
      generalLearningService.recordProgress(profile.uid, id, 4); // 4 = Easy/Mastered
    } else {
      setIsCorrect(false);
      generalLearningService.recordProgress(profile.uid, id, 1); // 1 = Again/Fail
    }
    setMode('result');
  };

  if (authLoading || loading) return (
    <div className="flex min-h-screen bg-[#F8FAFC] items-center justify-center">
       <RefreshCw className="animate-spin text-primary" size={32} />
    </div>
  );

  const title = item.title || item.word || item.topic;
  const category = item.type;

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900 selection:bg-primary/10">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title="Active Learning" />

        <div className="max-w-4xl mx-auto p-6 md:p-10 space-y-8">

           <div className="flex items-center justify-between">
              <button
                onClick={() => router.back()}
                className="flex items-center gap-3 px-6 py-3 bg-white border border-slate-200 rounded-2xl text-xs font-bold uppercase tracking-widest text-slate-600 hover:text-primary transition-all shadow-sm"
              >
                 <ArrowLeft size={16} /> Exit
              </button>

              <div className="flex bg-slate-100 p-1.5 rounded-2xl border border-slate-200">
                 <div className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${mode === 'learn' ? 'bg-white text-primary shadow-sm' : 'text-slate-400'}`}>Learn</div>
                 <div className={`px-6 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest transition-all ${mode === 'practice' ? 'bg-white text-primary shadow-sm' : 'text-slate-400'}`}>Practice</div>
              </div>
           </div>

           <AnimatePresence mode="wait">
              {mode === 'learn' && (
                <motion.div
                   key="learn"
                   initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -20 }}
                   className="space-y-8"
                >
                   <section className="bg-white border border-slate-200 rounded-[48px] p-10 md:p-16 shadow-xl relative overflow-hidden">
                      <div className="relative z-10 space-y-12">
                         <div className="flex items-center gap-4">
                            <div className="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100 shadow-sm">
                               {category === 'vocabulary' ? <Book size={24} /> : category === 'brain_boost' ? <Brain size={24} /> : <Globe size={24} />}
                            </div>
                            <div>
                               <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none mb-1">{category.replace('_', ' ')}</p>
                               <h2 className="text-4xl font-black text-slate-900 tracking-tight">{title}</h2>
                            </div>
                         </div>

                         <div className="space-y-8">
                            {category === 'vocabulary' ? (
                               <div className="grid gap-8">
                                  <div className="space-y-3">
                                     <p className="text-xs font-black text-primary uppercase tracking-widest">Meaning</p>
                                     <p className="text-2xl font-bold text-slate-800 italic leading-relaxed">
                                        &ldquo;{item.meaning}&rdquo;
                                     </p>
                                  </div>
                                  <div className="space-y-3 p-8 bg-slate-50 rounded-[32px] border border-slate-100">
                                     <p className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                        <Volume2 size={14} /> Example Usage
                                     </p>
                                     <p className="text-xl font-medium text-slate-700 leading-relaxed italic">
                                        &ldquo;{item.example}&rdquo;
                                     </p>
                                  </div>
                                  <div className="grid grid-cols-2 gap-6">
                                     <div className="p-6 bg-emerald-50/50 border border-emerald-100 rounded-3xl">
                                        <p className="text-[10px] font-black text-emerald-600 uppercase tracking-widest mb-2">Synonyms</p>
                                        <p className="font-bold text-slate-700">{item.synonyms?.join(', ')}</p>
                                     </div>
                                     <div className="p-6 bg-rose-50/50 border border-rose-100 rounded-3xl">
                                        <p className="text-[10px] font-black text-rose-600 uppercase tracking-widest mb-2">Antonyms</p>
                                        <p className="font-bold text-slate-700">{item.antonyms?.join(', ')}</p>
                                     </div>
                                  </div>
                               </div>
                            ) : (
                               <div className="space-y-6">
                                  <div className="p-10 bg-slate-50 border border-slate-100 rounded-[40px]">
                                     <p className="text-xs font-black text-slate-400 uppercase tracking-widest mb-4">The Topic</p>
                                     <h3 className="text-3xl font-black text-slate-800 leading-tight">{item.topic}</h3>
                                     <div className="mt-8 prose prose-slate max-w-none text-xl leading-relaxed">
                                        {item.explanation}
                                     </div>
                                  </div>
                               </div>
                            )}
                         </div>

                         <button
                           onClick={() => setMode('practice')}
                           className="w-full bg-primary text-white py-6 rounded-3xl font-black text-sm uppercase tracking-widest flex items-center justify-center gap-3 hover:bg-blue-700 transition-all shadow-xl shadow-blue-500/20 active:scale-95"
                         >
                            Test Your Knowledge <ArrowRight size={20} />
                         </button>
                      </div>

                      <div className="absolute top-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-[100px] -mr-32 -mt-32 pointer-events-none" />
                   </section>
                </motion.div>
              )}

              {mode === 'practice' && (
                 <motion.div
                    key="practice"
                    initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} exit={{ opacity: 0, scale: 0.95 }}
                    className="space-y-10"
                 >
                    <div className="bg-white border border-slate-200 rounded-[48px] p-10 md:p-16 shadow-xl space-y-12">
                       <div className="space-y-4">
                          <p className="text-xs font-black text-primary uppercase tracking-widest">Knowledge Check</p>
                          <h3 className="text-3xl font-black text-slate-900 leading-tight">
                             {item.question || item.practice?.question}
                          </h3>
                       </div>

                       <div className="grid gap-4">
                          {(item.options || [item.word, 'Random', 'Another', 'Distractor']).map((opt: string) => (
                             <button
                                key={opt}
                                onClick={() => setSelectedOption(opt)}
                                className={`p-8 rounded-[32px] border-2 text-left font-bold text-xl transition-all ${
                                   selectedOption === opt
                                   ? 'bg-primary border-primary text-white shadow-xl scale-105'
                                   : 'bg-white border-slate-100 text-slate-600 hover:border-primary/20'
                                }`}
                             >
                                {opt}
                             </button>
                          ))}
                       </div>

                       <button
                          disabled={!selectedOption}
                          onClick={handlePractice}
                          className="w-full bg-slate-900 text-white py-6 rounded-3xl font-black text-sm uppercase tracking-widest flex items-center justify-center gap-3 hover:bg-black transition-all disabled:opacity-50"
                       >
                          Confirm Answer <ChevronRight size={20} />
                       </button>
                    </div>
                 </motion.div>
              )}

              {mode === 'result' && (
                 <motion.div
                    key="result"
                    initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
                    className="text-center space-y-12 py-12"
                 >
                    <div className={`w-32 h-32 rounded-full mx-auto flex items-center justify-center shadow-2xl ${isCorrect ? 'bg-emerald-500 text-white' : 'bg-rose-500 text-white'}`}>
                       {isCorrect ? <CheckCircle2 size={64} /> : <X size={64} />}
                    </div>

                    <div className="space-y-4">
                       <h2 className="text-5xl font-black tracking-tight text-slate-900">
                          {isCorrect ? 'Masterfully Done!' : 'Not Quite Yet'}
                       </h2>
                       <p className="text-xl font-medium text-slate-500 max-w-lg mx-auto leading-relaxed">
                          {isCorrect
                             ? 'Your memory bank has been updated. This item is now tracked in your neural network.'
                             : 'Mistakes are the best teachers. We will review this concept again soon to strengthen your foundation.'}
                       </p>
                    </div>

                    <div className="pt-6 flex flex-col items-center gap-4">
                       <button
                          onClick={() => router.push(`/general-learning/${category}`)}
                          className="bg-primary text-white px-16 py-5 rounded-3xl font-black text-sm uppercase tracking-widest hover:bg-blue-700 shadow-xl transition-all active:scale-95 flex items-center gap-3"
                       >
                          <Zap size={20} /> Back to {category.replace('_', ' ')}
                       </button>
                       <button
                          onClick={() => router.push('/general-learning')}
                          className="text-slate-400 font-bold uppercase tracking-widest text-xs hover:text-primary transition-colors"
                       >
                          Back to Knowledge Hub
                       </button>
                    </div>
                 </motion.div>
              )}
           </AnimatePresence>

        </div>
      </main>
    </div>
  );
}
