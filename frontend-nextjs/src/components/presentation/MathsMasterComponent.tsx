import React, { useState } from 'react';

interface MathsMasterProps {
  data: any;
}

export default function MathsMasterComponent({ data }: MathsMasterProps) {
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No master practice content available.</div>;
  }

  const coreConcepts = data.core_concepts || [];
  const competencies = data.key_competencies || [];
  const misconceptions = data.common_misconceptions || [];
  const questionBank = data.question_bank || {};

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-8">
      {/* Core Concepts */}
      {Array.isArray(coreConcepts) && coreConcepts.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Core Mathematical Concepts</h3>
          <ul className="space-y-3">
            {coreConcepts.map((cc: string, idx: number) => (
              <li key={idx} className="flex items-start gap-3 p-4 bg-indigo-50/50 border border-indigo-100 rounded-2xl text-slate-800 text-sm font-medium">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-indigo-600 text-white font-bold flex items-center justify-center text-xs">{idx + 1}</span>
                <span>{cc}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Key Competencies */}
      {Array.isArray(competencies) && competencies.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Key Mathematical Competencies</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {competencies.map((comp: string, idx: number) => (
              <div key={idx} className="p-4 bg-emerald-50/50 border border-emerald-100 rounded-2xl text-slate-800 text-sm font-medium">
                ✓ {comp}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Common Misconceptions */}
      {Array.isArray(misconceptions) && misconceptions.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Common Misconceptions to Avoid</h3>
          <div className="space-y-3">
            {misconceptions.map((misc: string, idx: number) => (
              <div key={idx} className="p-4 bg-rose-50/50 border border-rose-100 rounded-2xl text-slate-800 text-sm font-medium flex items-start gap-3">
                <span className="flex-shrink-0 text-rose-600 font-bold">⚠️</span>
                <span>{misc}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Question Bank */}
      {questionBank && Object.keys(questionBank).length > 0 && (
        <div className="space-y-6">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Master Question Bank & Practice</h3>
          {Object.entries(questionBank).map(([sectionKey, qList]: [string, any], sIdx: number) => (
            Array.isArray(qList) && qList.length > 0 && (
              <div key={sIdx} className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
                <h4 className="text-sm font-black uppercase tracking-widest text-indigo-700 bg-indigo-50 p-3 rounded-xl border border-indigo-100">
                  {sectionKey.replace(/_/g, ' ')}
                </h4>
                <div className="space-y-4 pt-2">
                  {qList.map((q: any, qIdx: number) => {
                    const qKey = `${sIdx}-${qIdx}`;
                    const isVisible = showAnswers[qKey];
                    const answer = q.correct_answer || q.final_answer;

                    return (
                      <div key={qIdx} className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-3">
                        <div className="flex items-center justify-between text-xs font-bold text-slate-500">
                          <span>{q.id || `Q${qIdx + 1}`}</span>
                          <span className="px-2 py-0.5 bg-slate-200 text-slate-800 rounded font-mono text-[10px]">{q.type}</span>
                        </div>

                        <div className="text-sm font-bold text-slate-900 leading-snug">
                          {q.question || q.context_scenario || ''}
                        </div>

                        {/* Options if MCQ */}
                        {Array.isArray(q.options) && (
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                            {q.options.map((opt: string, oIdx: number) => (
                              <div key={oIdx} className={`p-3 rounded-xl text-xs font-medium border ${isVisible && opt === answer ? 'bg-emerald-50 border-emerald-300 text-emerald-900 font-bold' : 'bg-white border-slate-200 text-slate-700'}`}>
                                {opt} {isVisible && opt === answer ? '✓' : ''}
                              </div>
                            ))}
                          </div>
                        )}

                        {/* Procedural Steps */}
                        {Array.isArray(q.steps) && (
                          <div className="p-3 bg-indigo-50/40 border border-indigo-100 rounded-xl space-y-1">
                            <div className="text-xs font-bold text-indigo-900">Step-by-Step Solution:</div>
                            <ol className="list-decimal list-inside text-xs text-slate-700 space-y-1">
                              {q.steps.map((step: string, stIdx: number) => (
                                <li key={stIdx}>{step}</li>
                              ))}
                            </ol>
                          </div>
                        )}

                        {/* Sub Questions (Case Study) */}
                        {Array.isArray(q.sub_questions) && (
                          <div className="space-y-2 pt-2">
                            {q.sub_questions.map((sub: any, subIdx: number) => (
                              <div key={subIdx} className="p-3 bg-white border border-slate-200 rounded-xl space-y-1">
                                <div className="text-xs font-bold text-slate-800">({sub.sub_id}) {sub.question}</div>
                                <div className="text-xs text-emerald-700 font-semibold">Answer: {sub.answer}</div>
                              </div>
                            ))}
                          </div>
                        )}

                        {/* Answer Toggle */}
                        {answer && !q.sub_questions && (
                          <div className="pt-2 border-t border-slate-200/60 mt-2">
                            <button
                              onClick={() => toggleAnswer(qKey)}
                              className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                            >
                              {isVisible ? 'Hide Solution ▴' : 'Show Solution ▾'}
                            </button>

                            {isVisible && (
                              <div className="mt-2 p-4 bg-emerald-50/60 border border-emerald-100 rounded-xl text-xs text-slate-800 leading-relaxed space-y-1">
                                <div><strong className="text-emerald-900">Final Answer:</strong> {String(answer)}</div>
                                {q.explanation && <div className="text-slate-600 pt-1"><em>Explanation:</em> {q.explanation}</div>}
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
