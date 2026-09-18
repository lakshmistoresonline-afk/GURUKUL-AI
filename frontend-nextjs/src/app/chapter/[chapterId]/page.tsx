'use client';

import React, { useEffect, useState, useMemo } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Layout } from '@/presentation/components/common/Layout';
import { studentApi, ChapterFull, ContentBlock, Subject } from '@/services/api/student_api';
import {
  ChevronLeft, ChevronRight, Info, BookOpen, Target, ShieldCheck,
  HelpCircle, RefreshCw, Globe, CheckCircle2, Music, Sparkles,
  ExternalLink, Video, Play, Search, Eye, FileText, Award, Compass, Calculator
} from 'lucide-react';
import { MarkdownRenderer } from '@/presentation/components/common/MarkdownRenderer';
import Link from 'next/link';

export default function ChapterContentPage() {
  const { chapterId } = useParams();
  const router = useRouter();
  const [data, setData] = useState<ChapterFull | null>(null);
  const [subject, setSubject] = useState<Subject | null>(null);
  const [loading, setLoading] = useState(true);
  const [activePillar, setActivePillar] = useState<'learn' | 'practice' | 'assess' | 'revise' | 'resources'>('learn');
  const [isAuditMode, setIsAuditMode] = useState(false);
  const [showTextbookSource, setShowTextbookSource] = useState(false);

  useEffect(() => {
    let mounted = true;
    if (chapterId) {
      setLoading(true);
      studentApi.getChapterFull(chapterId as string)
        .then(res => {
          if (mounted) {
            setData(res);
            const subj_id = res.subjectId;
            studentApi.getSubject(subj_id).then(subj => {
               if (mounted) {
                  setSubject(subj);
                  setLoading(false);
               }
            }).catch(() => { if (mounted) setLoading(false); });
          }
        })
        .catch(() => { if (mounted) setLoading(false); });
    }
    return () => { mounted = false; };
  }, [chapterId]);

  useEffect(() => {
    if (!loading && data) document.body.setAttribute('data-gurukul-ready', 'true');
    else if (!loading && !data) document.body.setAttribute('data-gurukul-ready', 'false');
  }, [loading, data]);

  const nav = useMemo(() => {
    if (!subject || !data) return null;
    const currentIndex = subject.chapters.findIndex(c => c.id === data.id);
    return {
      current: currentIndex + 1,
      total: subject.chapters.length,
      prev: currentIndex > 0 ? subject.chapters[currentIndex - 1].id : null,
      next: currentIndex < subject.chapters.length - 1 ? subject.chapters[currentIndex + 1].id : null
    };
  }, [subject, data]);

  // UNIT AGGREGATOR: Group Logical Records into Educational Units (UI Cards)
  const educationalUnits = useMemo(() => {
    if (!data || !data[activePillar]) return [];
    const items = data[activePillar];
    const units: ContentBlock[][] = [];
    let currentUnit: ContentBlock[] = [];

    items.forEach((item) => {
       const prevItem = currentUnit.length > 0 ? currentUnit[currentUnit.length - 1] : null;

       if (item.type === 'heading') {
          if (currentUnit.length > 0) units.push(currentUnit);
          currentUnit = [item];
       }
       else if (currentUnit.length === 0) {
          currentUnit.push(item);
       }
       else {
          let shouldGroup = false;

          if (prevItem?.type === 'heading') shouldGroup = true;
          else if (item.type === prevItem?.type) {
             if (['dialogue', 'poem', 'question'].includes(item.type)) shouldGroup = true;
          }
          else if (item.type === 'paragraph' && prevItem?.type === 'paragraph' && (item.text?.length || 0) < 300) {
             shouldGroup = true;
          }

          if (shouldGroup) {
             currentUnit.push(item);
          } else {
             units.push(currentUnit);
             currentUnit = [item];
          }
       }
    });
    if (currentUnit.length > 0) units.push(currentUnit);
    return units;
  }, [data, activePillar]);

  if (loading) return <Layout><div className="p-16 text-center font-bold text-slate-400 uppercase tracking-widest animate-pulse">Synchronizing Educational Stream...</div></Layout>;
  if (!data) return <Layout><div className="p-16 text-center text-red-500 font-bold uppercase tracking-wider">Chapter Not Found</div></Layout>;

  const displayTitle = data.title && data.title.includes('_')
    ? data.title.split('_').slice(1).join(' ').replace(/\b\w/g, l => l.toUpperCase())
    : data.title || 'Untitled Chapter';

  const pillarEmptyMessages: Record<string, string> = {
    learn: 'No lesson material is available for this chapter.',
    practice: 'No practice activities are available for this chapter.',
    assess: 'No assessment questions are available for this chapter.',
    revise: 'No revision material is available for this chapter.',
    resources: 'No verified YouTube video lesson was found for this chapter.',
  };

  const subjectClean = data.subjectId ? data.subjectId.replace(/_/g, ' ').toUpperCase() : 'CURRICULUM';

  return (
    <Layout>
      <div id="gurukul-chapter-container" data-chapter-id={data.id} data-class-id={data.classId} data-subject-id={data.subjectId} className="w-full">
        {/* COMPACT STICKY PILLAR BAR */}
        <div className="bg-white/95 backdrop-blur-md border-b border-slate-200 sticky top-16 z-40 shadow-xs py-2.5 px-4 sm:px-8">
          <div className="max-w-6xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
             <div className="flex items-center gap-2 shrink-0">
                <Link href={`/subject/${data.subjectId}`} className="flex items-center gap-1.5 text-slate-700 font-semibold text-xs hover:text-blue-600 transition-all bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200">
                    <ChevronLeft size={14} /> Back
                </Link>
                <button onClick={() => setShowTextbookSource(!showTextbookSource)} className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${showTextbookSource ? 'bg-blue-50 text-blue-700 border-blue-200' : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'}`}>
                  <FileText size={14} /> {showTextbookSource ? 'Hide Textbook Source' : 'View Textbook Source'}
                </button>
                <button onClick={() => setIsAuditMode(!isAuditMode)} className={`px-2.5 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider border transition-all ${isAuditMode ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-500 border-slate-200 hover:bg-slate-50'}`}>
                  {isAuditMode ? 'Audit Mode On' : 'Audit Mode'}
                </button>
             </div>
             <div className="flex items-center gap-2 overflow-x-auto w-full sm:w-auto no-scrollbar py-1">
                {[
                  { id: 'learn', label: 'Learn', icon: BookOpen },
                  { id: 'practice', label: 'Practice', icon: Target },
                  { id: 'assess', label: 'Assess', icon: HelpCircle },
                  { id: 'revise', label: 'Revise', icon: RefreshCw },
                  { id: 'resources', label: 'Resources', icon: Globe },
                ].map(pillar => (
                  <button key={pillar.id} onClick={() => setActivePillar(pillar.id as any)} className={`flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-semibold transition-all shrink-0 border ${activePillar === pillar.id ? 'bg-blue-600 text-white border-blue-600 shadow-sm' : 'bg-white text-slate-700 border-slate-200 hover:bg-slate-50'}`}>
                    <pillar.icon size={14} />
                    <span className="capitalize">{pillar.label}</span>
                    <span className={`ml-1 px-2 py-0.5 rounded-full text-[10px] font-bold ${activePillar === pillar.id ? 'bg-blue-500 text-white' : 'bg-slate-100 text-slate-600'}`}>{data.counts[pillar.id] || 0}</span>
                  </button>
                ))}
             </div>
          </div>
        </div>

        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          {/* HEADER */}
          <header className="space-y-4 text-center max-w-4xl mx-auto">
             <div className="flex items-center justify-center gap-2 text-blue-600 font-bold text-xs uppercase tracking-widest bg-blue-50 w-fit mx-auto px-4 py-1.5 rounded-full border border-blue-100">
                <ShieldCheck size={16} /> Verified NCERT Curriculum
             </div>
             <h1 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight uppercase">{displayTitle}</h1>
             <div className="flex flex-col items-center gap-2 pt-2">
                <p className="text-xs sm:text-sm text-slate-500 font-semibold uppercase tracking-wider flex items-center gap-3">
                   <span>Level {data.classId?.split('_')[1] || '5'}</span>
                   <span className="w-1.5 h-1.5 rounded-full bg-slate-300" />
                   <span>{subjectClean}</span>
                </p>
                {nav && (
                   <div className="flex items-center gap-4 mt-3">
                      <button disabled={!nav.prev} onClick={() => router.push(`/chapter/${nav.prev}`)} className="p-2 rounded-xl bg-white border border-slate-200 text-slate-500 hover:text-blue-600 hover:border-blue-600 disabled:opacity-20 transition-all group">
                         <ChevronLeft size={18} className="group-hover:-translate-x-0.5 transition-transform" />
                      </button>
                      <span className="text-xs font-semibold text-slate-700 bg-slate-100 px-4 py-1.5 rounded-full border border-slate-200">
                         Chapter {nav.current} of {nav.total}
                      </span>
                      <button disabled={!nav.next} onClick={() => router.push(`/chapter/${nav.next}`)} className="p-2 rounded-xl bg-white border border-slate-200 text-slate-500 hover:text-blue-600 hover:border-blue-600 disabled:opacity-20 transition-all group">
                         <ChevronRight size={18} className="group-hover:translate-x-0.5 transition-transform" />
                      </button>
                   </div>
                )}
             </div>

             {/* WHAT YOU WILL LEARN SUMMARY */}
             <div className="bg-slate-50/80 border border-slate-200/80 rounded-2xl p-4 sm:p-5 text-left max-w-3xl mx-auto space-y-2">
                <div className="flex items-center gap-2 text-blue-600 font-bold text-xs uppercase tracking-wider">
                   <Compass size={16} /> What You Will Learn in This Chapter
                </div>
                <p className="text-slate-700 text-sm leading-relaxed">
                   Explore core concepts, guided activities, source-derived explanations, and practice exercises for <strong>{displayTitle}</strong> in {subjectClean}.
                </p>
             </div>
          </header>

          {/* TEXTBOOK SOURCE DRAWER */}
          {showTextbookSource && (
             <div className="bg-amber-50/90 border border-amber-200 rounded-3xl p-6 max-w-4xl mx-auto space-y-4 transition-all">
                <div className="flex items-center justify-between border-b border-amber-200 pb-3">
                   <div className="flex items-center gap-2 text-amber-800 font-bold text-xs uppercase tracking-wider">
                      <FileText size={18} /> Verified NCERT Textbook Source Material
                   </div>
                   <span className="text-[10px] font-bold text-amber-700 uppercase bg-amber-100 px-2.5 py-0.5 rounded-md">Immutable Source</span>
                </div>
                <div className="text-xs sm:text-sm font-serif leading-relaxed text-amber-950 space-y-3 max-h-80 overflow-y-auto pr-2">
                   {data.learn.slice(0, 5).map((b, idx) => (
                      <p key={`src-${idx}`}>{b.text}</p>
                   ))}
                </div>
             </div>
          )}

          {/* MAIN CONTENT AREA */}
          <div className="space-y-8 w-full max-w-4xl mx-auto">
             {educationalUnits.map((unit, uIdx) => (
                <EducationalUnitCard key={`unit-${activePillar}-${uIdx}-${unit[0]?.id || "empty"}`} unit={unit} index={uIdx + 1} audit={isAuditMode} chapterId={data.id} section={activePillar} subjectId={data.subjectId} />
             ))}
             {educationalUnits.length === 0 && (
                <div className="p-12 bg-slate-50 rounded-2xl border border-dashed border-slate-200 text-center space-y-2 w-full">
                   <Info size={32} className="mx-auto text-slate-400" />
                   <p className="text-slate-600 font-semibold text-sm">{pillarEmptyMessages[activePillar] || 'No content is available for this pillar.'}</p>
                </div>
             )}
          </div>

          {nav && (
             <div className="pt-12 pb-8 flex justify-center gap-4">
                {nav.prev && <button onClick={() => router.push(`/chapter/${nav.prev}`)} className="flex items-center gap-2 px-5 py-3 rounded-2xl border border-slate-200 bg-white hover:border-blue-600 text-slate-800 font-semibold text-xs transition-all group">&larr; Previous Unit</button>}
                {nav.next && <button onClick={() => router.push(`/chapter/${nav.next}`)} className="flex items-center gap-2 px-5 py-3 rounded-2xl border border-slate-200 bg-white hover:border-blue-600 text-slate-800 font-semibold text-xs transition-all group">Continue Journey &rarr;</button>}
             </div>
          )}
        </div>
      </div>
    </Layout>
  );
}

function EducationalUnitCard({ unit, index, audit, chapterId, section, subjectId }: { unit: ContentBlock[]; index: number; audit: boolean; chapterId: string; section: string; subjectId: string }) {
  const hasHeading = unit[0].type === 'heading';
  const headingText = hasHeading ? unit[0].text : null;
  const content = hasHeading ? unit.slice(1) : unit;

  const isQuestionSet = content.some(b => b.type === 'question' || b.type === 'mcq' || b.type === 'short_answer');

  if (content.length === 0 && hasHeading) {
     return (
        <div className="py-6 border-b-2 border-slate-200 mb-8 w-full">
           <h2 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight flex items-center gap-3">
              <span className="w-8 h-1 bg-blue-600 rounded-full" />
              {headingText}
           </h2>
        </div>
     );
  }

  return (
    <div className={`transition-all relative group/unit w-full ${isQuestionSet ? 'bg-slate-50/70 border border-slate-200 rounded-3xl p-6 sm:p-8 space-y-6' : 'space-y-6'}`}>
       {headingText && (
          <div className={`inline-flex items-center gap-2 font-bold text-xs uppercase tracking-wider mb-4 ${isQuestionSet ? 'bg-blue-600 text-white px-4 py-1.5 rounded-lg shadow-sm' : 'text-blue-600'}`}>
             {isQuestionSet ? <Target size={14} /> : <Sparkles size={14} />}
             {headingText}
          </div>
       )}

       <div className="space-y-6 w-full">
          {content.map((block, blockIndex) => (
             <LogicalRecordRenderer key={`record-${section}-${index}-${block.id || "record"}-${blockIndex}`} block={block} audit={audit} chapterId={chapterId} section={section} subjectId={subjectId} />
          ))}
       </div>

       {audit && (
          <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between text-[10px] text-slate-400 font-mono">
             <span>Module Unit {index}</span>
             <span>{content.length} records</span>
          </div>
       )}
    </div>
  );
}

function LogicalRecordRenderer({ block, audit, chapterId, section, subjectId }: { block: ContentBlock; audit: boolean; chapterId: string; section: string; subjectId: string }) {
  const text = block.text || '';
  const lines = text.split('\n').filter(l => l.trim().length > 0);

  const isPoem = block.type === 'poem';
  const isDialogue = block.type === 'dialogue';
  const isQuestion = block.type === 'question' || block.type === 'mcq' || block.type === 'short_answer';
  const isResource = section === 'resources' || ['video_resource', 'resource_search', 'channel_resource', 'official_resource', 'youtube'].includes(block.type);
  const isYouTube = block.type === 'youtube' || (block.url && block.url.includes('youtube.com/watch'));
  const isSearchQuery = block.type === 'resource_search' || block.resource_category === 'DISCOVERY_QUERY';

  const isMaths = subjectId && subjectId.includes('math');
  const isHindi = subjectId && subjectId.includes('hindi');
  const isEVS = subjectId && subjectId.includes('evs');

  return (
    <div
      className="relative group/record w-full"
      data-gurukul-record-id={block.id}
      data-chapter-id={chapterId}
      data-section={section}
      data-sequence={block.order}
      data-content-type={block.type}
    >
       {isResource ? (
          <div className={`p-6 sm:p-8 rounded-3xl border shadow-md space-y-4 w-full ${isYouTube ? 'bg-red-950 text-white border-red-900' : isSearchQuery ? 'bg-slate-900 text-white border-slate-800' : 'bg-white text-slate-900 border-slate-200'}`}>
             <div className="flex items-center justify-between">
                <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wider text-blue-500">
                   {isYouTube ? <Video size={18} className="text-red-500" /> : isSearchQuery ? <Search size={16} className="text-blue-400" /> : <Globe size={16} className="text-blue-600" />}
                   <span>{isYouTube ? 'VERIFIED YOUTUBE LESSON' : isSearchQuery ? 'DISCOVER MORE SEARCH DESCRIPTOR' : 'OFFICIAL EDUCATIONAL RESOURCE'}</span>
                </div>
                <span className={`text-[10px] font-bold uppercase tracking-wider px-2.5 py-0.5 rounded-md ${isYouTube ? 'bg-red-900 text-red-100' : isSearchQuery ? 'bg-slate-800 text-slate-300' : 'bg-blue-50 text-blue-700 border border-blue-200'}`}>
                   {isYouTube ? 'Verified Video' : isSearchQuery ? 'Discovery Descriptor' : 'Official Portal'}
                </span>
             </div>

             <div className={`text-base sm:text-lg font-semibold leading-relaxed ${isYouTube || isSearchQuery ? 'text-slate-100' : 'text-slate-900'}`}>
                <MarkdownRenderer content={text} />
             </div>

             {block.url ? (
                <a
                   href={block.url}
                   target="_blank"
                   rel="noopener noreferrer"
                   className={`inline-flex items-center gap-2 px-5 py-2.5 font-bold text-xs uppercase tracking-wider rounded-xl transition-all shadow-sm ${isYouTube ? 'bg-red-600 hover:bg-red-500 text-white' : 'bg-blue-600 hover:bg-blue-500 text-white'}`}
                >
                   {isYouTube ? <Play size={14} /> : <ExternalLink size={14} />}
                   {isYouTube ? 'Watch Verified Video' : 'Open Resource Link &rarr;'}
                </a>
             ) : null}
          </div>
       ) : isDialogue ? (
          <div className="space-y-3 bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm w-full">
             {lines.map((line, idx) => {
                const [speaker, ...speech] = line.split(':');
                if (!speech.length) return <p key={idx} className="text-slate-800 text-base leading-relaxed">{line}</p>;
                return (
                   <div key={idx} className="flex flex-col sm:flex-row gap-2 items-start">
                      <span className="font-bold text-blue-600 uppercase text-xs tracking-wider shrink-0 w-28 pt-1 text-left sm:text-right border-r-2 border-blue-100 pr-3">{speaker.trim()}</span>
                      <span className="text-slate-900 font-medium text-base sm:text-lg leading-relaxed">{speech.join(':').trim()}</span>
                   </div>
                );
             })}
          </div>
       ) : isPoem ? (
          <div className="py-6 px-8 bg-indigo-50/40 rounded-3xl border-l-4 border-blue-600 shadow-xs w-full">
             <div className="inline-flex p-2 bg-blue-600 text-white rounded-lg mb-4 shadow-sm">
                <Music size={20} />
             </div>
             <div className="space-y-2 font-serif">
                {text.split('\n').map((line, idx) => (
                   <p key={idx} className="text-slate-900 font-semibold tracking-wide text-lg sm:text-xl leading-relaxed">{line}</p>
                ))}
             </div>
          </div>
       ) : isQuestion ? (
          <div className="space-y-4 w-full">
             <div className="flex items-center gap-2 text-blue-600 font-bold text-xs uppercase tracking-wider">
                <HelpCircle size={16} /> {isEVS ? 'Observation & Inquiry Prompt' : isMaths ? 'Problem & Numerical Challenge' : 'Exploration Prompt'}
             </div>
             <div className="text-lg sm:text-xl font-bold text-slate-900 leading-snug">
                <MarkdownRenderer content={text} />
             </div>
             {block.answer && (
                <div className="mt-4 p-6 bg-emerald-50/60 border border-emerald-200 rounded-2xl space-y-3">
                   <div className="flex items-center gap-2 text-emerald-700 font-bold text-xs uppercase tracking-wider">
                      <CheckCircle2 size={18} /> Verified Guidance & Solution
                   </div>
                   <div className="text-base font-medium text-emerald-900 leading-relaxed">
                      <MarkdownRenderer content={block.answer} />
                   </div>
                </div>
             )}
          </div>
       ) : (
          <div className="text-base sm:text-lg text-slate-800 leading-relaxed font-normal w-full">
             {isMaths && block.type === 'worked_practice' && (
                <div className="flex items-center gap-2 text-indigo-600 font-bold text-xs uppercase tracking-wider mb-2">
                   <Calculator size={16} /> Step-by-Step Mathematical Worked Solution
                </div>
             )}
             <MarkdownRenderer content={text} />
          </div>
       )}

       {audit && (
          <div className="opacity-0 group-hover/record:opacity-100 transition-opacity absolute -right-6 top-0 translate-x-full p-4 bg-white shadow-xl rounded-xl border border-slate-200 text-[10px] font-mono text-slate-500 space-y-1 w-56 z-10">
             <p className="text-slate-900 font-bold border-b pb-1 mb-1 uppercase tracking-wider">Forensic Audit</p>
             <p>UID: {block.id}</p>
             <p>PAGE: {block.source?.page || 'N/A'}</p>
             <p>TYPE: {block.type}</p>
             <p className="truncate">FILE: {block.source?.file}</p>
          </div>
       )}
    </div>
  );
}
