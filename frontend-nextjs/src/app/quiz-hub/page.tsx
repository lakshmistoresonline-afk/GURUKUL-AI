'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { chapterService, quizService } from '@/services/api';
import { getChapterDisplayData, normalizeClassName } from '@/utils/chapter';
import {
  Zap,
  Search,
  Filter,
  ChevronRight,
  Trophy,
  History,
  Target,
  Sparkles
} from 'lucide-react';
import Link from 'next/link';

import { useAuth } from '@/context/AuthContext';

export default function QuizHubPage() {
  const { profile, loading: authLoading } = useAuth();
  const [hierarchy, setHierarchy] = useState<any>(null);
  const [bankStats, setBankStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [h, stats] = await Promise.all([
          chapterService.getHierarchy(),
          quizService.getBankStats()
        ]);
        setHierarchy(h);
        setBankStats(stats);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const activeClass = profile?.className || 'class_5';

  if (authLoading) return null;

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="Quiz Hub" />

        <div className="max-w-7xl mx-auto p-10 space-y-12">

           {/* Stats Header */}
           <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <QuizStatCard icon={Target} label="Questions Available" value={bankStats?.total_questions?.toLocaleString() || '...'} color="blue" />
              <QuizStatCard icon={History} label="Concepts Mapped" value={bankStats?.concepts_covered || '...'} color="purple" />
              <QuizStatCard icon={Trophy} label="Chapters Ready" value={bankStats?.chapters_covered || '...'} color="amber" />
           </section>

           {/* AI Challenge Section */}
           <section className="bg-gradient-to-br from-indigo-600 to-blue-700 rounded-[48px] p-12 text-white shadow-2xl relative overflow-hidden">
              <div className="relative z-10 max-w-xl space-y-6">
                 <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/10 backdrop-blur-md rounded-full border border-white/10 text-[10px] font-black uppercase tracking-widest text-blue-200">
                    <Sparkles size={12} /> Adaptive Engine
                 </div>
                 <h2 className="text-5xl font-black tracking-tight leading-none">AI Adaptive Practice</h2>
                 <p className="text-blue-100 font-medium text-lg">
                    Launch a custom session that targets your specific weak areas across all subjects.
                 </p>
                 <Link
                    href="/quiz/interleaved?class=6&subject=mathematics&type=quick"
                    className="inline-block bg-white text-indigo-700 px-10 py-5 rounded-2xl font-black text-sm uppercase tracking-widest hover:bg-blue-50 shadow-xl transition-all active:scale-95 text-center"
                 >
                    Start Adaptive Session
                 </Link>
              </div>
              <Zap className="absolute -right-10 -bottom-10 w-80 h-80 text-white/[0.05] -rotate-12" />
           </section>

           {/* Chapter Wise Quizzes */}
           <section className="space-y-8">
              <div className="flex items-center justify-between px-2">
                 <h3 className="text-sm font-black text-slate-400 uppercase tracking-[0.2em]">Chapter-wise Assessment</h3>
                 <div className="flex gap-3">
                    <div className="relative">
                       <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" size={16} />
                       <input type="text" placeholder="Search chapters..." className="pl-10 pr-4 py-2 bg-white border border-border rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-primary/20 shadow-sm w-64" />
                    </div>
                 </div>
              </div>

              {loading ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 animate-pulse">
                   {[1,2,3].map(i => <div key={i} className="h-32 bg-slate-100 rounded-3xl"></div>)}
                </div>
              ) : hierarchy && (
                <div className="space-y-12">
                   {Object.entries(hierarchy[activeClass] || hierarchy[normalizeClassName(activeClass)] || {}).map(([subject, chapters]: [string, any]) => (
                      <div key={subject} className="space-y-6">
                         <h4 className="text-lg font-black text-slate-800 capitalize flex items-center gap-3 px-2">
                            <div className="w-1.5 h-6 bg-primary rounded-full"></div> {subject}
                         </h4>
                         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                            {chapters.slice(0, 8).map((ch: any) => (
                               <QuizLink key={ch.id} id={ch.id} name={ch.name} subject={subject} classId={activeClass} />
                            ))}
                         </div>
                      </div>
                   ))}
                </div>
              )}
           </section>
        </div>
      </main>
    </div>
  );
}

function QuizStatCard({ icon: Icon, label, value, color }: any) {
  const colors: any = {
    blue: "text-blue-600 bg-blue-50 border-blue-100",
    amber: "text-amber-600 bg-amber-50 border-amber-100",
    purple: "text-purple-600 bg-purple-50 border-purple-100",
  };
  return (
    <div className={`p-8 bg-white border rounded-[32px] shadow-sm flex items-center gap-6 ${colors[color]}`}>
       <div className="w-14 h-14 rounded-2xl bg-white border border-inherit flex items-center justify-center">
          <Icon size={28} />
       </div>
       <div>
          <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest leading-none mb-2">{label}</p>
          <h4 className="text-3xl font-black text-slate-800">{value}</h4>
       </div>
    </div>
  );
}

function QuizLink({ id, name, subject, classId }: any) {
   const displayData = getChapterDisplayData(id);
   const chapterName = name || displayData.name;

   return (
      <Link
        href={`/quiz/${id}?class=${classId}&subject=${subject}`}
        className="p-5 bg-white border border-border rounded-2xl hover:border-primary/40 hover:shadow-lg transition-all group flex items-center justify-between"
      >
         <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-400 group-hover:bg-primary/10 group-hover:text-primary transition-colors">
               <Zap size={18} />
            </div>
            <div>
               <h5 className="text-sm font-bold text-slate-800 leading-tight capitalize">{chapterName}</h5>
               <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest mt-1">Chapter {displayData.number || '...'}</p>
            </div>
         </div>
         <ChevronRight size={14} className="text-slate-200 group-hover:text-primary transition-all" />
      </Link>
   );
}
