'use client';

import React, { useEffect, useState } from 'react';
import { chapterService } from '@/services/api';
import {
  BookOpen, Brain, Zap, Target, HelpCircle,
  Sparkles, ListTodo, History, Info, Layers,
  ChevronRight, Play, CheckCircle2, MessageSquare,
  Lightbulb, AlertCircle, X as XIcon, ClipboardCheck,
  TrendingUp, Compass, Flag, Map, GraduationCap,
  Microscope, PenTool, Puzzle, Users, Star,
  LightbulbIcon, BookOpenCheck, Layout, BrainCircuit,
  ArrowDownCircle, Award, BookMarked, MonitorPlay
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import FormattedText from '@/components/FormattedText';
import { getChapterDisplayData } from '@/utils/chapter';

interface ChapterContentRendererProps {
  className: string;
  subject: string;
  chapterId: string;
}

export default function ChapterContentRenderer({ className, subject, chapterId }: ChapterContentRendererProps) {
  const [pkg, setPkg] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedMedia, setSelectedMedia] = useState<{ title: string, url: string } | null>(null);

  const displayData = getChapterDisplayData(chapterId, pkg);

  useEffect(() => {
    const fetchPackage = async () => {
      setLoading(true);
      try {
        const normSubject = subject.toLowerCase().replace(/ /g, '_');
        const data = await chapterService.getPackage(className, normSubject, chapterId);
        setPkg(data);
      } catch (e) {
        console.error("Failed to fetch chapter package", e);
      } finally {
        setLoading(false);
      }
    };
    fetchPackage();
  }, [className, subject, chapterId]);

  if (loading) {
    return (
      <div className="space-y-16 animate-pulse w-full max-w-7xl mx-auto px-6">
        <div className="h-96 bg-white border border-slate-100 rounded-[64px]" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="h-64 bg-white border border-slate-100 rounded-[48px]" />
            <div className="h-64 bg-white border border-slate-100 rounded-[48px]" />
            <div className="h-64 bg-white border border-slate-100 rounded-[48px]" />
        </div>
      </div>
    );
  }

  if (!pkg) return <div className="text-center py-20 text-slate-400 font-bold uppercase tracking-[0.4em] text-[10px]">Neural link lost. Content not found.</div>;

  const components = pkg.components || {};

  return (
    <div className="w-full space-y-32 pb-40 max-w-7xl mx-auto px-4 md:px-10">

      {/* 1. MASTER CHAPTER HEADER */}
      <header className="space-y-12">
        <div className="space-y-6">
            <div className="flex items-center gap-3 text-primary">
                <Sparkles size={20} className="animate-pulse" />
                <span className="font-black uppercase shadow-sm px-4 py-1.5 bg-primary/5 border border-primary/10 rounded-full tracking-[0.5em] text-[9px]">Verified Content Stream</span>
            </div>
            <h1 className="text-6xl md:text-8xl font-black text-slate-900 tracking-tighter leading-[0.9] uppercase italic">
                {displayData.name}
            </h1>
            <div className="flex flex-wrap items-center gap-6">
                <p className="text-slate-400 font-black text-2xl tracking-tight uppercase">
                    {subject.replace(/_/g, ' ')}
                </p>
                <div className="w-1.5 h-1.5 rounded-full bg-slate-200" />
                <p className="text-primary font-black text-2xl tracking-tight uppercase">
                    Grade {displayData.className.split('_').pop()}
                </p>
            </div>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            <StatsBadge icon={<Layout />} label="Integrated Modules" value="42 V3 Nodes" color="blue" />
            <StatsBadge icon={<Target />} label="Concept Density" value="Deep Learning" color="emerald" />
            <StatsBadge icon={<Award />} label="Mastery Engine" value="Adaptive Path" color="purple" />
        </div>

        <div className="pt-10 flex items-center gap-6 text-slate-300 font-black text-[9px] uppercase tracking-[0.4em]">
            <span>Deep dive initiated</span>
            <div className="flex-1 h-px bg-slate-100" />
            <ArrowDownCircle size={24} className="animate-bounce text-primary" />
        </div>
      </header>

      {/* 2. THE FOUNDATION (Objectives & Prerequisites) */}
      <SectionWrapper id="foundation" title="Theoretical Framework" icon={<Flag />} color="rose">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
            <div className="space-y-8 bg-white p-12 rounded-[56px] border border-slate-200 shadow-sm group hover:shadow-xl transition-all h-full">
                <h4 className="text-[10px] font-black text-rose-500 uppercase tracking-[0.4em] px-2 flex items-center gap-3">
                    <Target size={14} /> Learning Objectives
                </h4>
                <div className="space-y-6">
                    {components.learning_objectives?.content?.objectives?.map((obj: string, i: number) => (
                        <div key={i} className="flex gap-6">
                            <div className="w-10 h-10 rounded-2xl bg-rose-50 flex items-center justify-center text-rose-600 font-black text-sm shrink-0 shadow-inner">{i+1}</div>
                            <p className="text-xl font-bold text-slate-800 leading-tight pt-1">{obj}</p>
                        </div>
                    ))}
                </div>
            </div>
            <div className="space-y-8 p-12 bg-slate-900 rounded-[56px] text-white shadow-2xl relative overflow-hidden h-full">
                <h4 className="text-[10px] font-black text-primary uppercase tracking-[0.4em] px-2 relative z-10">Prerequisites</h4>
                <div className="space-y-8 relative z-10">
                    <p className="text-slate-400 text-lg font-medium leading-relaxed italic">Building on existing knowledge nodes:</p>
                    <div className="space-y-5">
                        {components.prerequisites?.content?.assumed_knowledge?.map((item: string, i: number) => (
                            <div key={i} className="flex items-center gap-4 bg-white/5 p-5 rounded-[32px] border border-white/10 hover:bg-white/10 transition-colors">
                                <CheckCircle2 size={20} className="text-primary" />
                                <span className="font-bold text-slate-200 text-lg">{item}</span>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="absolute top-0 right-0 w-64 h-64 bg-primary/10 rounded-full blur-[100px] -mr-32 -mt-32" />
            </div>
        </div>
      </SectionWrapper>

      {/* 3. THE MASTER LESSON (Comprehensive Content) */}
      <SectionWrapper id="lesson" title="Authoritative Lesson" icon={<BookMarked />} color="indigo">
        <div className="space-y-20">
            {/* Primary Content Card */}
            <article className="prose prose-slate max-w-none">
                <div className="p-16 md:p-24 bg-white border border-slate-200 rounded-[80px] shadow-sm relative overflow-hidden">
                    <div className="relative z-10 space-y-12">
                        <div className="flex items-center gap-4">
                            <span className="px-5 py-2 bg-indigo-50 text-indigo-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-indigo-100">Primary Stream</span>
                        </div>
                        <h4 className="text-5xl font-black text-slate-900 leading-[1.1] tracking-tight">{displayData.name}</h4>
                        <div className="text-3xl leading-relaxed text-slate-700 font-medium">
                            <FormattedText content={components.chapter_content?.content?.overview} />
                        </div>

                        <div className="grid gap-12 pt-16 border-t border-slate-100">
                             <h5 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.4em]">Core Knowledge Nodes</h5>
                             <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                                {components.chapter_content?.content?.source_grounded_key_points?.map((point: string, i: number) => (
                                    <div key={i} className="space-y-4 p-10 bg-slate-50/50 border border-slate-100 rounded-[48px] hover:bg-white hover:border-indigo-200 transition-all shadow-sm">
                                        <div className="w-10 h-10 rounded-2xl bg-white flex items-center justify-center text-indigo-400 font-black text-sm shadow-inner border border-slate-100">{i+1}</div>
                                        <p className="text-xl font-bold text-slate-800 leading-relaxed">{point}</p>
                                    </div>
                                ))}
                             </div>
                        </div>
                    </div>
                    <div className="absolute top-0 right-0 w-96 h-96 bg-indigo-500/5 rounded-full blur-[120px] -mr-48 -mt-48" />
                </div>
            </article>

            {/* Teacher Insights */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
                <div className="space-y-8 p-16 bg-slate-900 rounded-[64px] text-white shadow-2xl relative overflow-hidden group h-full">
                    <div className="relative z-10 space-y-12">
                        <div className="flex items-center gap-4">
                            <div className="w-14 h-14 rounded-[28px] bg-white/10 flex items-center justify-center border border-white/10 text-primary shadow-inner"><Users size={28} /></div>
                            <div>
                                <h4 className="text-2xl font-black uppercase tracking-tight">Academic Perspective</h4>
                                <p className="text-slate-400 text-xs font-bold uppercase tracking-widest mt-1">Pedagogical Insights</p>
                            </div>
                        </div>
                        <div className="space-y-12">
                             {components.teacher_explanation?.content?.explanation_sections?.map((sec: any, i: number) => (
                                <div key={i} className="space-y-4 group/item">
                                    <h5 className="text-[10px] font-black text-primary uppercase tracking-[0.3em] flex items-center gap-3">
                                        <div className="w-1.5 h-1.5 rounded-full bg-primary" /> {sec.title}
                                    </h5>
                                    <p className="text-xl font-bold leading-relaxed text-slate-200 group-hover/item:text-white transition-colors">{sec.explanation}</p>
                                </div>
                             ))}
                        </div>
                    </div>
                    <div className="absolute bottom-0 right-0 w-[500px] h-[500px] bg-primary/10 rounded-full blur-[100px] -mb-64 -mr-64 opacity-50" />
                </div>

                <div className="space-y-12 h-full">
                    <div className="bg-amber-50 border border-amber-100 p-16 rounded-[64px] space-y-10 relative overflow-hidden group hover:shadow-xl transition-all">
                        <div className="flex items-center gap-4 relative z-10">
                            <div className="w-14 h-14 rounded-[28px] bg-white flex items-center justify-center text-amber-500 shadow-sm border border-amber-100"><Sparkles size={28} /></div>
                            <h4 className="text-3xl font-black text-amber-900 tracking-tight italic uppercase">Story Narrative</h4>
                        </div>
                        <div className="text-2xl font-bold text-amber-800/80 leading-relaxed italic relative z-10">
                            <FormattedText content={components.story_mode?.content?.opening} />
                        </div>
                        <div className="absolute -bottom-10 -right-10 w-48 h-48 bg-amber-500/10 rounded-full blur-3xl" />
                    </div>

                    <div className="p-16 bg-white border border-slate-200 rounded-[64px] shadow-sm space-y-8">
                        <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.4em] px-2 flex items-center gap-3">
                            <LightbulbIcon size={14} className="text-amber-500" /> Simplified Logic
                        </h4>
                        <div className="text-2xl font-bold text-slate-700 leading-relaxed italic border-l-4 border-primary pl-8 py-2">
                            <FormattedText content={components.student_explanation?.content?.simple_explanation} />
                        </div>
                    </div>
                </div>
            </div>
        </div>
      </SectionWrapper>

      {/* 4. KNOWLEDGE WEB (Concepts & Mappings) */}
      <SectionWrapper id="knowledge" title="The Knowledge Grid" icon={<Layers />} color="blue">
        <div className="space-y-20">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                {components.concepts?.content?.concepts?.map((concept: any, i: number) => (
                    <div key={i} className="p-12 bg-white border border-slate-200 rounded-[64px] shadow-sm space-y-10 hover:shadow-2xl transition-all group relative overflow-hidden">
                        <div className="flex items-center justify-between relative z-10">
                            <div className="w-16 h-16 rounded-[28px] bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100 shadow-inner group-hover:bg-blue-600 group-hover:text-white transition-all duration-500">
                                <Brain size={32} />
                            </div>
                            <div className="px-5 py-2 bg-emerald-50 text-emerald-600 rounded-full text-[9px] font-black uppercase tracking-widest border border-emerald-100 opacity-0 group-hover:opacity-100 transition-opacity">Core Node</div>
                        </div>
                        <div className="space-y-8 relative z-10">
                            <h5 className="text-4xl font-black text-slate-900 tracking-tighter leading-none">{concept.name}</h5>
                            <p className="text-2xl font-bold text-slate-600 leading-relaxed italic border-l-2 border-slate-100 pl-8">&ldquo;{concept.definition}&rdquo;</p>
                            <div className="pt-10 border-t border-slate-50">
                                <p className="text-[10px] font-black text-blue-400 uppercase tracking-[0.3em] mb-4">Empirical Evidence</p>
                                <p className="text-lg text-slate-500 font-bold leading-relaxed">{concept.source_evidence || concept.evidence}</p>
                            </div>
                        </div>
                        <div className="absolute -bottom-20 -right-20 w-64 h-64 bg-blue-500/5 rounded-full blur-[80px] group-hover:bg-blue-500/10 transition-colors" />
                    </div>
                ))}
            </div>

            <div className="p-16 bg-slate-900 rounded-[80px] text-white space-y-20 shadow-[0_50px_100px_-20px_rgba(0,0,0,0.4)] relative overflow-hidden">
                <div className="relative z-10 flex flex-col md:flex-row md:items-end justify-between gap-12">
                    <div className="space-y-4">
                        <div className="inline-flex items-center gap-3 px-5 py-2 bg-primary/20 border border-primary/20 rounded-full text-primary font-black text-[9px] uppercase tracking-[0.4em]">Integrated Lexicon</div>
                        <h4 className="text-6xl font-black tracking-tight italic uppercase">Essential Vocabulary</h4>
                        <p className="text-slate-400 text-2xl font-medium max-w-2xl">Master these linguistic nodes to unlock the chapter&apos;s full semantic depth.</p>
                    </div>
                </div>
                <div className="relative z-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
                    {components.key_terms?.content?.terms?.slice(0, 9).map((term: any, i: number) => (
                        <div key={i} className="p-12 bg-white/5 border border-white/5 rounded-[56px] hover:bg-white/10 hover:border-white/10 transition-all group/term">
                            <h5 className="text-3xl font-black text-primary mb-4 group-hover/term:scale-105 transition-transform origin-left">{term.term}</h5>
                            <p className="text-lg text-slate-400 font-bold leading-relaxed">{term.student_friendly_meaning || term.meaning}</p>
                        </div>
                    ))}
                </div>
                <div className="absolute top-0 right-0 w-[800px] h-[800px] bg-primary/10 rounded-full blur-[200px] -mr-32 -mt-32 opacity-60" />
            </div>
        </div>
      </SectionWrapper>

      {/* 5. MULTIMEDIA & VISUALS */}
      <SectionWrapper id="multimedia" title="Visual Discovery" icon={<MonitorPlay />} color="blue">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
            <div
                onClick={() => {
                    const multimedia = components.multimedia?.content;
                    const video = multimedia?.resources?.find((r: any) => r.type === 'video' || r.type === 'video_discovery') ||
                                  multimedia?.videos?.[0] ||
                                  multimedia?.discovery_links?.[0];

                    if (video?.url) {
                        setSelectedMedia({ title: video.title || 'Visual Narrative', url: video.url });
                    } else {
                        alert("AI Visual Narrative is currently being indexed for this chapter.");
                    }
                }}
                className="lg:col-span-2 aspect-video bg-slate-900 rounded-[64px] flex flex-col items-center justify-center border-[16px] border-white shadow-2xl relative group overflow-hidden cursor-pointer"
            >
                <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/30 to-purple-600/30 group-hover:opacity-0 transition-opacity" />
                <div className="w-28 h-24 bg-white rounded-[40px] flex items-center justify-center text-primary shadow-2xl group-hover:scale-110 transition-transform relative z-10">
                    <Play size={48} fill="currentColor" className="ml-1" />
                </div>
                <div className="mt-10 text-center relative z-10 px-12">
                    <p className="font-black text-white text-lg uppercase tracking-[0.5em] shadow-sm">Launch AI Visual Narrative</p>
                    <p className="text-white/40 text-[11px] font-bold uppercase mt-3 tracking-widest italic">Chapter Streaming Package V3</p>
                </div>
                <div className="absolute bottom-12 left-12 flex items-center gap-3 z-10 opacity-60">
                    <div className="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-[10px] font-black text-white uppercase tracking-[0.3em]">Verified V3 Media Stream</span>
                </div>
            </div>
            <div className="bg-white border border-slate-200 p-16 rounded-[72px] shadow-sm flex flex-col justify-between hover:shadow-xl transition-all group h-full">
                <div className="space-y-8">
                    <div className="w-20 h-20 rounded-[32px] bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100 shadow-inner group-hover:bg-blue-600 group-hover:text-white transition-all"><BrainCircuit size={40} /></div>
                    <div className="space-y-4">
                        <h4 className="text-4xl font-black text-slate-900 tracking-tighter uppercase italic leading-none">Knowledge Galaxy</h4>
                        <p className="text-xl text-slate-500 font-medium leading-relaxed">Interactive concept mapping of all V3 components within this unit.</p>
                    </div>
                </div>
                <button className="w-full py-6 bg-slate-900 text-white rounded-[32px] font-black text-xs uppercase tracking-[0.4em] hover:bg-primary transition-all shadow-2xl active:scale-95 mt-12">
                    Enter Galaxy
                </button>
            </div>
        </div>
      </SectionWrapper>

      {/* 6. QUESTION BANK & ASSESSMENT */}
      <SectionWrapper id="assessment" title="Mastery Validation" icon={<Award />} color="amber">
        <div className="space-y-24">
             <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                 <div className="lg:col-span-8 space-y-16">
                    <div className="flex items-center justify-between px-4">
                        <h4 className="text-[10px] font-black text-slate-400 uppercase tracking-[0.4em]">Integrated Question Bank</h4>
                        <span className="text-[10px] font-black text-amber-600 uppercase tracking-widest italic">{components.practice_bank?.content?.items?.length || 0} Nodes Available</span>
                    </div>
                    <div className="space-y-12">
                        {components.practice_bank?.content?.items?.slice(0, 3).map((q: any, i: number) => (
                            <div key={i} className="p-16 bg-white border border-slate-200 rounded-[80px] shadow-sm space-y-12 group hover:shadow-xl transition-all relative overflow-hidden">
                                <div className="flex items-center justify-between relative z-10">
                                    <span className="px-6 py-2 bg-slate-50 text-slate-400 rounded-full text-[10px] font-black uppercase tracking-widest border border-slate-100">Validated Item {i+1}</span>
                                    <span className="text-[10px] font-black text-primary uppercase tracking-[0.5em] opacity-0 group-hover:opacity-100 transition-opacity">Smart Key: {String.fromCharCode(65 + q.correct_option)}</span>
                                </div>
                                <h5 className="text-4xl font-black text-slate-900 leading-[1.2] tracking-tighter relative z-10">{q.question}</h5>
                                <div className="grid grid-cols-1 gap-4 relative z-10">
                                    {q.options?.map((opt: string, idx: number) => (
                                        <div key={idx} className="p-10 rounded-[40px] bg-slate-50/50 border border-slate-100 font-bold text-xl text-slate-500 hover:bg-white hover:border-amber-200 hover:text-amber-600 transition-all cursor-pointer flex items-center gap-6">
                                            <span className="w-12 h-12 rounded-2xl bg-white border border-slate-200 flex-none text-center leading-[48px] text-lg font-black shadow-sm">{String.fromCharCode(65 + idx)}</span>
                                            <span className="leading-tight">{opt}</span>
                                        </div>
                                    ))}
                                </div>
                                <div className="absolute top-0 right-0 w-48 h-48 bg-amber-500/5 rounded-full blur-[80px] -mr-24 -mt-24" />
                            </div>
                        ))}
                    </div>
                    <div className="flex justify-center pt-10">
                        <button className="px-16 py-8 bg-slate-900 text-white rounded-[40px] font-black text-sm uppercase tracking-[0.4em] hover:bg-amber-600 transition-all shadow-[0_30px_60px_-12px_rgba(0,0,0,0.3)] active:scale-95">
                            Launch Full Adaptive Quiz
                        </button>
                    </div>
                 </div>

                 <div className="lg:col-span-4 space-y-12">
                    <div className="p-16 bg-amber-50 border border-amber-100 rounded-[72px] flex flex-col justify-center items-center text-center space-y-12 sticky top-10 shadow-sm">
                        <div className="w-28 h-28 bg-white rounded-[40px] flex items-center justify-center text-amber-600 shadow-2xl shadow-amber-500/10"><Star size={56} fill="currentColor" /></div>
                        <div className="space-y-8">
                            <h4 className="text-5xl font-black text-amber-900 tracking-tighter leading-none italic uppercase">Ready for Finals?</h4>
                            <p className="text-2xl font-bold text-amber-800/60 leading-relaxed max-w-xs mx-auto">Neural sync complete for <span className="text-amber-900">{displayData.name}</span>. Proceed to validation.</p>
                        </div>
                        <button className="w-full py-8 bg-amber-600 text-white rounded-[40px] font-black text-base uppercase tracking-[0.3em] hover:bg-amber-700 transition-all shadow-[0_20px_50px_-10px_rgba(217,119,6,0.3)] active:scale-95">
                            Start Unit Mastery
                        </button>
                    </div>
                 </div>
             </div>

             {/* Final Synthesis Recap */}
             <div className="p-20 md:p-28 border-[16px] border-white rounded-[96px] bg-slate-50 shadow-inner relative overflow-hidden">
                <div className="relative z-10 flex flex-col md:flex-row gap-20 items-start">
                    <div className="w-24 h-24 bg-white rounded-[40px] flex items-center justify-center text-slate-400 shadow-2xl shrink-0"><ClipboardCheck size={48} /></div>
                    <div className="space-y-10">
                        <h4 className="text-4xl font-black text-slate-900 uppercase tracking-tighter italic">Chapter Synthesis</h4>
                        <div className="text-4xl font-bold text-slate-500/80 leading-[1.6] italic max-w-5xl">
                            <FormattedText content={components.chapter_summary?.content?.summary} />
                        </div>
                    </div>
                </div>
                <div className="absolute top-0 right-0 w-96 h-96 bg-slate-200/30 rounded-full blur-[150px] -mr-48 -mt-48" />
             </div>
        </div>
      </SectionWrapper>

      {/* Media Modal */}
      <AnimatePresence>
        {selectedMedia && (
            <motion.div
                initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
                className="fixed inset-0 z-[110] bg-slate-900/90 backdrop-blur-2xl flex items-center justify-center p-6"
                onClick={() => setSelectedMedia(null)}
            >
                <motion.div
                    initial={{ scale: 0.9, y: 20 }} animate={{ scale: 1, y: 0 }} exit={{ scale: 0.9, y: 20 }}
                    className="bg-black w-full max-w-6xl aspect-video rounded-[64px] overflow-hidden shadow-[0_60px_120px_-20px_rgba(0,0,0,0.8)] border-[12px] border-white/10"
                    onClick={e => e.stopPropagation()}
                >
                    <iframe
                        src={selectedMedia.url.replace('watch?v=', 'embed/')}
                        className="w-full h-full"
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        allowFullScreen
                    />
                </motion.div>
                <button className="absolute top-10 right-10 w-20 h-20 bg-white/10 hover:bg-white/20 rounded-full flex items-center justify-center text-white backdrop-blur-xl transition-all shadow-2xl">
                    <XIcon size={40} />
                </button>
            </motion.div>
        )}
      </AnimatePresence>

      <style jsx global>{`
         .custom-scrollbar::-webkit-scrollbar { width: 8px; }
         .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
         .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.08); border-radius: 20px; }
         .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.15); }
      `}</style>
    </div>
  );
}

function SectionWrapper({ id, title, icon, color, children }: { id: string, title: string, icon: any, color: string, children: React.ReactNode }) {
    const colorClasses: Record<string, string> = {
        blue: 'bg-blue-600 shadow-blue-500/30',
        indigo: 'bg-indigo-600 shadow-indigo-500/30',
        emerald: 'bg-emerald-600 shadow-emerald-500/30',
        amber: 'bg-amber-500 shadow-amber-500/30',
        rose: 'bg-rose-600 shadow-rose-500/30',
    };

    return (
        <section id={id} className="space-y-20">
            <div className="flex items-center gap-10 px-4">
                <div className={`w-24 h-24 rounded-[40px] flex items-center justify-center text-white shadow-2xl transition-all duration-1000 hover:rotate-[360deg] ${colorClasses[color]}`}>
                    {React.cloneElement(icon as React.ReactElement, { size: 48 })}
                </div>
                <div className="space-y-2">
                    <p className="text-[11px] font-black text-slate-400 uppercase tracking-[0.5em]">Node Category</p>
                    <h3 className="text-6xl font-black text-slate-900 tracking-tighter uppercase italic leading-none">{title}</h3>
                </div>
            </div>
            <div className="relative">
                {children}
            </div>
        </section>
    );
}

function StatsBadge({ icon, label, value, color }: { icon: any, label: string, value: string, color: string }) {
    const colors: Record<string, string> = {
        blue: 'text-blue-600 bg-blue-50 border-blue-100',
        emerald: 'text-emerald-600 bg-emerald-50 border-emerald-100',
        purple: 'text-purple-600 bg-purple-50 border-purple-100',
    };
    return (
        <div className={`p-10 rounded-[56px] border flex items-center gap-8 shadow-sm transition-all hover:shadow-2xl hover:-translate-y-2 group ${colors[color]}`}>
            <div className="w-20 h-20 rounded-[32px] bg-white flex items-center justify-center shadow-inner group-hover:scale-110 transition-transform duration-500">
                {React.cloneElement(icon as React.ReactElement, { size: 36 })}
            </div>
            <div>
                <p className="text-[11px] font-black uppercase tracking-[0.4em] leading-none mb-3 opacity-60">{label}</p>
                <p className="text-2xl font-black leading-none tracking-tight">{value}</p>
            </div>
        </div>
    );
}
