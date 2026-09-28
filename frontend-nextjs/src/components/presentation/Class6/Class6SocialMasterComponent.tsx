import React, { useState } from 'react';

interface SocialMasterProps {
  data: any;
}

export default function Class6SocialMasterComponent({ data }: SocialMasterProps) {
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No master content available.</div>;
  }

  const keywords = data.keywords_and_definitions || {};
  const notes = data.exhaustive_notes || [];
  const questionBank = data.question_bank || {};

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-8">
      {/* Keywords & Definitions */}
      {keywords && Object.keys(keywords).length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Keywords & Definitions</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(keywords).map(([term, def]: [string, any], idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{term}</div>
                <div className="text-xs text-slate-700">{typeof def === 'string' ? def : JSON.stringify(def)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Exhaustive Notes */}
      {Array.isArray(notes) && notes.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Exhaustive Master Notes</h3>
          <div className="space-y-4">
            {notes.map((item: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-2">
                <div className="text-xs font-black uppercase text-indigo-600">{item.title || item.heading || `Note #${idx + 1}`}</div>
                <p className="text-slate-700 text-sm leading-relaxed">{item.content || item.description || JSON.stringify(item)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Question Bank */}
      {questionBank && Object.keys(questionBank).length > 0 && (
        <div className="space-y-6">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Master Question Bank</h3>
          {Object.entries(questionBank).map(([qType, qArr]: [string, any], tIdx: number) => (
            Array.isArray(qArr) && qArr.length > 0 && (
              <div key={tIdx} className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
                <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">{qType.replace(/_/g, ' ')}</h4>
                <div className="space-y-4">
                  {qArr.map((q: any, qIdx: number) => {
                    const qKey = `${tIdx}-${qIdx}`;
                    const isVisible = showAnswers[qKey];
                    const ans = q.answer || q.correct_answer || q.solution;

                    return (
                      <div key={qIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                        <div className="text-xs font-bold text-slate-700">Q{qIdx + 1}: {q.question || q.q || JSON.stringify(q)}</div>
                        {ans && (
                          <div className="pt-2 border-t border-slate-200/60 mt-2">
                            <button
                              onClick={() => toggleAnswer(qKey)}
                              className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                            >
                              {isVisible ? 'Hide Answer ▴' : 'Show Answer ▾'}
                            </button>
                            {isVisible && (
                              <div className="mt-2 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-medium">
                                Answer: {typeof ans === 'string' ? ans : JSON.stringify(ans)}
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
