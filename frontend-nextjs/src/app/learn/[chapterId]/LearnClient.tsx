'use client';

import React, { useState, useEffect, useCallback, Suspense } from 'react';
import { useParams, useSearchParams, useRouter } from 'next/navigation';
import { chapterService, progressService, masteryService } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import {
  X, ChevronLeft, ChevronRight, Volume2, VolumeX,
  Brain, BookOpen, Sparkles, Zap, Trophy,
  AlertTriangle, Lightbulb, Activity, Play,
  Layers, Users, Star, ArrowRight, BrainCircuit,
  MessageSquare, ClipboardCheck, History, BookMarked,
  Flag, Map, GraduationCap, Compass, Target
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import FormattedText from '@/components/FormattedText';
import { getChapterDisplayData } from '@/utils/chapter';
import { normalizeLesson } from '@/utils/lesson';
import MindMap from '@/components/mindmap/MindMap';

const BOILERPLATE_PHRASES = [
  "chapter-relevant word",
  "statement unrelated to the chapter",
  "statement that contradicts",
  "cannot be checked from the chapter",
  "source-supported points below",
  "extracted from the uploaded chapter PDF",
  "full PDF remains the source of truth"
];

function isBoilerplate(text: string): boolean {
  if (!text) return true;
  return BOILERPLATE_PHRASES.some(phrase => text.toLowerCase().includes(phrase.toLowerCase()));
}

function LearnContent() {
  const { profile, loading: authLoading } = useAuth();
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const chapterId = params.chapterId as string;
  const className = searchParams.get('class') || profile?.className;
  const subject = searchParams.get('subject') || 'mathematics';

  const [pkg, setPackage] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [currentStep, setCurrentStep] = useState(0);
  const [isReading, setIsReading] = useState(false);
  const [remediationContent, setRemediationContent] = useState<any[]>([]);
  const [isRemediating, setIsRemediating] = useState(false);
  const [selectedMedia, setSelectedMedia] = useState<{ title: string, url: string } | null>(null);

  useEffect(() => {
    if (authLoading || !profile || !className) return;

    if (profile?.className && className !== profile.className) {
      router.replace('/library');
      return;
    }

    const loadContent = async () => {
      try {
        const data = await chapterService.getPackage(className, subject, chapterId);
        setPackage(data);

        const mode = searchParams.get('mode');
        if (mode === 'remediation') {
           setIsRemediating(true);
           const mastery = await progressService.getMastery(chapterId);
           const weakIds = (mastery as any)?.weak_concepts || [];
           if (weakIds.length > 0) {
              const contents = await Promise.all(weakIds.map((id: string) =>
                 masteryService.getRemediation(className, subject, chapterId, id)
              ));
              setRemediationContent(contents);
           }
        }
      } catch (error) {
        console.error("Failed to load learning content", error);
      } finally {
        setLoading(false);
      }
    };
    loadContent();
  }, [chapterId, className, subject, authLoading, profile, router, searchParams]);

  const lesson = pkg ? normalizeLesson(pkg) : null;

  const steps = isRemediating ? ['Remediation'] : [
    (lesson?.introduction && !isBoilerplate(lesson.introduction)) ? 'Overview' : null,
    (lesson?.hasAnimation || lesson?.hasMindMap) ? 'Visual Lesson' : null,
    (lesson?.concepts?.filter(c => c.explanation && !isBoilerplate(c.explanation)).length) ? 'Concepts' : null,
    (lesson?.workedExamples?.length) ? 'Study Examples' : null,
    (lesson?.keyTerms?.length) ? 'Glossary' : null,
    (lesson?.teacherExplanation && !isBoilerplate(lesson.teacherExplanation)) ? 'Study Material' : null,
    (lesson?.story && !isBoilerplate(lesson.story)) ? 'Story Mode' : null,
    (lesson?.realWorldApplications?.length || lesson?.caseStudies?.length) ? 'Applications' : null,
    (lesson?.hindiSummary) ? 'Hindi Summary' : null,
    'Quick Quiz',
    (lesson?.flashcards?.length || lesson?.retrievalPractice?.length) ? 'Revision' : null,
    'AI Tutor',
    'Finish'
  ].filter(Boolean) as string[];

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(s => s + 1);
    }
  };
  const prevStep = () => currentStep > 0 && setCurrentStep(s => s - 1);

  const renderStepContent = (stepName: string) => {
    if (isRemediating) {
       return (
          <div className="space-y-12">
             <div className="flex items-center gap-6 p-8 bg-red-50 border border-red-100 rounded-[40px]">
                <AlertTriangle className="text-red-500 shrink-0" size={40} />
                <div>
                   <h2 className="text-2xl font-black text-red-900 uppercase italic tracking-tight">Adaptive Remediation Mode</h2>
                   <p className="text-red-700 font-medium">We&apos;ve identified specific concepts that need your attention. Let&apos;s fix them together.</p>
                </div>
             </div>
             <div className="space-y-8">
                {remediationContent.map((rem, i) => (
                   <div key={i} className="p-12 bg-white border border-border rounded-[50px] shadow-2xl space-y-10 relative overflow-hidden group">
                      <div className="flex items-center justify-between">
                         <div className="flex items-center gap-4">
                            <div className="w-12 h-12 bg-red-100 rounded-2xl flex items-center justify-center text-red-600">
                               <Sparkles size={24} />
                            </div>
                            <span className="px-4 py-1.5 bg-red-50 text-red-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-red-100">Targeted Review</span>
                         </div>
                         <span className="text-slate-300 font-black italic">Module {i+1}</span>
                      </div>
                      <div className="space-y-4">
                         <h3 className="text-4xl font-black text-slate-800 tracking-tighter">{rem.concept}</h3>
                         <div className="w-20 h-1.5 bg-red-500 rounded-full" />
                      </div>
                      <div className="grid grid-cols-1 gap-10">
                         <div className="space-y-4">
                            <h4 className="text-xs font-black uppercase tracking-widest text-slate-400">Core Explanation</h4>
                            <FormattedText content={rem.explanation} className="text-xl text-slate-700 leading-relaxed font-medium" />
                         </div>
                         {rem.example && (
                            <div className="p-8 bg-slate-50 rounded-[40px] border border-slate-100 space-y-4">
                               <h4 className="text-[10px] font-black uppercase tracking-widest text-blue-500">Illustrative Example</h4>
                               <FormattedText content={rem.example} className="text-lg text-slate-600 italic leading-relaxed" />
                            </div>
                         )}
                      </div>
                      <div className="pt-10 border-t border-slate-100 flex items-center justify-between">
                         <button
                            onClick={() => router.push(`/quiz/${chapterId}?class=${className}&subject=${subject}&difficulty=Easy`)}
                            className="bg-slate-900 text-white px-10 py-4 rounded-3xl font-black uppercase tracking-widest text-[10px] hover:bg-red-600 transition-all shadow-xl active:scale-95 flex items-center gap-3"
                         >
                            Retest this concept <ArrowRight size={16} />
                         </button>
                      </div>
                   </div>
                ))}
             </div>
          </div>
       );
    }

    switch(stepName) {
      case 'Overview':
        return (
          <div className="space-y-8 text-left">
             <h2 className="text-4xl font-black text-slate-800 leading-tight tracking-tight italic">Let&apos;s get started.</h2>
             <FormattedText content={lesson?.introduction || ''} className="text-xl font-bold text-slate-600 leading-relaxed" />
             {lesson?.learningGoals && lesson.learningGoals.length > 0 && (
                <div className="p-10 bg-blue-50 rounded-[48px] border border-blue-100/50 space-y-6 shadow-inner">
                   <div className="flex items-center gap-3">
                      <Target className="text-primary" size={24} />
                      <h4 className="font-black text-slate-900 uppercase text-sm tracking-widest">Mastery Objectives</h4>
                   </div>
                   <ul className="space-y-4">
                      {lesson.learningGoals.map((goal, i) => (
                         <li key={i} className="text-base font-bold text-slate-700 flex gap-4">
                            <span className="w-6 h-6 bg-white rounded-lg flex items-center justify-center text-primary text-[10px] shadow-sm border border-blue-100 shrink-0">{i+1}</span>
                            <FormattedText content={goal} />
                         </li>
                      ))}
                   </ul>
                </div>
             )}
          </div>
        );
      case 'Visual Lesson':
        return (
          <div className="space-y-12 text-center">
             <div className="space-y-4">
                <h2 className="text-4xl font-black text-slate-800 uppercase tracking-tight italic">Conceptual Visual</h2>
                <p className="text-slate-500 font-bold tracking-widest uppercase text-[10px]">Mapping the relationship between ideas.</p>
             </div>

             {lesson?.hasMindMap && (
                <div className="bg-slate-900 p-2 rounded-[60px] shadow-2xl overflow-hidden border-[12px] border-white">
                   <MindMap data={lesson.mindMap} />
                </div>
             )}

             {lesson?.hasAnimation && (
                <div
                   onClick={() => {
                      const multimedia = pkg?.components?.multimedia?.content;
                      const video = multimedia?.resources?.find((r: any) => r.type === 'video' || r.type === 'video_discovery') ||
                                    multimedia?.videos?.[0] ||
                                    multimedia?.discovery_links?.[0];

                      if (video?.url) {
                          setSelectedMedia({ title: video.title || 'Visual Narrative', url: video.url });
                      }
                   }}
                   className="aspect-video bg-slate-900 rounded-[48px] flex flex-col items-center justify-center border-8 border-white shadow-2xl relative group overflow-hidden cursor-pointer"
                >
                   <div className="absolute inset-0 bg-gradient-to-br from-blue-600/20 to-purple-600/20 group-hover:opacity-0 transition-opacity" />
                   <div className="w-24 h-24 bg-white rounded-full flex items-center justify-center text-primary shadow-2xl group-hover:scale-110 transition-transform relative z-10">
                      <Play size={40} fill="currentColor" className="ml-1" />
                   </div>
                   <p className="mt-8 font-black text-white text-sm uppercase tracking-[0.3em] relative z-10">Launch AI Visual Narrative</p>
                </div>
             )}
          </div>
        );
      case 'Concepts':
        return (
          <div className="space-y-10">
             <h2 className="text-3xl font-black text-slate-800 uppercase tracking-tight flex items-center gap-4 italic">
                <BrainCircuit className="text-purple-500" size={32} /> Core Pillars
             </h2>
             <div className="grid grid-cols-1 gap-6">
                {lesson?.concepts?.map((c, i)=>(
                   <div key={i} className="p-10 bg-white border border-border rounded-[48px] shadow-sm hover:shadow-xl transition-all flex flex-col gap-6">
                      <div className="flex items-center gap-5">
                         <span className="w-12 h-12 bg-purple-50 text-purple-600 rounded-2xl flex items-center justify-center font-black text-sm shrink-0 shadow-inner">{i+1}</span>
                         <h3 className="text-slate-900 font-black text-2xl tracking-tight">{c.name}</h3>
                      </div>
                      {c.explanation && <FormattedText content={c.explanation} className="text-lg text-slate-600 font-bold leading-relaxed pl-16 border-l-4 border-purple-50" />}
                      {c.example && (
                         <div className="ml-16 p-6 bg-slate-50 rounded-3xl border border-slate-100 flex gap-4">
                            <Sparkles className="text-amber-400 shrink-0" size={20} />
                            <div className="space-y-2">
                               <p className="text-[10px] font-black uppercase text-slate-400 tracking-widest">Illustrative Example</p>
                               <FormattedText content={c.example} className="text-base text-slate-500 font-bold italic" />
                            </div>
                         </div>
                      )}
                   </div>
                ))}
             </div>
          </div>
        );
      case 'Glossary':
        return (
          <div className="space-y-12">
             <div className="flex items-center gap-4">
                <div className="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center text-indigo-600 shadow-inner">
                   <Layers size={30} />
                </div>
                <div>
                   <h2 className="text-3xl font-black text-slate-900 uppercase tracking-tight leading-none italic">Vocabulary Bank</h2>
                   <p className="text-slate-400 font-black text-[10px] uppercase tracking-widest mt-1">Master the terminology</p>
                </div>
             </div>
             <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {lesson?.keyTerms?.map((term: any, i: number) => (
                   <div key={i} className="p-8 bg-white border border-slate-200 rounded-[40px] shadow-sm hover:border-indigo-200 transition-all group">
                      <h5 className="text-xl font-black text-indigo-600 mb-4 group-hover:scale-105 transition-transform origin-left">{term.term}</h5>
                      <p className="text-sm text-slate-500 font-bold leading-relaxed">{term.student_friendly_meaning || term.meaning}</p>
                   </div>
                ))}
             </div>
          </div>
        );
      case 'Study Material':
        return (
          <div className="space-y-10 text-left">
             <div className="flex items-center justify-between mb-4">
                <h2 className="text-4xl font-black text-slate-800 tracking-tight flex items-center gap-4 italic">
                   <BookOpen className="text-blue-500" size={32} /> Teacher Explanation
                </h2>
                <span className="px-6 py-2 bg-blue-50 text-blue-600 rounded-full text-[10px] font-black uppercase tracking-[0.2em] border border-blue-100 shadow-sm">Academic View</span>
             </div>
             <div className="p-12 bg-white border-8 border-slate-50 rounded-[64px] shadow-sm">
                <FormattedText content={lesson?.teacherExplanation || ''} className="text-xl text-slate-700 leading-[1.8] font-bold" />
             </div>
          </div>
        );
      case 'Story Mode':
        return (
          <div className="space-y-10 bg-amber-50/50 p-16 rounded-[64px] border border-amber-100 shadow-inner text-left relative overflow-hidden">
             <div className="flex items-center gap-4 relative z-10">
                <div className="w-12 h-12 bg-white rounded-2xl flex items-center justify-center text-amber-500 shadow-sm border border-amber-100"><Sparkles size={24} /></div>
                <h2 className="text-3xl font-black text-orange-900 tracking-tight italic">The Learning Narrative</h2>
             </div>
             <div className="relative z-10">
                <FormattedText content={lesson?.story || ''} className="text-2xl text-orange-950/80 font-black italic leading-loose" />
             </div>
             <div className="absolute top-0 right-0 w-64 h-64 bg-amber-200/20 rounded-full blur-[80px] -mr-32 -mt-32" />
          </div>
        );
      case 'Applications':
        return (
          <div className="space-y-12">
             <div className="flex items-center gap-5">
                <div className="w-16 h-16 bg-emerald-50 rounded-[24px] flex items-center justify-center text-emerald-600 shadow-inner"><Compass size={36} /></div>
                <h2 className="text-4xl font-black text-slate-900 uppercase tracking-tight italic">Real World Context</h2>
             </div>
             <div className="space-y-8">
                {lesson?.realWorldApplications?.map((app: any, i: number) => (
                   <div key={i} className="p-10 bg-white border border-emerald-100 rounded-[50px] shadow-sm flex gap-8 items-center group hover:bg-emerald-50/30 transition-all">
                      <div className="w-16 h-16 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-500 shrink-0 group-hover:scale-110 transition-transform">
                         {app.context === 'home' ? <Users size={28} /> : <Map size={28} />}
                      </div>
                      <div className="space-y-2">
                         <h4 className="text-[10px] font-black uppercase text-emerald-600 tracking-widest">Application: {app.context || 'General'}</h4>
                         <p className="text-2xl font-bold text-slate-800 leading-tight">{app.task || app.description}</p>
                      </div>
                   </div>
                ))}
                {lesson?.caseStudies?.map((cs: any, i: number) => (
                   <div key={`cs-${i}`} className="p-12 bg-slate-900 rounded-[64px] text-white shadow-2xl space-y-8">
                      <div className="flex items-center gap-4">
                         <GraduationCap className="text-primary" size={32} />
                         <h3 className="text-2xl font-black uppercase tracking-tight">{cs.title || 'Case Study'}</h3>
                      </div>
                      <p className="text-xl text-slate-300 font-bold leading-relaxed italic border-l-4 border-primary pl-8">{cs.case}</p>
                      <div className="pt-6 space-y-4">
                         <p className="text-[10px] font-black uppercase text-slate-500 tracking-widest">Think about it:</p>
                         <ul className="space-y-3">
                            {cs.questions?.map((q: string, qi: number) => (
                               <li key={qi} className="flex gap-4 text-lg font-bold text-slate-100">
                                  <span className="text-primary">?</span> {q}
                               </li>
                            ))}
                         </ul>
                      </div>
                   </div>
                ))}
             </div>
          </div>
        );
      case 'Hindi Summary':
        return (
          <div className="space-y-10 bg-slate-900 p-16 rounded-[64px] text-white shadow-2xl relative overflow-hidden">
             <div className="flex items-center gap-5 relative z-10">
                <div className="w-14 h-14 bg-white/10 rounded-2xl flex items-center justify-center border border-white/10 text-primary shrink-0">
                   <Users size={28} />
                </div>
                <h2 className="text-3xl font-black uppercase tracking-tight italic">Hindi Summary</h2>
             </div>
             <div className="relative z-10 p-10 bg-white/5 border border-white/5 rounded-[40px]">
                <p className="text-3xl font-bold leading-relaxed text-slate-100 italic">
                   {lesson?.hindiSummary}
                </p>
             </div>
             <div className="absolute -bottom-20 -left-20 w-80 h-80 bg-blue-500/10 rounded-full blur-[100px]" />
          </div>
        );
      case 'Study Examples':
        return (
          <div className="space-y-12">
             <div className="flex items-center gap-5">
                <div className="w-16 h-16 bg-emerald-50 rounded-[28px] flex items-center justify-center text-emerald-600 shadow-inner"><GraduationCap size={36} /></div>
                <h2 className="text-4xl font-black text-slate-900 uppercase tracking-tight italic">Worked Examples</h2>
             </div>
             <div className="grid grid-cols-1 gap-8">
                {lesson?.workedExamples?.map((ex: any, i: number) => (
                   <div key={i} className="p-12 bg-white border border-border rounded-[56px] shadow-sm space-y-10 group hover:shadow-xl transition-all">
                      <div className="space-y-4">
                         <span className="text-[10px] font-black uppercase tracking-widest text-emerald-600">Example {i+1}</span>
                         <h3 className="text-2xl font-black text-slate-800 leading-tight">{ex.task || ex.problem}</h3>
                      </div>
                      <div className="p-8 bg-slate-50 rounded-[40px] border border-slate-100 space-y-6">
                         <div className="flex items-center gap-3">
                            <Brain className="text-indigo-500" size={20} />
                            <p className="text-[11px] font-black uppercase tracking-widest text-slate-500">Methodology & Thinking</p>
                         </div>
                         <p className="text-lg font-bold text-slate-600 leading-relaxed italic">{ex.thinking || ex.solution_steps?.join(' ')}</p>
                      </div>
                      <div className="bg-emerald-600 p-8 rounded-[36px] text-white">
                         <p className="text-[10px] font-black uppercase tracking-widest opacity-60 mb-2">Final Answer</p>
                         <p className="text-xl font-black">{ex.answer || ex.result}</p>
                      </div>
                   </div>
                ))}
             </div>
          </div>
        );
      case 'Quick Quiz':
        return (
          <div className="space-y-12 text-center py-10">
             <div className="relative inline-block">
                <Zap className="text-green-500 w-24 h-24 animate-pulse" fill="currentColor" />
                <div className="absolute -top-4 -right-4 w-12 h-12 bg-primary rounded-full flex items-center justify-center text-white font-black text-xl border-4 border-white shadow-xl">!</div>
             </div>
             <div className="space-y-4">
                <h2 className="text-5xl font-black text-slate-800 tracking-tighter uppercase italic">Knowledge Check</h2>
                <p className="text-slate-400 font-black uppercase tracking-widest text-xs">Ready for the 5-Question AI Quiz?</p>
             </div>
             <button
               onClick={() => router.push(`/quiz/${chapterId}?class=${className}&subject=${subject}`)}
               className="bg-primary text-white px-16 py-6 rounded-[32px] font-black text-xl shadow-2xl shadow-blue-200 hover:scale-105 active:scale-95 transition-all uppercase tracking-widest"
             >
                Launch Quiz
             </button>
          </div>
        );
      case 'Revision':
        return (
          <div className="space-y-12">
             <div className="flex items-center justify-between">
                <h2 className="text-3xl font-black text-slate-800 tracking-tight flex items-center gap-4 italic">
                   <History className="text-pink-500" size={32} /> Fast Revision
                </h2>
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-[0.2em]">Active Recall Mode</span>
             </div>
             {lesson?.flashcards && lesson.flashcards.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                   {lesson.flashcards.slice(0, 4).map((f:any, i:number) => (
                      <div key={i} className="p-10 bg-white border border-border rounded-[48px] shadow-sm flex flex-col gap-8 hover:border-pink-200 transition-all hover:shadow-xl group">
                         <span className="text-[10px] font-black uppercase tracking-widest text-pink-400 opacity-60">Memory Card {i+1}</span>
                         <p className="text-2xl font-black text-slate-900 tracking-tight leading-snug">{f.front}</p>
                         <div className="p-6 bg-slate-50 rounded-3xl border border-slate-100 opacity-0 group-hover:opacity-100 transition-all">
                            <p className="text-sm font-bold text-slate-500 leading-relaxed italic">{f.back}</p>
                         </div>
                      </div>
                   ))}
                </div>
             )}
          </div>
        );
      case 'AI Tutor':
        return (
          <div className="space-y-12 text-center py-10">
             <div className="w-24 h-24 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-10 border-4 border-white shadow-2xl">
                <MessageSquare size={40} />
             </div>
             <div className="space-y-4">
                <h2 className="text-4xl font-black text-slate-800 leading-tight tracking-tight uppercase italic">Any lingering doubts?</h2>
                <p className="text-lg text-slate-500 font-medium max-w-lg mx-auto leading-relaxed">
                   Ask Gurukul AI for more examples, simpler explanations, or even a deep dive into any topic.
                </p>
             </div>
             <div className="flex flex-col gap-3 max-w-xs mx-auto">
                <button
                  onClick={() => router.push(`/tutor?chapter=${chapterId}&class=${className}&subject=${subject}`)}
                  className="py-6 bg-indigo-600 text-white rounded-3xl font-black uppercase tracking-widest text-xs shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all active:scale-95"
                >
                  Start Chat Session
                </button>
             </div>
          </div>
        );
      case 'Finish':
        return (
          <div className="space-y-12 text-center py-10">
             <div className="relative inline-block">
                <Trophy className="w-32 h-32 text-amber-400" />
                <div className="absolute top-0 left-0 w-full h-full animate-ping bg-amber-100 rounded-full opacity-20"></div>
             </div>
             <div className="space-y-4">
                <h2 className="text-6xl font-black text-slate-800 tracking-tighter uppercase italic">Mastered!</h2>
                <p className="text-xl text-slate-500 font-bold uppercase tracking-widest opacity-60">Lesson Journey Complete</p>
             </div>
             <div className="p-10 bg-slate-50 rounded-[56px] border border-slate-100 max-w-md mx-auto flex items-center justify-center gap-12 shadow-inner">
                <div className="text-center">
                   <p className="text-4xl font-black text-slate-800">+50</p>
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">XP Gained</p>
                </div>
                <div className="w-px h-16 bg-slate-200"></div>
                <div className="text-center">
                   <p className="text-4xl font-black text-slate-800">+10</p>
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Coins</p>
                </div>
             </div>
             <button
               onClick={() => router.back()}
               className="px-12 py-5 bg-slate-900 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-black transition-all shadow-xl active:scale-95"
             >
                Return to Library
             </button>
          </div>
        );
      default:
        return null;
    }
  };

  if (loading || authLoading) return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center font-black text-slate-400 uppercase tracking-widest text-[10px]">
       Setting up your classroom...
    </div>
  );

  const displayData = getChapterDisplayData(chapterId, pkg);

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col h-screen overflow-hidden">

      <header className="h-24 bg-white border-b border-slate-200 flex items-center justify-between px-10 shrink-0 shadow-sm relative z-50">
         <div className="flex items-center gap-8">
            <button onClick={() => router.back()} className="p-3 hover:bg-slate-50 rounded-2xl transition-colors border border-transparent hover:border-slate-100">
               <X size={24} className="text-slate-400" />
            </button>
            <div className="w-px h-10 bg-slate-200"></div>
            <div>
               <p className="text-[10px] font-black text-slate-400 uppercase tracking-[0.3em] mb-1.5 leading-none">
                  {subject.replace(/_/g, ' ')} • Class {className?.split('_').pop()}
               </p>
               <h1 className="text-lg font-black text-slate-900 uppercase tracking-tight flex items-center gap-3">
                  {displayData.name}
                  <span className="w-1.5 h-1.5 bg-primary/20 rounded-full"></span>
                  <span className="text-primary italic">{steps[currentStep]}</span>
               </h1>
            </div>
         </div>

         <div className="flex items-center gap-10">
            <div className="hidden lg:flex items-center gap-6">
               <span className="text-[11px] font-black text-slate-400 uppercase tracking-[0.2em]">
                  Phase {currentStep + 1} / {steps.length}
               </span>
               <div className="w-64 h-2.5 bg-slate-100 rounded-full overflow-hidden border border-slate-200 shadow-inner">
                  <motion.div
                    className="h-full bg-primary"
                    initial={false}
                    animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                    transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                  />
               </div>
            </div>
            <button
              onClick={() => setIsReading(!isReading)}
              className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all ${isReading ? 'bg-primary text-white shadow-xl shadow-blue-200' : 'bg-slate-50 text-slate-400 border border-slate-200 hover:border-primary/40 hover:bg-white'}`}
            >
               {isReading ? <Volume2 size={24} /> : <VolumeX size={24} />}
            </button>
         </div>
      </header>

      <main className="flex-1 overflow-y-auto relative bg-white custom-scrollbar">
         <div className="max-w-5xl mx-auto py-20 px-10">
            <AnimatePresence mode="wait">
               <motion.div
                  key={currentStep}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ duration: 0.4, ease: [0.22, 1, 0.36, 1] }}
                  className="space-y-16"
               >
                  {renderStepContent(steps[currentStep])}
               </motion.div>
            </AnimatePresence>
         </div>
      </main>

      <footer className="h-28 bg-white border-t border-slate-200 flex items-center justify-center px-10 shrink-0 shadow-[0_-15px_50px_rgba(0,0,0,0.03)] relative z-50">
         <div className="max-w-5xl w-full flex items-center justify-between gap-10">
            <button
               onClick={prevStep}
               disabled={currentStep === 0}
               className={`flex items-center gap-4 px-10 py-4.5 rounded-2xl font-black text-xs uppercase tracking-widest transition-all ${currentStep === 0 ? 'opacity-0 pointer-events-none' : 'bg-white border border-slate-200 text-slate-400 hover:bg-slate-50 hover:text-slate-600 hover:border-slate-300'}`}
            >
               <ChevronLeft size={18} /> Back
            </button>

            <button
               onClick={currentStep === steps.length - 1 ? () => router.back() : nextStep}
               className="flex items-center gap-4 px-14 py-5 bg-slate-900 text-white rounded-[24px] font-black text-xs uppercase tracking-[0.2em] hover:bg-black transition-all shadow-2xl shadow-slate-300 active:scale-95 group"
            >
               {currentStep === steps.length - 1 ? 'Finish Journey' : 'Next Phase'}
               <ChevronRight size={18} className="group-hover:translate-x-1 transition-transform" />
            </button>
         </div>
      </footer>

      <AnimatePresence>
        {selectedMedia && (
            <motion.div
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="fixed inset-0 z-[110] bg-slate-900/95 backdrop-blur-3xl flex items-center justify-center p-10"
                onClick={() => setSelectedMedia(null)}
            >
                <motion.div
                    initial={{ scale: 0.95, y: 30 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.95, y: 30 }}
                    className="bg-black w-full max-w-7xl aspect-video rounded-[56px] overflow-hidden shadow-[0_80px_160px_-40px_rgba(0,0,0,0.9)] border-[12px] border-white/10"
                    onClick={e => e.stopPropagation()}
                >
                    <iframe
                        src={selectedMedia.url.replace('watch?v=', 'embed/')}
                        className="w-full h-full"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                    />
                </motion.div>
                <button
                  onClick={() => setSelectedMedia(null)}
                  className="absolute top-12 right-12 w-20 h-20 bg-white/10 hover:bg-white/20 rounded-full flex items-center justify-center text-white backdrop-blur-2xl transition-all shadow-2xl border border-white/10"
                >
                    <X size={36} />
                </button>
            </motion.div>
        )}
      </AnimatePresence>

      <style jsx global>{`
         .custom-scrollbar::-webkit-scrollbar { width: 8px; }
         .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
         .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(15, 23, 42, 0.05); border-radius: 20px; }
         .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(15, 23, 42, 0.1); }
      `}</style>
    </div>
  );
}

export default function LearnPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-50 flex items-center justify-center font-black text-slate-400 uppercase tracking-widest text-[10px]">Loading Classroom...</div>}>
      <LearnContent />
    </Suspense>
  );
}
