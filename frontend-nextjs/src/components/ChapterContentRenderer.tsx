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
  ArrowDownCircle, Award, BookMarked, MonitorPlay, ArrowRight
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import FormattedText from '@/components/FormattedText';
import { getChapterDisplayData } from '@/utils/chapter';

import Link from 'next/link';

interface ChapterContentRendererProps {
  className: string;
  subject: string;
  chapterId: string;
}

const BOILERPLATE_PHRASES = [
  "chapter-relevant word",
  "statement unrelated to the chapter",
  "statement that contradicts",
  "cannot be checked from the chapter",
  "develops reading, language, interpretation",
  "main learning is organised around",
  "source-supported points below",
  "Explain the central ideas and evidence",
  "Use the chapter's concepts or language",
  "Identify relationships, patterns",
  "Communicate reasoning clearly",
  "Apply at least one chapter idea",
  "extracted from the uploaded chapter PDF",
  "full PDF remains the source of truth"
];

function isBoilerplate(text: string): boolean {
  if (!text) return true;
  return BOILERPLATE_PHRASES.some(phrase => text.toLowerCase().includes(phrase.toLowerCase()));
}

function cleanContent(text: string): string {
  if (!text) return "";
  // Remove common boilerplate paragraphs
  return text.split('\n').filter(p => !isBoilerplate(p)).join('\n').trim();
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
      <div className="space-y-8 animate-pulse w-full max-w-5xl mx-auto">
        <div className="h-64 bg-white border border-slate-100 rounded-3xl" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="h-48 bg-white border border-slate-100 rounded-3xl" />
            <div className="h-48 bg-white border border-slate-100 rounded-3xl" />
            <div className="h-48 bg-white border border-slate-100 rounded-3xl" />
        </div>
      </div>
    );
  }

  if (!pkg) return <div className="text-center py-20 text-slate-400 font-bold uppercase tracking-widest text-[10px]">Content not found.</div>;

  const components = pkg.components || {};

  // Filter components for real content
  const objectives = components.learning_objectives?.content?.objectives?.filter((o: string) => !isBoilerplate(o)) || [];
  const prerequisites = components.prerequisites?.content?.assumed_knowledge?.filter((a: string) => !isBoilerplate(a)) || [];
  const keyPoints = components.chapter_content?.content?.source_grounded_key_points?.filter((p: string) => !isBoilerplate(p)) || [];
  const teacherSections = components.teacher_explanation?.content?.explanation_sections?.filter((s: any) => !isBoilerplate(s.explanation)) || [];
  const storyContent = components.story_mode?.content?.opening || "";
  const simpleExpl = components.student_explanation?.content?.simple_explanation || "";
  const concepts = components.concepts?.content?.concepts?.filter((c: any) => !isBoilerplate(c.definition)) || [];
  const keyTerms = components.key_terms?.content?.terms?.filter((t: any) => !isBoilerplate(t.meaning)) || [];

  const practiceItems = components.practice_bank?.content?.items?.filter((q: any) => {
      const optionsBoilerplate = q.options?.some((o: string) => isBoilerplate(o));
      return !optionsBoilerplate;
  }) || [];

  const summary = cleanContent(components.chapter_summary?.content?.summary || "");

  const multimedia = components.multimedia?.content;
  const videoResource = multimedia?.resources?.find((r: any) => r.type === 'video' || r.type === 'video_discovery') ||
                        multimedia?.videos?.[0] ||
                        multimedia?.discovery_links?.[0];

  return (
    <div className="w-full space-y-16 pb-20 max-w-5xl mx-auto">

      {/* 1. MASTER CHAPTER HEADER */}
      <header className="space-y-8 px-2">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-8">
            <div className="space-y-4">
                <div className="flex items-center gap-2 text-primary">
                    <Sparkles size={16} className="animate-pulse" />
                    <span className="font-black uppercase px-3 py-1 bg-primary/5 border border-primary/10 rounded-full tracking-widest text-[8px]">Academic Stream</span>
                </div>
                <h1 className="text-4xl md:text-5xl font-black text-slate-900 tracking-tight leading-tight">
                    {displayData.name}
                </h1>
                <div className="flex items-center gap-4 text-slate-400 font-black text-sm md:text-lg tracking-tight uppercase">
                    <span>{subject.replace(/_/g, ' ')}</span>
                    <div className="w-1 h-1 rounded-full bg-slate-200" />
                    <span className="text-primary">
                        Grade {className.match(/\d+/)?.[0] || displayData.className.match(/\d+/)?.[0] || ''}
                    </span>
                </div>
            </div>

            <Link
                href={`/learn/${chapterId}?class=${className}&subject=${subject}`}
                className="bg-primary text-white px-10 py-5 rounded-2xl font-black text-xs uppercase tracking-widest flex items-center gap-3 shadow-xl shadow-primary/20 hover:bg-blue-700 active:scale-95 transition-all w-fit"
            >
                Start Full Lesson <ArrowRight size={16} />
            </Link>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <StatsBadge icon={<Layout />} label="Modules" value="Active Learning" color="blue" />
            <StatsBadge icon={<Target />} label="Focus" value="Conceptual" color="emerald" />
            <StatsBadge icon={<Award />} label="Mastery" value="Adaptive" color="purple" />
        </div>
      </header>

      {/* 2. THE FOUNDATION */}
      {(objectives.length > 0 || prerequisites.length > 0) && (
        <SectionWrapper id="foundation" title="Learning Foundation" icon={<Flag />} color="rose">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {objectives.length > 0 && (
                    <div className="space-y-6 bg-white p-8 rounded-3xl border border-slate-200 shadow-sm h-full">
                        <h4 className="text-[10px] font-black text-rose-500 uppercase tracking-widest flex items-center gap-2">
                            <Target size={12} /> Objectives
                        </h4>
                        <div className="space-y-4">
                            {objectives.map((obj: string, i: number) => (
                                <div key={i} className="flex gap-4">
                                    <div className="w-8 h-8 rounded-xl bg-rose-50 flex items-center justify-center text-rose-600 font-black text-xs shrink-0">{i+1}</div>
                                    <p className="text-base font-bold text-slate-700 leading-tight pt-1">{obj}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
                {prerequisites.length > 0 && (
                    <div className="space-y-6 p-8 bg-slate-900 rounded-3xl text-white shadow-xl h-full">
                        <h4 className="text-[10px] font-black text-primary uppercase tracking-widest">Context</h4>
                        <div className="space-y-4">
                            {prerequisites.map((item: string, i: number) => (
                                <div key={i} className="flex items-center gap-3 bg-white/5 p-4 rounded-2xl border border-white/10">
                                    <CheckCircle2 size={16} className="text-primary" />
                                    <span className="font-bold text-slate-200 text-sm">{item}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </SectionWrapper>
      )}

      {/* 3. THE MASTER LESSON */}
      <SectionWrapper id="lesson" title="Chapter Explorer" icon={<BookMarked />} color="indigo">
        <div className="space-y-10">
            <article className="prose prose-slate max-w-none">
                <div className="p-10 md:p-16 bg-white border border-slate-200 rounded-[40px] shadow-sm relative overflow-hidden">
                    <div className="relative z-10 space-y-8">
                        <h4 className="text-3xl font-black text-slate-900 leading-tight tracking-tight">{displayData.name}</h4>

                        {keyPoints.length > 0 && (
                            <div className="grid gap-6 pt-4 border-t border-slate-100">
                                <h5 className="text-[9px] font-black text-slate-400 uppercase tracking-widest">Key Concepts from Text</h5>
                                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                                    {keyPoints.map((point: string, i: number) => (
                                        <div key={i} className="p-6 bg-slate-50/50 border border-slate-100 rounded-3xl flex gap-4">
                                            <div className="w-8 h-8 rounded-lg bg-white flex items-center justify-center text-indigo-400 font-black text-xs shadow-inner border border-slate-100 shrink-0">{i+1}</div>
                                            <p className="text-sm font-bold text-slate-800 leading-relaxed">{point}</p>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </article>

            {/* Insights */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {teacherSections.length > 0 && (
                    <div className="space-y-6 p-10 bg-slate-900 rounded-[40px] text-white shadow-xl relative overflow-hidden h-full">
                        <div className="relative z-10 space-y-8">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-xl bg-white/10 flex items-center justify-center border border-white/10 text-primary shrink-0"><Users size={20} /></div>
                                <h4 className="text-lg font-black uppercase tracking-tight">Academic View</h4>
                            </div>
                            <div className="space-y-6">
                                {teacherSections.map((sec: any, i: number) => (
                                    <div key={i} className="space-y-2">
                                        <h5 className="text-[9px] font-black text-primary uppercase tracking-widest flex items-center gap-2">
                                            <div className="w-1 h-1 rounded-full bg-primary" /> {sec.title}
                                        </h5>
                                        <p className="text-sm font-bold leading-relaxed text-slate-300">{sec.explanation}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                <div className="space-y-6">
                    {storyContent && !isBoilerplate(storyContent) && (
                        <div className="bg-amber-50 border border-amber-100 p-10 rounded-[40px] space-y-4">
                            <div className="flex items-center gap-3">
                                <div className="w-10 h-10 rounded-xl bg-white flex items-center justify-center text-amber-500 shadow-sm border border-amber-100 shrink-0"><Sparkles size={20} /></div>
                                <h4 className="text-xl font-black text-amber-900 tracking-tight italic">Story Mode</h4>
                            </div>
                            <div className="text-lg font-bold text-amber-800/80 leading-relaxed italic">
                                <FormattedText content={storyContent} />
                            </div>
                        </div>
                    )}

                    {simpleExpl && !isBoilerplate(simpleExpl) && (
                        <div className="p-10 bg-white border border-slate-200 rounded-[40px] shadow-sm space-y-4">
                            <h4 className="text-[9px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                                <LightbulbIcon size={12} className="text-amber-500" /> Simplified
                            </h4>
                            <div className="text-lg font-bold text-slate-700 leading-relaxed italic border-l-2 border-primary pl-6">
                                <FormattedText content={simpleExpl} />
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
      </SectionWrapper>

      {/* 4. KNOWLEDGE WEB */}
      {(concepts.length > 0 || keyTerms.length > 0) && (
        <SectionWrapper id="knowledge" title="Concepts & Glossary" icon={<Layers />} color="blue">
            <div className="space-y-12">
                {concepts.length > 0 && (
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                        {concepts.map((concept: any, i: number) => (
                            <div key={i} className="p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-6 hover:shadow-lg transition-all group">
                                <div className="w-12 h-12 rounded-xl bg-blue-50 flex items-center justify-center text-blue-600 border border-blue-100 shadow-inner group-hover:bg-blue-600 group-hover:text-white transition-all">
                                    <Brain size={24} />
                                </div>
                                <div className="space-y-4">
                                    <h5 className="text-xl font-black text-slate-900 tracking-tight">{concept.name}</h5>
                                    <p className="text-base font-bold text-slate-600 leading-relaxed italic border-l border-slate-100 pl-6">&ldquo;{concept.definition}&rdquo;</p>
                                </div>
                            </div>
                        ))}
                    </div>
                )}

                {keyTerms.length > 0 && (
                    <div className="p-12 bg-slate-900 rounded-[48px] text-white space-y-12 shadow-xl relative overflow-hidden">
                        <div className="relative z-10 space-y-4">
                            <div className="inline-flex items-center gap-2 px-3 py-1 bg-primary/20 border border-primary/20 rounded-full text-primary font-black text-[8px] uppercase tracking-widest">Vocabulary</div>
                            <h4 className="text-3xl font-black tracking-tight uppercase">Key Terms</h4>
                        </div>
                        <div className="relative z-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                            {keyTerms.slice(0, 9).map((term: any, i: number) => (
                                <div key={i} className="p-6 bg-white/5 border border-white/5 rounded-2xl">
                                    <h5 className="text-lg font-black text-primary mb-2">{term.term}</h5>
                                    <p className="text-sm text-slate-400 font-bold leading-relaxed">{term.student_friendly_meaning || term.meaning}</p>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </div>
        </SectionWrapper>
      )}

      {/* 5. MULTIMEDIA */}
      {videoResource?.url && (
        <SectionWrapper id="multimedia" title="Visual Narrative" icon={<MonitorPlay />} color="blue">
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                <div
                    onClick={() => setSelectedMedia({ title: videoResource.title || 'Video Narrative', url: videoResource.url })}
                    className="lg:col-span-12 aspect-video bg-slate-900 rounded-[40px] flex flex-col items-center justify-center border-8 border-white shadow-xl relative group overflow-hidden cursor-pointer"
                >
                    <div className="absolute inset-0 bg-gradient-to-br from-indigo-600/20 to-purple-600/20 group-hover:opacity-0 transition-opacity" />
                    <div className="w-20 h-16 bg-white rounded-2xl flex items-center justify-center text-primary shadow-xl group-hover:scale-110 transition-transform relative z-10">
                        <Play size={32} fill="currentColor" className="ml-1" />
                    </div>
                    <div className="mt-6 text-center relative z-10 px-8">
                        <p className="font-black text-white text-base uppercase tracking-widest">Launch Visual Narrative</p>
                    </div>
                </div>
            </div>
        </SectionWrapper>
      )}

      {/* 6. PRACTICE */}
      <SectionWrapper id="assessment" title="Practice & Mastery" icon={<Award />} color="amber">
        <div className="space-y-12">
             <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                 <div className="lg:col-span-8 space-y-10">
                    <div className="space-y-8">
                        {practiceItems.length > 0 ? practiceItems.slice(0, 3).map((q: any, i: number) => (
                            <div key={i} className="p-10 bg-white border border-slate-200 rounded-[32px] shadow-sm space-y-8 relative overflow-hidden">
                                <span className="px-4 py-1 bg-slate-50 text-slate-400 rounded-full text-[8px] font-black uppercase tracking-widest border border-slate-100">Question {i+1}</span>
                                <h5 className="text-2xl font-black text-slate-900 tracking-tight relative z-10">{q.question}</h5>
                                <div className="grid grid-cols-1 gap-3 relative z-10">
                                    {q.options?.map((opt: string, idx: number) => (
                                        <div key={idx} className="p-5 rounded-2xl bg-slate-50/50 border border-slate-100 font-bold text-base text-slate-500 hover:bg-white hover:border-amber-200 hover:text-amber-600 transition-all cursor-pointer flex items-center gap-4">
                                            <span className="w-8 h-8 rounded-lg bg-white border border-slate-200 flex-none text-center leading-[30px] text-xs font-black shadow-sm">{String.fromCharCode(65 + idx)}</span>
                                            <span className="leading-tight">{opt}</span>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        )) : (
                            <div className="p-10 bg-white border border-slate-200 border-dashed rounded-[32px] text-center text-slate-400 font-bold uppercase tracking-widest text-[10px]">
                                Preparing conceptual assessments...
                            </div>
                        )}
                    </div>
                    <div className="flex justify-center">
                        <button className="px-10 py-5 bg-slate-900 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-amber-600 transition-all shadow-lg active:scale-95">
                            Adaptive Quiz
                        </button>
                    </div>
                 </div>

                 <div className="lg:col-span-4">
                    <div className="p-10 bg-amber-50 border border-amber-100 rounded-[40px] flex flex-col items-center text-center space-y-8 sticky top-10">
                        <div className="w-20 h-20 bg-white rounded-2xl flex items-center justify-center text-amber-600 shadow-lg"><Star size={36} fill="currentColor" /></div>
                        <div className="space-y-4">
                            <h4 className="text-3xl font-black text-amber-900 tracking-tight leading-none italic uppercase">Final Mastery</h4>
                            <p className="text-sm font-bold text-amber-800/60 leading-relaxed">Ready to validate your understanding?</p>
                        </div>
                        <button className="w-full py-5 bg-amber-600 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-amber-700 transition-all active:scale-95">
                            Start Mastery
                        </button>
                    </div>
                 </div>
             </div>

             {summary && (
                <div className="p-12 border-8 border-white rounded-[48px] bg-slate-50 shadow-inner relative overflow-hidden">
                    <div className="relative z-10 flex gap-8 items-start">
                        <div className="w-16 h-16 bg-white rounded-2xl flex items-center justify-center text-slate-400 shadow-lg shrink-0"><ClipboardCheck size={32} /></div>
                        <div className="space-y-4">
                            <h4 className="text-2xl font-black text-slate-900 uppercase tracking-tight italic">Synthesis</h4>
                            <div className="text-xl font-bold text-slate-500/80 leading-relaxed italic">
                                <FormattedText content={summary} />
                            </div>
                        </div>
                    </div>
                </div>
             )}
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
         .custom-scrollbar::-webkit-scrollbar { width: 6px; }
         .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
         .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.05); border-radius: 20px; }
         .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(0,0,0,0.1); }
      `}</style>
    </div>
  );
}

function SectionWrapper({ id, title, icon, color, children }: { id: string, title: string, icon: any, color: string, children: React.ReactNode }) {
    const colorClasses: Record<string, string> = {
        blue: 'bg-blue-600 shadow-blue-500/20',
        indigo: 'bg-indigo-600 shadow-indigo-500/20',
        emerald: 'bg-emerald-600 shadow-emerald-500/20',
        amber: 'bg-amber-500 shadow-amber-500/20',
        rose: 'bg-rose-600 shadow-rose-500/20',
    };

    return (
        <section id={id} className="space-y-10 px-2">
            <div className="flex items-center gap-6">
                <div className={`w-16 h-16 rounded-2xl flex items-center justify-center text-white shadow-lg transition-all duration-1000 hover:rotate-[360deg] shrink-0 ${colorClasses[color]}`}>
                    {React.cloneElement(icon as React.ReactElement, { size: 32 })}
                </div>
                <div className="space-y-1">
                    <p className="text-[9px] font-black text-slate-400 uppercase tracking-widest">Academic Module</p>
                    <h3 className="text-4xl font-black text-slate-900 tracking-tight uppercase italic leading-none">{title}</h3>
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
        <div className={`p-6 rounded-[32px] border flex items-center gap-4 shadow-sm transition-all hover:shadow-md group ${colors[color]}`}>
            <div className="w-12 h-12 rounded-xl bg-white flex items-center justify-center shadow-inner shrink-0">
                {React.cloneElement(icon as React.ReactElement, { size: 24 })}
            </div>
            <div>
                <p className="text-[9px] font-black uppercase tracking-widest leading-none mb-1.5 opacity-60">{label}</p>
                <p className="text-lg font-black leading-none tracking-tight">{value}</p>
            </div>
        </div>
    );
}
