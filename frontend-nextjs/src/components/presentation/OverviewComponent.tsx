import React from 'react';

interface OverviewProps {
  data: any;
  chapterTitle?: string;
  unitTitle?: string;
}

export default function OverviewComponent({ data, chapterTitle, unitTitle }: OverviewProps) {
  if (!data) {
    return (
      <div className="p-12 text-center text-slate-600 bg-white rounded-3xl border border-slate-200 space-y-3 shadow-sm">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold uppercase tracking-wider">
          <span>Overview Ready</span>
        </div>
        <h3 className="text-xl font-black text-slate-900 tracking-tight">Chapter Overview</h3>
        <p className="text-slate-600 text-sm leading-relaxed max-w-md mx-auto">
          No overview content is available for this chapter yet.
        </p>
      </div>
    );
  }

  const summary = data.summary || data.overview || data.core_summary || data.description || '';
  const theme = data.centralTheme || data.theme_and_moral || data.central_theme || '';
  const objectives = data.learningObjectives || data.pedagogical_objectives || data.key_concepts || [];
  const takeaways = data.importantTakeaways || data.key_takeaways || [];
  const terms = data.keyTerminology || data.vocabulary || data.key_terms || [];

  return (
    <div className="space-y-8">
      {/* Chapter Hero */}
      <div className="p-8 sm:p-10 bg-gradient-to-br from-indigo-900 via-indigo-800 to-slate-900 rounded-3xl text-white shadow-xl space-y-4">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-700/60 border border-indigo-500/40 text-indigo-200 text-xs font-bold uppercase tracking-wider">
          <span>{unitTitle || 'Curriculum Unit'}</span>
        </div>
        <h2 className="text-3xl sm:text-4xl font-black tracking-tight">{chapterTitle || 'Chapter Overview'}</h2>
        {summary && (
          <p className="text-indigo-100 text-base sm:text-lg leading-relaxed max-w-3xl opacity-90">
            {summary}
          </p>
        )}
      </div>

      {/* The Big Idea / Central Theme */}
      {theme && (
        <div className="p-6 sm:p-8 bg-white rounded-3xl border border-slate-200 shadow-sm space-y-3">
          <h3 className="text-xs font-black tracking-widest text-indigo-600 uppercase">The Big Idea & Theme</h3>
          <p className="text-slate-800 text-base font-semibold leading-relaxed">
            {typeof theme === 'string' ? theme : JSON.stringify(theme)}
          </p>
        </div>
      )}

      {/* What You Will Learn / Key Concepts */}
      {Array.isArray(objectives) && objectives.length > 0 && (
        <div className="p-6 sm:p-8 bg-white rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-xs font-black tracking-widest text-indigo-600 uppercase">What You Will Learn</h3>
          <ul className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {objectives.map((obj: any, idx: number) => (
              <li key={idx} className="flex items-start gap-3 p-4 bg-slate-50 border border-slate-100 rounded-2xl text-slate-700 text-sm font-medium">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-100 text-indigo-700 font-bold flex items-center justify-center text-xs">✓</span>
                <span>{typeof obj === 'string' ? obj : obj.title || obj.objective || JSON.stringify(obj)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Key Takeaways */}
      {Array.isArray(takeaways) && takeaways.length > 0 && (
        <div className="p-6 sm:p-8 bg-white rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-xs font-black tracking-widest text-indigo-600 uppercase">Key Takeaways</h3>
          <div className="space-y-3">
            {takeaways.map((t: any, idx: number) => (
              <div key={idx} className="p-4 bg-amber-50/50 border border-amber-100 rounded-2xl text-slate-800 text-sm leading-relaxed font-medium">
                {typeof t === 'string' ? t : t.takeaway || t.text || JSON.stringify(t)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Terms Vocabulary Chips */}
      {Array.isArray(terms) && terms.length > 0 && (
        <div className="p-6 sm:p-8 bg-white rounded-3xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-xs font-black tracking-widest text-indigo-600 uppercase">Key Vocabulary & Terms</h3>
          <div className="flex flex-wrap gap-2">
            {terms.map((term: any, idx: number) => {
              const termName = typeof term === 'string' ? term : term.term || term.word || '';
              const def = typeof term === 'object' ? term.definition || term.meaning : '';
              return (
                <div key={idx} className="group relative px-4 py-2.5 bg-indigo-50 hover:bg-indigo-600 border border-indigo-200 hover:border-indigo-600 rounded-2xl text-indigo-900 hover:text-white text-xs font-bold transition-all cursor-default shadow-sm">
                  <span>{termName}</span>
                  {def && (
                    <div className="absolute bottom-full left-1/2 -translate-x-1/2 mb-2 hidden group-hover:block w-64 p-3 bg-slate-900 text-white text-xs rounded-xl shadow-xl z-10 font-normal normal-case leading-normal">
                      {def}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
