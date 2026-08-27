'use client';

import React, { useState, useEffect, useMemo } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import Breadcrumbs from '@/components/Breadcrumbs';
import { getChapterDisplayData } from '@/utils/chapter';
import { Search as SearchIcon, ChevronRight, Loader2 } from 'lucide-react';
import Link from 'next/link';
import { chapterService } from '@/services/api';

export default function SearchPage() {
  const [query, setQuery] = useState('');
  const [hierarchy, setHierarchy] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchHierarchy = async () => {
      try {
        const h = await chapterService.getHierarchy();
        setHierarchy(h);
      } catch (e) {
        console.error("Failed to fetch hierarchy", e);
      } finally {
        setLoading(false);
      }
    };
    fetchHierarchy();
  }, []);

  const results = useMemo(() => {
    if (!hierarchy || !query || query.length < 2) return [];

    const allResults: any[] = [];
    const q = query.toLowerCase();

    Object.entries(hierarchy).forEach(([className, subjects]: [string, any]) => {
      Object.entries(subjects).forEach(([subject, chapters]: [string, any]) => {
        chapters.forEach((chap: any) => {
          if (
            chap.name.toLowerCase().includes(q) ||
            subject.toLowerCase().includes(q) ||
            chap.id.toLowerCase().includes(q)
          ) {
            allResults.push({
              ...chap,
              subject,
              className
            });
          }
        });
      });
    });

    return allResults.slice(0, 20); // Limit results
  }, [hierarchy, query]);

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="Discovery Engine" />

        <div className="max-w-4xl mx-auto p-10">
          <Breadcrumbs items={[{ label: 'Discovery', href: '#' }]} />

          <div className="space-y-12">
            <section className="bg-white border border-border rounded-[40px] p-2 shadow-xl flex items-center pr-6">
              <div className="w-16 h-16 flex items-center justify-center text-slate-400">
                {loading ? <Loader2 className="animate-spin" size={24} /> : <SearchIcon size={24} />}
              </div>
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for chapters, topics, or AI content..."
                className="flex-1 bg-transparent border-none focus:outline-none text-xl font-bold text-slate-800 placeholder:text-slate-200"
              />
              {query && (
                <button
                  onClick={() => setQuery('')}
                  className="px-4 py-2 bg-slate-100 text-slate-400 rounded-xl font-bold text-xs uppercase hover:bg-slate-200 transition-all"
                >
                  Clear
                </button>
              )}
            </section>

            <div className="space-y-6">
              <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest px-4">
                {query ? `${results.length} results for "${query}"` : "Search Results"}
              </h3>

              {!query ? (
                <div className="py-20 text-center space-y-4 opacity-30 grayscale">
                  <SearchIcon size={64} className="mx-auto" />
                  <p className="font-bold uppercase tracking-widest text-[10px]">Type to begin searching the NCERT index</p>
                </div>
              ) : results.length > 0 ? (
                <div className="space-y-3">
                  {results.map((res) => (
                    <ResultItem
                      key={res.id}
                      title={res.name}
                      subject={res.subject}
                      classLevel={res.className.split('_').pop()}
                      id={res.id}
                      className={res.className}
                    />
                  ))}
                </div>
              ) : (
                <div className="py-20 text-center space-y-4 opacity-30 grayscale">
                  <p className="font-bold uppercase tracking-widest text-[10px]">No matching chapters found in Class {hierarchy ? Object.keys(hierarchy)[0]?.split('_').pop() : '?'}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function ResultItem({ title, subject, classLevel, id, className }: any) {
  const displayData = getChapterDisplayData(id);
  const safeSubject = subject.toLowerCase().replace(' ', '_');

  return (
    <Link
      href={`/library/${className}/${safeSubject}/${id}`}
      className="p-6 bg-white border border-border rounded-3xl hover:border-primary/40 hover:shadow-lg transition-all flex items-center justify-between group"
    >
      <div className="flex items-center gap-6">
        <div className="w-12 h-12 bg-blue-50 text-primary rounded-2xl flex items-center justify-center font-black">
          {displayData.number || '?'}
        </div>
        <div>
          <h4 className="font-black text-slate-800 text-lg capitalize">{title}</h4>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{subject} • Class {classLevel} • Chapter {displayData.number || '?'}</p>
        </div>
      </div>
      <ChevronRight className="text-slate-200 group-hover:text-primary transition-all" size={20} />
    </Link>
  );
}
