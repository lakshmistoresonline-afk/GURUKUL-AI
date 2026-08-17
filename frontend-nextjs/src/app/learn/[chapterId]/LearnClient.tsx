'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { chapterService, masteryService } from '@/services/api';
import { progressService } from '@/services/progress';
import { getChapterDisplayData } from '@/utils/chapter';
import { normalizeLesson, NormalizedLesson } from '@/utils/lesson';
import {
  ChevronLeft,
  Zap,
  Bot,
  ChevronRight,
  Volume2,
  VolumeX,
  X,
  Play,
  Lightbulb,
  BookOpen,
  BrainCircuit,
  MessageSquare,
  Trophy,
  Activity,
  History,
  Info,
  AlertTriangle,
  ArrowRight
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import FormattedText from '@/components/FormattedText';
import MindMap from '@/components/mindmap/MindMap';
import { useAuth } from '@/context/AuthContext';

export default function LearnClient() {
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

  useEffect(() => {
    if (authLoading || !profile || !className) return;

    // Data Isolation Check
    if (profile?.className && className !== profile.className) {
      console.warn("Unauthorized class access attempt");
      router.replace('/library');
      return;
    }

    const loadContent = async () => {
      try {
        const data = await chapterService.getPackage(className, subject, chapterId);
        setPackage(data);

        // Handle Remediation Mode
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
    'Overview',
    (lesson?.hasAnimation || lesson?.hasMindMap) ? 'Visual Lesson' : null,
    lesson?.concepts?.length ? 'Concepts' : null,
    'Study Material',
    lesson?.story ? 'Story Mode' : null,
    lesson?.activities?.length ? 'Activity' : null,
    'Quick Quiz',
    lesson?.flashcards?.length ? 'Revision' : null,
    'AI Tutor',
    'Finish'
  ].filter(Boolean) as string[];

  const nextStep = () => {
    if (currentStep < steps.length - 1) {
      setCurrentStep(s => s + 1);
    }
  };
  const prevStep = () => currentStep > 0 && setCurrentStep(s => s - 1);

  if (loading || authLoading) return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center font-black text-slate-400 uppercase tracking-widest text-[10px]">
       Setting up your classroom...
    </div>
  );

  const displayData = getChapterDisplayData(chapterId, pkg);

  const renderStepContent = (stepName: string) => {
    if (isRemediating && remediationContent.length > 0) {
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
                   <div key={i} className="p-10 bg-white border border-border rounded-[50px] shadow-xl space-y-6 relative overflow-hidden group">
                      <div className="flex items-center justify-between">
                         <span className="px-4 py-1.5 bg-red-50 text-red-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-red-100">Weak Concept Identified</span>
                         <span className="text-slate-300 font-black italic">Ref: 0{i+1}</span>
                      </div>
                      <h3 className="text-3xl font-black text-slate-800 tracking-tighter">{rem.concept}</h3>
                      <FormattedText content={rem.explanation} className="text-lg text-slate-600 leading-relaxed" />

                      {rem.hint && (
                         <div className="p-6 bg-blue-50/50 rounded-3xl border border-blue-100 flex gap-4">
                            <Lightbulb className="text-amber-400 shrink-0" size={24} />
                            <p className="text-sm font-medium text-slate-700 italic">{rem.hint}</p>
                         </div>
                      )}

                      <button
                         onClick={() => router.push(`/quiz/${chapterId}?class=${className}&subject=${subject}&difficulty=Easy`)}
                         className="flex items-center gap-3 text-primary font-black uppercase tracking-widest text-xs hover:gap-5 transition-all"
                      >
                         Practice Reassessment <ArrowRight size={16} />
                      </button>
                      <div className="absolute top-0 right-0 w-32 h-32 bg-red-500/5 rounded-full blur-3xl -mr-10 -mt-10" />
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
             <h2 className="text-4xl font-black text-slate-800 leading-tight">Ready to master this chapter?</h2>
             <FormattedText content={lesson?.introduction || ''} className="text-lg" />
             {lesson?.learningGoals && lesson.learningGoals.length > 0 && (
                <div className="p-8 bg-blue-50/50 rounded-[40px] border border-blue-100/50 flex gap-6">
                   <Lightbulb className="text-amber-400 shrink-0" size={32} />
                   <div className="flex-1 min-w-0">
                      <h4 className="font-black text-primary uppercase text-[10px] tracking-widest mb-3">Learning Goals</h4>
                      <ul className="space-y-2">
                         {lesson.learningGoals.map((goal, i) => (
                            <li key={i} className="text-sm italic text-slate-700 flex gap-2">
                               <span className="text-blue-400">•</span>
                               <FormattedText content={goal} />
                            </li>
                         ))}
                      </ul>
                   </div>
                </div>
             )}
          </div>
        );
      case 'Visual Lesson':
        return (
          <div className="space-y-12 text-center">
             <div className="space-y-4">
                <h2 className="text-3xl font-black text-slate-800 uppercase tracking-tight">Visual Discovery</h2>
                <p className="text-slate-500 font-medium">Seeing the connections between ideas.</p>
             </div>

             {lesson?.hasMindMap && (
                <div className="bg-slate-50 p-10 rounded-[60px] border-2 border-slate-100 shadow-inner">
                   <MindMap data={lesson.mindMap} />
                </div>
             )}

             {lesson?.hasAnimation && (
                <div className="aspect-video bg-slate-100 rounded-[40px] flex flex-col items-center justify-center border-2 border-dashed border-slate-200 relative group overflow-hidden">
                   <div className="w-20 h-20 bg-white rounded-full flex items-center justify-center text-primary shadow-xl group-hover:scale-110 transition-transform cursor-pointer">
                      <Play size={32} fill="currentColor" />
                   </div>
                   <p className="mt-6 font-black text-slate-400 text-xs uppercase tracking-[0.2em]">Play AI Animated Lesson</p>
                </div>
             )}

             {!lesson?.hasMindMap && !lesson?.hasAnimation && lesson?.animationFallback && (
                <div className="p-10 bg-blue-50/30 rounded-[40px] border border-blue-100 italic text-slate-600 leading-relaxed">
                   <FormattedText content={lesson.animationFallback} />
                </div>
             )}
          </div>
        );
      case 'Concepts':
        return (
          <div className="space-y-8">
             <h2 className="text-2xl font-black text-slate-800 uppercase tracking-tight flex items-center gap-3">
                <BrainCircuit className="text-purple-500" size={24} /> Key Concepts
             </h2>
             <div className="grid grid-cols-1 gap-4">
                {lesson?.concepts?.map((c, i)=>(
                   <div key={i} className="p-8 bg-white border border-border rounded-[40px] shadow-sm hover:border-purple-200 transition-colors flex flex-col gap-4">
                      <div className="flex items-center gap-4">
                         <span className="w-10 h-10 bg-purple-50 text-purple-600 rounded-2xl flex items-center justify-center font-black text-xs shrink-0">{i+1}</span>
                         <h3 className="text-slate-800 font-black text-xl">{c.name}</h3>
                      </div>
                      {c.explanation && <FormattedText content={c.explanation} className="text-slate-600 leading-relaxed pl-14" />}
                      {c.example && (
                         <div className="mt-2 ml-14 p-4 bg-slate-50 rounded-2xl border border-slate-100">
                            <p className="text-[10px] font-black uppercase text-slate-400 mb-2">Example from source</p>
                            <FormattedText content={c.example} className="text-sm text-slate-500 italic" />
                         </div>
                      )}
                   </div>
                ))}
             </div>
          </div>
        );
      case 'Study Material':
        return (
          <div className="space-y-8 text-left">
             <div className="flex items-center justify-between mb-8">
                <h2 className="text-3xl font-black text-slate-800 tracking-tight flex items-center gap-3">
                   <BookOpen className="text-blue-500" size={28} /> Teacher Explanation
                </h2>
                <span className="px-4 py-1 bg-slate-100 text-slate-400 rounded-full text-[10px] font-black uppercase tracking-widest">Academic View</span>
             </div>
             <FormattedText content={lesson?.teacherExplanation || ''} className="text-lg leading-loose" />
          </div>
        );
      case 'Story Mode':
        return (
          <div className="space-y-8 bg-amber-50/30 p-12 rounded-[60px] border border-amber-100/50 text-left">
             <h2 className="text-3xl font-black text-orange-800 tracking-tight flex items-center gap-3">
                <Lightbulb className="text-orange-500" size={28} /> The Narrative Story
             </h2>
             <FormattedText content={lesson?.story || ''} className="text-xl text-orange-950/70 font-bold italic" />
          </div>
        );
      case 'Activity':
        return (
          <div className="space-y-12">
             <div className="text-center">
                <div className="w-24 h-24 bg-emerald-50 text-emerald-500 rounded-[32px] flex items-center justify-center mx-auto mb-10 shadow-xl shadow-emerald-50">
                   <Activity size={40} />
                </div>
                <h2 className="text-4xl font-black text-slate-800 leading-tight">Interactive Lab</h2>
                <p className="text-lg text-slate-500 font-medium">Applying your knowledge through practical tasks.</p>
             </div>

             <div className="space-y-6">
                {lesson?.activities.map((act, i) => (
                   <div key={i} className="p-10 bg-white border-2 border-emerald-100 rounded-[50px] text-left">
                      <h4 className="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-600 mb-6">{act.title}</h4>
                      <FormattedText content={act.description} className="text-2xl font-bold text-slate-800 leading-tight" />
                      {act.concept && <p className="mt-6 text-xs font-black text-slate-400 uppercase tracking-widest">Focus: {act.concept}</p>}
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
                <h2 className="text-5xl font-black text-slate-800 tracking-tighter uppercase">Knowledge Check</h2>
                <p className="text-slate-400 font-black uppercase tracking-widest text-xs">Ready for the 5-Question AI Quiz?</p>
             </div>
             <button
               onClick={() => router.push(`/quiz/${chapterId}?class=${className}&subject=${subject}`)}
               className="bg-primary text-white px-12 py-5 rounded-[32px] font-black text-lg shadow-2xl shadow-blue-100 hover:scale-105 active:scale-95 transition-all"
             >
                Launch Interactive Quiz
             </button>
          </div>
        );
      case 'Revision':
        return (
          <div className="space-y-12">
             <div className="flex items-center justify-between">
                <h2 className="text-3xl font-black text-slate-800 tracking-tight flex items-center gap-3">
                   <History className="text-pink-500" size={28} /> Fast Revision
                </h2>
                <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Retrieval Practice</span>
             </div>

             {lesson?.flashcards && lesson.flashcards.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                   {lesson.flashcards.slice(0, 4).map((f:any, i:number) => (
                      <div key={i} className="p-8 bg-white border border-border rounded-[40px] shadow-sm flex flex-col gap-6 hover:border-pink-200 transition-colors">
                         <span className="text-[9px] font-black uppercase tracking-widest text-pink-400">Memory Card {i+1}</span>
                         <p className="text-xl font-black text-slate-800">{f.front}</p>
                         <p className="text-sm text-slate-400 font-medium line-clamp-2">{f.back}</p>
                      </div>
                   ))}
                </div>
             )}

             {lesson?.retrievalPractice && lesson.retrievalPractice.length > 0 && (
                <div className="bg-slate-50 p-10 rounded-[50px] border border-slate-100 space-y-8">
                   <h4 className="text-xs font-black uppercase tracking-widest text-slate-500 text-center">Brain Challenge: Can you answer these?</h4>
                   <div className="space-y-4">
                      {lesson.retrievalPractice.slice(0, 3).map((prompt, i) => (
                         <div key={i} className="bg-white p-6 rounded-3xl border border-slate-200 flex gap-4 items-center">
                            <div className="w-8 h-8 rounded-full bg-pink-50 flex items-center justify-center text-pink-500 font-black text-xs shrink-0">?</div>
                            <p className="text-slate-700 font-bold">{prompt}</p>
                         </div>
                      ))}
                   </div>
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
                <h2 className="text-4xl font-black text-slate-800 leading-tight tracking-tight">Any lingering doubts?</h2>
                <p className="text-lg text-slate-500 font-medium max-w-lg mx-auto leading-relaxed">
                   Ask Gurukul AI for more examples, simpler explanations, or even a deep dive into any topic.
                </p>
             </div>
             <div className="flex flex-col gap-3 max-w-xs mx-auto">
                <button
                  onClick={() => router.push(`/tutor?chapter=${chapterId}&class=${className}&subject=${subject}`)}
                  className="py-5 bg-indigo-600 text-white rounded-3xl font-black uppercase tracking-widest text-xs shadow-xl shadow-indigo-100 hover:bg-indigo-700 transition-all"
                >
                  Start Chat Session
                </button>
                <button
                  onClick={() => nextStep()}
                  className="py-5 bg-white text-slate-400 rounded-3xl font-black uppercase tracking-widest text-xs hover:bg-slate-50 transition-all"
                >
                  Ask later
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
                <h2 className="text-5xl font-black text-slate-800 tracking-tighter uppercase">Mastered!</h2>
                <p className="text-lg text-slate-500 font-medium">You have completed all stages of this lesson.</p>
             </div>
             <div className="p-8 bg-slate-50 rounded-[48px] border border-slate-100 max-w-sm mx-auto flex items-center justify-center gap-8">
                <div className="text-center">
                   <p className="text-3xl font-black text-slate-800">+50</p>
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">XP Gained</p>
                </div>
                <div className="w-px h-10 bg-slate-200"></div>
                <div className="text-center">
                   <p className="text-3xl font-black text-slate-800">+10</p>
                   <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Coins</p>
                </div>
             </div>
          </div>
        );
      default:
        return null;
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] flex flex-col h-screen overflow-hidden">

      {/* Dynamic Header */}
      <header className="h-20 bg-white border-b border-slate-200 flex items-center justify-between px-8 shrink-0">
         <div className="flex items-center gap-6">
            <button onClick={() => router.back()} className="p-2 hover:bg-slate-100 rounded-xl transition-colors">
               <X size={20} className="text-slate-400" />
            </button>
            <div className="w-px h-8 bg-slate-200"></div>
            <div>
               <p className="text-[9px] font-black text-slate-400 uppercase tracking-[0.2em] mb-1 leading-none">
                  {subject} • Class {className?.split('_').pop()}
               </p>
               <h1 className="text-sm font-black text-primary uppercase tracking-tight flex items-center gap-2">
                  <span className="text-slate-800">{displayData.fullName}</span>
                  <span className="w-1 h-1 bg-slate-200 rounded-full"></span>
                  {steps[currentStep]}
               </h1>
            </div>
         </div>

         <div className="flex items-center gap-8">
            <div className="hidden md:flex items-center gap-4">
               <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">
                  Step {currentStep + 1} of {steps.length}
               </span>
               <div className="w-48 h-2 bg-slate-100 rounded-full overflow-hidden border border-slate-200">
                  <motion.div
                    className="h-full bg-primary"
                    initial={false}
                    animate={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
                  />
               </div>
            </div>
            <button
              onClick={() => setIsReading(!isReading)}
              className={`w-10 h-10 rounded-xl flex items-center justify-center transition-all ${isReading ? 'bg-primary text-white shadow-lg shadow-blue-100' : 'bg-slate-50 text-slate-400 border border-slate-200 hover:border-primary/40'}`}
            >
               {isReading ? <Volume2 size={20} /> : <VolumeX size={20} />}
            </button>
         </div>
      </header>

      {/* Main Player Area */}
      <main className="flex-1 overflow-y-auto relative bg-white">
         <div className="max-w-4xl mx-auto py-16 px-8">
            <AnimatePresence mode="wait">
               <motion.div
                  key={currentStep}
                  initial={{ opacity: 0, x: 20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, x: -20 }}
                  transition={{ duration: 0.3 }}
                  className="space-y-12"
               >
                  {renderStepContent(steps[currentStep])}
               </motion.div>
            </AnimatePresence>
         </div>
      </main>

      {/* Footer Navigation */}
      <footer className="h-24 bg-white border-t border-slate-200 flex items-center justify-center px-8 shrink-0 shadow-[0_-10px_40px_rgba(0,0,0,0.02)]">
         <div className="max-w-4xl w-full flex items-center justify-between gap-6">
            <button
               onClick={prevStep}
               disabled={currentStep === 0}
               className={`flex items-center gap-3 px-8 py-3.5 rounded-2xl font-black text-xs uppercase tracking-widest transition-all ${currentStep === 0 ? 'opacity-0' : 'bg-white border border-border text-slate-400 hover:bg-slate-50 hover:text-slate-600'}`}
            >
               <ChevronLeft size={16} /> Previous
            </button>

            <button
               onClick={currentStep === steps.length - 1 ? () => router.back() : nextStep}
               className="flex items-center gap-3 px-10 py-4 bg-slate-900 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-black transition-all shadow-xl shadow-slate-200 active:scale-95"
            >
               {currentStep === steps.length - 1 ? 'Finish' : 'Next Step'} <ChevronRight size={16} />
            </button>
         </div>
      </footer>
    </div>
  );
}
