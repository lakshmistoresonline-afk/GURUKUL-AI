'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { CurriculumApiClient, CurriculumIdentity, buildCurriculumUrl } from '@/lib/curriculumClient';
import RendererRegistry from '@/components/presentation/RendererRegistry';

interface Props {
  segments: string[];
}

const CONTENT_TYPE_LABELS: Record<string, string> = {
  overview: 'Overview',
  notes: 'Notes',
  master: 'Master',
  foundational: 'Foundational',
  flashcards: 'Flashcards',
  mindmaps: 'Mindmaps',
  quiz: 'Quiz',
  question_papers: 'Question Papers',
};

export default function CatchAllChapterClient({ segments }: Props) {
  const [activeTab, setActiveTab] = useState<string>('');
  const [availableContentTypes, setAvailableContentTypes] = useState<string[]>([]);
  const [contentData, setContentData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [statusCode, setStatusCode] = useState<number | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  // WS4 & WS20 state
  const [isBookmarked, setIsBookmarked] = useState<boolean>(false);
  const [isNeedPractice, setIsNeedPractice] = useState<boolean>(false);
  const [tutorOpen, setTutorOpen] = useState<boolean>(false);
  const [tutorResponse, setTutorResponse] = useState<string>('');

  const grade = segments[0] || '';
  const subject = segments[1] || '';
  const book = segments[2] || '';
  const part = segments[3] || '';
  const unit = segments[4] || '';
  const chapterId = segments[5] || '';

  // Canonical identity key for complete identity safety (Item 5 / WS20)
  const canonicalIdentityKey = `${grade}:${subject.toLowerCase()}:${book.toLowerCase()}:${part.toLowerCase()}:${unit.toUpperCase()}:${chapterId.toLowerCase()}`;

  const chapterUrl = segments.length >= 6 ? buildCurriculumUrl({ grade, subject, book, part, unit, chapter_id: chapterId }) : '';

  // 1. Identity Initialization & Recent History (Runs ONLY when route identity changes - Item 6 & 7)
  useEffect(() => {
    async function initializeChapterIdentity() {
      if (segments.length < 6) {
        setStatusCode(400);
        setErrorMsg('Invalid Curriculum Identity: Incomplete 6 identity dimensions required (grade, subject, book, part, unit, chapter_id).');
        setLoading(false);
        return;
      }

      try {
        setLoading(true);
        setErrorMsg(null);
        setStatusCode(null);

        // Check bookmarks & need practice
        const bks = JSON.parse(localStorage.getItem('gurukul_canonical_bookmarks') || '[]');
        setIsBookmarked(bks.includes(canonicalIdentityKey));

        const np = JSON.parse(localStorage.getItem('gurukul_canonical_need_practice') || '[]');
        setIsNeedPractice(np.includes(canonicalIdentityKey));

        // Record recent history strictly on chapter entry (Item 7)
        const recent = JSON.parse(localStorage.getItem('gurukul_recent_chapters') || '[]');
        const updatedRecent = [
          { canonicalIdentityKey, grade, subject, book, part, unit, chapterId, timestamp: Date.now() },
          ...recent.filter((r: any) => r.canonicalIdentityKey !== canonicalIdentityKey)
        ].slice(0, 10);
        localStorage.setItem('gurukul_recent_chapters', JSON.stringify(updatedRecent));

        // Fetch authoritative hierarchy to determine available content types
        const hierarchy = await CurriculumApiClient.fetchHierarchy();
        let foundChapter: any = null;

        for (const g of hierarchy) {
          if (String(g.grade) === String(grade)) {
            for (const s of g.subjects || []) {
              if (s.canonical_subject?.toLowerCase() === subject.toLowerCase() || s.subject?.toLowerCase() === subject.toLowerCase()) {
                for (const b of s.books || []) {
                  if (b.book_id?.toLowerCase() === book.toLowerCase() && b.part?.toLowerCase() === part.toLowerCase()) {
                    for (const u of b.units || []) {
                      if (u.unit_id?.toUpperCase() === unit.toUpperCase()) {
                        const ch = (u.chapters || []).find((c: any) => c.chapter_id?.toLowerCase() === chapterId.toLowerCase());
                        if (ch) {
                          foundChapter = ch;
                          break;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }

        if (!foundChapter) {
          setStatusCode(404);
          setErrorMsg(`Chapter identity not found in authoritative registry: Class ${grade} / ${subject} / ${book} / ${part} / ${unit} / ${chapterId}`);
          setLoading(false);
          return;
        }

        const validContentTypes = foundChapter.content_types || ['overview'];
        setAvailableContentTypes(validContentTypes);
        if (!validContentTypes.includes(activeTab)) {
          setActiveTab(validContentTypes[0]);
        }
      } catch (err: any) {
        setStatusCode(500);
        setErrorMsg(err.message || 'Failed to initialize chapter identity.');
        setLoading(false);
      }
    }

    initializeChapterIdentity();
  }, [segments, grade, subject, book, part, unit, chapterId, canonicalIdentityKey]);

  // 2. Content Loading Effect (Runs when activeTab changes without refetching hierarchy - Item 6)
  useEffect(() => {
    async function loadContentForTab() {
      if (!activeTab || segments.length < 6) return;

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
        setStatusCode(200);
      } catch (err: any) {
        const msg = err.message || '';
        let code = 500;
        if (msg.includes('400') || msg.includes('INVALID')) code = 400;
        else if (msg.includes('404') || msg.includes('NOT_FOUND')) code = 404;
        else if (msg.includes('409') || msg.includes('CONFLICT')) code = 409;
        else if (msg.includes('422') || msg.includes('SCHEMA')) code = 422;

        setStatusCode(code);
        setErrorMsg(msg || 'An unexpected content resolution failure occurred.');
        setContentData(null);
      } finally {
        setLoading(false);
      }
    }

    loadContentForTab();
  }, [activeTab, grade, subject, book, part, unit, chapterId, segments.length]);

  const toggleBookmark = () => {
    const bks = JSON.parse(localStorage.getItem('gurukul_canonical_bookmarks') || '[]');
    let nextBks;
    if (isBookmarked) {
      nextBks = bks.filter((key: string) => key !== canonicalIdentityKey);
      setIsBookmarked(false);
    } else {
      nextBks = [...bks, canonicalIdentityKey];
      setIsBookmarked(true);
    }
    localStorage.setItem('gurukul_canonical_bookmarks', JSON.stringify(nextBks));
  };

  const toggleNeedPractice = () => {
    const np = JSON.parse(localStorage.getItem('gurukul_canonical_need_practice') || '[]');
    let nextNp;
    if (isNeedPractice) {
      nextNp = np.filter((key: string) => key !== canonicalIdentityKey);
      setIsNeedPractice(false);
    } else {
      nextNp = [...np, canonicalIdentityKey];
      setIsNeedPractice(true);
    }
    localStorage.setItem('gurukul_canonical_need_practice', JSON.stringify(nextNp));
  };

  // WS16: Honest AI Tutor state without fake AI generation
  const askAiTutor = (action: string) => {
    setTutorOpen(true);
    setTutorResponse('🤖 AI Tutor is not available for this chapter yet. Please refer to authoritative NCERT Notes and Overview tabs.');
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 p-6 sm:p-10 space-y-8">
      {/* Top Identity Header */}
      <div className="max-w-6xl mx-auto bg-gradient-to-r from-indigo-950 via-indigo-900 to-slate-900 text-white p-6 sm:p-8 rounded-3xl shadow-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex flex-wrap items-center gap-2 text-xs font-mono uppercase text-indigo-300">
            <span>Class {grade}</span> / <span>{subject}</span> / <span>Book: {book}</span> / <span>Part: {part}</span> / <span>Unit: {unit}</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={toggleBookmark}
              className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all border ${
                isBookmarked ? 'bg-amber-500 text-white border-amber-600' : 'bg-white/10 text-white border-white/20 hover:bg-white/20'
              }`}
            >
              {isBookmarked ? '★ Bookmarked' : '☆ Bookmark'}
            </button>
            <button
              onClick={toggleNeedPractice}
              className={`px-3 py-1.5 rounded-xl text-xs font-extrabold transition-all border ${
                isNeedPractice ? 'bg-rose-500 text-white border-rose-600' : 'bg-white/10 text-white border-white/20 hover:bg-white/20'
              }`}
            >
              {isNeedPractice ? '🔍 Need Practice' : '🔍 Mark for Practice'}
            </button>
          </div>
        </div>
        <h1 className="text-2xl sm:text-3xl font-black tracking-tight">Chapter: {chapterId}</h1>

        {/* AI Tutor Entry Points (WS16) */}
        <div className="flex flex-wrap items-center gap-2 pt-2 border-t border-indigo-800/60">
          <span className="text-xs font-bold text-indigo-200">🤖 AI Tutor:</span>
          <button onClick={() => askAiTutor('explain')} className="px-3 py-1 rounded-lg bg-indigo-800/80 hover:bg-indigo-700 text-xs font-bold transition-all text-indigo-100">
            Explain Simply
          </button>
          <button onClick={() => askAiTutor('example')} className="px-3 py-1 rounded-lg bg-indigo-800/80 hover:bg-indigo-700 text-xs font-bold transition-all text-indigo-100">
            Give an Example
          </button>
          <button onClick={() => askAiTutor('quiz')} className="px-3 py-1 rounded-lg bg-indigo-800/80 hover:bg-indigo-700 text-xs font-bold transition-all text-indigo-100">
            Quiz Me
          </button>
          <button onClick={() => askAiTutor('help')} className="px-3 py-1 rounded-lg bg-indigo-800/80 hover:bg-indigo-700 text-xs font-bold transition-all text-indigo-100">
            I Don&apos;t Understand
          </button>
        </div>

        {tutorOpen && (
          <div className="bg-indigo-950/90 border border-indigo-700/60 p-4 rounded-2xl text-sm text-indigo-100 relative mt-3 space-y-2">
            <button onClick={() => setTutorOpen(false)} className="absolute top-3 right-3 text-indigo-400 hover:text-white font-bold text-xs">✕ Close</button>
            <p className="font-medium">{tutorResponse}</p>
          </div>
        )}
      </div>

      {/* Authoritative Content-Type Tabs Bar */}
      {availableContentTypes.length > 0 && (
        <div className="max-w-6xl mx-auto flex flex-wrap gap-2 bg-white p-3 rounded-2xl border border-slate-200 shadow-sm">
          {availableContentTypes.map(ct => (
            <button
              key={ct}
              onClick={() => setActiveTab(ct)}
              className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all ${
                activeTab === ct
                  ? 'bg-indigo-600 text-white shadow-md'
                  : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              {CONTENT_TYPE_LABELS[ct] || ct}
            </button>
          ))}
        </div>
      )}

      {/* Main Content Area */}
      <div className="max-w-6xl mx-auto">
        {loading && (
          <div className="p-16 text-center text-slate-500 bg-white rounded-3xl border border-slate-200 shadow-sm">
            <div className="animate-spin w-8 h-8 border-4 border-indigo-600 border-t-transparent rounded-full mx-auto mb-4"></div>
            <p className="text-sm font-bold">Resolving authoritative curriculum identity...</p>
          </div>
        )}

        {statusCode && statusCode !== 200 && !loading && (
          <div className="p-12 bg-rose-50 border border-rose-200 rounded-3xl text-center space-y-3 shadow-sm">
            <h3 className="text-lg font-black text-rose-900">
              {statusCode === 400 && 'Bad Request: Invalid Curriculum Identity (400)'}
              {statusCode === 404 && 'Curriculum Identity Not Found (404)'}
              {statusCode === 409 && 'Identity Conflict (409)'}
              {statusCode === 422 && 'Content Schema Corruption (422)'}
              {statusCode === 500 && 'Internal Server Error (500)'}
            </h3>
            <p className="text-sm text-rose-700 max-w-md mx-auto">{errorMsg}</p>
            <Link href="/" className="inline-block mt-4 px-6 py-2.5 bg-indigo-600 text-white text-xs font-bold rounded-xl shadow-md hover:bg-indigo-500 transition-all">
              Return to Curriculum Explorer ↻
            </Link>
          </div>
        )}

        {statusCode === 200 && !loading && contentData && (
          <div className="bg-white rounded-3xl border border-slate-200 shadow-sm p-6 sm:p-8">
            {RendererRegistry.resolve({
              grade,
              subject,
              book,
              part,
              contentType: activeTab,
              data: contentData
            })}
          </div>
        )}
      </div>
    </div>
  );
}
