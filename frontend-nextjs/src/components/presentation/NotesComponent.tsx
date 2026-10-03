import React, { useState } from 'react';
import HindiNotesComponent from './HindiNotesComponent';
import MathsNotesComponent from './MathsNotesComponent';
import { renderSafeText, SafeStructuredCard } from './safeRender';

interface NotesProps {
  data: any;
  subject?: string;
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

  const rawOverview = data.overview || data.summary || data.section_1_core_map_and_conceptual_architecture || '';
  const centralTheme = data.centralTheme || data.core_theme_and_moral || data.theme || '';

  let overviewText = '';
  let subSections: any[] = [];
  if (typeof rawOverview === 'object' && rawOverview !== null) {
    overviewText = rawOverview.overview || rawOverview.synopsis || rawOverview.big_idea_summary || '';
    subSections = rawOverview.keySections || rawOverview.core_themes || rawOverview.topic_hierarchy || [];
  } else {
    overviewText = rawOverview;
  }

  const breakdown = data.detailedBreakdown || data.detailed_summary_and_explanation || data.conceptual_foundation || data.scientificPrinciples || data.paragraphs || [];
  const keyVocabulary = data.keyVocabulary || data.exhaustive_vocabulary || data.glossary || data.vocabulary || data.section_2_essential_vocabulary || [];
  const formulas = data.key_formulas_and_rules || data.numericalsAndFormulas || [];
  const applications = data.real_world_applications || data.activities || [];
  const didYouKnow = data.didYouKnow || [];
  const takeaways = data.importantTakeaways || data.key_takeaways || [];
  const misconceptions = data.misconceptionsAndPitfalls || data.section_3_misconceptions_and_pitfall_prevention || [];

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
        {keyVocabulary.length > 0 && (
          <button
            onClick={() => setActiveSubTab('glossary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'glossary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 Glossary ({keyVocabulary.length})
          </button>
        )}
        {misconceptions.length > 0 && (
          <button
            onClick={() => setActiveSubTab('pitfalls')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'pitfalls' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ⚠️ Pitfalls ({misconceptions.length})
          </button>
        )}
      </div>

      {/* Tab 1: Summary & Theme */}
      {activeSubTab === 'summary' && (
        <div className="space-y-6 animate-in fade-in duration-200">
          {rawOverview && typeof rawOverview === 'object' && ('big_idea_summary' in rawOverview || 'topic_hierarchy' in rawOverview) ? (
            <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
              <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Core Map & Conceptual Architecture</h3>
              <SafeStructuredCard item={rawOverview} />
            </div>
          ) : (overviewText || centralTheme || subSections.length > 0) && (
            <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
              <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Chapter Summary & Theme</h3>
              {overviewText && <p className="text-slate-700 text-sm leading-relaxed">{renderSafeText(overviewText)}</p>}

              {Array.isArray(subSections) && subSections.length > 0 && (
                <div className="space-y-3 pt-3 border-t border-slate-100">
                  {subSections.map((ks: any, kIdx: number) => (
                    <div key={kIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                      {ks.heading && <div className="text-xs font-extrabold text-indigo-700 uppercase tracking-wide">{ks.heading}</div>}
                      {ks.topic && <div className="text-xs font-extrabold text-indigo-700 uppercase tracking-wide">{ks.topic}</div>}
                      <div className="text-xs text-slate-700 leading-relaxed">{renderSafeText(ks.content || ks.subtopics || ks)}</div>
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
        </div>
      )}

      {/* Tab 4: Glossary */}
      {activeSubTab === 'glossary' && keyVocabulary.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Essential Vocabulary & Glossary</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {keyVocabulary.map((v: any, idx: number) => (
              <SafeStructuredCard key={idx} item={v} />
            ))}
          </div>
        </div>
      )}

      {/* Pitfalls */}
      {activeSubTab === 'pitfalls' && misconceptions.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Misconceptions & Pitfall Prevention</h3>
          <div className="space-y-3">
            {misconceptions.map((m: any, idx: number) => (
              <div key={idx} className="p-4 bg-rose-50/50 border border-rose-100 rounded-2xl text-slate-800 text-xs space-y-1">
                {m.misconception && <div className="font-bold text-rose-800">⚠️ Misconception: {m.misconception}</div>}
                {m.correction && <div className="font-medium text-emerald-800">✓ Correction: {m.correction}</div>}
                {!m.misconception && <div className="font-medium text-slate-700">{renderSafeText(m)}</div>}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
