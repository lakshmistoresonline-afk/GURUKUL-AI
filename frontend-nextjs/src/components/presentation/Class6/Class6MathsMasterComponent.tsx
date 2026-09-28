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
    if (val.problem_statement) return (
      <div className="space-y-1">
        <strong>Problem:</strong> {val.problem_statement}
        {val.given_data && <div><em>Given:</em> {JSON.stringify(val.given_data)}</div>}
        {val.solution_steps && <div><em>Steps:</em> {renderSafeText(val.solution_steps)}</div>}
      </div>
    );
    return Object.entries(val).map(([k, v], idx) => (
      <div key={idx} className="text-xs space-y-0.5">
        <strong className="capitalize text-indigo-700">{k.replace(/_/g, ' ')}:</strong> {renderSafeText(v)}
      </div>
    ));
  }
  return String(val);
}

interface MathsMasterProps {
  data: any;
}

export default function Class6MathsMasterComponent({ data }: MathsMasterProps) {
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No master content available.</div>;
  }

  const cheatSheet = data.section_1_quick_revision_cheat_sheet || [];
  const pitfalls = data.section_2_common_pitfalls_and_error_analysis || [];
  const questionBank = data.section_3_categorized_exam_question_bank || {};

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-8">
      {/* Cheat Sheet */}
      {Array.isArray(cheatSheet) && cheatSheet.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Quick Revision Cheat Sheet</h3>
          <ul className="space-y-3">
            {cheatSheet.map((item: any, idx: number) => (
              <li key={idx} className="flex items-start gap-3 p-4 bg-indigo-50/50 border border-indigo-100 rounded-2xl text-slate-800 text-sm font-medium">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-xs">{idx + 1}</span>
                <span>{renderSafeText(item)}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Pitfalls */}
      {Array.isArray(pitfalls) && pitfalls.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Common Pitfalls & Error Analysis</h3>
          <div className="space-y-3">
            {pitfalls.map((p: any, idx: number) => (
              <div key={idx} className="p-4 bg-rose-50/50 border border-rose-100 rounded-2xl text-slate-800 text-sm font-medium flex items-start gap-3">
                <span className="flex-shrink-0 text-rose-600 font-bold">⚠️</span>
                <span>{renderSafeText(p)}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Question Bank */}
      {questionBank && Object.keys(questionBank).length > 0 && (
        <div className="space-y-6">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Categorized Exam Question Bank</h3>
          {Object.entries(questionBank).map(([qType, qArr]: [string, any], tIdx: number) => (
            Array.isArray(qArr) && qArr.length > 0 && (
              <div key={tIdx} className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
                <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">{qType.replace(/_/g, ' ')}</h4>
                <div className="space-y-4">
                  {qArr.map((q: any, qIdx: number) => {
                    const qKey = `${tIdx}-${qIdx}`;
                    const isVisible = showAnswers[qKey];
                    const ans = q.answer || q.correct_answer || q.solution || q.final_answer;

                    return (
                      <div key={qIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                        <div className="text-xs font-bold text-slate-700">Q{qIdx + 1}: {renderSafeText(q.question || q.q || q.problem_statement || q)}</div>

                        {/* Options if MCQ */}
                        {Array.isArray(q.options) && (
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                            {q.options.map((opt: string, oIdx: number) => (
                              <div key={oIdx} className={`p-2.5 rounded-xl text-xs font-medium border ${opt === ans ? 'bg-emerald-50 border-emerald-200 text-emerald-900' : 'bg-white border-slate-200 text-slate-700'}`}>
                                {opt} {opt === ans ? '✓' : ''}
                              </div>
                            ))}
                          </div>
                        )}

                        {ans && (
                          <div className="pt-2 border-t border-slate-200/60 mt-2">
                            <button
                              onClick={() => toggleAnswer(qKey)}
                              className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                            >
                              {isVisible ? 'Hide Solution ▴' : 'Show Solution ▾'}
                            </button>
                            {isVisible && (
                              <div className="mt-2 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-medium">
                                Answer / Solution: {renderSafeText(ans)}
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
