'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import Link from 'next/link';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { chapterService, mediaService, resourceService, aiService, masteryService } from '@/services/api';
import { progressService, MasteryRecord } from '@/services/progress';
import { getChapterDisplayData } from '@/utils/chapter';
import { normalizeLesson } from '@/utils/lesson';
import {
  Play,
  BookOpen,
  Lightbulb,
  BrainCircuit,
  MessageSquare,
  ChevronLeft,
  ArrowRight,
  RefreshCw,
  Zap,
  ExternalLink,
  Sparkles,
  Globe,
  Youtube,
  FileText,
  X as XIcon,
  Languages,
  Layers,
  Target,
  CheckCircle,
  Activity,
  AlertTriangle,
  Brain,
  GraduationCap,
  BookMarked,
  Trophy,
  MonitorPlay
} from 'lucide-react';
import VideoPlayer from '@/components/VideoPlayer';
import Breadcrumbs from '@/components/Breadcrumbs';
import MindMap from '@/components/mindmap/MindMap';
import FormattedText from '@/components/FormattedText';
import ConceptGalaxy from '@/components/ConceptGalaxy';
import VoiceNarrator from '@/components/VoiceNarrator';
import ChapterVideoResources from '@/components/ChapterVideoResources';
import PracticeSessionModal from '@/components/PracticeSessionModal';
import AdaptiveRecommendation from '@/components/AdaptiveRecommendation';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import { featureFlags } from '@/config/featureFlags';

export default function ChapterDashboardClient() {
  const { profile, loading: authLoading } = useAuth();
  const params = useParams();
  const router = useRouter();
  const [pkg, setPackage] = useState<any>(null);
  const [chapterConfig, setChapterConfig] = useState<any>(null);
  const [resources, setResources] = useState<any[]>([]);
  const [externalResources, setExternalResources] = useState<any[]>([]);
  const [gurukulMedia, setGurukulMedia] = useState<any[]>([]);
  const [mastery, setMastery] = useState<MasteryRecord | null>(null);
  const [loading, setLoading] = useState(true);
  const [modalContent, setModalContent] = useState<{ title: string, body: any, subtitles?: string, isVideo?: boolean, isMindMap?: boolean } | null>(null);
  const [isPracticeModalOpen, setIsPracticeModalOpen] = useState(false);

  const [showGalaxy, setShowGalaxy] = useState(false);
  const [language, setLanguage] = useState<'en' | 'hi'>('en');
  const [translatedStory, setTranslatedStory] = useState<string | null>(null);
  const [isTranslating, setIsTranslating] = useState(false);

  const classId = params.classId as string;
  const subject = params.subject as string;
  const chapterId = params.chapterId as string;

  useEffect(() => {
    if (authLoading || !profile) return;

    if (profile.className && classId !== profile.className) {
      console.warn("Unauthorized chapter access attempt");
      router.replace('/library');
      return;
    }

    const controller = new AbortController();
    let isMounted = true;

    const fetchCritical = async () => {
       try {
          // Fetch package first as it's the most critical
          const pkgData = await chapterService.getPackage(classId, subject, chapterId, controller.signal);
          if (!isMounted) return;
          setPackage(pkgData);

          const story = pkgData?.content?.story_explanation || "";
          if (story && /[\u0900-\u097F]/.test(story)) {
            setLanguage('hi');
          }

          // Fetch other critical data in parallel but don't let them crash the whole thing
          const [configData, masteryData] = await Promise.allSettled([
             masteryService.getConfig(classId, subject, chapterId),
             progressService.getMastery(chapterId)
          ]);

          if (!isMounted) return;

          if (configData.status === 'fulfilled') {
             setChapterConfig(configData.value);
          } else {
             console.warn("Failed to load chapter config", configData.reason);
          }

          if (masteryData.status === 'fulfilled') {
             setMastery(masteryData.value);
          } else {
             console.warn("Failed to load mastery record", masteryData.reason);
          }

          setLoading(false);

          // Fetch Secondary Data
          fetchSecondary();
       } catch (err: any) {
          if (err.isCanceled) return;
          console.error("Critical chapter package fetch failed", err);
          setLoading(false);
       }
    };

    const fetchSecondary = async () => {
      try {
        const [mediaData, resourceData, extMediaData] = await Promise.all([
          mediaService.getChapterMedia(chapterId, controller.signal),
          resourceService.getChapterResources(chapterId, controller.signal),
          mediaService.getExternalResources({ chapter_id: chapterId }, controller.signal)
        ]);

        if (!isMounted) return;

        setGurukulMedia(mediaData || []);
        setResources(resourceData || []);
        setExternalResources(extMediaData || []);

      } catch (error: any) {
        if (error.isCanceled) return;
        console.error("Failed to load secondary chapter data", error);
      }
    };

    fetchCritical();

    return () => {
       isMounted = false;
       controller.abort();
    };
  }, [classId, subject, chapterId, authLoading, profile?.uid, profile, router]);

  const toggleLanguage = async () => {
    const newLang = language === 'en' ? 'hi' : 'en';
    setLanguage(newLang);

    if (newLang === 'hi' && !translatedStory) {
       setIsTranslating(true);
       try {
          const original = pkg?.content?.story_explanation || pkg?.content?.introduction || "";
          const res = await aiService.generate(`Translate and transform this educational content into an engaging 'Kahani Mode' (Story Mode) in Hindi for a Class 5 student:\n\n${original}`, 'simple');
          setTranslatedStory(res.response);
       } catch (e) {
          console.error("Translation failed", e);
       } finally {
          setIsTranslating(false);
       }
    }
  };

  if (loading || authLoading) return (
    <div className="flex min-h-screen bg-[#F8FAFC] items-center justify-center">
       <div className="flex flex-col items-center gap-6">
          <RefreshCw className="animate-spin text-blue-600" size={32} />
          <p className="font-bold text-slate-500 uppercase tracking-widest text-xs">Preparing Classroom...</p>
       </div>
    </div>
  );

  const lesson = normalizeLesson(pkg);
  const displayData = getChapterDisplayData(chapterId, pkg);

  const getPillarStatus = (label: string): 'locked' | 'available' | 'in_progress' | 'completed' => {
    if (!mastery) return label === 'Learn' ? 'available' : 'locked';

    const keyMap: Record<string, string> = {
      'Learn': 'understand',
      'Practice': 'apply',
      'Challenge': 'analyze',
      'Apply': 'transfer',
      'Explain': 'teach'
    };

    const key = (keyMap[label] || label.toLowerCase()) as keyof typeof mastery.evidence;
    if (mastery.evidence?.[key]) return 'completed';

    const hasAnyProgress = (mastery?.progress || 0) > 0;

    switch(label) {
      case 'Learn':
        return hasAnyProgress ? 'in_progress' : 'available';
      case 'Practice':
        return mastery?.evidence?.understand ? 'available' : 'locked';
      case 'Challenge':
        const hasAnalyze = chapterConfig?.concepts?.some((c: any) =>
          c.assessmentEvidence?.availableLevels?.includes('mastery') ||
          c.assessmentEvidence?.availableLevels?.includes('hots')
        );
        if (!hasAnalyze) return 'locked';
        return mastery?.evidence?.apply ? 'available' : 'locked';
      case 'Apply':
        const hasTransfer = chapterConfig?.concepts?.some((c: any) =>
          c.assessmentEvidence?.availableLevels?.includes('challenge')
        );
        if (!hasTransfer) return 'locked';
        return mastery?.evidence?.analyze ? 'available' : 'locked';
      case 'Explain':
        const needsTransfer = chapterConfig?.concepts?.some((c: any) => c.assessmentEvidence?.availableLevels?.includes('challenge'));
        const readyForTeach = needsTransfer ? mastery?.evidence?.transfer : (mastery?.evidence?.analyze || mastery?.evidence?.apply);
        return readyForTeach ? 'available' : 'locked';
      default:
        return 'locked';
    }
  };

  const getStudentFriendlyStatus = (status?: string) => {
    switch (status) {
      case 'NOT_STARTED': return 'Ready to Begin';
      case 'LEARNING': return 'Keep Going';
      case 'ASSESSMENT_READY': return 'Final Check';
      case 'MASTERED': return 'Mastered';
      case 'NEEDS_REMEDIATION': return 'Needs Review';
      default: return status?.replace('_', ' ') || 'Ready to Begin';
    }
  };

  const getNextMilestoneLabel = () => {
    if (!mastery || mastery.status === 'NOT_STARTED') return 'Start Learning';
    if (mastery.status === 'LEARNING') return 'Continue Learning';
    if (mastery.status === 'ASSESSMENT_READY') return 'Complete Final Check';
    if (mastery.status === 'MASTERED') return 'Review Concepts';
    return 'Next Milestone';
  };

  const activeStory = language === 'hi'
    ? (translatedStory || pkg?.content?.hindi_story || lesson.story)
    : (pkg?.content?.english_story || lesson.story);

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900 selection:bg-blue-100">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-20 scrollbar-hide">
        <TopBar title={displayData.name} />

        <div className="max-w-7xl mx-auto p-8 space-y-12">

          <div className="flex items-center justify-between px-2">
             <button
                onClick={() => router.back()}
                className="flex items-center gap-3 px-6 py-3 bg-white border border-slate-200/60 rounded-2xl text-xs font-bold uppercase tracking-wider text-slate-600 hover:text-blue-600 hover:border-blue-200 transition-all shadow-sm group"
             >
                <ChevronLeft size={18} className="group-hover:-translate-x-1 transition-transform" /> Back to Library
             </button>
             <div className="flex items-center gap-4">
                <button
                  onClick={() => setShowGalaxy(true)}
                  className="flex items-center gap-3 px-6 py-3 bg-indigo-50 border border-indigo-100 rounded-2xl text-xs font-bold uppercase tracking-wider text-indigo-600 hover:bg-indigo-100 transition-all shadow-sm"
                >
                   <Layers size={18} /> Knowledge Galaxy
                </button>
                <div className="hidden md:block">
                   <Breadcrumbs items={[
                      { label: 'Library', href: '/library' },
                      { label: subject.toUpperCase(), href: `/library/${classId}/${subject}` },
                      { label: displayData.name, href: '#' },
                   ]} />
                </div>
             </div>
          </div>

          {/* Hero Section: Classroom Style */}
          <section className="bg-white rounded-[48px] p-12 md:p-16 border border-slate-200/60 relative overflow-hidden shadow-sm">
             <div className="relative z-10 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
                <div className="space-y-8">
                   <div className="flex items-center gap-3 text-sm font-bold text-blue-600 bg-blue-50 px-4 py-2 rounded-full border border-blue-100 inline-flex">
                      <GraduationCap size={18} /> Class {classId} • {subject.toUpperCase()}
                   </div>
                   <div className="space-y-4">
                      <p className="text-slate-500 font-bold uppercase tracking-wider text-sm">Chapter {displayData.number || '...'}</p>
                      <h2 className="text-5xl md:text-6xl font-black tracking-tight text-slate-900 leading-tight">
                         {displayData.name}
                      </h2>
                   </div>
                   <p className="text-slate-600 text-xl font-medium leading-relaxed max-w-xl">
                      {lesson.introduction.slice(0, 220)}...
                   </p>
                   <div className="flex flex-wrap gap-4 pt-4">
                      {featureFlags.adaptiveMastery.diagnostic && (
                        <button
                          onClick={() => router.push(`/diagnostic/${chapterId}?class=${classId}&subject=${subject}`)}
                          className="bg-blue-600 text-white px-10 py-5 rounded-3xl font-bold text-lg hover:bg-blue-700 hover:shadow-lg hover:shadow-blue-200 transition-all active:scale-95 flex items-center gap-3"
                        >
                           <Brain size={24} /> Start Diagnostic
                        </button>
                      )}
                      <button
                        onClick={() => router.push(`/learn/${chapterId}?class=${classId}&subject=${subject}`)}
                        className="px-10 py-5 bg-white border border-slate-200 rounded-3xl font-bold text-lg text-slate-700 hover:bg-slate-50 transition-all flex items-center gap-3 shadow-sm"
                      >
                         <Play size={24} fill="currentColor" className="text-blue-600" /> {featureFlags.adaptiveMastery.diagnostic ? 'Skip to Learning' : 'Begin Learning'}
                      </button>
                   </div>
                </div>

                <div className="hidden lg:flex justify-center relative">
                   <motion.div
                     animate={{ y: [0, -15, 0] }}
                     transition={{ duration: 5, repeat: Infinity, ease: "easeInOut" }}
                     className="w-full max-w-md aspect-square bg-blue-50 rounded-[64px] flex items-center justify-center border border-blue-100 shadow-inner relative"
                   >
                      <BookMarked size={160} className="text-blue-200" />
                      <div className="absolute top-12 right-12 w-20 h-20 bg-white rounded-3xl shadow-lg flex items-center justify-center border border-slate-100">
                         <Zap size={32} className="text-amber-500 animate-pulse" />
                      </div>
                      <div className="absolute bottom-12 left-12 w-24 h-24 bg-white rounded-3xl shadow-lg flex items-center justify-center border border-slate-100">
                         <Trophy size={40} className="text-blue-600" />
                      </div>
                   </motion.div>
                </div>
             </div>
             <div className="absolute top-0 right-0 w-96 h-96 bg-blue-50/50 rounded-full blur-[100px] -mr-32 -mt-32" />
          </section>

          {/* Learning Journey Progression */}
          <section className="bg-white border border-slate-200/60 rounded-[48px] p-10 shadow-sm">
             <div className="flex items-center justify-between mb-12">
                <div className="flex items-center gap-4">
                   <div className="w-12 h-12 rounded-2xl bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100 shadow-sm">
                      <Target size={24} />
                   </div>
                   <div>
                      <h3 className="text-2xl font-extrabold text-slate-900">Master This Chapter</h3>
                      <p className="text-slate-500 text-sm font-medium">Your step-by-step path to excellence</p>
                   </div>
                </div>
                <div className={`px-6 py-2.5 rounded-full text-xs font-bold uppercase tracking-wider border shadow-sm ${
                   mastery?.status === 'MASTERED' ? 'bg-emerald-50 text-emerald-600 border-emerald-100' :
                   mastery?.status === 'NEEDS_REMEDIATION' ? 'bg-red-50 text-red-600 border-red-100' :
                   'bg-blue-50 text-blue-600 border-blue-100'
                }`}>
                   {getStudentFriendlyStatus(mastery?.status)}
                </div>
             </div>

             <div className="grid grid-cols-1 md:grid-cols-5 gap-6 mb-12">
                <EvidenceNode label="Learn" status={getPillarStatus('Learn')} />
                <EvidenceNode label="Practice" status={getPillarStatus('Practice')} />
                <EvidenceNode label="Challenge" status={getPillarStatus('Challenge')} />
                <EvidenceNode label="Apply" status={getPillarStatus('Apply')} />
                <EvidenceNode label="Explain" status={getPillarStatus('Explain')} />
             </div>

             <div className="pt-10 border-t border-slate-100 flex flex-col md:flex-row items-center justify-between gap-8">
                <div className="flex-1 w-full space-y-4">
                   <div className="flex justify-between text-sm font-black text-slate-700 uppercase tracking-widest">
                      <span>Course Progress</span>
                      <span className="text-blue-600">{Math.round((mastery as any)?.progress * 100 || 0)}% Completed</span>
                   </div>
                   <div className="h-4 bg-slate-100 rounded-full overflow-hidden p-1 border border-slate-100">
                      <motion.div
                         initial={{ width: 0 }}
                         animate={{ width: `${(mastery as any)?.progress * 100 || 0}%` }}
                         className="h-full bg-blue-600 rounded-full shadow-sm"
                      />
                   </div>
                </div>
                <button
                   onClick={() => router.push(`/quiz/${chapterId}?class=${classId}&subject=${subject}`)}
                   className="px-10 py-5 bg-slate-900 text-white rounded-3xl font-bold text-base hover:bg-blue-600 transition-all shadow-md active:scale-95 shrink-0"
                >
                   {getNextMilestoneLabel()}
                </button>
             </div>
          </section>

          {/* Remediation Alert */}
          {mastery?.status === 'NEEDS_REMEDIATION' && (
             <section className="bg-red-50 border border-red-100 rounded-[40px] p-8 flex flex-col md:flex-row items-center justify-between gap-8 shadow-sm">
                <div className="flex items-center gap-6">
                   <div className="w-16 h-16 bg-red-600 rounded-3xl flex items-center justify-center text-white shadow-lg">
                      <AlertTriangle size={32} />
                   </div>
                   <div>
                      <h4 className="text-2xl font-extrabold text-slate-900">Let&apos;s Strengthen Your Foundation</h4>
                      <p className="text-slate-600 text-lg font-medium mt-1">We&apos;ve identified a few concepts that need a quick review.</p>
                   </div>
                </div>
                <button
                  onClick={() => router.push(`/learn/${chapterId}?class=${classId}&subject=${subject}&mode=remediation`)}
                  className="px-10 py-5 bg-red-600 text-white rounded-2xl font-bold text-lg hover:bg-red-700 transition-all shadow-md active:scale-95"
                >
                   Start Focus Review
                </button>
             </section>
          )}

          {/* What You'll Learn: Clean Concept Grid */}
          <section className="bg-white border border-slate-200/60 rounded-[48px] p-12 shadow-sm">
             <div className="flex items-center gap-4 mb-10">
                <div className="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600 border border-indigo-100">
                   <BrainCircuit size={24} />
                </div>
                <div>
                   <h3 className="text-2xl font-extrabold text-slate-900">What You&apos;ll Learn</h3>
                   <p className="text-slate-500 text-sm font-medium">Core concepts covered in this module</p>
                </div>
             </div>

             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {chapterConfig?.concepts?.map((c: any, i: number) => (
                   <div key={i} className="p-6 bg-slate-50 border border-slate-100 rounded-3xl flex items-center justify-between group hover:border-indigo-300 hover:bg-white transition-all shadow-sm">
                      <span className="text-lg font-black text-slate-800 group-hover:text-slate-900 transition-colors line-clamp-1">{c.conceptName}</span>
                      {(mastery?.conceptPerformance?.[c.conceptId]?.foundation ?? 0) >= 0.7 ? (
                        <div className="w-8 h-8 bg-emerald-100 rounded-full flex items-center justify-center text-emerald-600">
                           <CheckCircle size={18} />
                        </div>
                      ) : (
                        <div className="w-8 h-8 rounded-full border-2 border-slate-200 flex items-center justify-center text-slate-300">
                           <Play size={14} fill="currentColor" />
                        </div>
                      )}
                   </div>
                ))}
                {(!chapterConfig?.concepts || chapterConfig.concepts.length === 0) && (
                   <p className="text-lg font-medium text-slate-400 italic">No concepts mapped yet.</p>
                )}
             </div>
          </section>

          {/* Story Mode: Premium Reading Experience */}
          {activeStory && (
            <section className="bg-white border border-slate-200/60 rounded-[48px] p-12 space-y-10 shadow-sm">
               <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
                  <div className="space-y-2">
                     <div className="flex items-center gap-4">
                        <div className="w-12 h-12 rounded-2xl bg-amber-50 flex items-center justify-center text-amber-600 border border-amber-100">
                           <Lightbulb size={24} />
                        </div>
                        <h3 className="text-3xl font-extrabold text-slate-900">Mastery Lab: Story Mode</h3>
                     </div>
                     <p className="text-slate-500 text-lg font-medium">Engaging narratives for better retention.</p>
                  </div>

                  <div className="flex items-center gap-4">
                     <button
                       onClick={toggleLanguage}
                       className="flex items-center gap-3 px-6 py-3 bg-slate-50 border border-slate-200 rounded-2xl text-sm font-bold text-slate-700 hover:bg-white hover:border-blue-300 transition-all shadow-sm"
                     >
                        <Languages size={18} className="text-blue-600" /> {language === 'en' ? 'English' : 'हिंदी'}
                     </button>
                     <VoiceNarrator text={activeStory} lang={language === 'en' ? 'en-IN' : 'hi-IN'} />
                  </div>
               </div>

               <div className="relative">
                  {isTranslating && (
                     <div className="absolute inset-0 z-10 bg-white/80 backdrop-blur-sm rounded-[40px] flex items-center justify-center">
                        <div className="flex flex-col items-center gap-4">
                          <RefreshCw className="animate-spin text-blue-600" size={48} />
                          <p className="text-sm font-bold uppercase tracking-wider text-blue-600">Preparing Story...</p>
                        </div>
                     </div>
                  )}
                  <div className="p-10 md:p-16 bg-slate-50 border border-slate-100 rounded-[40px] shadow-inner relative overflow-hidden">
                     <FormattedText content={activeStory} className="prose-slate max-w-none text-xl leading-relaxed text-slate-700" />
                  </div>
               </div>
            </section>
          )}

          {/* Navigation Modules */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-6">
             <ModernModuleCard icon={BookOpen} label="Academic" title="Study Guide" color="blue" onClick={() => setModalContent({ title: 'Teacher Explanation', body: lesson.teacherExplanation })} />
             <ModernModuleCard icon={Lightbulb} label="Engagement" title="Chapter Story" color="orange" onClick={() => setModalContent({ title: 'Story Mode', body: lesson.story })} />
             <ModernModuleCard icon={MonitorPlay} label="Visuals" title="Video Lessons" color="pink" onClick={() => {
                const el = document.getElementById('multimedia-section');
                el?.scrollIntoView({ behavior: 'smooth' });
             }} />
             <ModernModuleCard icon={BrainCircuit} label="Visual" title="Mind Map" color="purple" onClick={() => setModalContent({ title: 'Concept Map', body: lesson.mindMap, isMindMap: true })} />
             <ModernModuleCard icon={Zap} label="Training" title="Practice Hub" color="emerald" onClick={() => setIsPracticeModalOpen(true)} />
             <ModernModuleCard icon={MessageSquare} label="Intelligence" title="AI Tutor" color="indigo" onClick={() => router.push(`/tutor?chapter=${chapterId}&class=${classId}&subject=${subject}`)} />
          </div>

          <div className="grid grid-cols-1 xl:grid-cols-3 gap-12 pt-10">
             <div className="xl:col-span-2 space-y-12">

                {/* Multimedia Learning Section */}
                <div id="multimedia-section" className="bg-white border border-slate-200/60 rounded-[48px] p-10 shadow-sm space-y-8">
                   <div className="flex items-center justify-between px-4">
                      <div className="flex items-center gap-4">
                         <div className="w-1.5 h-8 bg-pink-500 rounded-full shadow-lg shadow-pink-500/20" />
                         <h3 className="text-2xl font-black text-slate-900 tracking-tight">Multimedia Learning</h3>
                      </div>
                      {gurukulMedia.length > 0 && (
                         <span className="px-4 py-1.5 bg-blue-50 text-blue-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-blue-100">Gurukul AI Generated</span>
                      )}
                   </div>

                   {/* AI Generated Lessons First */}
                   {gurukulMedia.length > 0 && (
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                         {gurukulMedia.map((v: any) => (
                            <div key={v.job_id} className="p-8 bg-blue-50/30 border border-blue-100 rounded-[40px] flex items-center justify-between group hover:bg-white transition-all shadow-sm">
                               <div className="flex items-center gap-6">
                                  <div className="w-16 h-16 bg-blue-600 rounded-3xl flex items-center justify-center text-white shadow-lg group-hover:scale-110 transition-transform">
                                     <MonitorPlay size={32} />
                                  </div>
                                  <div>
                                     <h4 className="text-xl font-black text-slate-900 leading-tight">AI Visual Lesson</h4>
                                     <p className="text-xs font-bold text-blue-600 uppercase mt-1 tracking-wider">Gurukul Intelligence</p>
                                  </div>
                               </div>
                               <button
                                 onClick={() => setModalContent({ title: 'AI Visual Lesson', body: v.output_path, subtitles: v.subtitles_path, isVideo: true })}
                                 className="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white hover:bg-blue-700 transition-all shadow-md"
                               >
                                  <Play size={20} fill="currentColor" />
                               </button>
                            </div>
                         ))}
                      </div>
                   )}

                   {/* Verified External Multimedia */}
                   {externalResources.length > 0 && (
                      <div className="space-y-6 pt-6">
                         <div className="flex items-center gap-3 px-4">
                            <Globe size={18} className="text-emerald-500" />
                            <h4 className="text-sm font-black text-slate-500 uppercase tracking-[0.2em]">Learn More: Verified External Nodes</h4>
                         </div>
                         <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                            {externalResources.map((res) => (
                               <a key={res.id} href={res.url} target="_blank" rel="noopener noreferrer" className="p-8 bg-slate-50 border border-slate-100 rounded-[40px] hover:bg-white hover:border-emerald-200 transition-all group flex items-center justify-between shadow-sm">
                                  <div className="flex items-center gap-6">
                                     <div className="w-14 h-14 bg-white rounded-2xl flex items-center justify-center text-slate-400 group-hover:text-emerald-600 transition-all shadow-inner border border-slate-100">
                                        <Globe size={28} />
                                     </div>
                                     <div>
                                        <p className="text-[10px] font-black text-emerald-600 uppercase tracking-widest">{res.provider}</p>
                                        <h5 className="text-lg font-bold text-slate-900 leading-tight line-clamp-1">{res.title}</h5>
                                     </div>
                                  </div>
                                  <div className="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-400 group-hover:text-emerald-600 transition-all">
                                     <ExternalLink size={18} />
                                  </div>
                               </a>
                            ))}
                         </div>
                      </div>
                   )}

                   {/* YouTube Discovery */}
                   <div className="pt-6">
                      <ChapterVideoResources
                        verifiedVideos={gurukulMedia.filter(m => m.type === 'video').map(m => m.metadata)}
                        discoveryLinks={gurukulMedia.filter(m => m.type === 'video_discovery').map(m => m.metadata)}
                      />
                   </div>
                </div>

                <div className="space-y-6">
                   <div className="flex items-center justify-between px-4">
                      <h3 className="text-xl font-extrabold text-slate-900">Verified Resources</h3>
                      <div className="flex items-center gap-2 px-4 py-1.5 bg-emerald-50 text-emerald-600 rounded-full text-xs font-bold uppercase tracking-wider border border-emerald-100">
                         <Zap size={14} /> {resources.length} active nodes
                      </div>
                   </div>

                   <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      {resources.map((res: any) => <ImmersiveResourceCard key={res.id} resource={res} />)}
                      {resources.length === 0 && (
                         <div className="md:col-span-2 py-32 text-center border-2 border-dashed border-slate-200 rounded-[48px] bg-white">
                            <Globe size={48} className="mx-auto text-slate-300 mb-6" />
                            <p className="text-slate-400 font-bold uppercase tracking-wider text-sm">Expanding Knowledge Base...</p>
                         </div>
                      )}
                   </div>
                </div>
             </div>

             <div className="space-y-8">
                {lesson.learningGoals.length > 0 && (
                  <div className="bg-white border border-slate-200/60 rounded-[48px] p-10 shadow-sm">
                     <h3 className="text-lg font-extrabold text-slate-900 mb-8">Learning Objectives</h3>
                     <div className="space-y-6">
                        {lesson.learningGoals.slice(0, 8).map((obj, i) => (
                           <div key={i} className="flex gap-5 group">
                              <div className="w-8 h-8 rounded-xl bg-blue-50 border border-blue-100 flex items-center justify-center text-blue-600 font-black text-xs shrink-0 mt-1 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-sm">{i+1}</div>
                              <p className="text-lg font-bold text-slate-800 group-hover:text-primary transition-colors leading-relaxed">{obj}</p>
                           </div>
                        ))}
                     </div>
                  </div>
                )}

                <Link
                  href={`/quiz/${chapterId}?class=${classId}&subject=${subject}`}
                  className="group bg-white border border-slate-200/60 rounded-[48px] p-10 flex items-center justify-between hover:border-emerald-300 hover:bg-emerald-50 transition-all shadow-sm"
                >
                   <div className="flex items-center gap-6">
                      <div className="w-16 h-16 bg-emerald-600 rounded-3xl flex items-center justify-center text-white shadow-md group-hover:scale-110 transition-transform">
                         <Zap size={32} />
                      </div>
                      <div>
                         <h4 className="font-extrabold text-slate-900 text-lg">Interactive Quiz</h4>
                         <p className="text-sm font-bold text-emerald-600 uppercase mt-1 tracking-wider">Validate Mastery</p>
                      </div>
                   </div>
                   <ArrowRight size={28} className="text-emerald-600 group-hover:translate-x-2 transition-transform" />
                </Link>

                <AdaptiveRecommendation profile={profile} currentChapter={{ id: chapterId, subject }} />
             </div>
          </div>
        </div>

        <AnimatePresence>
          {showGalaxy && lesson.mindMap && (
             <ConceptGalaxy
               data={lesson.mindMap}
               onClose={() => setShowGalaxy(false)}
             />
          )}

          {modalContent && (
             <motion.div
               initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
               className="fixed inset-0 z-50 flex items-center justify-center p-6 bg-slate-900/40 backdrop-blur-xl"
             >
                <motion.div
                  initial={{ scale: 0.95, y: 30 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.95, y: 30 }}
                  className="bg-white border border-slate-200 w-full max-w-5xl max-h-[90vh] overflow-hidden rounded-[48px] shadow-2xl flex flex-col"
                >
                   <div className="p-8 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                      <div className="flex items-center gap-6">
                         <div className="w-12 h-12 rounded-2xl bg-blue-600 flex items-center justify-center text-white shadow-md"><BookOpen size={24} /></div>
                         <h3 className="text-2xl font-black text-slate-900">{modalContent.title}</h3>
                      </div>
                      <button onClick={() => setModalContent(null)} className="p-4 bg-white hover:bg-slate-100 border border-slate-100 rounded-2xl transition-all text-slate-400 hover:text-slate-900 shadow-sm">
                         <XIcon size={24} />
                      </button>
                   </div>
                   <div className="flex-1 overflow-y-auto p-12 md:p-16 custom-scrollbar">
                      {modalContent.isVideo ? (
                         <VideoPlayer url={modalContent.body} subtitlesUrl={modalContent.subtitles} />
                      ) : modalContent.isMindMap ? (
                         <MindMap data={modalContent.body} />
                      ) : (
                         <FormattedText content={modalContent.body} className="prose-slate max-w-none text-xl leading-relaxed" />
                      )}
                   </div>
                </motion.div>
             </motion.div>
          )}
        </AnimatePresence>

        <PracticeSessionModal
          isOpen={isPracticeModalOpen}
          onClose={() => setIsPracticeModalOpen(false)}
          chapterId={chapterId}
          className={classId}
          subject={subject}
          concepts={lesson.concepts}
          onStart={(type, count, conceptId) => {
             const url = `/quiz/${chapterId}?class=${classId}&subject=${subject}&type=${type}&count=${count}${conceptId ? `&conceptId=${conceptId}` : ''}`;
             router.push(url);
             setIsPracticeModalOpen(false);
          }}
        />
      </main>

      <style jsx global>{`
         .custom-scrollbar::-webkit-scrollbar { width: 8px; }
         .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
         .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.05); border-radius: 20px; }
         .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.1); }
      `}</style>
    </div>
  );
}

function EvidenceNode({ label, status }: { label: string, status: 'locked' | 'available' | 'in_progress' | 'completed' }) {
  const config = {
    locked: { bg: 'bg-slate-50', border: 'border-slate-100', text: 'text-slate-500', icon: 'bg-slate-100', glyph: <div className="w-2 h-2 rounded-full bg-current" />, grayscale: true },
    available: { bg: 'bg-blue-50', border: 'border-blue-100', text: 'text-blue-700', icon: 'bg-blue-100', glyph: <div className="w-2.5 h-2.5 rounded-full bg-current animate-pulse" />, grayscale: false },
    in_progress: { bg: 'bg-amber-50', border: 'border-amber-100', text: 'text-amber-700', icon: 'bg-amber-100', glyph: <Activity size={20} className="animate-pulse" />, grayscale: false },
    completed: { bg: 'bg-emerald-50', border: 'border-emerald-100', text: 'text-emerald-700', icon: 'bg-emerald-500', glyph: <CheckCircle size={22} className="text-white" />, grayscale: false }
  }[status];

  return (
    <div className={`p-8 rounded-[32px] border flex flex-col items-center gap-5 transition-all shadow-sm ${config.bg} ${config.border} ${config.text} ${config.grayscale ? 'opacity-60' : 'scale-105 shadow-md ring-4 ring-white'}`}>
       <div className={`w-14 h-14 rounded-2xl flex items-center justify-center ${config.icon} shadow-inner`}>
          {config.glyph}
       </div>
       <span className="text-sm font-black uppercase tracking-[0.15em]">{label}</span>
    </div>
  );
}

function ModernModuleCard({ icon: Icon, label, title, onClick, color }: any) {
   const colors: any = {
      blue: "text-blue-700 bg-white border-slate-200/60 hover:border-blue-300 shadow-sm hover:shadow-md",
      orange: "text-orange-700 bg-white border-slate-200/60 hover:border-orange-300 shadow-sm hover:shadow-md",
      purple: "text-purple-700 bg-white border-slate-200/60 hover:border-purple-300 shadow-sm hover:shadow-md",
      indigo: "text-indigo-700 bg-white border-slate-200/60 hover:border-indigo-300 shadow-sm hover:shadow-md",
      emerald: "text-emerald-700 bg-white border-slate-200/60 hover:border-emerald-300 shadow-sm hover:shadow-md",
      pink: "text-pink-700 bg-white border-slate-200/60 hover:border-pink-300 shadow-sm hover:shadow-md",
   };
   return (
      <button
        onClick={onClick}
        className={`group border rounded-[40px] p-10 text-left transition-all ${colors[color] || colors.blue}`}
      >
         <div className={`w-16 h-16 rounded-2xl flex items-center justify-center mb-10 transition-all duration-500 group-hover:scale-110 bg-slate-50 shadow-inner`}>
            <Icon size={32} />
         </div>
         <p className={`text-[10px] font-black uppercase tracking-[0.2em] mb-3 text-slate-500`}>{label}</p>
         <h4 className="text-2xl font-black text-slate-900 leading-tight">{title}</h4>
      </button>
   );
}

function ImmersiveResourceCard({ resource }: any) {
  const Icon = resource.type === 'video' ? Youtube : FileText;
  return (
    <a href={resource.url} target="_blank" rel="noopener noreferrer" className="p-8 bg-white border border-slate-200/60 rounded-[40px] hover:border-blue-400 transition-all group flex items-center justify-between shadow-sm hover:shadow-md">
       <div className="flex items-center gap-6">
          <div className="w-16 h-16 bg-slate-50 rounded-2xl flex items-center justify-center text-slate-400 group-hover:bg-blue-600 group-hover:text-white transition-all shadow-inner border border-slate-100"><Icon size={32} /></div>
          <div>
             <h5 className="text-xl font-bold text-slate-900 leading-tight line-clamp-1">{resource.title}</h5>
             <div className="flex items-center gap-4 mt-3">
                <span className="text-xs font-black text-slate-500 uppercase tracking-widest">{resource.source}</span>
                <div className="w-1.5 h-1.5 rounded-full bg-slate-200" />
                <span className="text-xs font-black text-blue-700 uppercase tracking-widest bg-blue-50 px-2.5 py-0.5 rounded-lg border border-blue-100">{resource.type}</span>
             </div>
          </div>
       </div>
       <div className="w-12 h-12 rounded-full bg-slate-50 flex items-center justify-center text-slate-400 group-hover:bg-blue-50 group-hover:text-blue-600 transition-all">
          <ExternalLink size={20} />
       </div>
    </a>
  );
}
