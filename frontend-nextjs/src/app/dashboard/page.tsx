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
import { useLearning } from '@/context/LearningContext';
import ChapterContentRenderer from '@/components/ChapterContentRenderer';
import SelectionScreen from '@/components/SelectionScreen';

export default function DashboardPage() {
  const { profile, loading: authLoading, mustOnboard } = useAuth();
  const { isContextComplete, activeSubject, activeChapter, setSubject, setChapter } = useLearning();
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
    const currentClassRecords = statsData.allMastery.filter(r => r && normalizeClassName(r.className) === normUserClass);
    if (currentClassRecords.length === 0) return 0;
    const sum = currentClassRecords.reduce((acc, curr) => acc + (curr?.progress || 0), 0);
    return Math.round((sum / currentClassRecords.length) * 100);
  }, [statsData, profile]);

  const subjectMastery = useMemo(() => {
    if (!statsData || !profile?.className || !criticalData?.hierarchy) return [];

    const normUserClass = normalizeClassName(profile.className);
    const currentClassRecords = statsData.allMastery.filter(r => r && normalizeClassName(r.className) === normUserClass);

    // Get all subjects from curriculum hierarchy
    const classKey = Object.keys(criticalData.hierarchy).find(k => normalizeClassName(k) === normUserClass) || profile.className;
    const hierarchy = criticalData.hierarchy;
    const classHierarchy = hierarchy[classKey] || {};
    const curriculumSubjects = Object.keys(classHierarchy);

    const subjects: Record<string, { total: number, count: number }> = {};

    // Initialize with 0 for all curriculum subjects (normalized keys)
    curriculumSubjects.forEach(s => {
      subjects[s.toLowerCase().replace(/_/g, ' ')] = { total: 0, count: 0 };
    });

    currentClassRecords.forEach(r => {
      if (r) {
        const normSub = r.subject.toLowerCase().replace(/_/g, ' ');
        if (subjects[normSub] !== undefined) {
          subjects[normSub].total += (r.progress || 0);
          subjects[normSub].count += 1;
        }
      }
    });

    return Object.entries(subjects).map(([name, data]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value: data.count > 0 ? Math.round((data.total / data.count) * 100) : 0
    })).sort((a, b) => b.value - a.value || a.name.localeCompare(b.name));
  }, [statsData, profile, criticalData]);

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
          progressService.getRecentActivity(10),
          progressService.getStudentMastery()
        ]);

        const userClass = normalizeClassName(profile.className);
        const filteredActivity = activity.filter(a => a && normalizeClassName(a.className) === userClass);

        setCriticalData({
          hierarchy: h,
          recentChapters: filteredActivity
        });

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

  if (authLoading) {
    return (
       <div className="min-h-screen bg-slate-50 flex items-center justify-center font-black text-slate-400 uppercase tracking-widest text-[10px]">
          Initializing Workspace...
       </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900 selection:bg-primary/10">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-24">
        <TopBar title={isContextComplete ? activeChapter?.name || "Learning Mode" : "Student Hub"} />

        <div className="max-w-6xl mx-auto p-4 md:p-8 space-y-8">

            <section className="px-2 space-y-2">
              <p className="text-primary font-black uppercase tracking-[0.2em] text-[10px]">
                {greeting}, {profile?.name?.split(' ')[0] || 'Scholar'}!
              </p>
              <h2 className="text-4xl font-black tracking-tight text-slate-900">
                 {isContextComplete ? activeChapter?.name : `Class ${profile?.classId || '?'}`}
              </h2>
              <p className="text-slate-500 font-bold text-sm uppercase tracking-[0.15em]">
                {isContextComplete ? `${activeSubject?.replace('_', ' ')} • Authorized Learning Hub` : "Intelligent Curriculum Dashboard"}
              </p>
            </section>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">

             {/* MAIN CONTENT AREA */}
             <div className="lg:col-span-9 space-y-8">

                {isContextComplete ? (
                    /* CHAPTER FOCUS MODE */
                    <motion.div
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="space-y-8"
                    >
                        <ChapterContentRenderer
                            className={profile!.className}
                            subject={activeSubject!}
                            chapterId={activeChapter!.id}
                        />
                    </motion.div>
                ) : (
                    /* HOME DISCOVERY MODE */
                    <div className="space-y-10">
                        {/* SELECTION HUB - PRIMARY FOCUS */}
                        <section className="space-y-4">
                            <div className="flex items-center gap-3 px-2">
                                <Layout size={18} className="text-primary" />
                                <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em]">Start Learning</h3>
                            </div>
                            <SelectionScreen />
                        </section>

                        {/* NEXT BEST ACTION */}
                        <section className="space-y-4">
                           <div className="flex items-center gap-3 px-2">
                              <Sparkles size={18} className="text-primary" />
                              <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em]">Pick up where you left off</h3>
                           </div>
                           {loadingStates.critical ? <NextStepSkeleton /> : (
                             <AdaptiveRecommendation profile={profile} currentChapter={continueChapter ? { id: continueChapter.chapterId, subject: continueChapter.subject } : null} />
                           )}
                        </section>

                        {/* TODAY'S MISSION */}
                        <section className="bg-white border border-slate-200 rounded-[32px] p-8 shadow-sm space-y-6 relative overflow-hidden">
                           <div className="flex items-center justify-between relative z-10">
                              <div className="flex items-center gap-3">
                                 <div className="w-10 h-10 rounded-xl bg-indigo-50 flex items-center justify-center text-indigo-600 border border-indigo-100">
                                    <ListTodo size={20} />
                                 </div>
                                 <h3 className="text-xl font-black tracking-tight text-slate-900">Today&apos;s Mission</h3>
                              </div>
                              {!loadingStates.mission && missionData && (
                                 <div className="px-4 py-1.5 bg-emerald-50 text-emerald-600 border border-emerald-100 rounded-full text-[10px] font-black uppercase tracking-widest">
                                    {missionData.tasks.filter((t:any) => t.status === 'COMPLETED').length} / {missionData.tasks.length} Done
                                 </div>
                              )}
                           </div>

                           {loadingStates.mission ? <MissionSkeleton /> : missionData && missionData.tasks.length > 0 ? (
                              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 relative z-10">
                                 {missionData.tasks.map((task: any, i: number) => (
                                    <div key={i} className="p-4 rounded-2xl bg-slate-50 border border-slate-100 flex items-center gap-4 group hover:border-primary/30 hover:bg-white transition-all">
                                       <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center shrink-0 transition-colors ${
                                          task.status === 'COMPLETED' ? 'bg-emerald-500 border-emerald-500 text-white' : 'border-slate-200 text-transparent'
                                       }`}>
                                          <CheckCircle2 size={12} />
                                       </div>
                                       <div className="flex-1">
                                          <h4 className={`text-sm font-bold text-slate-800 ${task.status === 'COMPLETED' ? 'line-through opacity-50' : ''}`}>{task.label}</h4>
                                          <p className="text-[9px] font-bold text-slate-500 uppercase tracking-widest mt-0.5">{task.type}</p>
                                       </div>
                                    </div>
                                 ))}
                              </div>
                           ) : (
                              <div className="py-8 text-center bg-slate-50/50 rounded-2xl border border-dashed border-slate-200">
                                 <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px]">Mission path clear. Ready for new exploration!</p>
                              </div>
                           )}
                        </section>
                    </div>
                )}
             </div>

             {/* SIDEBAR / STATS AREA */}
             <div className="lg:col-span-3 space-y-8">

                {/* Progress Summary */}
                <section className="bg-slate-900 rounded-[32px] p-8 text-white space-y-8 shadow-xl relative overflow-hidden group">
                   <div className="relative z-10 space-y-1">
                      <p className="text-primary font-black uppercase tracking-[0.2em] text-[9px]">Command Center</p>
                      <h3 className="text-xl font-black tracking-tight">Your Progress</h3>
                   </div>

                   <div className="space-y-6 relative z-10">
                      <ProgressMetric
                        label="Overall Mastery"
                        value={currentClassMastery}
                        unit="%"
                        loading={loadingStates.stats}
                        icon={TrendingUp}
                        color="blue"
                      />
                      <ProgressMetric
                        label="Due Reviews"
                        value={statsData?.reviewsDue || 0}
                        loading={loadingStates.stats}
                        icon={RotateCcw}
                        color="orange"
                        urgent={statsData?.reviewsDue ? statsData.reviewsDue > 0 : false}
                      />
                      <ProgressMetric
                        label="Total XP"
                        value={profile?.xp || 0}
                        loading={authLoading}
                        icon={Medal}
                        color="blue"
                      />
                   </div>

                   <div className="absolute top-0 right-0 w-48 h-48 bg-primary/10 rounded-full blur-[60px] -mr-24 -mt-24" />
                </section>

                {/* Explorer Links */}
                <section className="space-y-4">
                   <div className="flex items-center gap-3 px-2">
                      <Layout size={18} className="text-primary" />
                      <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em]">Quick Access</h3>
                   </div>
                   <div className="grid gap-3">
                      <ExplorerLink icon={Library} title="Library" desc="Full Curriculum" href="/library" color="blue" />
                      <ExplorerLink icon={Zap} title="Practice" desc="Quizzes" href="/quiz-hub" color="orange" />
                   </div>
                </section>

                {/* Activity Timeline */}
                <section className="space-y-4">
                   <div className="flex items-center gap-3 px-2">
                      <Clock size={18} className="text-primary" />
                      <h3 className="text-[10px] font-black text-slate-500 uppercase tracking-[0.3em]">Recent Activity</h3>
                   </div>

                   {loadingStates.critical ? <div className="h-32 bg-white border border-slate-100 rounded-2xl animate-pulse" /> : (
                      <div className="bg-white border border-slate-200 rounded-[32px] p-6 shadow-sm">
                         {criticalData?.recentChapters && criticalData.recentChapters.length > 0 ? (
                            <div className="space-y-6">
                               {criticalData.recentChapters.slice(0, 3).map((act, i) => (
                                  <ActivityRow key={i} act={act} hierarchy={criticalData.hierarchy} />
                               ))}
                            </div>
                         ) : (
                            <p className="text-center text-slate-400 py-6 font-bold uppercase tracking-widest text-[9px]">No recent activity...</p>
                         )}
                      </div>
                   )}
                </section>
             </div>

          </div>

          {/* Activity Timeline (Footer Section) */}
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
                      <p className="text-center text-slate-400 py-10 font-bold uppercase tracking-widest text-xs">No recent activity detected...</p>
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
   if (!chapter) return null;
   const normClassName = normalizeClassName(chapter.className || '');
   const classEntry = hierarchy?.[chapter.className] || hierarchy?.[normClassName];
   const subjectEntry = classEntry?.[chapter.subject];
   const chapterEntry = subjectEntry?.find((c: any) => c.id === chapter.chapterId);
   const chapterName = chapterEntry?.name || (chapter.chapterId ? getChapterDisplayData(chapter.chapterId).name : 'Unknown Chapter');

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
            <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Chapter {chapter.chapterId ? getChapterDisplayData(chapter.chapterId).number : ''}</span>
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
   if (!act) return null;
   const normClassName = normalizeClassName(act.className);
   const classEntry = hierarchy?.[act.className] || hierarchy?.[normClassName];
   const subjectEntry = classEntry?.[act.subject];
   const chapterEntry = subjectEntry?.find((c: any) => c.id === act.chapterId);
   const chapterName = chapterEntry?.name || (act.chapterId ? getChapterDisplayData(act.chapterId).name : 'Unknown Chapter');

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
