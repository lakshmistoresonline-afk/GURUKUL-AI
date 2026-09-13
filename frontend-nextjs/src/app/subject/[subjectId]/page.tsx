'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Layout } from '@/presentation/components/common/Layout';
import { studentApi, Subject, ChapterSummary } from '@/services/api/student_api';
import { ChevronLeft, ChevronRight, BookOpen, GraduationCap } from 'lucide-react';
import Link from 'next/link';

export default function SubjectChaptersPage() {
  const params = useParams();
  const subjectId = params?.subjectId as string;
  const [subject, setSubject] = useState<Subject | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!subjectId) return;

    // Reset readiness while a subject is loading.
    document.body.removeAttribute('data-gurukul-ready');

    studentApi.getSubject(subjectId)
      .then(res => {
        setSubject(res);
        setLoading(false);

        // Canonical production-readiness contract.
        // The page is ready only after a valid subject is loaded.
        document.body.setAttribute('data-gurukul-ready', 'true');
      })
      .catch(err => {
        console.error("Failed to load subject", err);
        setLoading(false);

        // Failed subject loads must never report the page as ready.
        document.body.removeAttribute('data-gurukul-ready');
      });

    return () => {
      document.body.removeAttribute('data-gurukul-ready');
    };
  }, [subjectId]);

  if (loading) return (
    <Layout>
      <div className="p-20 text-center font-black text-slate-300 uppercase animate-pulse">
        Assembling Course Curriculum...
      </div>
    </Layout>
  );

  if (!subject) return (
    <Layout>
      <div className="p-20 text-center font-black text-red-600">
        Subject Not Found
      </div>
    </Layout>
  );

  const subjectName = subject.name || 'Untitled Subject';
  const subjectTitle = subjectName.includes('_')
    ? subjectName.split('_').slice(1).join(' ').replace(/\b\w/g, l => l.toUpperCase())
    : subjectName;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-6 py-12 lg:py-20 space-y-16">
        <header className="space-y-6">
           <Link href="/" className="inline-flex items-center gap-2 text-slate-400 font-black text-[10px] uppercase tracking-widest hover:text-blue-600 transition-all mb-4 bg-slate-50 px-4 py-2 rounded-xl border border-slate-100">
              <ChevronLeft size={14} /> Back to Dashboard
           </Link>
           <h1 className="text-4xl sm:text-6xl font-black tracking-tighter text-slate-900 leading-none uppercase italic">
              {subjectTitle} <span className="text-blue-600">Curriculum</span>
           </h1>
        </header>

        <div className="grid grid-cols-1 gap-6">
           {subject.chapters && subject.chapters.map((chapter) => {
              const chapterTitle = chapter.title || 'Untitled Chapter';
              const displayTitle = chapterTitle.includes('_')
                ? chapterTitle.split('_').slice(1).join(' ').replace(/\b\w/g, l => l.toUpperCase())
                : chapterTitle;

              return (
                <Link key={chapter.id} href={`/chapter/${chapter.id}`} className="bg-white border-2 border-slate-100 rounded-[48px] p-8 sm:p-10 hover:border-blue-600 hover:shadow-2xl transition-all group flex flex-col sm:flex-row items-center justify-between relative overflow-hidden gap-6">
                   <div className="flex items-center gap-6 sm:gap-10 relative z-10 w-full sm:w-auto">
                      <div className="w-16 h-16 sm:w-20 sm:h-20 bg-slate-50 rounded-[28px] sm:rounded-[32px] flex items-center justify-center text-slate-400 group-hover:bg-blue-600 group-hover:text-white transition-all shrink-0">
                         <span className="text-2xl sm:text-3xl font-black">{chapter.chapter_id}</span>
                      </div>
                      <div className="space-y-1">
                         <p className="text-[10px] font-black text-blue-600 uppercase tracking-widest leading-none">Verified Unit</p>
                         <h3 className="text-2xl sm:text-4xl font-black text-slate-900 group-hover:text-blue-600 transition-colors tracking-tighter leading-tight uppercase italic">
                            {displayTitle}
                         </h3>
                         <div className="flex gap-2 flex-wrap pt-2">
                            {chapter.counts && Object.entries(chapter.counts).map(([layer, count]) => (
                               (count as number) > 0 && <span key={layer} className="px-2 py-1 bg-slate-100 rounded-md text-[8px] font-black uppercase text-slate-500 tracking-tighter">{layer}: {count}</span>
                            ))}
                         </div>
                      </div>
                   </div>
                   <div className="hidden sm:flex w-14 h-14 rounded-full bg-slate-50 items-center justify-center text-slate-200 group-hover:bg-blue-600 group-hover:text-white transition-all">
                      <ChevronRight size={32} />
                   </div>
                </Link>
              );
           })}
        </div>
      </div>
    </Layout>
  );
}
