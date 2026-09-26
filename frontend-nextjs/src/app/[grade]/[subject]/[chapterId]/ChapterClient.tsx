'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { ReadingComfortControl, ReadingTheme, TextSize, LineSpacing } from '../../../../components/ReadingComfortControl';
import OverviewComponent from '../../../../components/presentation/OverviewComponent';
import NotesComponent from '../../../../components/presentation/NotesComponent';
import MasterComponent from '../../../../components/presentation/MasterComponent';
import MindmapComponent from '../../../../components/presentation/MindmapComponent';
import QuestionPapersComponent from '../../../../components/presentation/QuestionPapersComponent';
import QuizComponent from '../../../../components/presentation/QuizComponent';
import FlashcardsComponent from '../../../../components/presentation/FlashcardsComponent';

interface ChapterSourceData {
  chapterId: string;
  grade: string;
  subject: string;
  chapterNumber: number;
  chapterTitle: string;
  unitTitle: string;
  sections: {
    overview: any | null;
    notes: any;
    master: any;
    flashcards: any[];
    mindmaps: any;
    quiz: any[];
    question_papers: any | null;
  };
}

interface ChapterClientProps {
  grade: string;
  subject: string;
  chapterId: string;
}

interface ApiDiagnostics {
  endpoint: string;
  status?: number;
  error: string;
}

const FIXED_TABS = [
  { id: 'overview', label: 'Overview' },
  { id: 'notes', label: 'Notes' },
  { id: 'master', label: 'Master' },
  { id: 'flashcards', label: 'Flashcards' },
  { id: 'mindmaps', label: 'Mindmaps' },
  { id: 'quiz', label: 'Quiz' },
  { id: 'question_papers', label: 'Question Papers' },
];

export default function ChapterClient({ grade, subject, chapterId }: ChapterClientProps) {
  const [sourceData, setSourceData] = useState<ChapterSourceData | null>(null);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [loading, setLoading] = useState<boolean>(true);
  const [apiError, setApiError] = useState<ApiDiagnostics | null>(null);

  const [readingTheme, setReadingTheme] = useState<ReadingTheme>('light');
  const [textSize, setTextSize] = useState<TextSize>('medium');
  const [lineSpacing, setLineSpacing] = useState<LineSpacing>('normal');

  useEffect(() => {
    async function loadChapterSource() {
      try {
        setLoading(true);
        setApiError(null);

        const primaryUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
        const fallbackUrl = 'http://127.0.0.1:8080';
        const endpoint = `${primaryUrl}/api/v1/chapters/${chapterId}/source?grade=${grade}&subject=${subject}`;

        let res: Response;
        try {
          res = await fetch(endpoint);
        } catch {
          res = await fetch(`${fallbackUrl}/api/v1/chapters/${chapterId}/source?grade=${grade}&subject=${subject}`);
        }

        if (res.ok) {
          const data: ChapterSourceData = await res.json();
          setSourceData(data);
        } else {
          setApiError({
            endpoint,
            status: res.status,
            error: `API returned HTTP ${res.status}: ${res.statusText}`,
          });
        }
      } catch (err: any) {
        console.error('Failed to load direct chapter source:', err);
        setApiError({
          endpoint: `http://localhost:8080/api/v1/chapters/${chapterId}/source`,
          error: err.message || 'TypeError: Failed to fetch',
        });
      } finally {
        setLoading(false);
      }
    }

    loadChapterSource();
  }, [grade, subject, chapterId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F8FAFC] text-slate-600">
        <div className="animate-spin w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full mr-3" />
        <span className="font-semibold">Loading Educational Experience...</span>
      </div>
    );
  }

  if (apiError) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] text-slate-900 p-6 md:p-12 max-w-4xl mx-auto flex flex-col justify-center items-center text-center space-y-6">
        <div className="p-8 bg-white border border-red-200 rounded-3xl space-y-4 shadow-xl max-w-xl w-full">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-red-50 border border-red-200 text-red-700 text-xs font-bold uppercase tracking-wider">
            <span>Content Service Unavailable</span>
          </div>
          <h2 className="text-2xl font-black text-slate-900 tracking-tight">
            Backend API Connection Error
          </h2>
          <p className="text-slate-600 text-sm leading-relaxed">
            The frontend could not reach the FastAPI persistent processed source endpoint.
          </p>
          <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl text-left space-y-2 font-mono text-xs text-red-600">
            <div><strong className="text-slate-500">Endpoint:</strong> {apiError.endpoint}</div>
            {apiError.status && <div><strong className="text-slate-500">Status:</strong> {apiError.status}</div>}
            <div><strong className="text-slate-500">Error:</strong> {apiError.error}</div>
          </div>
          <button
            onClick={() => window.location.reload()}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-2xl shadow-lg shadow-indigo-600/20 transition-all"
          >
            Retry Connection ↻
          </button>
        </div>
      </div>
    );
  }

  const displayTitle = sourceData?.chapterTitle || 'Chapter Information Unavailable';
  const unitTitle = sourceData?.unitTitle || 'Curriculum Unit';
  const chNumber = sourceData?.chapterNumber || 1;

  const themeBgClass =
    readingTheme === 'dark'
      ? 'bg-slate-950 text-slate-100'
      : readingTheme === 'warm'
      ? 'bg-[#FFFBEB] text-[#1C1917]'
      : 'bg-[#F8FAFC] text-[#0F172A]';

  const textSizeClass =
    textSize === 'large' ? 'text-lg' : textSize === 'xlarge' ? 'text-xl' : 'text-base';

  const lineSpacingClass =
    lineSpacing === 'comfortable' ? 'leading-loose' : lineSpacing === 'spacious' ? 'leading-[2.2]' : 'leading-relaxed';

  // Render Section Content based on activeTab with Purpose-Built UI Components
  const renderActiveSectionContent = () => {
    if (!sourceData) return null;
    const { sections } = sourceData;

    switch (activeTab) {
      case 'overview':
        return (
          <OverviewComponent
            data={sections.overview}
            chapterTitle={displayTitle}
            unitTitle={unitTitle}
          />
        );

      case 'question_papers':
        return <QuestionPapersComponent data={sections.question_papers} />;

      case 'notes':
        return <NotesComponent data={sections.notes} subject={subject} />;

      case 'master':
        return <MasterComponent data={sections.master} subject={subject} />;

      case 'flashcards':
        return <FlashcardsComponent flashcards={sections.flashcards} />;

      case 'mindmaps':
        return <MindmapComponent data={sections.mindmaps} />;

      case 'quiz':
        return <QuizComponent quiz={sections.quiz} />;

      default:
        return <p className="text-sm text-slate-500">Select a section above.</p>;
    }
  };

  return (
    <div className={`min-h-screen ${themeBgClass} transition-colors duration-300 selection:bg-indigo-500 selection:text-white`}>
      <div className="mx-auto w-full max-w-6xl px-4 sm:px-6 lg:px-8 py-8 md:py-12 space-y-8">
        <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-200/80 pb-6">
          <div className="flex items-center gap-3 text-xs font-bold uppercase tracking-wider opacity-70">
            <Link href="/" className="hover:text-indigo-600 transition-colors">
              Dashboard
            </Link>
            <span>/</span>
            <span>Class {grade}</span>
            <span>/</span>
            <span>{subject}</span>
          </div>

          <ReadingComfortControl
            theme={readingTheme}
            textSize={textSize}
            lineSpacing={lineSpacing}
            onThemeChange={setReadingTheme}
            onTextSizeChange={setTextSize}
            onLineSpacingChange={setLineSpacing}
          />
        </div>

        <header className="space-y-2 border-b border-slate-200/80 pb-6">
          <div className="text-xs font-black tracking-widest text-indigo-600 uppercase">
            {subject} • {unitTitle} • Chapter {chNumber}
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight">
            {displayTitle}
          </h1>
          <div className="text-xs font-mono opacity-50">
            Canonical ID: {chapterId}
          </div>
        </header>

        {/* Exactly 7 Fixed Tabs Navigation Bar */}
        <nav className="flex flex-wrap gap-2 border-b border-slate-200/80 pb-4" aria-label="Chapter Primary Navigation">
          {FIXED_TABS.map((tab) => {
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-5 py-2.5 rounded-2xl text-xs sm:text-sm font-extrabold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30 border border-indigo-500'
                    : 'bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200'
                }`}
                aria-selected={isActive}
                role="tab"
              >
                {tab.label}
              </button>
            );
          })}
        </nav>

        <main className={`space-y-8 min-h-[400px] ${textSizeClass} ${lineSpacingClass}`}>
          {renderActiveSectionContent()}
        </main>
      </div>
    </div>
  );
}
