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
  const [activeTab, setActiveTab] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);
  const [apiError, setApiError] = useState<ApiDiagnostics | null>(null);

  // Reading Comfort Controls State (Default: Light Theme matching Dashboard)
  const [readingTheme, setReadingTheme] = useState<ReadingTheme>('light');
  const [textSize, setTextSize] = useState<TextSize>('medium');
  const [lineSpacing, setLineSpacing] = useState<LineSpacing>('normal');

  useEffect(() => {
    async function loadChapterData() {
      try {
        setLoading(true);
        setApiError(null);

        // Standardize primary backend URL to port 8080 (FastAPI main.py port)
        const primaryUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
        const fallbackUrl = 'http://127.0.0.1:8080';

        let targetUrl = primaryUrl;

        // Diagnostic fetch with fallback port verification
        let contentRes: Response | null = null;
        let chapterRes: Response | null = null;
        let manifestRes: Response | null = null;
        let navRes: Response | null = null;

        try {
          [chapterRes, manifestRes, navRes, contentRes] = await Promise.all([
            fetch(`${targetUrl}/api/v1/chapters/${chapterId}?grade=${grade}&subject=${subject}`),
            fetch(`${targetUrl}/api/v1/chapters/${chapterId}/manifest?grade=${grade}&subject=${subject}`),
            fetch(`${targetUrl}/api/v1/chapters/${chapterId}/navigation?grade=${grade}&subject=${subject}`),
            fetch(`${targetUrl}/api/v1/chapters/${chapterId}/content?grade=${grade}&subject=${subject}`),
          ]);
        } catch {
          targetUrl = fallbackUrl;
          try {
            [chapterRes, manifestRes, navRes, contentRes] = await Promise.all([
              fetch(`${targetUrl}/api/v1/chapters/${chapterId}?grade=${grade}&subject=${subject}`),
              fetch(`${targetUrl}/api/v1/chapters/${chapterId}/manifest?grade=${grade}&subject=${subject}`),
              fetch(`${targetUrl}/api/v1/chapters/${chapterId}/navigation?grade=${grade}&subject=${subject}`),
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

          let computedTabs: NavigationTab[] = [];
          if (navRes && navRes.ok) {
            const navData = await navRes.json();
            computedTabs = navData.tabs || [];
          }

          if (computedTabs.length === 0) {
            computedTabs = NavigationBuilder.buildNavigation(subject, manifestData);
          }

          setTabs(computedTabs);
          if (computedTabs.length > 0) {
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

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-[#F8FAFC] text-slate-600">
        <div className="animate-spin w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full mr-3" />
        <span className="font-semibold">Loading Chapter Content...</span>
      </div>
    );
  }

  // Explicit API Error Diagnostic Card
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

          <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl text-left text-xs text-indigo-800 space-y-1">
            <div className="font-bold text-indigo-900">Troubleshooting Steps:</div>
            <div>1. Ensure the Python FastAPI server is running: <code className="bg-white px-1.5 py-0.5 rounded text-indigo-700 font-mono border border-indigo-200">python backend/src/main.py</code></div>
            <div>2. Verify the server is listening on port <code className="bg-white px-1.5 py-0.5 rounded text-indigo-700 font-mono border border-indigo-200">http://localhost:8080</code>.</div>
          </div>

          <button
            onClick={() => window.location.reload()}
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-2xl shadow-lg shadow-indigo-600/20 transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
          >
            Retry Connection ↻
          </button>
        </div>
      </div>
    );
  }

  const currentTabObj = tabs.find((t) => t.id === activeTab);
  const activeTypes = currentTabObj ? currentTabObj.contentTypes : [];
  const activeBlocks = blocks.filter(
    (b) => activeTypes.includes(b.sourceType) || activeTypes.includes(b.normalizedType) || activeTypes.includes(b.renderer)
  );

  const blockTitle = blocks.find((b) => b.data?.chapterTitle || b.data?.title)?.data?.chapterTitle || blocks.find((b) => b.data?.chapterTitle || b.data?.title)?.data?.title;

  const displayTitle =
    chapterDetails?.chapterTitle ||
    chapterDetails?.title ||
    blockTitle ||
    (subject === 'Hindi' ? 'किरन' : subject === 'Maths' ? 'Travelling, Now and Then' : subject === 'Science' ? 'Water — The Essence of Life' : 'Papa’s Spectacles');

  const unitTitle = chapterDetails?.unitTitle || 'Let’s Have Fun';
  const chNumber = chapterDetails?.chapterNumber || 1;

  // Compute Reading Comfort Styles (Default: Option C Soft Blue / Cloud White Light Theme)
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
        {/* Top Header Bar with Breadcrumb & Reading Comfort Control */}
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

        {/* Chapter Title Banner (LINE 1: Retained Metadata | LINE 2: REAL CHAPTER NAME | LINE 3: Retained Canonical ID) */}
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

        {/* Unified 5-Stage Navigation Tabs Bar */}
        {tabs.length > 0 && (
          <nav className="flex flex-wrap gap-2 border-b border-slate-200/80 pb-4" aria-label="Chapter Primary Navigation">
            {tabs.map((tab) => {
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-6 py-2.5 rounded-2xl text-sm font-extrabold transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 ${
                    isActive
                      ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-600/30 border border-indigo-500'
                      : 'bg-white text-slate-600 hover:text-slate-900 hover:bg-slate-100 border border-slate-200'
                  }`}
                  aria-selected={isActive}
                  role="tab"
                >
                  {tab.label || tab.id}
                </button>
              );
            })}
          </nav>
        )}

        {/* Active Stage Content Blocks Area with Reading Width Constraint */}
        <main className={`space-y-8 min-h-[400px] ${textSizeClass} ${lineSpacingClass}`}>
          {activeBlocks.length > 0 ? (
            activeBlocks.map((block) => {
              const RendererComponent = RendererRegistry.getRenderer(block.renderer);
              return (
                <section key={block.id} className="space-y-4">
                  <RendererComponent data={block.data} title={block.title} />
                </section>
              );
            })
          ) : (
            <div className="p-12 text-center text-slate-500 bg-white rounded-3xl border border-slate-200 space-y-2 shadow-sm">
              <p className="text-base font-semibold text-slate-700">No content available for this section.</p>
              <p className="text-xs text-slate-500">This learning stage contains no items for this chapter.</p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
