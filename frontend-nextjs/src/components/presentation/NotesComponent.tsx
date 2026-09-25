import React from 'react';

interface NotesProps {
  data: any;
}

export default function NotesComponent({ data }: NotesProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No notes available.</div>;
  }

  const breakdown = data.detailedBreakdown || data.summary_and_theme || [];
  const poeticDevices = data.poeticDevices || {};
  const grammar = data.grammarFocus || [];

  return (
    <div className="space-y-8">
      {/* Detailed Breakdown / Stanza Analysis */}
      {Array.isArray(breakdown) && breakdown.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Detailed Section Analysis</h3>
          <div className="space-y-4">
            {breakdown.map((section: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-600">Section #{idx + 1}: {section.sectionTitle || section.title || ''}</div>
                {section.lines && (
                  <div className="p-4 bg-slate-50 border border-slate-100 rounded-2xl font-serif italic text-slate-800 text-sm leading-relaxed">
                    &ldquo;{Array.isArray(section.lines) ? section.lines.join(' ') : section.lines}&rdquo;
                  </div>
                )}
                <p className="text-slate-700 text-sm leading-relaxed">
                  {section.explanation || section.analysis || section.description || JSON.stringify(section)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Literary / Poetic Devices */}
      {poeticDevices && Object.keys(poeticDevices).length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Literary & Poetic Devices</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(poeticDevices).map(([key, val]: [string, any], idx: number) => (
              <div key={idx} className="p-5 bg-indigo-50/40 border border-indigo-100 rounded-2xl space-y-1">
                <div className="text-xs font-extrabold text-indigo-600 uppercase tracking-wide">{key.replace(/_/g, ' ')}</div>
                <div className="text-slate-800 text-sm font-semibold">{typeof val === 'string' ? val : JSON.stringify(val)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Grammar Focus */}
      {Array.isArray(grammar) && grammar.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Grammar & Language Focus</h3>
          <div className="space-y-3">
            {grammar.map((g: any, idx: number) => (
              <div key={idx} className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-2xl text-slate-800 text-sm leading-relaxed">
                {typeof g === 'string' ? g : g.topic || g.title || JSON.stringify(g)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* General Raw Fallback if structured breakdown is absent */}
      {!breakdown.length && !Object.keys(poeticDevices).length && (
        <div className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm">
          <pre className="whitespace-pre-wrap font-sans text-sm text-slate-700 leading-relaxed overflow-x-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
