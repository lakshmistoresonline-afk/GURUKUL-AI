import React, { useState } from 'react';

interface ScienceMasterProps {
  data: any;
}

export default function Class6ScienceMasterComponent({ data }: ScienceMasterProps) {
  const notes = data?.zero_omission_notes || [];
  const labManual = data?.lab_and_activity_manual || [];
  const diagramBank = data?.diagram_and_sketching_bank || [];
  const glossary = data?.master_glossary_and_units || {};
  const questionBank = data?.exam_question_bank || {};
  const hasQBank = questionBank && Object.keys(questionBank).length > 0;

  const [activeSubTab, setActiveSubTab] = useState<string>(() => {
    if (notes.length > 0) return 'notes';
    if (labManual.length > 0) return 'lab';
    if (diagramBank.length > 0) return 'diagrams';
    if (Object.keys(glossary).length > 0) return 'glossary';
    if (hasQBank) return 'qbank';
    return 'notes';
  });

  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No master content available.</div>;
  }

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        {notes.length > 0 && (
          <button
            onClick={() => setActiveSubTab('notes')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'notes' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📖 Master Notes ({notes.length})
          </button>
        )}
        {labManual.length > 0 && (
          <button
            onClick={() => setActiveSubTab('lab')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'lab' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            🧪 Lab & Activity ({labManual.length})
          </button>
        )}
        {diagramBank.length > 0 && (
          <button
            onClick={() => setActiveSubTab('diagrams')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'diagrams' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📐 Diagrams ({diagramBank.length})
          </button>
        )}
        {Object.keys(glossary).length > 0 && (
          <button
            onClick={() => setActiveSubTab('glossary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'glossary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 Glossary ({Object.keys(glossary).length})
          </button>
        )}
        {hasQBank && (
          <button
            onClick={() => setActiveSubTab('qbank')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'qbank' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📋 Question Bank
          </button>
        )}
      </div>

      {/* Tab 1: Notes */}
      {activeSubTab === 'notes' && notes.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Zero-Omission Master Notes</h3>
          <div className="space-y-3">
            {notes.map((item: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{item.topic || item.heading || `Note #${idx + 1}`}</div>
                <div className="text-xs text-slate-700 leading-relaxed">{item.content || item.explanation || JSON.stringify(item)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 2: Lab Manual */}
      {activeSubTab === 'lab' && labManual.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Lab & Activity Manual</h3>
          <div className="space-y-3">
            {labManual.map((lab: any, idx: number) => (
              <div key={idx} className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-2xl space-y-2">
                <div className="text-sm font-extrabold text-emerald-900">{lab.title || lab.activity_name || `Activity #${idx + 1}`}</div>
                {lab.objective && <div className="text-xs text-slate-700"><strong>Objective:</strong> {lab.objective}</div>}
                {lab.procedure && <div className="text-xs text-slate-700"><strong>Procedure:</strong> {lab.procedure}</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Diagrams */}
      {activeSubTab === 'diagrams' && diagramBank.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Diagram & Sketching Bank</h3>
          <div className="space-y-3">
            {diagramBank.map((diag: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{diag.title || diag.diagram_title || `Diagram #${idx + 1}`}</div>
                <div className="text-xs text-slate-700 leading-relaxed">{diag.description || diag.instructions || JSON.stringify(diag)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Glossary */}
      {activeSubTab === 'glossary' && Object.keys(glossary).length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Master Glossary & Units</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(glossary).map(([term, def]: [string, any], idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{term}</div>
                <div className="text-xs text-slate-700">{typeof def === 'string' ? def : JSON.stringify(def)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: Question Bank */}
      {activeSubTab === 'qbank' && hasQBank && (
        <div className="space-y-6 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Exam Question Bank</h3>
          {Object.entries(questionBank).map(([qType, qList]: [string, any], tIdx: number) => (
            Array.isArray(qList) && qList.length > 0 && (
              <div key={tIdx} className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
                <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">{qType.replace(/_/g, ' ')}</h4>
                <div className="space-y-4">
                  {qList.map((q: any, qIdx: number) => {
                    const qKey = `${tIdx}-${qIdx}`;
                    const isVisible = showAnswers[qKey];
                    const answer = q.answer || q.correct_answer || q.solution;

                    return (
                      <div key={qIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                        <div className="text-xs font-bold text-slate-700">Q{qIdx + 1}: {q.question || q.q || JSON.stringify(q)}</div>
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
                                Answer: {typeof answer === 'string' ? answer : JSON.stringify(answer)}
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
    </div>
  );
}
