'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { generalLearningService } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import {
  Zap,
  RefreshCw,
  ArrowRight,
  Trophy,
  Star,
  CheckCircle2
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function DailySetPage() {
  const { profile, loading: authLoading } = useAuth();
  const router = useRouter();

  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);

  useEffect(() => {
    if (authLoading || !profile) return;

    const fetchSet = async () => {
      try {
        const data = await generalLearningService.getToday(profile.uid);
        setItems(data);
      } catch (err) {
        console.error("Failed to load daily set", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSet();
  }, [authLoading, profile]);

  if (authLoading || loading) return (
    <div className="flex min-h-screen bg-[#F8FAFC] items-center justify-center">
       <RefreshCw className="animate-spin text-primary" size={32} />
    </div>
  );

  if (items.length === 0) return (
     <div className="flex min-h-screen bg-[#F8FAFC] items-center justify-center p-6">
        <div className="text-center space-y-6">
           <CheckCircle2 size={64} className="mx-auto text-emerald-500" />
           <h2 className="text-3xl font-black text-slate-800">You&apos;re All Caught Up!</h2>
           <p className="text-slate-500 font-medium max-w-sm mx-auto">No new items for today. Check back tomorrow or explore categories manually.</p>
           <button onClick={() => router.push('/general-learning')} className="bg-primary text-white px-8 py-3 rounded-2xl font-bold">Back to Hub</button>
        </div>
     </div>
  );

  const currentItem = items[currentIndex];

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title="Daily Learning Set" />

        <div className="max-w-4xl mx-auto p-6 md:p-10 space-y-12">

           <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                 <div className="w-10 h-10 rounded-xl bg-primary/10 flex items-center justify-center text-primary font-black">
                    {currentIndex + 1}
                 </div>
                 <div className="space-y-1">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-none">Step {currentIndex + 1} of {items.length}</p>
                    <h3 className="text-lg font-black text-slate-800 uppercase tracking-tight">{currentItem.type.replace('_', ' ')}</h3>
                 </div>
              </div>

              <div className="w-48 h-2 bg-slate-100 rounded-full overflow-hidden">
                 <motion.div
                    className="h-full bg-primary"
                    initial={{ width: 0 }}
                    animate={{ width: `${((currentIndex + 1) / items.length) * 100}%` }}
                 />
              </div>
           </div>

           <div className="bg-white border border-slate-200 rounded-[48px] p-10 md:p-16 shadow-xl relative overflow-hidden text-center space-y-12">
              <div className="space-y-4">
                 <p className="text-xs font-black text-primary uppercase tracking-[0.2em]">Next Item Found</p>
                 <h2 className="text-5xl md:text-6xl font-black tracking-tight text-slate-900">
                    {currentItem.title || currentItem.word || currentItem.topic}
                 </h2>
                 <p className="text-xl font-medium text-slate-500 italic max-w-lg mx-auto">
                    &ldquo;{currentItem.meaning || currentItem.topic}&rdquo;
                 </p>
              </div>

              <div className="flex justify-center gap-6">
                 <div className="px-8 py-4 bg-slate-50 rounded-2xl border border-slate-100 flex items-center gap-3">
                    <Star className="text-amber-400 fill-current" size={18} />
                    <span className="text-xs font-black text-slate-600 uppercase tracking-widest">Mastery Opportunity</span>
                 </div>
              </div>

              <button
                onClick={() => router.push(`/general-learning/learn/${currentItem.id}`)}
                className="w-full bg-primary text-white py-6 rounded-3xl font-black text-sm uppercase tracking-widest flex items-center justify-center gap-3 hover:bg-blue-700 shadow-xl shadow-blue-500/20 active:scale-95 transition-all"
              >
                 Initialize Module <ArrowRight size={20} />
              </button>

              <div className="absolute top-0 right-0 w-64 h-64 bg-primary/5 rounded-full blur-[80px] -mr-32 -mt-32 pointer-events-none" />
           </div>

        </div>
      </main>
    </div>
  );
}
