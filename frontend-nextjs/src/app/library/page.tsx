'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { chapterService } from '@/services/api';
import { getChapterDisplayData, normalizeClassName } from '@/utils/chapter';
import {
  BookOpen,
  ChevronRight,
  Search,
  BookMarked,
  Sparkles,
  Layers,
  GraduationCap
} from 'lucide-react';
import Link from 'next/link';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';

export default function LibraryPage() {
  const { profile, loading: authLoading, mustOnboard } = useAuth();
  const router = useRouter();
  const [hierarchy, setHierarchy] = useState<any>(null);

  useEffect(() => {
    if (!authLoading && mustOnboard) {
      router.replace('/profile');
    }
  }, [authLoading, mustOnboard, router]);
  const [loading, setLoading] = useState(true);
  const [activeClass, setActiveClass] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    if (authLoading || !profile) return;

    setActiveClass(profile.className);

    const fetchHierarchy = async () => {
      try {
        const data = await chapterService.getHierarchy();
        console.log("Library Hierarchy Loaded:", data);
        setHierarchy(data);
      } catch (error) {
        console.error("Failed to load library hierarchy", error);
      } finally {
        setLoading(false);
      }
    };
    fetchHierarchy();
  }, [authLoading, profile]);

  const filteredSubjects = (subjects: any) => {
    if (!subjects) return [];
    if (!searchQuery) return Object.entries(subjects);

    const filtered: [string, any][] = [];
    Object.entries(subjects).forEach(([sub, chapters]: [string, any]) => {
      const matchingChapters = chapters.filter((ch: any) =>
        ch.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
        ch.id.toLowerCase().includes(searchQuery.toLowerCase())
      );
      if (sub.toLowerCase().includes(searchQuery.toLowerCase()) || matchingChapters.length > 0) {
        filtered.push([sub, matchingChapters]);
      }
    });
    return filtered;
  };

  if (authLoading) return null;

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title="National Curriculum Index" />

        <div className="max-w-7xl mx-auto px-8 py-12 space-y-16">

          {/* Header Section */}
          <section className="relative p-16 bg-white rounded-[48px] border border-slate-200/60 overflow-hidden shadow-sm">
             <div className="absolute inset-0 bg-gradient-to-br from-blue-50/50 to-transparent pointer-events-none" />
             <div className="relative z-10 flex flex-col lg:flex-row lg:items-center justify-between gap-10">
                <div className="space-y-6">
                   <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-50 text-blue-600 rounded-full text-xs font-bold uppercase tracking-wider border border-blue-100">
                      <Layers size={16} /> Knowledge Base
                   </div>
                   <h2 className="text-6xl font-black tracking-tight text-slate-900 leading-tight">Curriculum Hub</h2>
                   <p className="text-slate-600 font-medium max-w-xl text-xl leading-relaxed">
                     Explore official NCERT modules enhanced with intelligent AI insights for a personalized learning journey.
                   </p>
                </div>

                <div className="flex bg-slate-50 p-2 rounded-3xl border border-slate-200">
                    <div className="px-12 py-5 bg-slate-900 text-white rounded-[22px] font-black text-sm uppercase tracking-[0.2em] shadow-lg">
                      {activeClass?.replace('_', ' ').toUpperCase()}
                    </div>
                </div>
             </div>
             <GraduationCap className="absolute -right-12 -bottom-12 w-96 h-96 text-slate-100/50 -rotate-12 pointer-events-none" />
          </section>

          {/* Search Bar */}
          <div className="flex items-center justify-between px-4">
             <h3 className="text-sm font-black text-slate-500 uppercase tracking-[0.3em]">Available Subjects</h3>
             <div className="relative group">
                <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-500 transition-colors" size={20} />
                <input
                   type="text"
                   value={searchQuery}
                   onChange={(e) => setSearchQuery(e.target.value)}
                   placeholder="Search your library..."
                   className="pl-12 pr-6 py-4 bg-white border border-slate-200 rounded-2xl text-base font-medium focus:outline-none focus:ring-4 focus:ring-blue-500/10 focus:border-blue-500/50 w-96 transition-all text-slate-900 placeholder:text-slate-400 shadow-sm"
                />
             </div>
          </div>

          {/* Grid View */}
          <AnimatePresence mode="wait">
            {loading ? (
              <div key="loading" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
                 {[1,2,3,4,5,6].map(i => <div key={i} className="h-72 bg-white rounded-[40px] animate-pulse border border-slate-100 shadow-sm" />)}
              </div>
            ) : hierarchy && activeClass && (hierarchy[activeClass] || hierarchy[normalizeClassName(activeClass)]) ? (
              <motion.div
                key={activeClass}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="space-y-24"
              >
                 {filteredSubjects(hierarchy[activeClass] || hierarchy[normalizeClassName(activeClass)]).map(([subject, chapters]: [string, any]) => {
                   // Group chapters by part
                   const parts: Record<string, any[]> = {};
                   chapters.forEach((ch: any) => {
                      const partName = ch.part || 'Standard';
                      if (!parts[partName]) parts[partName] = [];
                      parts[partName].push(ch);
                   });

                   return (
                     <section key={subject} className="space-y-10">
                        <div className="flex items-center gap-6 px-4">
                           <div className="w-2 h-10 bg-blue-600 rounded-full shadow-lg shadow-blue-600/20" />
                           <h3 className="text-4xl font-black text-slate-900 capitalize tracking-tight">{subject}</h3>
                           <span className="text-xs font-black text-slate-500 bg-slate-100 px-4 py-1.5 rounded-full uppercase tracking-widest">{chapters.length} Modules</span>
                        </div>

                        {Object.entries(parts).map(([partName, partChapters]) => (
                          <div key={partName} className="space-y-6">
                            {partName !== 'Standard' && (
                              <div className="flex items-center gap-4 px-6">
                                <Layers size={16} className="text-slate-400" />
                                <h4 className="text-sm font-black text-slate-400 uppercase tracking-[0.2em]">{partName}</h4>
                                <div className="flex-1 h-px bg-slate-100" />
                              </div>
                            )}
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 2xl:grid-cols-4 gap-10">
                               {partChapters.map((ch: any) => (
                                 <ModernLibraryCard
                                    key={ch.id}
                                    id={ch.id}
                                    name={ch.name}
                                    subject={subject}
                                    className={activeClass}
                                    number={ch.number}
                                 />
                               ))}
                            </div>
                          </div>
                        ))}
                     </section>
                   );
                 })}
              </motion.div>
            ) : (
              <div key="empty" className="py-48 text-center bg-white border-2 border-dashed border-slate-200 rounded-[60px] shadow-sm">
                 <BookMarked size={80} className="mx-auto text-slate-200 mb-8" />
                 <p className="text-slate-500 font-bold uppercase tracking-widest text-sm">No chapters found for {activeClass}</p>
              </div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

function ModernLibraryCard({ id, name, subject, className, number }: any) {
  const displayData = getChapterDisplayData(id);
  const chapterName = name || displayData.name;
  const chapterNumber = number || displayData.number;

  return (
    <motion.div whileHover={{ y: -8, scale: 1.01 }} transition={{ type: "spring", stiffness: 300, damping: 25 }}>
       <Link
         href={`/library/${className}/${subject}/${id}`}
         className="group block bg-white border border-slate-200/60 rounded-[40px] p-10 h-full relative overflow-hidden shadow-sm hover:shadow-xl hover:border-blue-200 transition-all duration-300"
       >
         <div className="relative z-10 flex flex-col h-full">
            <div className="flex items-start justify-between mb-16">
               <div className="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center text-slate-400 group-hover:bg-blue-600 group-hover:text-white transition-all duration-500 shadow-sm">
                  <BookOpen size={32} />
               </div>
               <div className="px-4 py-1.5 bg-emerald-50 text-emerald-700 rounded-full text-[10px] font-bold uppercase tracking-wider border border-emerald-100">
                  Ready to Learn
               </div>
            </div>

            <div className="space-y-3 mt-auto">
               <p className="text-xs font-bold text-blue-600 uppercase tracking-[0.2em]">Chapter {chapterNumber || '00'}</p>
               <h4 className="font-black text-slate-900 text-2xl leading-tight line-clamp-2 group-hover:text-blue-600 transition-colors">
                  {chapterName}
               </h4>
            </div>

            <div className="mt-10 flex items-center justify-between pt-8 border-t border-slate-100">
               <div className="flex items-center gap-2">
                  <Sparkles size={16} className="text-blue-500" />
                  <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest">Enhanced Content</span>
               </div>
               <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-sm">
                  <ChevronRight size={20} />
               </div>
            </div>
         </div>
       </Link>
    </motion.div>
  );
}
