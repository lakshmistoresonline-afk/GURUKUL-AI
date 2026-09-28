import React, { useState } from 'react';

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
    if (val.summary) return val.summary;
    if (val.definition) return `${val.term || val.word || ''}: ${val.definition}`;
    if (val.question_text) return val.question_text;
    if (val.detailed_answer) return val.detailed_answer;
    return Object.entries(val).map(([k, v], idx) => (
      <div key={idx} className="text-xs space-y-0.5">
        <strong className="capitalize text-indigo-700">{k.replace(/_/g, ' ')}:</strong> {renderSafeText(v)}
      </div>
    ));
  }
  return String(val);
}

interface Class7NotesProps {
  data: any;
}

export default function Class7UniversalNotesComponent({ data }: Class7NotesProps) {
  const m1 = data?.m1_zero_omission_notes || {};
  const m2 = data?.m2_key_terms_formulas_and_rules || [];
  const m3 = data?.m3_practical_activities_and_procedures || [];
  const m4 = data?.m4_diagrams_and_tables || [];
  const m5 = data?.m5_textbook_solutions_and_extracts || [];
  const m6 = data?.m6_tiered_exam_question_bank || {};
  const m7 = data?.m7_common_pitfalls || [];

  const hasM1 = m1 && Object.keys(m1).length > 0;
  const hasM2 = Array.isArray(m2) && m2.length > 0;
  const hasM3 = Array.isArray(m3) && m3.length > 0;
  const hasM4 = Array.isArray(m4) && m4.length > 0;
  const hasM5 = Array.isArray(m5) && m5.length > 0;
  const hasM6 = m6 && Object.keys(m6).length > 0;
  const hasM7 = Array.isArray(m7) && m7.length > 0;

  const [activeSubTab, setActiveSubTab] = useState<string>(() => {
    if (hasM1) return 'm1';
    if (hasM2) return 'm2';
    if (hasM5) return 'm5';
    if (hasM6) return 'm6';
    return 'm1';
  });

  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No notes available for this chapter.</div>;
  }

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        {hasM1 && (
          <button
            onClick={() => setActiveSubTab('m1')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'm1' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📖 Summary & Detailed Sections
          </button>
        )}
        {hasM2 && (
          <button
            onClick={() => setActiveSubTab('m2')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'm2' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 Key Terms & Rules ({m2.length})
          </button>
        )}
        {hasM3 && (
          <button
            onClick={() => setActiveSubTab('m3')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'm3' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            🧪 Practical Activities ({m3.length})
          </button>
        )}
        {hasM4 && (
          <button
            onClick={() => setActiveSubTab('m4')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'm4' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📐 Diagrams & Tables ({m4.length})
          </button>
        )}
        {hasM5 && (
          <button
            onClick={() => setActiveSubTab('m5')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'm5' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📋 Textbook Solutions ({m5.length})
          </button>
        )}
        {hasM6 && (
          <button
            onClick={() => setActiveSubTab('m6')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'm6' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ✍️ Exam Question Bank
          </button>
        )}
        {hasM7 && (
          <button
            onClick={() => setActiveSubTab('m7')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'm7' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ⚠️ Common Pitfalls ({m7.length})
          </button>
        )}
      </div>

      {/* Tab 1: Summary & Detailed Sections */}
      {activeSubTab === 'm1' && hasM1 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Zero-Omission Chapter Notes</h3>
          {m1.summary && (
            <div className="space-y-1">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">Summary</h4>
              <p className="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap">{renderSafeText(m1.summary)}</p>
            </div>
          )}

          {Array.isArray(m1.detailed_sections) && m1.detailed_sections.length > 0 && (
            <div className="space-y-4 pt-4 border-t border-slate-100">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">Detailed Sections</h4>
              {m1.detailed_sections.map((ds: any, idx: number) => (
                <div key={idx} className="p-5 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                  <div className="text-xs font-bold text-indigo-700 uppercase">{ds.section || `Section #{idx + 1}`}</div>
                  <div className="text-xs text-slate-700 leading-relaxed whitespace-pre-wrap">{renderSafeText(ds.full_notes || ds.notes || ds)}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Key Terms & Rules */}
      {activeSubTab === 'm2' && hasM2 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Key Terms, Formulas & Rules</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {m2.map((term: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{term.term || term.rule_name || `Term #${idx + 1}`}</div>
                <div className="text-xs text-slate-700">{renderSafeText(term.definition || term.rule || term)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Practical Activities */}
      {activeSubTab === 'm3' && hasM3 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Practical Activities & Procedures</h3>
          <div className="space-y-3">
            {m3.map((act: any, idx: number) => (
              <div key={idx} className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-2xl space-y-2">
                <div className="text-sm font-extrabold text-emerald-900">{act.activity_title || act.title || `Activity #${idx + 1}`}</div>
                <div className="text-xs text-slate-700 leading-relaxed">{renderSafeText(act.procedure || act.description || act)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Diagrams & Tables */}
      {activeSubTab === 'm4' && hasM4 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Diagrams & Tabular Data</h3>
          <div className="space-y-3">
            {m4.map((diag: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{diag.title || diag.table_title || `Item #${idx + 1}`}</div>
                <div className="text-xs text-slate-700 leading-relaxed">{renderSafeText(diag.description || diag.data || diag)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: Textbook Solutions */}
      {activeSubTab === 'm5' && hasM5 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Textbook Solutions & Extracts</h3>
          <div className="space-y-3">
            {m5.map((sol: any, idx: number) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                <div className="text-xs font-bold text-slate-500">Question #{idx + 1}</div>
                <div className="text-sm font-bold text-slate-900">{renderSafeText(sol.question || sol.q || '')}</div>
                <div className="text-xs text-emerald-800 bg-emerald-50 p-3 rounded-xl border border-emerald-100 font-semibold">
                  Solution: {renderSafeText(sol.solution || sol.answer || sol)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 6: Exam Question Bank */}
      {activeSubTab === 'm6' && hasM6 && (
        <div className="space-y-6 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Tiered Exam Question Bank</h3>
          {Object.entries(m6).map(([qType, qList]: [string, any], tIdx: number) => (
            Array.isArray(qList) && qList.length > 0 && (
              <div key={tIdx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
                <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">{qType.replace(/_/g, ' ')}</h4>
                <div className="space-y-3">
                  {qList.map((q: any, qIdx: number) => {
                    const qKey = `${tIdx}-${qIdx}`;
                    const isVisible = showAnswers[qKey];
                    const answer = q.answer || q.correct_answer || q.solution;

                    return (
                      <div key={qIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                        <div className="text-xs font-bold text-slate-700">Q{qIdx + 1}: {renderSafeText(q.question || q.q || q)}</div>
                        {answer && (
                          <div className="pt-2 border-t border-slate-200/60 mt-2">
                            <button
                              onClick={() => toggleAnswer(qKey)}
                              className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                            >
                              {isVisible ? 'Hide Answer ▴' : 'Show Answer ▾'}
                            </button>
                            {isVisible && (
                              <div className="mt-2 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-medium">
                                Answer: {renderSafeText(answer)}
                              </div>
                            )}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            )
          ))}
        </div>
      )}

      {/* Tab 7: Pitfalls */}
      {activeSubTab === 'm7' && hasM7 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Common Pitfalls & Error Analysis</h3>
          <div className="space-y-3">
            {m7.map((cp: any, idx: number) => (
              <div key={idx} className="p-4 bg-rose-50/50 border border-rose-100 rounded-2xl text-slate-800 text-sm font-medium flex items-start gap-3">
                <span className="flex-shrink-0 text-rose-600 font-bold">⚠️</span>
                <span>{renderSafeText(cp)}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
