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
    return (
      <div className="space-y-2 text-xs">
        {val.case_scenario_task && <div className="font-bold text-indigo-900 bg-indigo-50/60 p-3 rounded-xl border border-indigo-100"><strong>Scenario Task:</strong> {val.case_scenario_task}</div>}
        {val.problem_statement && <div><strong>Problem:</strong> {val.problem_statement}</div>}
        {val.given_data && <div><strong>Given:</strong> {typeof val.given_data === 'object' ? JSON.stringify(val.given_data) : val.given_data}</div>}
        {Array.isArray(val.sub_questions) && (
          <div className="space-y-1.5 pt-1">
            <strong className="text-indigo-800 uppercase tracking-wide text-[11px]">Sub-Questions:</strong>
            {val.sub_questions.map((sq: any, sIdx: number) => (
              <div key={sIdx} className="pl-3 border-l-2 border-indigo-300 py-0.5">{renderSafeText(sq)}</div>
            ))}
          </div>
        )}
        {val.detailed_solution && <div className="text-emerald-900 bg-emerald-50/80 p-3 rounded-xl border border-emerald-100 mt-1"><strong>Detailed Solution:</strong> {val.detailed_solution}</div>}
        {val.solution_steps && <div><strong>Steps:</strong> {renderSafeText(val.solution_steps)}</div>}
        {!val.case_scenario_task && !val.problem_statement && !val.detailed_solution && Object.entries(val).map(([k, v], idx) => (
          <div key={idx} className="space-y-0.5">
            <strong className="capitalize text-indigo-700">{k.replace(/_/g, ' ')}:</strong> {renderSafeText(v)}
          </div>
        ))}
      </div>
    );
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
                    const ans = q.answer || q.correct_answer || q.solution || q.final_answer || q.detailed_solution;

                    return (
                      <div key={qIdx} className="p-5 bg-slate-50 border border-slate-100 rounded-2xl space-y-3 shadow-xs">
                        <div className="text-xs font-bold text-slate-800">Q{qIdx + 1}: {renderSafeText(q.question || q.q || q.problem_statement || q)}</div>

                        {/* Options if MCQ */}
                        {Array.isArray(q.options) && (
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                            {q.options.map((opt: string, oIdx: number) => (
                              <div key={oIdx} className={`p-3 rounded-xl text-xs font-medium border ${opt === ans || (typeof ans === 'string' && opt.startsWith(ans)) ? 'bg-emerald-50 border-emerald-200 text-emerald-900 font-bold' : 'bg-white border-slate-200 text-slate-700'}`}>
                                {opt} {opt === ans || (typeof ans === 'string' && opt.startsWith(ans)) ? '✓' : ''}
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
                              <div className="mt-2 p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-900 space-y-1">
                                <strong>Answer / Solution:</strong> {renderSafeText(ans)}
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
