'use client';

import React, { useEffect, useState } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { useAuth } from '@/context/AuthContext';
import { generalLearningService } from '@/services/api';
import {
  Book,
  Globe,
  Brain,
  ChevronRight,
  Sparkles,
  Trophy,
  Target,
  Zap,
  Clock,
  ArrowRight,
  CheckCircle2
} from 'lucide-react';
import Link from 'next/link';
import { motion } from 'framer-motion';

export default function GeneralLearningHub() {
  const { profile, loading: authLoading } = useAuth();
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authLoading || !profile) return;

    const fetchSummary = async () => {
      try {
        const data = await generalLearningService.getHome(profile.uid);
        setSummary(data);
      } catch (err) {
        console.error("Failed to load General Learning summary", err);
      } finally {
        setLoading(false);
      }
    };
    fetchSummary();
  }, [authLoading, profile]);

  if (authLoading || loading) return (
    <div className="flex min-h-screen bg-[#F8FAFC] items-center justify-center">
       <div className="animate-pulse flex flex-col items-center gap-4">
          <Globe size={40} className="text-primary" />
          <p className="text-sm font-bold text-slate-500 uppercase tracking-widest">Opening Knowledge Hub...</p>
       </div>
    </div>
  );

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900 selection:bg-primary/10">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title="General Learning Hub" />

        <div className="max-w-7xl mx-auto p-6 md:p-10 space-y-12">

           {/* Hero Section */}
           <section className="bg-slate-900 rounded-[48px] p-12 md:p-16 text-white relative overflow-hidden flex flex-col md:flex-row items-center gap-12 shadow-2xl">
              <div className="relative z-10 flex-1 space-y-8">
                 <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 text-blue-400 rounded-full border border-blue-500/20 text-xs font-black uppercase tracking-widest">
                    <Sparkles size={16} /> Knowledge Beyond Textbooks
                 </div>
                 <h2 className="text-5xl md:text-6xl font-black tracking-tight leading-tight">
                    Expand Your<br /><span className="text-primary">Horizons</span>
                 </h2>
                 <p className="text-slate-400 font-medium max-w-lg text-lg leading-relaxed">
                    Master essential vocabulary, explore general knowledge, and boost your brain power with curated daily activities.
                 </p>
                 <div className="flex gap-4 pt-4">
                    <Link
                      href="/general-learning/today"
                      className="bg-primary text-white px-10 py-4 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-blue-600 shadow-xl shadow-blue-500/20 flex items-center gap-3 transition-all active:scale-95"
                    >
                       <Zap size={20} fill="currentColor" />
                       Start Today&apos;s Set
                    </Link>
                 </div>
              </div>

              <div className="relative z-10 w-full md:w-[400px] aspect-square bg-white/5 rounded-[60px] border border-white/10 backdrop-blur-3xl flex items-center justify-center p-12">
                 <div className="grid grid-cols-2 gap-4 w-full h-full">
                    <div className="bg-blue-500/20 rounded-3xl flex items-center justify-center"><Book className="text-blue-400" size={48} /></div>
                    <div className="bg-emerald-500/20 rounded-3xl flex items-center justify-center"><Globe className="text-emerald-400" size={48} /></div>
                    <div className="bg-orange-500/20 rounded-3xl flex items-center justify-center"><Brain className="text-orange-400" size={48} /></div>
                    <div className="bg-purple-500/20 rounded-3xl flex items-center justify-center"><Trophy className="text-purple-400" size={48} /></div>
                 </div>
              </div>

              <Globe className="absolute -left-20 -bottom-20 w-[400px] h-[400px] text-white/[0.03] -rotate-12 pointer-events-none" />
           </section>

           {/* Progress Summary */}
           <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <StatCard
                 icon={Target}
                 label="Overall Mastery"
                 value={`${summary?.overall_progress || 0}%`}
                 color="blue"
                 desc="Completion of current class items"
              />
              <StatCard
                 icon={CheckCircle2}
                 label="Items Learned"
                 value={Object.values(summary?.categories || {}).reduce((acc: number, curr: any) => acc + (curr.learned || 0), 0).toString()}
                 color="emerald"
                 desc="Total items verified in your memory"
              />
              <StatCard
                 icon={Clock}
                 label="Daily Streak"
                 value="0 Days"
                 color="orange"
                 desc="Coming soon in V1.1"
              />
           </section>

           {/* Categories */}
           <div className="space-y-8">
              <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.4em] px-4">Learning Categories</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8">
                 <CategoryCard
                    id="english_vocabulary"
                    title="English Vocabulary"
                    desc="New words, meanings and usage."
                    icon={Book}
                    color="blue"
                    stats={summary?.categories?.english_vocabulary}
                 />
                 <CategoryCard
                    id="general_knowledge"
                    title="General Knowledge"
                    desc="Facts about the world and science."
                    icon={Globe}
                    color="emerald"
                    stats={summary?.categories?.general_knowledge}
                 />
                 <CategoryCard
                    id="science_facts"
                    title="Science Facts"
                    desc="Amazing scientific discoveries."
                    icon={Sparkles}
                    color="purple"
                    stats={summary?.categories?.science_facts}
                 />
                 <CategoryCard
                    id="maths_quick_practice"
                    title="Maths Quick Practice"
                    desc="Speed drills and mental maths."
                    icon={Target}
                    color="orange"
                    stats={summary?.categories?.maths_quick_practice}
                 />
                 <CategoryCard
                    id="india_and_world"
                    title="India & World"
                    desc="Geography, history and cultures."
                    icon={Globe}
                    color="blue"
                    stats={summary?.categories?.india_and_world}
                 />
                 <CategoryCard
                    id="life_skills"
                    title="Life Skills"
                    desc="Values and practical wisdom."
                    icon={Zap}
                    color="emerald"
                    stats={summary?.categories?.life_skills}
                 />
                 <CategoryCard
                    id="logic_and_reasoning"
                    title="Logic & Reasoning"
                    desc="Puzzles and brain teasers."
                    icon={Brain}
                    color="orange"
                    stats={summary?.categories?.logic_and_reasoning}
                 />
              </div>
           </div>

        </div>
      </main>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color, desc }: any) {
   const colors: any = {
      blue: "text-blue-600 bg-blue-50 border-blue-100",
      emerald: "text-emerald-600 bg-emerald-50 border-emerald-100",
      orange: "text-orange-600 bg-orange-50 border-orange-100",
   };
   return (
      <div className="bg-white border border-slate-200/60 p-8 rounded-[40px] shadow-sm space-y-4">
         <div className="flex items-center gap-4">
            <div className={`w-12 h-12 rounded-2xl flex items-center justify-center ${colors[color]}`}>
               <Icon size={24} />
            </div>
            <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{label}</p>
         </div>
         <div className="space-y-1">
            <h4 className="text-4xl font-black text-slate-900">{value}</h4>
            <p className="text-xs text-slate-400 font-medium">{desc}</p>
         </div>
      </div>
   );
}

function CategoryCard({ id, title, desc, icon: Icon, color, stats }: any) {
   const colors: any = {
      blue: "text-blue-600 bg-blue-50 border-blue-100 hover:border-blue-400",
      emerald: "text-emerald-600 bg-emerald-50 border-emerald-100 hover:border-emerald-400",
      orange: "text-orange-600 bg-orange-50 border-orange-100 hover:border-orange-400",
      purple: "text-purple-600 bg-purple-50 border-purple-100 hover:border-purple-400",
   };

   const progress = stats ? Math.round((stats.learned / stats.total) * 100) : 0;

   return (
      <Link href={`/general-learning/${id}`} className="group block bg-white border border-slate-200/60 rounded-[48px] p-10 hover:shadow-xl transition-all h-full relative overflow-hidden">
         <div className="relative z-10 space-y-10 flex flex-col h-full">
            <div className="flex items-start justify-between">
               <div className={`w-16 h-16 rounded-3xl flex items-center justify-center ${colors[color]} shadow-inner transition-all group-hover:scale-110`}>
                  <Icon size={32} />
               </div>
               <div className="text-right">
                  <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Progress</p>
                  <p className="text-xl font-black text-slate-900">{progress}%</p>
               </div>
            </div>

            <div className="space-y-3 flex-1">
               <h4 className="text-2xl font-black text-slate-900 group-hover:text-primary transition-colors">{title}</h4>
               <p className="text-sm font-medium text-slate-500 leading-relaxed">{desc}</p>
            </div>

            <div className="pt-8 border-t border-slate-100 flex items-center justify-between">
               <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  {stats?.learned || 0} / {stats?.total || 0} Mastered
               </span>
               <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-sm">
                  <ArrowRight size={20} />
               </div>
            </div>
         </div>
      </Link>
   );
}
