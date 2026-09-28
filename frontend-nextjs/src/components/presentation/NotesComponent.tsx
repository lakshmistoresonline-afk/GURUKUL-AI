import React, { useState } from 'react';
import HindiNotesComponent from './HindiNotesComponent';
import MathsNotesComponent from './MathsNotesComponent';

interface NotesProps {
  data: any;
  subject?: string;
}

function renderSafeText(val: any): React.ReactNode {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string' || typeof val === 'number') return val;
  if (Array.isArray(val)) {
    return val.map((item, idx) => (
      <div key={idx} className="my-1">{renderSafeText(item)}</div>
    ));
  }
  if (typeof val === 'object') {
    if (val.text) return val.text;
    if (val.synopsis) return val.synopsis;
    if (val.heading && val.content) return `${val.heading}: ${val.content}`;
    if (val.concept && val.explanation) return `${val.concept}: ${val.explanation}`;
    return Object.entries(val).map(([k, v], idx) => (
      <div key={idx} className="text-xs">
        <strong className="capitalize text-indigo-700">{k.replace(/_/g, ' ')}:</strong> {renderSafeText(v)}
      </div>
    ));
  }
  return String(val);
}

export default function NotesComponent({ data, subject }: NotesProps) {
  const [activeSubTab, setActiveSubTab] = useState<string>('summary');

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No notes available.</div>;
  }

  // Check if this is Hindi schema
  if (data.core_theme_and_moral || data.detailed_summary_and_explanation || data.exhaustive_vocabulary) {
    return <HindiNotesComponent data={data} />;
  }

  // Check if this is Maths schema
  if (data.conceptual_foundation && typeof data.conceptual_foundation === 'object') {
    return <MathsNotesComponent data={data} />;
  }

  const rawOverview = data.overview || data.summary || '';
  const centralTheme = data.centralTheme || data.core_theme_and_moral || data.theme || '';

  let overviewText = '';
  let subSections: any[] = [];
  if (typeof rawOverview === 'object' && rawOverview !== null) {
    overviewText = rawOverview.overview || rawOverview.synopsis || '';
    subSections = rawOverview.keySections || rawOverview.core_themes || [];
  } else {
    overviewText = rawOverview;
  }

  const breakdown = data.detailedBreakdown || data.detailed_summary_and_explanation || data.conceptual_foundation || data.scientificPrinciples || data.paragraphs || [];
  const keyVocabulary = data.keyVocabulary || data.exhaustive_vocabulary || data.glossary || data.vocabulary || [];
  const formulas = data.key_formulas_and_rules || data.numericalsAndFormulas || [];
  const applications = data.real_world_applications || data.activities || [];
  const didYouKnow = data.didYouKnow || [];
  const takeaways = data.importantTakeaways || data.key_takeaways || [];

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        <button
          onClick={() => setActiveSubTab('summary')}
          className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'summary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
        >
          📖 Summary & Theme
        </button>
        {breakdown.length > 0 && (
          <button
            onClick={() => setActiveSubTab('concepts')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'concepts' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            🔬 Core Concepts ({breakdown.length})
          </button>
        )}
        {formulas.length > 0 && (
          <button
            onClick={() => setActiveSubTab('formulas')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'formulas' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📐 Formulas & Rules ({formulas.length})
          </button>
        )}
        {keyVocabulary.length > 0 && (
          <button
            onClick={() => setActiveSubTab('glossary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'glossary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 Glossary ({keyVocabulary.length})
          </button>
        )}
        {applications.length > 0 && (
          <button
            onClick={() => setActiveSubTab('applications')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'applications' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            🌍 Applications ({applications.length})
          </button>
        )}
      </div>

      {/* Tab 1: Summary & Theme */}
      {activeSubTab === 'summary' && (
        <div className="space-y-6 animate-in fade-in duration-200">
          {(overviewText || centralTheme || subSections.length > 0) && (
            <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
              <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Chapter Summary & Theme</h3>
              {overviewText && <p className="text-slate-700 text-sm leading-relaxed">{renderSafeText(overviewText)}</p>}

              {Array.isArray(subSections) && subSections.length > 0 && (
                <div className="space-y-3 pt-3 border-t border-slate-100">
                  {subSections.map((ks: any, kIdx: number) => (
                    <div key={kIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                      {ks.heading && <div className="text-xs font-extrabold text-indigo-700 uppercase tracking-wide">{ks.heading}</div>}
                      <div className="text-xs text-slate-700 leading-relaxed">{renderSafeText(ks.content || ks)}</div>
                    </div>
                  ))}
                </div>
              )}

              {centralTheme && (
                <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl text-indigo-900 text-xs font-bold">
                  Central Theme: {renderSafeText(centralTheme)}
                </div>
              )}
            </div>
          )}

          {Array.isArray(takeaways) && takeaways.length > 0 && (
            <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
              <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Important Takeaways</h3>
              <div className="space-y-3">
                {takeaways.map((t: string, idx: number) => (
                  <div key={idx} className="p-4 bg-amber-50/50 border border-amber-100 rounded-2xl text-slate-800 text-sm font-medium">
                    {t}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Core Concepts */}
      {activeSubTab === 'concepts' && breakdown.length > 0 && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Detailed Section Analysis & Core Concepts</h3>
          <div className="space-y-4">
            {breakdown.map((section: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-600">
                  Section #{idx + 1}: {section.sectionTitle || section.title || section.principleTitle || section.principle_title || section.concept || section.para_no || ''}
                </div>
                {section.lines && (
                  <div className="p-4 bg-slate-50 border border-slate-100 rounded-2xl font-serif italic text-slate-800 text-sm leading-relaxed">
                    &ldquo;{Array.isArray(section.lines) ? section.lines.join(' ') : section.lines}&rdquo;
                  </div>
                )}
                <div className="text-slate-700 text-sm leading-relaxed">
                  {renderSafeText(section.explanation || section.analysis || section.description || section.text || section.principleExplanation || section.principle_explanation || section)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Formulas & Rules */}
      {activeSubTab === 'formulas' && formulas.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Key Formulas, Rules & Numericals</h3>
          <div className="grid grid-cols-1 gap-4">
            {formulas.map((f: any, idx: number) => (
              <div key={idx} className="p-6 bg-indigo-50/40 border border-indigo-100 rounded-2xl space-y-3">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-700">{f.formulaName || f.rule_name || f.title || `Formula #${idx + 1}`}</div>
                <div className="text-slate-800 text-sm font-semibold">{renderSafeText(f)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Glossary */}
      {activeSubTab === 'glossary' && keyVocabulary.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Key Vocabulary & Glossary</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {keyVocabulary.map((v: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{v.term || v.word}</div>
                <div className="text-xs text-slate-700">{v.definition || v.meaning}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: Applications */}
      {activeSubTab === 'applications' && applications.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Real-World Applications & Activities</h3>
          <div className="space-y-3">
            {applications.map((app: any, idx: number) => (
              <div key={idx} className="p-4 bg-amber-50/50 border border-amber-100 rounded-2xl text-slate-800 text-sm font-medium">
                {typeof app === 'string' ? app : app.title || app.activity || app.name || JSON.stringify(app)}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
