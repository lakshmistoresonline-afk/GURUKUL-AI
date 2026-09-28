'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { ReadingComfortControl, ReadingTheme, TextSize, LineSpacing } from '../../../../components/ReadingComfortControl';
import AudioReaderToolbar from '../../../../components/AudioReaderToolbar';
import OverviewComponent from '../../../../components/presentation/OverviewComponent';
import NotesComponent from '../../../../components/presentation/NotesComponent';
import MasterComponent from '../../../../components/presentation/MasterComponent';
import MindmapComponent from '../../../../components/presentation/MindmapComponent';
import QuestionPapersComponent from '../../../../components/presentation/QuestionPapersComponent';
import QuizComponent from '../../../../components/presentation/QuizComponent';
import FlashcardsComponent from '../../../../components/presentation/FlashcardsComponent';
import Class6MasterComponent from '../../../../components/presentation/Class6/Class6MasterComponent';
import Class6HindiMasterComponent from '../../../../components/presentation/Class6/Class6HindiMasterComponent';
import Class6HindiNotesComponent from '../../../../components/presentation/Class6/Class6HindiNotesComponent';
import Class6MathsMasterComponent from '../../../../components/presentation/Class6/Class6MathsMasterComponent';
import Class6MathsNotesComponent from '../../../../components/presentation/Class6/Class6MathsNotesComponent';
import Class6ScienceMasterComponent from '../../../../components/presentation/Class6/Class6ScienceMasterComponent';
import Class6SocialMasterComponent from '../../../../components/presentation/Class6/Class6SocialMasterComponent';
import Class6SocialNotesComponent from '../../../../components/presentation/Class6/Class6SocialNotesComponent';
import Class6SocialFlashcardsComponent from '../../../../components/presentation/Class6/Class6SocialFlashcardsComponent';
import Class6SocialMindmapComponent from '../../../../components/presentation/Class6/Class6SocialMindmapComponent';
import Class7UniversalNotesComponent from '../../../../components/presentation/Class7/Class7UniversalNotesComponent';
import Class7UniversalMasterComponent from '../../../../components/presentation/Class7/Class7UniversalMasterComponent';
import Class6MindmapComponent from '../../../../components/presentation/Class6/Class6MindmapComponent';
import Class6HindiMindmapComponent from '../../../../components/presentation/Class6/Class6HindiMindmapComponent';
import Class6MathsMindmapComponent from '../../../../components/presentation/Class6/Class6MathsMindmapComponent';
import Class6ScienceMindmapComponent from '../../../../components/presentation/Class6/Class6ScienceMindmapComponent';

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
  { id: 'overview', label: 'Overview', icon: '📖' },
  { id: 'notes', label: 'Notes', icon: '📝' },
  { id: 'master', label: 'Master Practice', icon: '⚡' },
  { id: 'flashcards', label: 'Flashcards', icon: '🃏' },
  { id: 'mindmaps', label: 'Mindmaps', icon: '🧠' },
  { id: 'quiz', label: 'Quiz', icon: '✍️' },
  { id: 'question_papers', label: 'Question Papers', icon: '📋' },
];

export default function ChapterClient({ grade, subject, chapterId }: ChapterClientProps) {
  const [sourceData, setSourceData] = useState<ChapterSourceData | null>(null);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [loading, setLoading] = useState<boolean>(true);
  const [apiError, setApiError] = useState<ApiDiagnostics | null>(null);
  const [completedTabs, setCompletedTabs] = useState<Record<string, boolean>>({ overview: true });
  const [isMobileTocOpen, setIsMobileTocOpen] = useState<boolean>(false);
  const [isZenMode, setIsZenMode] = useState<boolean>(false);

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

          try {
            const recent = JSON.parse(localStorage.getItem('gurukul_recent_chapters') || '[]');
            const newEntry = { id: chapterId, title: data.chapterTitle, grade, subject, timestamp: Date.now() };
            const filtered = recent.filter((r: any) => r.id !== chapterId);
            localStorage.setItem('gurukul_recent_chapters', JSON.stringify([newEntry, ...filtered].slice(0, 5)));
          } catch {}
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
    const saved = localStorage.getItem(`gurukul_progress_${chapterId}`);
    if (saved) {
      try {
        setCompletedTabs(JSON.parse(saved));
      } catch {}
    } else {
      const initial = { overview: true };
      setCompletedTabs(initial);
      localStorage.setItem(`gurukul_progress_${chapterId}`, JSON.stringify(initial));
    }
  }, [grade, subject, chapterId]);

  const handleTabClick = (tabId: string) => {
    setActiveTab(tabId);
    const updated = { ...completedTabs, [tabId]: true };
    setCompletedTabs(updated);
    localStorage.setItem(`gurukul_progress_${chapterId}`, JSON.stringify(updated));
    setIsMobileTocOpen(false);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F8FAFC] text-slate-600">
        <div className="animate-spin w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full mr-3" />
        <span className="font-semibold">Loading World-Class Workspace...</span>
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

  // Extract text to read from active section data for TTS
  const getActiveTextToRead = () => {
    if (!sourceData) return '';
    const { sections } = sourceData;
    let targetData = null;
    if (activeTab === 'overview') targetData = sections.overview;
    if (activeTab === 'notes') targetData = sections.notes;
    if (activeTab === 'master') targetData = sections.master;
    if (!targetData) return '';
    return JSON.stringify(targetData).replace(/[{}[\]",:]/g, ' ');
  };

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
            subject={subject}
          />
        );

      case 'question_papers':
        return <QuestionPapersComponent data={sections.question_papers} />;

      case 'notes':
        if (grade === '7') {
          return <Class7UniversalNotesComponent data={sections.notes} />;
        }
        if (grade === '6') {
          if (subject === 'Hindi') return <Class6HindiNotesComponent data={sections.notes} />;
          if (subject === 'Maths') return <Class6MathsNotesComponent data={sections.notes} />;
          if (subject === 'Social') return <Class6SocialNotesComponent data={sections.notes} />;
        }
        return <NotesComponent data={sections.notes} subject={subject} />;

      case 'master':
        if (grade === '7') {
          return <Class7UniversalMasterComponent data={sections.master} />;
        }
        if (grade === '6') {
          if (subject === 'English') return <Class6MasterComponent data={sections.master} />;
          if (subject === 'Hindi') return <Class6HindiMasterComponent data={sections.master} />;
          if (subject === 'Maths') return <Class6MathsMasterComponent data={sections.master} />;
          if (subject === 'Science') return <Class6ScienceMasterComponent data={sections.master} />;
          if (subject === 'Social') return <Class6SocialMasterComponent data={sections.master} />;
        }
        return <MasterComponent data={sections.master} subject={subject} />;

      case 'flashcards':
        if (grade === '6' && subject === 'Social') {
          return <Class6SocialFlashcardsComponent flashcards={sections.flashcards} />;
        }
        return <FlashcardsComponent flashcards={sections.flashcards} />;

      case 'mindmaps':
        if (grade === '6') {
          if (subject === 'Hindi') return <Class6HindiMindmapComponent data={sections.mindmaps} />;
          if (subject === 'Maths') return <Class6MathsMindmapComponent data={sections.mindmaps} />;
          if (subject === 'Science') return <Class6ScienceMindmapComponent data={sections.mindmaps} />;
          if (subject === 'Social') return <Class6SocialMindmapComponent data={sections.mindmaps} />;
          return <Class6MindmapComponent data={sections.mindmaps} />;
        }
        return <MindmapComponent data={sections.mindmaps} />;

      case 'quiz':
        return <QuizComponent quiz={sections.quiz} />;

      default:
        return <p className="text-sm text-slate-500">Select a section above.</p>;
    }
  };

  return (
    <div className={`min-h-screen ${themeBgClass} transition-colors duration-300 selection:bg-indigo-500 selection:text-white`}>
      <div className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 py-8 md:py-10 space-y-8">
        {/* Top Glassmorphic Navigation Bar */}
        {!isZenMode && (
          <div className="relative z-50 flex flex-wrap items-center justify-between gap-4 border-b border-slate-200/80 pb-6 backdrop-blur-md">
            <div className="flex items-center gap-3 text-xs font-bold uppercase tracking-wider opacity-70">
              <Link href="/" className="hover:text-indigo-600 transition-colors">
                Dashboard
              </Link>
              <span>/</span>
              <span>Class {grade}</span>
              <span>/</span>
              <span>{subject}</span>
            </div>

            <div className="flex items-center gap-4">
              <button
                onClick={() => setIsZenMode(true)}
                className="px-3 py-1.5 bg-teal-600 hover:bg-teal-500 text-white rounded-xl text-xs font-bold shadow-xs transition-all"
                title="Zen Focus Mode"
              >
                🧘 Focus Mode
              </button>
              <button
                onClick={() => setIsMobileTocOpen(!isMobileTocOpen)}
                className="lg:hidden px-3 py-1.5 bg-indigo-600 text-white rounded-xl text-xs font-bold"
              >
                ☰ Navigation
              </button>
              <ReadingComfortControl
                theme={readingTheme}
                textSize={textSize}
                lineSpacing={lineSpacing}
                onThemeChange={setReadingTheme}
                onTextSizeChange={setTextSize}
                onLineSpacingChange={setLineSpacing}
              />
            </div>
          </div>
        )}

        {isZenMode && (
          <div className="flex justify-end pb-2">
            <button
              onClick={() => setIsZenMode(false)}
              className="px-4 py-2 bg-slate-900 text-white rounded-2xl text-xs font-bold shadow-lg"
            >
              ✕ Exit Focus Mode
            </button>
          </div>
        )}

        {!isZenMode && (
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
        )}

        {/* Global Audio Assistant Toolbar (Placed cleanly below chapter header, above grid) */}
        <AudioReaderToolbar textToRead={getActiveTextToRead()} subject={subject} />

        {/* Master-Detail Split Workspace */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start relative">
          {/* Sticky Left Sidebar TOC (Desktop + Mobile Drawer) */}
          {!isZenMode && (
            <aside className={`lg:col-span-3 lg:sticky lg:top-8 space-y-3 bg-white p-5 rounded-3xl border border-slate-200/80 shadow-sm z-30 ${isMobileTocOpen ? 'block' : 'hidden lg:block'}`}>
              <div className="flex items-center justify-between border-b border-slate-100 pb-1">
                <div className="text-xs font-black uppercase tracking-widest text-slate-400 px-2">
                  Chapter Navigation
                </div>
                <button onClick={() => setIsMobileTocOpen(false)} className="lg:hidden text-slate-400 font-bold text-xs">✕</button>
              </div>
              <nav className="space-y-1.5" aria-label="Chapter Workspace Navigation">
                {FIXED_TABS.map((tab) => {
                  const isActive = activeTab === tab.id;
                  const isDone = completedTabs[tab.id];
                  return (
                    <button
                      key={tab.id}
                      onClick={() => handleTabClick(tab.id)}
                      className={`w-full text-left px-4 py-3 rounded-2xl text-xs sm:text-sm font-bold transition-all flex items-center justify-between group ${
                        isActive
                          ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                          : 'bg-slate-50/70 text-slate-700 hover:bg-slate-100 hover:text-slate-900 border border-slate-100'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <span>{tab.icon}</span>
                        <span>{tab.label}</span>
                      </div>
                      {isDone && !isActive && <span className="text-emerald-600 font-black text-xs">✓</span>}
                    </button>
                  );
                })}
              </nav>
            </aside>
          )}

          {/* Right Main Reading Canvas */}
          <main className={`${isZenMode ? 'lg:col-span-12 max-w-4xl mx-auto' : 'lg:col-span-9'} space-y-8 min-h-[500px] ${textSizeClass} ${lineSpacingClass}`}>
            {renderActiveSectionContent()}
          </main>
        </div>
      </div>
    </div>
  );
}
