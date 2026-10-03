import React, { useState } from 'react';
import { renderSafeText } from './safeRender';

interface FoundationalProps {
  data: any;
}

export default function FoundationalComponent({ data }: FoundationalProps) {
  const [searchQuery, setSearchQuery] = useState<string>('');

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No foundational curriculum content available.</div>;
  }

  const metadata = data.textbook_metadata || {};
  const modules = data.modules || [];

  const filteredModules = modules.filter((m: any) => {
    if (!searchQuery) return true;
    const q = searchQuery.toLowerCase();
    const cat = (m.category || '').toLowerCase();
    const itemStr = JSON.stringify(m.item || {}).toLowerCase();
    return cat.includes(q) || itemStr.includes(q);
  });

  return (
    <div className="space-y-6">
      {/* Textbook Metadata Header */}
      <div className="p-6 sm:p-8 bg-gradient-to-br from-indigo-950 via-indigo-900 to-slate-900 rounded-3xl text-white shadow-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-700/60 border border-indigo-500/40 text-indigo-200 text-xs font-bold uppercase tracking-wider">
            <span>{metadata.curriculum_framework || 'NCF-SE 2023 / NEP 2020'}</span>
          </div>
          <span className="text-xs font-mono text-indigo-300 font-bold">{metadata.grade || 'Foundational Core'}</span>
        </div>
        <h3 className="text-2xl sm:text-3xl font-black tracking-tight">{metadata.textbook || 'Foundational Curriculum Module'}</h3>
        <p className="text-indigo-200 text-xs sm:text-sm">Publisher: {metadata.publisher || 'NCERT'}</p>

        {/* Search Bar */}
        <div className="pt-2">
          <input
            type="text"
            placeholder="Search foundational concepts, grammar, principles..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-4 py-3 bg-white/10 border border-indigo-500/30 rounded-2xl text-sm text-white placeholder-indigo-300 focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />
        </div>
      </div>

      {/* Foundational Modules Grid */}
      {filteredModules.length > 0 ? (
        <div className="space-y-4">
          <h4 className="text-sm font-black uppercase text-indigo-800 tracking-wider">Foundational Core Modules ({filteredModules.length})</h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {filteredModules.map((mod: any, idx: number) => {
              const item = mod.item || {};
              const cat = mod.category || 'Module';
              const concept = item.concept || item.title || item.name || cat;
              const explanation = item.explanation || item.definition || item.description || '';
              const examples = item.examples || item.subtopics || item.key_points || [];
              const sourceCtx = item.source_context || '';

              return (
                <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3 hover:border-indigo-300 transition-all">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                    <span className="text-[11px] font-black uppercase tracking-wider px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-lg">{cat}</span>
                    {sourceCtx && <span className="text-[10px] font-mono text-slate-400 font-bold">{sourceCtx}</span>}
                  </div>
                  <h5 className="text-base font-black text-slate-900">{renderSafeText(concept)}</h5>
                  {explanation && <p className="text-xs text-slate-700 leading-relaxed">{renderSafeText(explanation)}</p>}

                  {Array.isArray(examples) && examples.length > 0 && (
                    <div className="pt-1 space-y-1">
                      <div className="text-[11px] font-bold text-slate-500 uppercase">Examples / Key Points:</div>
                      <div className="flex flex-wrap gap-1.5">
                        {examples.map((ex: any, eIdx: number) => (
                          <span key={eIdx} className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-xl text-xs font-medium text-slate-700">
                            {renderSafeText(ex)}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      ) : (
        <div className="p-12 text-center text-slate-500 bg-white rounded-3xl border border-slate-200 shadow-sm">
          No foundational modules match your search.
        </div>
      )}
    </div>
  );
}
