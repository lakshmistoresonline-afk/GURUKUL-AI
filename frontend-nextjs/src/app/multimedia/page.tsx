'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import Breadcrumbs from '@/components/Breadcrumbs';
import { mediaService, chapterService } from '@/services/api';
import { getChapterDisplayData, normalizeClassName } from '@/utils/chapter';
import {
  Video,
  MonitorPlay,
  Play,
  Clock,
  Film,
  Sparkles,
  X,
  Globe,
  Youtube,
  ExternalLink,
  Layers,
  ChevronRight,
  FileText,
  Headphones,
  Zap
} from 'lucide-react';
import VideoPlayer from '@/components/VideoPlayer';
import { motion, AnimatePresence } from 'framer-motion';

import { useAuth } from '@/context/AuthContext';

export default function MultimediaPage() {
  const router = useRouter();
  const { profile, loading: authLoading } = useAuth();
  const [hierarchy, setHierarchy] = useState<any>(null);
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const studentClass = profile?.className;

  useEffect(() => {
    if (authLoading || !profile || !studentClass) return;

    const fetchData = async () => {
      setLoading(true);
      try {
        const data = await mediaService.getHubData();
        setHierarchy({ [studentClass]: data.hierarchy });
        setSummary(data.summary);
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [authLoading, profile, studentClass]);

  if (authLoading) return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
       <div className="animate-pulse flex flex-col items-center gap-4">
          <MonitorPlay size={40} className="text-primary" />
          <p className="text-sm font-bold text-slate-400 uppercase tracking-widest">Initialising Multimedia Hub...</p>
       </div>
    </div>
  );

  if (!profile) return (
     <div className="flex min-h-screen items-center justify-center bg-slate-50">
        <div className="text-center space-y-6">
           <Layers size={48} className="mx-auto text-slate-300" />
           <h2 className="text-2xl font-black text-slate-800">Authentication Required</h2>
           <button onClick={() => router.push('/login')} className="bg-primary text-white px-8 py-3 rounded-2xl font-bold">Sign In to Explore</button>
        </div>
     </div>
  );

  const classDisplay = studentClass?.replace('_', ' ').toUpperCase() || '...';
  const normClassName = studentClass ? normalizeClassName(studentClass) : '';
  const classHierarchy = (studentClass && (hierarchy?.[studentClass] || hierarchy?.[normClassName])) || {};

  return (
    <div className="flex min-h-screen bg-[#F8FAFC]">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title={`Multimedia Hub — ${classDisplay}`} />

        <div className="max-w-7xl mx-auto p-10 space-y-20">
           <Breadcrumbs items={[{ label: 'Multimedia Hub', href: '#' }]} />

           {/* Hero Section */}
           <section className="bg-slate-900 rounded-[60px] p-16 md:p-24 text-white relative overflow-hidden flex flex-col items-center text-center gap-10 shadow-2xl">
              <div className="relative z-10 space-y-6 max-w-3xl">
                 <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-500/20 text-blue-400 rounded-full border border-blue-500/20 text-xs font-black uppercase tracking-widest mx-auto">
                    <Sparkles size={16} /> Interactive Learning
                 </div>
                 <h2 className="text-6xl md:text-7xl font-black tracking-tight leading-none">
                    {classDisplay} Multimedia
                 </h2>
                 <p className="text-slate-400 font-medium text-xl leading-relaxed">
                    Explore visual lessons, videos and trusted learning resources
                    seamlessly integrated with your {classDisplay} curriculum.
                 </p>
                 <div className="flex flex-wrap justify-center gap-6 pt-8">
                    <button
                      onClick={() => router.push('/library')}
                      className="bg-primary text-white px-12 py-5 rounded-3xl font-black text-sm uppercase tracking-widest hover:bg-blue-600 shadow-2xl shadow-blue-500/30 flex items-center gap-3 active:scale-95 transition-all"
                    >
                       <Layers size={20} />
                       Open Library
                    </button>
                 </div>
              </div>

              <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
                 <Film className="absolute -left-20 -top-20 w-96 h-96 -rotate-12" />
                 <MonitorPlay className="absolute -right-20 -bottom-20 w-96 h-96 rotate-12" />
              </div>
           </section>

           {/* Curriculum Multimedia Index */}
           <div className="space-y-24">
              {Object.keys(classHierarchy).length > 0 ? (
                 Object.entries(classHierarchy).map(([subject, chapters]: [string, any]) => (
                   <section key={subject} className="space-y-12">
                      <div className="flex items-center gap-6 px-4">
                         <div className="w-1.5 h-10 bg-primary rounded-full shadow-lg shadow-blue-600/20" />
                         <h3 className="text-4xl font-black text-slate-900 capitalize tracking-tight">{subject}</h3>
                         <span className="text-xs font-black text-slate-500 bg-white border border-slate-200 px-4 py-2 rounded-full uppercase tracking-widest shadow-sm">
                            {chapters.length} Modules
                         </span>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                         {chapters.map((ch: any) => (
                           <ChapterMultimediaCard
                              key={ch.id}
                              chapter={ch}
                              subject={subject}
                              classId={studentClass!}
                              extCount={summary?.external?.[ch.id] || 0}
                              aiCount={summary?.ai_generated?.[ch.id] || 0}
                              ytStats={summary?.youtube?.[ch.id]}
                           />
                         ))}
                      </div>
                   </section>
                 ))
              ) : (
                 <div className="py-48 text-center bg-white border-2 border-dashed border-slate-200 rounded-[60px] shadow-sm">
                    <MonitorPlay size={80} className="mx-auto text-slate-200 mb-8" />
                    <p className="text-slate-500 font-bold uppercase tracking-widest text-sm">No multimedia chapters found for {classDisplay}</p>
                 </div>
              )}
           </div>

           {/* How It Works */}
           <section id="how-it-works" className="bg-white border border-slate-200/60 rounded-[48px] p-16 shadow-sm space-y-16">
              <div className="text-center space-y-4">
                 <h3 className="text-[10px] font-black text-primary uppercase tracking-[0.3em]">The Workflow</h3>
                 <h2 className="text-4xl font-black text-slate-900 tracking-tight">Connected Learning Journey</h2>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
                 <StepCard num="01" title="Select Your Class" desc="Ensure your profile is set to the correct class to see relevant resources." />
                 <StepCard num="02" title="Find Your Chapter" desc="Discover available visual lessons and external nodes in the hub." />
                 <StepCard num="03" title="Learn in Context" desc="Open the Chapter Dashboard for the full interactive experience." />
              </div>
           </section>
        </div>
      </main>
    </div>
  );
}

function ResourceTypeCard({ icon: Icon, title, desc, color }: any) {
   const colors: any = {
      blue: "text-blue-600 bg-blue-50 border-blue-100",
      red: "text-red-600 bg-red-50 border-red-100",
      emerald: "text-emerald-600 bg-emerald-50 border-emerald-100",
      orange: "text-orange-600 bg-orange-50 border-orange-100",
   };

   return (
      <div className="p-8 bg-white border border-slate-200/60 rounded-[40px] shadow-sm space-y-6 hover:shadow-xl transition-all group">
         <div className={`w-16 h-16 rounded-2xl flex items-center justify-center shadow-inner ${colors[color]}`}>
            <Icon size={32} />
         </div>
         <div className="space-y-2">
            <h4 className="text-xl font-black text-slate-900">{title}</h4>
            <p className="text-sm font-medium text-slate-500 leading-relaxed">{desc}</p>
         </div>
      </div>
   );
}

function StepCard({ num, title, desc }: any) {
   return (
      <div className="space-y-6">
         <div className="text-5xl font-black text-slate-100 italic leading-none">{num}</div>
         <div className="space-y-2">
            <h4 className="text-xl font-black text-slate-900">{title}</h4>
            <p className="text-sm font-medium text-slate-500 leading-relaxed">{desc}</p>
         </div>
      </div>
   );
}

function ChapterMultimediaCard({ chapter, subject, classId, extCount, aiCount, ytStats }: any) {
   const router = useRouter();
   const displayData = getChapterDisplayData(chapter.id);

   const directCount = ytStats?.direct || 0;
   const discoveryCount = ytStats?.discovery || 0;

   return (
      <motion.div
         whileHover={{ y: -8, scale: 1.01 }}
         onClick={() => router.push(`/library/${classId}/${subject}/${chapter.id}`)}
         className="bg-white border border-slate-200/60 rounded-[40px] p-10 shadow-sm hover:shadow-xl hover:border-primary/20 transition-all cursor-pointer flex flex-col h-full group"
      >
         <div className="flex items-start justify-between mb-12">
            <div className="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all duration-500 shadow-sm">
               <Video size={32} />
            </div>
            <div className="flex flex-col gap-2 items-end">
               {aiCount > 0 && (
                  <span className="px-3 py-1 bg-blue-50 text-blue-600 rounded-lg text-[8px] font-black uppercase tracking-widest border border-blue-100 flex items-center gap-1.5">
                     <Sparkles size={10} /> AI Visual Ready
                  </span>
               )}
               {extCount > 0 && (
                  <span className="px-3 py-1 bg-emerald-50 text-emerald-600 rounded-lg text-[8px] font-black uppercase tracking-widest border border-emerald-100 flex items-center gap-1.5">
                     <Globe size={10} /> {extCount} Verified Nodes
                  </span>
               )}
            </div>
         </div>

         <div className="space-y-3 flex-1">
            <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Module {displayData.number || '00'}</p>
            <h4 className="text-2xl font-black text-slate-900 leading-tight group-hover:text-primary transition-colors line-clamp-2">{chapter.name || displayData.name}</h4>
         </div>

         <div className="pt-8 mt-8 border-t border-slate-100 flex items-center justify-between">
            {directCount > 0 ? (
                <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest flex items-center gap-2">
                   <Youtube size={14} className="text-red-500" /> {directCount} Video Lessons
                </span>
            ) : discoveryCount > 0 ? (
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                   <Youtube size={14} className="text-slate-300" /> YouTube Search Available
                </span>
            ) : (
                <div />
            )}
            <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-sm">
               <ChevronRight size={20} />
            </div>
         </div>
      </motion.div>
   );
}
