'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Layout } from '@/presentation/components/common/Layout';
import { studentApi, ChapterFull, ContentBlock } from '@/services/api/student_api';
import { ChevronLeft, Info, BookOpen, Target, ShieldCheck, HelpCircle, RefreshCw, Globe, ChevronDown, CheckCircle2 } from 'lucide-react';
import { MarkdownRenderer } from '@/presentation/components/common/MarkdownRenderer';
import Link from 'next/link';

export default function ChapterContentPage() {
  const { chapterId } = useParams();
  const [data, setData] = useState<ChapterFull | null>(null);
  const [loading, setLoading] = useState(true);
  const [activePillar, setActivePillar] = useState<'learn' | 'practice' | 'assess' | 'revise' | 'resources'>('learn');
  const [isAuditMode, setIsAuditMode] = useState(false);

  useEffect(() => {
    let mounted = true;
    console.log(`[CHAPTER] Loading stream for ${chapterId}`);

    if (chapterId) {
      studentApi.getChapterFull(chapterId as string)
        .then(res => {
          if (mounted) {
            console.log(`[CHAPTER] Stream synced: ${res?.title}`);
            setData(res);
            setLoading(false);
          }
        })
        .catch(err => {
          if (mounted) {
            console.error(`[CHAPTER] Sync failure:`, err);
            setLoading(false);
          }
        });
    }

    return () => { mounted = false; };
  }, [chapterId]);

  if (loading) return <Layout><div className="p-20 text-center font-black text-slate-300 uppercase animate-pulse italic">Synchronizing Educational Stream...</div></Layout>;
  if (!data) return <Layout><div className="p-20 text-center text-red-500 font-black italic uppercase">Chapter Not Found</div></Layout>;

  const pillarConfig = [
    { id: 'learn', label: 'Learn', icon: BookOpen },
    { id: 'practice', label: 'Practice', icon: Target },
    { id: 'assess', label: 'Assess', icon: HelpCircle },
    { id: 'revise', label: 'Revise', icon: RefreshCw },
    { id: 'resources', label: 'Resources', icon: Globe },
  ] as const;

  const activeItems = data[activePillar] || [];

  // Human-readable title repair
  const displayTitle = data.title && data.title.includes('_')
    ? data.title.split('_').slice(1).join(' ').replace(/\b\w/g, l => l.toUpperCase())
    : data.title || 'Untitled Chapter';

  return (
    <Layout>
      <div className="bg-white border-b sticky top-20 z-50 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 lg:px-8 py-3 flex flex-col lg:flex-row items-center justify-between gap-4">
           <div className="flex items-center gap-4 shrink-0">
              <Link href={`/subject/${data.classId.toLowerCase().replace(' ', '_')}_${data.subjectId.toLowerCase().replace(' ', '_')}`} className="flex items-center gap-2 text-slate-500 font-bold text-xs hover:text-blue-600 transition-all bg-slate-50 px-4 py-2 rounded-xl border border-slate-200">
                  <ChevronLeft size={16} /> Back
              </Link>
              <button
                onClick={() => setIsAuditMode(!isAuditMode)}
                className={`px-3 py-2 rounded-xl text-[10px] font-black uppercase tracking-widest border transition-all ${
                  isAuditMode ? 'bg-slate-900 text-white border-slate-900' : 'bg-white text-slate-400 border-slate-100 hover:border-slate-200'
                }`}
              >
                {isAuditMode ? 'Audit Mode Active' : 'Enable Audit Mode'}
              </button>
           </div>

           <div className="flex items-center gap-2 overflow-x-auto w-full lg:w-auto no-scrollbar">
              {pillarConfig.map(pillar => {
                 const count = data.counts?.[pillar.id] || 0;
                 return (
                    <button
                      key={pillar.id}
                      onClick={() => setActivePillar(pillar.id)}
                      className={`flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs font-bold transition-all shrink-0 border ${
                          activePillar === pillar.id
                            ? 'bg-blue-600 text-white border-blue-600 shadow-md shadow-blue-100'
                            : 'bg-white text-slate-600 border-slate-200 hover:bg-slate-50'
                      }`}
                    >
                      <pillar.icon size={16} />
                      <span className="capitalize">{pillar.label}</span>
                      <span className={`ml-1.5 px-2 py-0.5 rounded-full text-[10px] ${
                        activePillar === pillar.id ? 'bg-blue-500 text-white' : 'bg-slate-100 text-slate-500'
                      }`}>
                        {count}
                      </span>
                    </button>
                 );
              })}
           </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 lg:py-16 space-y-12 lg:space-y-20">
        <header className="space-y-4 text-center max-w-4xl mx-auto">
           <div className="flex items-center justify-center gap-3 text-blue-600 font-black text-[10px] sm:text-xs uppercase tracking-[0.3em] mb-2 bg-blue-50 w-fit mx-auto px-4 py-1.5 rounded-full border border-blue-100 shadow-sm">
              <ShieldCheck size={16} /> Verified NCERT Curriculum
           </div>
           <h1 className="text-4xl sm:text-5xl lg:text-7xl font-black tracking-tight text-slate-900 leading-[1.1] uppercase italic underline decoration-slate-100 decoration-8 underline-offset-[12px]">
              {displayTitle}
           </h1>
           <p className="text-xs sm:text-sm text-slate-400 font-bold uppercase tracking-[0.3em] pt-4">
              Level {data.classId?.split(' ')[1] || '5'} • {data.subjectId?.replace(/_/g, ' ')} • CHAPTER {data.chapter_id}
           </p>
        </header>

        <div className="space-y-12 lg:space-y-16 max-w-6xl mx-auto">
           {activeItems.map((item, i) => (
              <ContentCard key={item.id} block={item} index={i + 1} audit={isAuditMode} />
           ))}

           {activeItems.length === 0 && (
              <div className="p-16 bg-slate-50 rounded-3xl border-2 border-dashed border-slate-200 text-center space-y-3">
                 <Info size={40} className="mx-auto text-slate-300" />
                 <p className="text-slate-500 font-bold text-sm">No items found in this section.</p>
              </div>
           )}
        </div>
      </div>
    </Layout>
  );
}

function ContentCard({ block, index, audit }: { block: ContentBlock; index: number; audit: boolean }) {
  const [showAnswer, setShowAnswer] = useState(false);
  const [showTrace, setShowTrace] = useState(audit);

  // Robust Content Type Detection
  const text = block.text || '';
  const isJumbledWord = text.match(/^[a-z]+$/i) && text.length < 15 && text.length > 2 && block.type !== 'HEADING' && !['Activity', 'Question', 'Note'].includes(text);

  // Dialogue: multiple lines, most ending/starting with speaker:
  const lines = text.split('\n').filter(l => l.trim().length > 0);
  const isDialogue = lines.length > 1 && lines.every(l => l.includes(':') && l.indexOf(':') < 25);

  const isTable = text.includes('|') || text.includes('\t\t');

  return (
    <div className={`bg-white border-2 rounded-[32px] p-6 sm:p-10 space-y-6 transition-all group relative overflow-hidden ${
      audit ? 'border-amber-100 shadow-sm shadow-amber-50' : 'border-slate-100 hover:border-blue-600 hover:shadow-xl'
    }`}>
       {audit && (
         <div className="absolute top-0 right-0 px-4 py-1 bg-amber-400 text-amber-900 text-[8px] font-black uppercase tracking-[0.2em] rounded-bl-xl">
           Internal Audit View
         </div>
       )}

       <div className="flex items-center justify-between border-b border-slate-50 pb-4">
          <div className="flex items-center gap-2">
             <span className={`px-3 py-1 rounded-lg text-[10px] font-black uppercase tracking-widest ${
               audit ? 'bg-amber-100 text-amber-700' : 'bg-slate-900 text-white'
             }`}>
               {block.type}
             </span>
             <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Item {index}</span>
          </div>
          {block.source.page && (
             <span className="text-[10px] font-black text-blue-600 bg-blue-50 px-3 py-1 rounded-full border border-blue-100 uppercase tracking-widest italic">Source Page {block.source.page}</span>
          )}
       </div>

       {block.title && (
          <h3 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tighter leading-tight uppercase italic decoration-blue-100 decoration-4">
            {block.title}
          </h3>
       )}

       {block.text && (
         <div className={`text-lg sm:text-xl text-slate-600 leading-relaxed ${
           isDialogue ? 'space-y-4' : 'space-y-2'
         }`}>
            {isDialogue ? (
               <div className="space-y-4 bg-slate-50 p-6 sm:p-8 rounded-3xl border border-slate-100 shadow-inner">
                  {lines.map((line, idx) => {
                     const [speaker, ...speech] = line.split(':');
                     if (!speech.length) return null;
                     return (
                        <div key={idx} className="flex flex-col sm:flex-row gap-1 sm:gap-4 items-start">
                           <span className="font-black text-blue-600 uppercase text-[10px] sm:text-xs tracking-[0.15em] shrink-0 w-28 pt-1 opacity-80">{speaker.trim()}:</span>
                           <span className="text-slate-800 font-semibold text-lg sm:text-xl leading-relaxed tracking-tight">{speech.join(':').trim()}</span>
                        </div>
                     );
                  })}
               </div>
            ) : isJumbledWord ? (
               <div className="flex items-center gap-4 bg-blue-50 p-6 rounded-2xl border-2 border-blue-100 border-dashed">
                  <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center text-white font-black italic shrink-0">?</div>
                  <div>
                    <p className="text-[10px] font-black text-blue-400 uppercase tracking-widest mb-1">Jumbled Activity</p>
                    <p className="text-2xl font-black tracking-[0.3em] text-blue-900 uppercase underline decoration-blue-200 underline-offset-8">{block.text}</p>
                  </div>
               </div>
            ) : isTable ? (
               <div className="overflow-x-auto bg-slate-50 rounded-2xl border border-slate-200 p-1">
                  <pre className="text-sm font-mono p-4 text-slate-700 leading-tight whitespace-pre">
                    {block.text}
                  </pre>
               </div>
            ) : (
              <MarkdownRenderer content={block.text} />
            )}
         </div>
       )}

       {/* Answer Section */}
       {block.answer && (
          <div className="pt-4 space-y-4">
             <button
               onClick={() => setShowAnswer(!showAnswer)}
               className="flex items-center gap-2 text-xs font-black text-blue-600 hover:text-blue-800 transition-all uppercase tracking-widest"
             >
                {showAnswer ? 'Hide Solution' : 'Reveal Solution'} <ChevronDown size={14} className={showAnswer ? 'rotate-180' : ''} />
             </button>
             {showAnswer && (
                <div className="p-6 bg-emerald-50 border-2 border-emerald-100 rounded-2xl space-y-2 animate-in fade-in slide-in-from-top-2">
                   <div className="flex items-center gap-2 text-[10px] font-black text-emerald-700 uppercase tracking-widest italic mb-2">
                      <CheckCircle2 size={16} /> Authoritative Guidance
                   </div>
                   <div className="text-lg font-bold text-emerald-900 leading-relaxed">
                      <MarkdownRenderer content={block.answer} />
                   </div>
                   {block.explanation && (
                      <div className="mt-4 pt-4 border-t border-emerald-100 text-sm font-medium text-emerald-700 italic">
                         {block.explanation}
                      </div>
                   )}
                </div>
             )}
          </div>
       )}

       {/* Audit Traceability */}
       <div className="pt-4 flex items-center justify-between">
          <button onClick={() => setShowTrace(!showTrace)} className={`text-[9px] font-black uppercase tracking-widest hover:text-slate-500 transition-colors ${
            showTrace ? 'text-blue-600' : 'text-slate-300'
          }`}>
            {showTrace ? 'Hide Forensic Info' : 'Show Forensic Info'}
          </button>
          {audit && (
            <div className="flex gap-2">
               <span className="text-[8px] font-bold text-slate-300 bg-slate-50 px-2 py-0.5 rounded uppercase tracking-tighter">SEC: {block.id.split('_')[5]}</span>
               <span className="text-[8px] font-bold text-slate-300 bg-slate-50 px-2 py-0.5 rounded uppercase tracking-tighter">HASH: {block.id.split('_').pop()?.slice(0, 8)}</span>
            </div>
          )}
       </div>

       {showTrace && (
          <div className="mt-2 p-6 bg-slate-50 rounded-2xl border border-slate-100 text-[10px] font-mono text-slate-500 space-y-2 grid grid-cols-1 md:grid-cols-2 gap-4">
             <div className="space-y-1">
                <p className="font-black text-slate-400 border-b border-slate-200 pb-1 mb-2 uppercase">Identity</p>
                <p><span className="text-slate-400">ID:</span> {block.id}</p>
                <p><span className="text-slate-400">ORDER:</span> {block.order}</p>
                <p><span className="text-slate-400">TYPE:</span> {block.type}</p>
             </div>
             <div className="space-y-1">
                <p className="font-black text-slate-400 border-b border-slate-200 pb-1 mb-2 uppercase">Provenance</p>
                <p><span className="text-slate-400">FILE:</span> {block.source.file}</p>
                <p><span className="text-slate-400">PAGE:</span> {block.source.page}</p>
                <p><span className="text-slate-400">UID:</span> {block.id.split('_').slice(0, 4).join('_')}</p>
             </div>
          </div>
       )}
    </div>
  );
}
