'use client';

import React, { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import Breadcrumbs from '@/components/Breadcrumbs';
import { getChapterDisplayData } from '@/utils/chapter';
import { Search, ChevronRight } from 'lucide-react';
import Link from 'next/link';

export default function SearchPage() {
  const [query, setQuery] = useState('');

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="Global Search" />

        <div className="max-w-4xl mx-auto p-10">
          <Breadcrumbs items={[{ label: 'Discovery', href: '#' }]} />

          <div className="space-y-12">
            <section className="bg-white border border-border rounded-[40px] p-2 shadow-xl flex items-center pr-6">
              <div className="w-16 h-16 flex items-center justify-center text-slate-400">
                <Search size={24} />
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
              <h3 className="text-sm font-black text-slate-400 uppercase tracking-widest px-4">Search Results</h3>

              {!query ? (
                <div className="py-20 text-center space-y-4 opacity-30 grayscale">
                  <Search size={64} className="mx-auto" />
                  <p className="font-bold uppercase tracking-widest text-xs">Type to begin searching the NCERT index</p>
                </div>
              ) : (
                <div className="space-y-3">
                  <ResultItem title="Gone with the Scooter" subject="English" classLevel="5" id="eesa102" />
                  <ResultItem title="Large Numbers" subject="Mathematics" classLevel="5" id="eemm110" />
                  <ResultItem title="The Fish Tale" subject="Mathematics" classLevel="5" id="eemm101" />
                </div>
              )}
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function ResultItem({ title, subject, classLevel, id }: any) {
  const displayData = getChapterDisplayData(id);
  return (
    <Link
      href={`/library/class_${classLevel}/${subject.toLowerCase()}/__CHAPTER_class_${classLevel}_${subject.toLowerCase()}_${id}`}
      className="p-6 bg-white border border-border rounded-3xl hover:border-primary/40 hover:shadow-lg transition-all flex items-center justify-between group"
    >
      <div className="flex items-center gap-6">
        <div className="w-12 h-12 bg-blue-50 text-primary rounded-2xl flex items-center justify-center font-black">
          {displayData.number}
        </div>
        <div>
          <h4 className="font-black text-slate-800 text-lg capitalize">{title}</h4>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">{subject} • Class {classLevel} • Chapter {displayData.number}</p>
        </div>
      </div>
      <ChevronRight className="text-slate-200 group-hover:text-primary transition-all" size={20} />
    </Link>
  );
}
