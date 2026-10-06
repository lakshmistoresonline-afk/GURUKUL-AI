'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { CurriculumApiClient, CurriculumIdentity } from '@/lib/curriculumClient';
import RendererRegistry from '@/components/presentation/RendererRegistry';

interface Props {
  segments: string[];
}

const TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'notes', label: 'Notes' },
  { id: 'master', label: 'Master' },
  { id: 'foundational', label: 'Foundational' },
  { id: 'flashcards', label: 'Flashcards' },
  { id: 'mindmaps', label: 'Mindmaps' },
  { id: 'quiz', label: 'Quiz' },
  { id: 'question_papers', label: 'Question Papers' },
];

export default function CatchAllChapterClient({ segments }: Props) {
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [contentData, setContentData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const grade = segments[0] || '';
  const subject = segments[1] || '';
  const book = segments[2] || '';
  const part = segments[3] || '';
  const unit = segments[4] || '';
  const chapterId = segments[5] || '';

  useEffect(() => {
    async function loadContent() {
      if (segments.length < 6) {
        setErrorMsg('Incomplete curriculum identity in route.');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setErrorMsg(null);
        const identity: CurriculumIdentity = {
          grade,
          subject,
          book,
          part,
          unit,
          chapter_id: chapterId,
          content_type: activeTab
        };
        const res = await CurriculumApiClient.fetchContent(identity);
        setContentData(res.data);
      } catch (err: any) {
        setErrorMsg(err.message || 'Chapter identity could not be resolved.');
        setContentData(null);
      } finally {
        setLoading(false);
      }
    }

    loadContent();
  }, [segments, grade, subject, book, part, unit, chapterId, activeTab]);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 p-6 sm:p-10 space-y-8">
      {/* Top Identity Header */}
      <div className="max-w-6xl mx-auto bg-gradient-to-r from-indigo-950 via-indigo-900 to-slate-900 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-3">
        <div className="flex flex-wrap items-center gap-2 text-xs font-mono uppercase text-indigo-300">
          <span>Class {grade}</span> / <span>{subject}</span> / <span>Book: {book}</span> / <span>Part: {part}</span> / <span>Unit: {unit}</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black tracking-tight">Chapter: {chapterId}</h1>
      </div>

      {/* Content-Type Tabs Bar */}
      <div className="max-w-6xl mx-auto flex flex-wrap gap-2 bg-white p-3 rounded-2xl border border-slate-200 shadow-sm">
        {TABS.map(tab => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all ${
              activeTab === tab.id
                ? 'bg-indigo-600 text-white shadow-md'
                : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Main Content Area */}
      <div className="max-w-6xl mx-auto">
        {loading && (
          <div className="p-16 text-center text-slate-500 bg-white rounded-3xl border border-slate-200 shadow-sm">
            <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-sm font-bold">Resolving authoritative curriculum identity...</p>
          </div>
        )}

        {errorMsg && !loading && (
          <div className="p-12 bg-rose-50 border border-rose-200 rounded-3xl text-center space-y-3 shadow-sm">
            <h3 className="text-lg font-black text-rose-900">Curriculum Identity Not Found (404)</h3>
            <p className="text-sm text-rose-700 max-w-md mx-auto">{errorMsg}</p>
            <Link href="/" className="inline-block mt-4 px-6 py-2.5 bg-indigo-600 text-white text-xs font-bold rounded-xl shadow-md hover:bg-indigo-500 transition-all">
              Return to Curriculum Explorer ↻
            </Link>
          </div>
        )}

        {!loading && !errorMsg && contentData && (
          <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8">
            {RendererRegistry.resolve({
              grade,
              subject,
              book,
              contentType: activeTab,
              data: contentData
            })}
          </div>
        )}
      </div>
    </div>
  );
}
