'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { chapterService } from '@/services/api';
import { getChapterDisplayData } from '@/utils/chapter';
import {
  BookOpen,
  ChevronRight,
  LayoutGrid,
  List,
  Sparkles,
  ArrowLeft,
  GraduationCap
} from 'lucide-react';
import Breadcrumbs from '@/components/Breadcrumbs';
import { motion } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import Link from 'next/link';

export default function SubjectExplorerClient() {
  const { profile, loading: authLoading } = useAuth();
  const params = useParams();
  const router = useRouter();
  const [chapters, setChapters] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const classId = params.classId as string;
  const subject = params.subject as string;

  useEffect(() => {
    if (authLoading) return;

    // Data Isolation Check
    if (profile?.className && classId !== profile.className) {
      console.warn("Unauthorized subject explorer access attempt");
      router.replace('/library');
      return;
    }

    const fetchChapters = async () => {
      try {
        const hierarchy = await chapterService.getHierarchy();
        const subjectChapters = hierarchy[classId]?.[subject] || [];
        setChapters(subjectChapters);
      } catch (error) {
        console.error("Failed to load subject chapters", error);
      } finally {
        setLoading(false);
      }
    };
    fetchChapters();
  }, [classId, subject, authLoading, profile, router]);

  if (authLoading || loading) return (
     <div className="flex min-h-screen bg-[#F8FAFC] items-center justify-center">
        <div className="animate-pulse flex flex-col items-center gap-4">
           <BookOpen size={40} className="text-primary" />
           <p className="text-sm font-bold text-slate-500 uppercase tracking-widest">Opening subject index...</p>
        </div>
     </div>
  );

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-20">
        <TopBar title={`${subject.toUpperCase()} Core`} />

        <div className="max-w-7xl mx-auto p-8 space-y-10">

           <div className="flex items-center justify-between px-2">
              <button
                onClick={() => router.back()}
                className="flex items-center gap-3 px-6 py-3 bg-white border border-slate-200 rounded-2xl text-xs font-bold uppercase tracking-widest text-slate-600 hover:text-primary hover:border-primary/30 transition-all shadow-sm group"
              >
                 <ArrowLeft size={16} className="group-hover:-translate-x-1 transition-transform" /> Back to Index
              </button>

              <div className="hidden md:block">
                 <Breadcrumbs items={[
                    { label: 'Library', href: '/library' },
                    { label: `Class ${classId.split('_').pop()}`, href: `/library` },
                    { label: subject.toUpperCase(), href: '#' },
                 ]} />
              </div>
           </div>

           {/* Hero Section */}
           <section className="bg-white border border-slate-200/60 rounded-[48px] p-12 md:p-16 shadow-xl shadow-slate-200/50 relative overflow-hidden">
               <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-10">
                  <div className="space-y-6">
                    <div className="inline-flex items-center gap-2 px-4 py-2 bg-blue-50 text-blue-700 rounded-full text-xs font-bold uppercase tracking-widest border border-blue-100">
                       <Sparkles size={16} /> Subject Exploration
                    </div>
                    <h2 className="text-6xl md:text-7xl font-black text-slate-900 capitalize leading-none tracking-tight">
                        {subject}
                    </h2>
                    <p className="text-slate-600 font-medium text-xl max-w-xl leading-relaxed">
                       Class {classId.split('_').pop()} curriculum modules. Discover lesson plans, interactive quizzes, and intelligent learning insights.
                    </p>
                  </div>

                  <div className="flex bg-slate-100/80 p-2 rounded-3xl border border-slate-200">
                     <button className="p-4 bg-white text-primary rounded-2xl shadow-md border border-slate-200"><LayoutGrid size={24} /></button>
                     <button className="p-4 text-slate-400 hover:text-slate-600"><List size={24} /></button>
                  </div>
               </div>
               <GraduationCap className="absolute -right-20 -top-20 w-96 h-96 text-slate-50 -rotate-45" />
           </section>

           {/* Chapters Grid */}
           <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
              {chapters.map((ch: any, idx: number) => (
                <motion.div
                  key={idx}
                  initial={{ opacity: 0, y: 30 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.05 }}
                >
                  <SubjectChapterTile
                     id={ch.id}
                     name={ch.name}
                     classId={classId}
                     subject={subject}
                  />
                </motion.div>
              ))}
           </div>
        </div>
      </main>
    </div>
  );
}

function SubjectChapterTile({ id, name, classId, subject }: any) {
  const displayData = getChapterDisplayData(id);
  const chapterName = name || displayData.name;

  return (
    <Link
      href={`/library/${classId}/${subject}/${id}`}
      className="group block bg-white border border-slate-200/60 rounded-[40px] p-10 hover:border-primary/40 hover:shadow-2xl hover:shadow-slate-200 transition-all h-full flex flex-col justify-between"
    >
      <div>
         <div className="w-16 h-16 bg-slate-50 rounded-3xl flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all mb-10 shadow-sm group-hover:rotate-6">
           <BookOpen size={32} />
         </div>
         <p className="text-slate-500 font-bold uppercase tracking-[0.2em] text-xs mb-3">Module {displayData.number || '00'}</p>
         <h4 className="text-2xl font-bold text-slate-900 leading-snug group-hover:text-primary transition-colors line-clamp-2 mb-8">
           {chapterName}
         </h4>
      </div>

      <div className="flex items-center justify-between pt-8 border-t border-slate-100">
        <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 flex items-center gap-2">
           <div className="w-2 h-2 rounded-full bg-emerald-500" /> Smart Learning
        </span>
        <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all">
           <ChevronRight size={20} />
        </div>
      </div>
    </Link>
  );
}
