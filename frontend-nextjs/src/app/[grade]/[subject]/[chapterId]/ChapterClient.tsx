'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { NavigationBuilder, NavigationTab, ContentManifest } from '../../../../navigation/NavigationBuilder';
import { RendererRegistry } from '../../../../renderers/RendererRegistry';
import { ReadingComfortControl, ReadingTheme, TextSize, LineSpacing } from '../../../../components/ReadingComfortControl';

interface ContentBlockData {
  id: string;
  sourceType: string;
  normalizedType: string;
  type?: string;
  title: string;
  data: any;
  renderer: string;
  order: number;
}

interface ChapterMetadata {
  chapterId: string;
  title?: string;
  chapterTitle?: string;
  unitTitle?: string;
  unitNumber?: number;
  chapterNumber?: number;
  blockCount?: number;
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

export default function ChapterClient({ grade, subject, chapterId }: ChapterClientProps) {
  const [chapterDetails, setChapterDetails] = useState<ChapterMetadata | null>(null);
  const [manifest, setManifest] = useState<ContentManifest | null>(null);
  const [blocks, setBlocks] = useState<ContentBlockData[]>([]);
  const [tabs, setTabs] = useState<NavigationTab[]>([]);
  const [activeTab, setActiveTab] = useState<string>('overview');
  const [loading, setLoading] = useState<boolean>(true);
  const [apiError, setApiError] = useState<ApiDiagnostics | null>(null);

  const [readingTheme, setReadingTheme] = useState<ReadingTheme>('light');
  const [textSize, setTextSize] = useState<TextSize>('medium');
  const [lineSpacing, setLineSpacing] = useState<LineSpacing>('normal');

  useEffect(() => {
    async function loadChapterData() {
      try {
        setLoading(true);
        setApiError(null);

        const primaryUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
        const fallbackUrl = 'http://127.0.0.1:8080';

        let targetUrl = primaryUrl;
        let contentRes: Response | null = null;
        let chapterRes: Response | null = null;
        let manifestRes: Response | null = null;

        try {
          [chapterRes, manifestRes, contentRes] = await Promise.all([
            fetch(`${targetUrl}/api/v1/chapters/${chapterId}?grade=${grade}&subject=${subject}`),
            fetch(`${targetUrl}/api/v1/chapters/${chapterId}/manifest?grade=${grade}&subject=${subject}`),
            fetch(`${targetUrl}/api/v1/chapters/${chapterId}/content?grade=${grade}&subject=${subject}`),
          ]);
        } catch {
          targetUrl = fallbackUrl;
          try {
            [chapterRes, manifestRes, contentRes] = await Promise.all([
              fetch(`${targetUrl}/api/v1/chapters/${chapterId}?grade=${grade}&subject=${subject}`),
              fetch(`${targetUrl}/api/v1/chapters/${chapterId}/manifest?grade=${grade}&subject=${subject}`),
              fetch(`${targetUrl}/api/v1/chapters/${chapterId}/content?grade=${grade}&subject=${subject}`),
            ]);
          } catch (retryErr: any) {
            setApiError({
              endpoint: `${primaryUrl}/api/v1/chapters/${chapterId}`,
              error: retryErr.message || 'TypeError: Failed to fetch (Connection Refused)',
            });
            setLoading(false);
            return;
          }
        }

        if (chapterRes && chapterRes.ok) {
          const details: ChapterMetadata = await chapterRes.json();
          setChapterDetails(details);
        }

        if (manifestRes && manifestRes.ok && contentRes && contentRes.ok) {
          const manifestData: ContentManifest = await manifestRes.json();
          const blocksData: ContentBlockData[] = await contentRes.json();

          setManifest(manifestData);
          setBlocks(blocksData);

          const computedTabs = NavigationBuilder.buildNavigation(subject, manifestData);
          setTabs(computedTabs);
          if (computedTabs.length > 0 && !computedTabs.some(t => t.id === activeTab)) {
            setActiveTab(computedTabs[0].id);
          }
        } else {
          setApiError({
            endpoint: `${targetUrl}/api/v1/chapters/${chapterId}`,
            status: contentRes?.status || 500,
            error: `API returned HTTP ${contentRes?.status || 500}: ${contentRes?.statusText || 'Internal Server Error'}`,
          });
        }
      } catch (err: any) {
        console.error('Failed to load chapter content:', err);
        setApiError({
          endpoint: `http://localhost:8080/api/v1/chapters/${chapterId}`,
          error: err.message || 'TypeError: Failed to fetch',
        });
      } finally {
        setLoading(false);
      }
    }

    loadChapterData();
  }, [grade, subject, chapterId]);

  const currentTabObj = tabs.find((t) => t.id === activeTab);
  const activeTypes = currentTabObj ? currentTabObj.contentTypes : [];
  const activeBlocks = blocks.filter(
    (b) => activeTypes.includes(b.sourceType) || activeTypes.includes(b.normalizedType) || activeTypes.includes(b.renderer) || (activeTab === 'overview' && b.normalizedType === 'overview')
  );

  // Forensic test-only render trace instrumentation (accumulating)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      if (!(window as any).__GURUKUL_RENDER_TRACE__) {
        (window as any).__GURUKUL_RENDER_TRACE__ = [];
      }
      const existing = (window as any).__GURUKUL_RENDER_TRACE__ as any[];
      activeBlocks.forEach((b, seq) => {
        const entry = {
          chapterId,
          blockId: b.id,
          sourceType: b.sourceType,
          normalizedType: b.normalizedType,
          renderer: b.renderer,
          title: b.title,
          activeTab: activeTab,
          renderSequence: seq,
          dataHash: b.data ? JSON.stringify(b.data).length : 0
        };
        if (!existing.some((ex) => ex.blockId === entry.blockId && ex.activeTab === entry.activeTab)) {
          existing.push(entry);
        }
      });
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeBlocks, chapterId]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F8FAFC] text-slate-600">
        <div className="animate-spin w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full mr-3" />
        <span className="font-semibold">Loading Chapter Content...</span>
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
            The frontend could not reach the FastAPI local engine bridge.
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

  const blockTitle = blocks.find((b) => b.data?.chapterTitle || b.data?.title)?.data?.chapterTitle || blocks.find((b) => b.data?.chapterTitle || b.data?.title)?.data?.title;

  const displayTitle =
    chapterDetails?.chapterTitle ||
    chapterDetails?.title ||
    blockTitle ||
    'Chapter Information Unavailable';

  const unitTitle = chapterDetails?.unitTitle || 'Curriculum Unit';
  const chNumber = chapterDetails?.chapterNumber || 1;

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
        {tabs.length > 0 && (
          <nav className="flex flex-wrap gap-2 border-b border-slate-200/80 pb-4" aria-label="Chapter Primary Navigation">
            {tabs.map((tab) => {
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
        )}

        <main className={`space-y-8 min-h-[400px] ${textSizeClass} ${lineSpacingClass}`}>
          {activeBlocks.length > 0 ? (
            activeBlocks.map((block) => {
              const RendererComponent = RendererRegistry.getRenderer(block.renderer);
              return (
                <section key={block.id} data-gurukul-record-id={block.id} className="space-y-4">
                  <RendererComponent data={block.data} title={block.title} />
                </section>
              );
            })
          ) : (
            <div className="p-12 text-center text-slate-600 bg-white rounded-3xl border border-slate-200 space-y-3 shadow-sm">
              <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold uppercase tracking-wider">
                <span>Section Ready</span>
              </div>
              <h3 className="text-xl font-black text-slate-900 tracking-tight">
                {activeTab === 'overview' ? 'Overview' : activeTab === 'question_papers' ? 'Question Papers' : 'Section Content'}
              </h3>
              <p className="text-slate-600 text-sm leading-relaxed max-w-md mx-auto">
                {activeTab === 'overview'
                  ? 'No overview content is available for this chapter yet. This section will automatically display the overview when the corresponding source data is added.'
                  : activeTab === 'question_papers'
                  ? 'No question papers are available for this chapter yet. Question papers will appear here when the corresponding source data is added.'
                  : 'No items are available for this section yet.'}
              </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
