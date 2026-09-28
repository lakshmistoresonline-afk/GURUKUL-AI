import React from 'react';

interface SocialNotesProps {
  data: any;
}

export default function Class6SocialNotesComponent({ data }: SocialNotesProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No notes available.</div>;
  }

  const theme = data.theme || '';
  const sec1 = data.section_1_core_map_and_conceptual_architecture || {};
  const sec2 = data.section_2_essential_vocabulary || {};
  const sec3 = data.section_3_analytical_breakdown_and_calculations || [];
  const sec4 = data.section_4_categorized_question_bank || {};
  const sec5 = data.section_5_misconceptions_and_pitfall_prevention || [];

  return (
    <div className="space-y-8">
      {/* Theme & Core Architecture */}
      <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
        {theme && <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full border border-indigo-200">Theme: {theme}</span>}
        <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Core Map & Conceptual Architecture</h3>
        {sec1 && (
          <div className="text-slate-700 text-sm leading-relaxed space-y-2">
            {typeof sec1 === 'string' ? sec1 : (
              <pre className="whitespace-pre-wrap font-sans text-xs text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-2xl overflow-x-auto">
                {JSON.stringify(sec1, null, 2)}
              </pre>
            )}
          </div>
        )}
      </div>

      {/* Essential Vocabulary */}
      {sec2 && Object.keys(sec2).length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Essential Vocabulary</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(sec2).map(([term, def]: [string, any], idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{term}</div>
                <div className="text-xs text-slate-700">{typeof def === 'string' ? def : JSON.stringify(def)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Analytical Breakdown */}
      {Array.isArray(sec3) && sec3.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Analytical Breakdown</h3>
          <div className="space-y-4">
            {sec3.map((item: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-2">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-600">Section #{idx + 1}: {item.title || item.heading || ''}</div>
                <p className="text-slate-700 text-sm leading-relaxed">{item.content || item.description || JSON.stringify(item)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Misconceptions & Pitfalls */}
      {Array.isArray(sec5) && sec5.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Misconceptions & Pitfall Prevention</h3>
          <div className="space-y-3">
            {sec5.map((p: any, idx: number) => (
              <div key={idx} className="p-4 bg-rose-50/50 border border-rose-100 rounded-2xl text-slate-800 text-sm font-medium flex items-start gap-3">
                <span className="flex-shrink-0 text-rose-600 font-bold">⚠️</span>
                <span>{typeof p === 'string' ? p : p.error || JSON.stringify(p)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
