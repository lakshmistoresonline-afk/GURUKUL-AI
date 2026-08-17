'use client';

import React, { useEffect, useState, useMemo } from 'react';
import { useRouter } from 'next/navigation';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import {
  chapterService,
  quizService,
  srsService
} from '@/services/api';
import { progressService, MasteryRecord } from '@/services/progress';
import { getChapterDisplayData, normalizeClassName } from '@/utils/chapter';
import {
  Play,
  Zap,
  Library,
  Video,
  ChevronRight,
  Sparkles,
  Target,
  ArrowRight,
  Brain,
  Medal,
  Clock,
  BookOpen,
  RotateCcw,
  CheckCircle2,
  ListTodo,
  TrendingUp,
  History,
  Layout,
  Globe
} from 'lucide-react';
import { motion } from 'framer-motion';
import AdaptiveRecommendation from '@/components/AdaptiveRecommendation';
import { HeaderSkeleton, NextStepSkeleton, MissionSkeleton } from '@/components/DashboardSkeletons';
import api from '@/services/api';

export default function DashboardPage() {
  const { profile, loading: authLoading, mustOnboard } = useAuth();
  const router = useRouter();

  // State management for progressive loading
  const [criticalData, setCriticalData] = useState<{
    recentChapters: any[],
    hierarchy: any,
  } | null>(null);

  useEffect(() => {
    if (!authLoading && mustOnboard) {
      router.replace('/profile');
    }
  }, [authLoading, mustOnboard, router]);

  const [missionData, setMissionData] = useState<any>(null);
  const [statsData, setStatsData] = useState<{
    allMastery: MasteryRecord[],
    reviewsDue: number,
  } | null>(null);

  const [loadingStates, setLoadingStates] = useState({
    critical: true,
    mission: true,
    stats: true
  });

  const [greeting, setGreeting] = useState('');

  // Derived metrics
  const currentClassMastery = useMemo(() => {
    if (!statsData || !profile?.className) return 0;
    const normUserClass = normalizeClassName(profile.className);
    const currentClassRecords = statsData.allMastery.filter(r => normalizeClassName(r.className) === normUserClass);
    if (currentClassRecords.length === 0) return 0;
    const sum = currentClassRecords.reduce((acc, curr) => acc + (curr.progress || 0), 0);
    return Math.round((sum / currentClassRecords.length) * 100);
  }, [statsData, profile?.className]);

  const subjectMastery = useMemo(() => {
    if (!statsData || !profile?.className || !criticalData?.hierarchy) return [];
    const normUserClass = normalizeClassName(profile.className);
    const currentClassRecords = statsData.allMastery.filter(r => normalizeClassName(r.className) === normUserClass);

    // Get all subjects from curriculum hierarchy
    const curriculumSubjects = Object.keys(criticalData.hierarchy[profile.className] || criticalData.hierarchy[normUserClass] || {});

    const subjects: Record<string, { total: number, count: number }> = {};

    // Initialize with 0 for all curriculum subjects
    curriculumSubjects.forEach(s => {
      subjects[s] = { total: 0, count: 0 };
    });

    currentClassRecords.forEach(r => {
      if (subjects[r.subject] !== undefined) {
        subjects[r.subject].total += (r.progress || 0);
        subjects[r.subject].count += 1;
      }
    });

    return Object.entries(subjects).map(([name, data]) => ({
      name,
      value: data.count > 0 ? Math.round((data.total / data.count) * 100) : 0
    })).sort((a, b) => b.value - a.value || a.name.localeCompare(b.name));
  }, [statsData, profile?.className, criticalData?.hierarchy]);

  useEffect(() => {
    const hours = new Date().getHours();
    if (hours < 12) setGreeting('Good Morning');
    else if (hours < 17) setGreeting('Good Afternoon');
    else setGreeting('Good Evening');
  }, []);

  // Fetch Main Dashboard Data (Consolidated)
  useEffect(() => {
    if (authLoading || !profile) return;

    const fetchAllData = async () => {
      try {
        // Step 1: Critical UI Data
        const [h, activity, allMastery] = await Promise.all([
          chapterService.getHierarchy(),
          progressService.getRecentActivity(5),
          progressService.getStudentMastery()
        ]);

        const userClass = normalizeClassName(profile.className);
        const filteredActivity = activity.filter(a => normalizeClassName(a.className) === userClass);

        setCriticalData({
          hierarchy: h,
          recentChapters: filteredActivity
        });

        // Prefetch first chapter if exists
        if (filteredActivity.length > 0) {
           const first = filteredActivity[0];
           chapterService.getPackage(first.className, first.subject, first.chapterId).catch(err => {
              console.warn("Prefetch failed:", err);
           });
        }

        setLoadingStates(prev => ({ ...prev, critical: false }));

        // Step 2: Secondary Data using Mastery
        const [missionRes, dueItems] = await Promise.all([
          api.post('/api/adaptive/daily-mission', {
             student_mastery: allMastery.map(m => ({
               ...m,
               lastAccessed: m.lastAccessed?.seconds ? m.lastAccessed.seconds : m.lastAccessed
             }))
          }),
          srsService.getDueItems(profile.uid, undefined, 10)
        ]);

        setMissionData(missionRes.data);
        setStatsData({
          allMastery,
          reviewsDue: dueItems.length
        });

      } catch (e) {
        console.error("Dashboard data fetch failed", e);
      } finally {
        setLoadingStates({
          critical: false,
          mission: false,
          stats: false
        });
      }
    };
    fetchAllData();
  }, [authLoading, profile]);

  const continueChapter = criticalData?.recentChapters?.[0];

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900 selection:bg-primary/10">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title="Personal Classroom" />

        <div className="max-w-7xl mx-auto p-6 md:p-10 space-y-12">

          {/* Compact Header */}
          {authLoading || !profile ? <HeaderSkeleton /> : (
            <section className="px-4 space-y-1">
              <p className="text-primary font-black uppercase tracking-[0.2em] text-sm">
                {greeting}, {profile.name?.split(' ')[0]}!
              </p>
              <h2 className="text-5xl font-black tracking-tight text-slate-900">
                 {profile.className?.replace('_', ' ').toUpperCase()}
              </h2>
              <p className="text-slate-500 font-bold text-lg">Here&apos;s what you should focus on today.</p>
            </section>
          )}

          <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">

             {/* Left Column: Actions & Missions */}
             <div className="lg:col-span-8 space-y-12">

                {/* NEXT BEST ACTION: The Core Focus */}
                <section className="space-y-6">
                   <div className="flex items-center gap-3 px-4">
                      <Sparkles size={20} className="text-primary" />
                      <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.4em]">Next Best Action</h3>
                   </div>
                   {loadingStates.critical ? <NextStepSkeleton /> : (
                     <AdaptiveRecommendation profile={profile} currentChapter={continueChapter ? { id: continueChapter.chapterId, subject: continueChapter.subject } : null} />
                   )}
                </section>

                {/* Today's Mission Checklist */}
                <section className="bg-white border border-slate-200/60 rounded-[48px] p-10 shadow-sm space-y-10 relative overflow-hidden">
                   <div className="flex items-center justify-between relative z-10">
                      <div className="flex items-center gap-4">
                         <div className="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600 border border-indigo-100">
                            <ListTodo size={24} />
                         </div>
                         <h3 className="text-2xl font-black tracking-tight text-slate-900">Today&apos;s Mission</h3>
                      </div>
                      {!loadingStates.mission && missionData && (
                         <div className="px-6 py-2 bg-emerald-50 text-emerald-600 border border-emerald-100 rounded-full text-xs font-black uppercase tracking-widest">
                            {missionData.tasks.filter((t:any) => t.status === 'COMPLETED').length} / {missionData.tasks.length} Done
                         </div>
                      )}
                   </div>

                   {loadingStates.mission ? <MissionSkeleton /> : missionData && missionData.tasks.length > 0 ? (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 relative z-10">
                         {missionData.tasks.map((task: any, i: number) => (
                            <div key={i} className="p-6 rounded-[32px] bg-slate-50 border border-slate-100 flex items-center gap-5 group hover:border-primary/30 hover:bg-white transition-all">
                               <div className={`w-8 h-8 rounded-full border-2 flex items-center justify-center transition-colors ${
                                  task.status === 'COMPLETED' ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-slate-200 text-transparent'
                               }`}>
                                  <CheckCircle2 size={16} />
                               </div>
                               <div className="flex-1">
                                  <h4 className={`font-black text-slate-800 ${task.status === 'COMPLETED' ? 'line-through opacity-50' : ''}`}>{task.label}</h4>
                                  <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mt-0.5">{task.type}</p>
                               </div>
                            </div>
                         ))}
                      </div>
                   ) : (
                      <div className="py-12 text-center bg-slate-50/50 rounded-3xl border border-dashed border-slate-200">
                         <p className="text-slate-400 font-bold uppercase tracking-widest text-xs">Mission path clear. Ready for new exploration!</p>
                      </div>
                   )}
                </section>

                {/* Continue Learning / Suggested Chapters */}
                <section className="space-y-8">
                   <div className="flex items-center justify-between px-4">
                      <div className="flex items-center gap-3">
                         {criticalData?.recentChapters && criticalData.recentChapters.length > 0 ? (
                           <>
                             <History size={20} className="text-primary" />
                             <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.4em]">Continue Learning</h3>
                           </>
                         ) : (
                           <>
                             <BookOpen size={20} className="text-primary" />
                             <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.4em]">Get Started</h3>
                           </>
                         )}
                      </div>
                   </div>

                   {loadingStates.critical ? (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                         {[1,2].map(i => <div key={i} className="h-48 bg-white border border-slate-100 rounded-[40px] animate-pulse" />)}
                      </div>
                   ) : criticalData?.recentChapters && criticalData.recentChapters.length > 0 ? (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                         {criticalData.recentChapters.slice(0, 4).map((chapter, i) => (
                            <ContinueCard key={i} chapter={chapter} hierarchy={criticalData.hierarchy} />
                         ))}
                      </div>
                   ) : (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                         {/* Show first few chapters from hierarchy if no history */}
                         {(() => {
                            const activeClass = profile?.className || 'class_5';
                            const classData = criticalData?.hierarchy?.[activeClass] || {};
                            const suggested: any[] = [];

                            Object.entries(classData).forEach(([subject, chapters]: [string, any]) => {
                               if (suggested.length < 4 && chapters.length > 0) {
                                  suggested.push({
                                     chapterId: chapters[0].id,
                                     subject,
                                     className: activeClass,
                                     progress: 0
                                  });
                               }
                            });

                            return suggested.map((chapter, i) => (
                               <ContinueCard key={i} chapter={chapter} hierarchy={criticalData?.hierarchy} />
                            ));
                         })()}
                      </div>
                   )}
                </section>
             </div>

             {/* Right Column: Progress & Nav */}
             <div className="lg:col-span-4 space-y-12">

                {/* Real-time Progress Metrics */}
                <section className="bg-slate-900 rounded-[48px] p-10 text-white space-y-10 shadow-2xl relative overflow-hidden group">
                   <div className="relative z-10 space-y-1">
                      <p className="text-primary font-black uppercase tracking-[0.2em] text-[10px]">Command Center</p>
                      <h3 className="text-2xl font-black tracking-tight">Your Progress</h3>
                   </div>

                   <div className="space-y-8 relative z-10">
                      <ProgressMetric
                        label="Overall Mastery"
                        value={currentClassMastery}
                        unit="%"
                        loading={loadingStates.stats}
                        icon={TrendingUp}
                        color="blue"
                      />
                      <ProgressMetric
                        label="Today's Target"
                        value={missionData?.tasks?.filter((t:any) => t.status === 'COMPLETED').length || 0}
                        max={missionData?.tasks?.length || 0}
                        loading={loadingStates.mission}
                        icon={Target}
                        color="emerald"
                      />
                      <ProgressMetric
                        label="Reviews Due"
                        value={statsData?.reviewsDue || 0}
                        loading={loadingStates.stats}
                        icon={RotateCcw}
                        color="orange"
                        urgent={statsData?.reviewsDue ? statsData.reviewsDue > 0 : false}
                      />
                      <ProgressMetric
                        label="Knowledge XP"
                        value={profile?.xp || 0}
                        loading={authLoading}
                        icon={Medal}
                        color="blue"
                      />
                   </div>

                   <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-[80px] -mr-32 -mt-32 group-hover:bg-primary/20 transition-all duration-1000" />
                </section>

                {/* Explore Actions */}
                <section className="space-y-6">
                   <div className="flex items-center gap-3 px-4">
                      <Layout size={20} className="text-primary" />
                      <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.4em]">Explore learning</h3>
                   </div>
                   <div className="grid gap-4">
                      <ExplorerLink
                        icon={Library}
                        title="Library"
                        desc="NCERT Textbooks & Notes"
                        href="/library"
                        color="blue"
                      />
                      <ExplorerLink
                        icon={Video}
                        title="Multimedia"
                        desc="AI Animated Lessons"
                        href="/multimedia"
                        color="emerald"
                      />
                      <ExplorerLink
                        icon={Zap}
                        title="Practice"
                        desc="Quizzes & Retrieval"
                        href="/quiz-hub"
                        color="orange"
                      />
                      <ExplorerLink
                        icon={Globe}
                        title="General"
                        desc="Vocab, GK & Brain Boost"
                        href="/general-learning"
                        color="purple"
                      />
                   </div>
                </section>

                {/* Current Class Subject Mastery */}
                {subjectMastery.length > 0 && (
                   <section className="bg-white border border-slate-200/60 rounded-[40px] p-10 shadow-sm space-y-8">
                      <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.4em]">Subject Proficiency</h3>
                      <div className="space-y-6">
                         {subjectMastery.map((sub, i) => (
                            <MasteryRow key={i} label={sub.name} value={sub.value} />
                         ))}
                      </div>
                   </section>
                )}
             </div>

          </div>

          {/* Activity Timeline */}
          <section className="space-y-8">
             <div className="flex items-center justify-between px-4">
                <div className="flex items-center gap-3">
                   <Clock size={20} className="text-primary" />
                   <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.4em]">Recent footprints</h3>
                </div>
             </div>

             {loadingStates.critical ? <div className="h-40 bg-white border border-slate-100 rounded-[48px] animate-pulse" /> : (
                <div className="bg-white border border-slate-200/60 rounded-[48px] p-10 shadow-sm">
                   {criticalData?.recentChapters && criticalData.recentChapters.length > 0 ? (
                      <div className="space-y-8">
                         {criticalData.recentChapters.slice(0, 3).map((act, i) => (
                            <ActivityRow key={i} act={act} hierarchy={criticalData.hierarchy} />
                         ))}
                      </div>
                   ) : (
                      <p className="text-center text-slate-400 py-10 font-bold uppercase tracking-widest text-xs">No footprint in this class yet...</p>
                   )}
                </div>
             )}
          </section>

        </div>
      </main>
    </div>
  );
}

function ContinueCard({ chapter, hierarchy }: { chapter: any, hierarchy: any }) {
   const normClassName = normalizeClassName(chapter.className);
   const classEntry = hierarchy?.[chapter.className] || hierarchy?.[normClassName];
   const subjectEntry = classEntry?.[chapter.subject];
   const chapterEntry = subjectEntry?.find((c: any) => c.id === chapter.chapterId);
   const chapterName = chapterEntry?.name || getChapterDisplayData(chapter.chapterId).name;

   return (
      <Link
        href={`/library/${chapter.className}/${chapter.subject}/${chapter.chapterId}`}
        className="group bg-white border border-slate-200/60 rounded-[40px] p-8 hover:border-primary/40 hover:shadow-xl transition-all h-full flex flex-col justify-between"
      >
         <div className="space-y-6">
            <div className="flex items-center justify-between">
               <div className="w-12 h-12 rounded-2xl bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-inner border border-slate-100">
                  <BookOpen size={24} />
               </div>
               <span className="text-[10px] font-black text-emerald-600 uppercase tracking-widest bg-emerald-50 px-3 py-1 rounded-lg border border-emerald-100">
                  {Math.round((chapter.progress || 0) * 100)}% Mastered
               </span>
            </div>
            <div className="space-y-2">
               <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{chapter.subject}</p>
               <h4 className="text-2xl font-black text-slate-900 leading-tight line-clamp-2 group-hover:text-primary transition-colors">{chapterName}</h4>
            </div>
         </div>
         <div className="pt-8 flex items-center justify-between border-t border-slate-100 mt-8">
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Chapter {getChapterDisplayData(chapter.chapterId).number}</span>
            <div className="w-10 h-10 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all">
               <ChevronRight size={20} />
            </div>
         </div>
      </Link>
   );
}

function ProgressMetric({ label, value, max, unit, loading, icon: Icon, color, urgent }: any) {
   const colors: any = {
      blue: "text-blue-400",
      emerald: "text-emerald-400",
      orange: "text-orange-400",
   };

   return (
      <div className="flex items-center justify-between group">
         <div className="flex items-center gap-4">
            <div className={`w-10 h-10 rounded-xl bg-white/5 border border-white/10 flex items-center justify-center ${colors[color]} group-hover:bg-white group-hover:text-slate-900 transition-all duration-500`}>
               <Icon size={20} className={urgent ? "animate-pulse" : ""} />
            </div>
            <span className="text-sm font-bold text-white/70 group-hover:text-white transition-colors">{label}</span>
         </div>
         {loading ? <div className="h-6 w-12 bg-white/5 rounded animate-pulse" /> : (
            <div className="text-2xl font-black tracking-tight">
               {value}{max ? <span className="text-xs text-white/30 ml-1">/ {max}</span> : unit || ''}
            </div>
         )}
      </div>
   );
}

function ExplorerLink({ icon: Icon, title, desc, href, color }: any) {
   const colors: any = {
      blue: "text-blue-600 bg-blue-50 border-blue-100",
      emerald: "text-emerald-600 bg-emerald-50 border-emerald-100",
      orange: "text-orange-600 bg-orange-50 border-orange-100",
      purple: "text-purple-600 bg-purple-50 border-purple-100",
   };
   return (
      <Link href={href} className="flex items-center gap-5 p-5 bg-white border border-slate-200/60 rounded-[32px] hover:border-primary/30 hover:shadow-lg transition-all group">
         <div className={`w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 ${colors[color]} group-hover:scale-110 transition-transform`}>
            <Icon size={28} />
         </div>
         <div className="flex-1 min-w-0">
            <h4 className="font-black text-slate-900 text-lg leading-none">{title}</h4>
            <p className="text-xs text-slate-500 font-bold mt-1 truncate">{desc}</p>
         </div>
         <ChevronRight size={18} className="text-slate-300 group-hover:text-primary group-hover:translate-x-1 transition-all mr-2" />
      </Link>
   );
}

function MasteryRow({ label, value }: any) {
   return (
      <div className="space-y-3 group">
         <div className="flex justify-between items-center text-[10px] font-black uppercase tracking-widest">
            <span className="text-slate-600 group-hover:text-slate-900 transition-colors capitalize">{label}</span>
            <span className="text-primary">{value}%</span>
         </div>
         <div className="h-2 bg-slate-50 border border-slate-100 rounded-full overflow-hidden">
            <motion.div
               initial={{ width: 0 }}
               animate={{ width: `${value}%` }}
               className="h-full bg-primary rounded-full shadow-[0_0_8px_rgba(37,99,235,0.4)]"
            />
         </div>
      </div>
   );
}

function ActivityRow({ act, hierarchy }: { act: any, hierarchy: any }) {
   const normClassName = normalizeClassName(act.className);
   const classEntry = hierarchy?.[act.className] || hierarchy?.[normClassName];
   const subjectEntry = classEntry?.[act.subject];
   const chapterEntry = subjectEntry?.find((c: any) => c.id === act.chapterId);
   const chapterName = chapterEntry?.name || getChapterDisplayData(act.chapterId).name;

   return (
      <div className="flex gap-6 group">
         <div className="w-10 h-10 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-center text-slate-400 group-hover:bg-primary group-hover:text-white transition-all shadow-sm">
            <Clock size={18} />
         </div>
         <div className="flex-1 space-y-1">
            <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
               {new Date(act.lastAccessed?.seconds * 1000 || Date.now()).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
            </p>
            <h4 className="font-black text-slate-800 line-clamp-1">{chapterName}</h4>
            <div className="flex items-center gap-3 text-[10px] font-black text-slate-500 uppercase">
               <span className="text-primary">{act.subject}</span>
               <div className="w-1 h-1 rounded-full bg-slate-200" />
               <span>{Math.round((act.progress || 0) * 100)}% Mastery</span>
            </div>
         </div>
         <Link
            href={`/library/${act.className}/${act.subject}/${act.chapterId}`}
            className="self-center p-3 rounded-xl bg-slate-50 text-slate-400 hover:bg-primary hover:text-white transition-all shadow-sm"
         >
            <ArrowRight size={16} />
         </Link>
      </div>
   );
}
