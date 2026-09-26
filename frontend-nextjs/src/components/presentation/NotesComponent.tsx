import React from 'react';
import HindiNotesComponent from './HindiNotesComponent';
import MathsNotesComponent from './MathsNotesComponent';

interface NotesProps {
  data: any;
  subject?: string;
}

export default function NotesComponent({ data, subject }: NotesProps) {
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

  // Extract overview text and key sections if summary is an object (Science schema)
  let overviewText = '';
  let scienceKeySections: any[] = [];
  if (typeof rawOverview === 'object' && rawOverview !== null) {
    overviewText = rawOverview.overview || '';
    scienceKeySections = rawOverview.keySections || [];
  } else {
    overviewText = rawOverview;
  }

  // Breakdown / Detailed Explanations
  const breakdown = data.detailedBreakdown || data.detailed_summary_and_explanation || data.conceptual_foundation || data.scientificPrinciples || [];

  // Subject specific sections
  const poeticDevices = data.poeticDevices || {};
  const characterAnalysis = data.characterAnalysis || data.character_and_element_sketches || [];
  const keyVocabulary = data.keyVocabulary || data.exhaustive_vocabulary || data.glossary || [];
  const grammarFocus = data.grammarFocus || data.comprehensive_grammar || data.grammar || null;
  const takeaways = data.importantTakeaways || data.key_takeaways || [];

  // Maths & Science specific fields
  const formulas = data.key_formulas_and_rules || data.numericalsAndFormulas || [];
  const applications = data.real_world_applications || data.activities || [];
  const didYouKnow = data.didYouKnow || [];

  return (
    <div className="space-y-8">
      {/* Chapter Overview & Central Theme */}
      {(overviewText || centralTheme || scienceKeySections.length > 0) && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Chapter Summary & Theme</h3>
          {overviewText && <p className="text-slate-700 text-sm leading-relaxed">{overviewText}</p>}

          {/* Science Key Sections */}
          {Array.isArray(scienceKeySections) && scienceKeySections.length > 0 && (
            <div className="space-y-3 pt-3 border-t border-slate-100">
              {scienceKeySections.map((ks: any, kIdx: number) => (
                <div key={kIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                  <div className="text-xs font-extrabold text-indigo-700 uppercase tracking-wide">{ks.heading}</div>
                  <p className="text-xs text-slate-700 leading-relaxed">{ks.content}</p>
                </div>
              ))}
            </div>
          )}

          {centralTheme && (
            <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl text-indigo-900 text-xs font-bold">
              Central Theme: {typeof centralTheme === 'string' ? centralTheme : JSON.stringify(centralTheme)}
            </div>
          )}
        </div>
      )}

      {/* Detailed Breakdown / Scientific Principles / Conceptual Foundation */}
      {Array.isArray(breakdown) && breakdown.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Detailed Section Analysis & Core Concepts</h3>
          <div className="space-y-4">
            {breakdown.map((section: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-600">
                  Section #{idx + 1}: {section.sectionTitle || section.title || section.principleTitle || section.principle_title || section.concept || ''}
                </div>
                {section.lines && (
                  <div className="p-4 bg-slate-50 border border-slate-100 rounded-2xl font-serif italic text-slate-800 text-sm leading-relaxed">
                    &ldquo;{Array.isArray(section.lines) ? section.lines.join(' ') : section.lines}&rdquo;
                  </div>
                )}
                <p className="text-slate-700 text-sm leading-relaxed">
                  {section.explanation || section.analysis || section.description || section.principleExplanation || section.principle_explanation || JSON.stringify(section)}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Formulas & Rules & Numericals (Maths / Science) */}
      {Array.isArray(formulas) && formulas.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Key Formulas, Rules & Numericals</h3>
          <div className="grid grid-cols-1 gap-4">
            {formulas.map((f: any, idx: number) => {
              if (typeof f === 'string') {
                return (
                  <div key={idx} className="p-5 bg-indigo-50/40 border border-indigo-100 rounded-2xl space-y-1">
                    <div className="text-xs font-extrabold text-indigo-600 uppercase tracking-wide">Formula #{idx + 1}</div>
                    <div className="text-slate-900 text-sm font-bold font-mono">{f}</div>
                  </div>
                );
              }
              return (
                <div key={idx} className="p-6 bg-indigo-50/40 border border-indigo-100 rounded-2xl space-y-3">
                  <div className="text-xs font-black uppercase tracking-wider text-indigo-700">{f.formulaName || f.rule_name || f.title || `Formula #${idx + 1}`}</div>
                  {f.formulaExpression && <div className="p-3 bg-white border border-indigo-200 rounded-xl font-mono text-xs font-bold text-indigo-900">Expression: {f.formulaExpression}</div>}
                  {f.exampleProblem && <div className="text-xs text-slate-800 font-medium"><strong>Problem:</strong> {f.exampleProblem}</div>}
                  {f.solution && <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-serif"><strong>Solution:</strong> {f.solution}</div>}
                  {f.statement && <div className="text-slate-800 text-sm font-semibold">{f.statement}</div>}
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Character Analysis */}
      {Array.isArray(characterAnalysis) && characterAnalysis.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Character Analysis</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {characterAnalysis.map((ch: any, idx: number) => (
              <div key={idx} className="p-5 bg-indigo-50/40 border border-indigo-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600 uppercase tracking-wide">{ch.character || ch.name || ''}</div>
                <div className="text-slate-800 text-xs leading-relaxed font-medium">{ch.traits || ch.description || JSON.stringify(ch)}</div>
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
                <div className="text-slate-800 text-sm font-semibold">
                  {Array.isArray(val) ? val.join(', ') : (typeof val === 'string' ? val : JSON.stringify(val))}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Key Vocabulary / Glossary */}
      {Array.isArray(keyVocabulary) && keyVocabulary.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Key Vocabulary & Glossary</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {keyVocabulary.map((v: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{v.term || v.word}</div>
                <div className="text-xs text-slate-700">{v.definition || v.meaning}</div>
                {v.synonym && <div className="text-xs text-slate-500">Synonym: {v.synonym} {v.antonym ? `| Antonym: ${v.antonym}` : ''}</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Real World Applications / Activities */}
      {Array.isArray(applications) && applications.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
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

      {/* Grammar Focus */}
      {grammarFocus && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">
            Grammar Focus: {grammarFocus.conceptTitle || grammarFocus.title || ''}
          </h3>
          <p className="text-slate-700 text-sm leading-relaxed">{grammarFocus.rules || grammarFocus.description || ''}</p>
          {Array.isArray(grammarFocus.examples) && grammarFocus.examples.length > 0 && (
            <div className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-2xl space-y-1">
              <div className="text-xs font-bold text-emerald-800 uppercase tracking-wider">Examples:</div>
              <ul className="list-disc list-inside text-xs text-slate-700 space-y-1">
                {grammarFocus.examples.map((ex: string, eIdx: number) => (
                  <li key={eIdx}>{ex}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Did You Know (Science) */}
      {Array.isArray(didYouKnow) && didYouKnow.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Did You Know?</h3>
          <div className="space-y-3">
            {didYouKnow.map((item: any, idx: number) => (
              <div key={idx} className="p-4 bg-sky-50 border border-sky-100 rounded-2xl text-slate-800 text-sm font-medium">
                {typeof item === 'string' ? item : item.fact || JSON.stringify(item)}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Important Takeaways */}
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
  );
}
