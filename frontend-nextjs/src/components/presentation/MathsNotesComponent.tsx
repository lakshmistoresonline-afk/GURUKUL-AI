import React from 'react';

interface MathsNotesProps {
  data: any;
}

export default function MathsNotesComponent({ data }: MathsNotesProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई गणित नोट्स उपलब्ध नहीं हैं।</div>;
  }

  const theme = data.theme || '';
  const foundation = data.conceptual_foundation || {};
  const intro = foundation.introduction || '';
  const coreConcepts = foundation.core_concepts || [];
  const formulas = data.key_formulas_and_rules || [];
  const realWorld = data.real_world_applications || '';

  return (
    <div className="space-y-8">
      {/* Chapter Theme & Introduction */}
      <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
        {theme && <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full border border-indigo-200">Theme: {theme}</span>}
        <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Conceptual Foundation</h3>
        {intro && <p className="text-slate-700 text-sm leading-relaxed">{intro}</p>}
      </div>

      {/* Core Mathematical Concepts */}
      {Array.isArray(coreConcepts) && coreConcepts.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Core Mathematical Concepts</h3>
          <div className="space-y-4">
            {coreConcepts.map((cc: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-600">Concept #{idx + 1}: {cc.concept}</div>
                <p className="text-slate-700 text-sm leading-relaxed">{cc.explanation}</p>
                {cc.example && (
                  <div className="p-4 bg-slate-50 border border-slate-100 rounded-2xl font-mono text-xs text-indigo-900 leading-relaxed">
                    <strong>Example:</strong> {cc.example}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Formulas & Rules */}
      {Array.isArray(formulas) && formulas.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Key Formulas & Rules</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {formulas.map((form: string, idx: number) => (
              <div key={idx} className="p-5 bg-indigo-50/50 border border-indigo-100 rounded-2xl space-y-1">
                <div className="text-xs font-extrabold text-indigo-600 uppercase tracking-wide">Rule #{idx + 1}</div>
                <div className="text-slate-900 text-sm font-bold font-mono">{form}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Real World Applications */}
      {realWorld && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Real-World Applications</h3>
          <p className="text-slate-700 text-sm leading-relaxed font-medium bg-amber-50/50 p-4 rounded-2xl border border-amber-100">{realWorld}</p>
        </div>
      )}
    </div>
  );
}
