import React, { useState } from 'react';

interface HindiMasterProps {
  data: any;
}

export default function Class6HindiMasterComponent({ data }: HindiMasterProps) {
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई मास्टर सामग्री उपलब्ध नहीं है।</div>;
  }

  const sec1 = data.section_1_author_and_central_theme || {};
  const sec2 = data.section_2_exhaustive_vocabulary_matrix || {};
  const sec3 = data.section_3_stanza_or_paragraph_explanations || [];
  const sec4 = data.section_4_character_sketches_and_summaries || {};
  const sec5 = data.section_5_bhasha_ki_baat_grammar_guide || {};
  const sec7 = data.section_7_exam_question_bank || {};

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-8">
      {/* Author & Central Theme */}
      {sec1 && Object.keys(sec1).length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">लेखक एवं केंद्रीय भाव (Author & Theme)</h3>
          {sec1.author_intro && <p className="text-slate-700 text-sm leading-relaxed">{sec1.author_intro}</p>}
          {sec1.central_theme && <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl text-indigo-900 text-xs font-bold">केंद्रीय भाव: {sec1.central_theme}</div>}
        </div>
      )}

      {/* Vocabulary Matrix */}
      {sec2 && Object.keys(sec2).length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">शब्द भंडार (Vocabulary Matrix)</h3>
          <pre className="whitespace-pre-wrap font-sans text-xs text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-2xl overflow-x-auto">
            {JSON.stringify(sec2, null, 2)}
          </pre>
        </div>
      )}

      {/* Stanza Explanations */}
      {Array.isArray(sec3) && sec3.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">व्याख्या एवं भावार्थ</h3>
          <div className="space-y-4">
            {sec3.map((st: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-2">
                <div className="text-xs font-black uppercase text-indigo-600">पद्यांश / गद्यांश #{idx + 1}</div>
                {st.text && <div className="p-4 bg-slate-50 rounded-2xl font-serif text-sm text-slate-900">{st.text}</div>}
                <p className="text-slate-700 text-sm leading-relaxed">{st.explanation || st.meaning || JSON.stringify(st)}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Question Bank */}
      {sec7 && Object.keys(sec7).length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">प्रश्न बैंक (Question Bank)</h3>
          <div className="space-y-4">
            {Object.entries(sec7).map(([qType, qList]: [string, any], catIdx: number) => (
              Array.isArray(qList) && qList.length > 0 && (
                <div key={catIdx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                  <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">{qType.replace(/_/g, ' ')}</h4>
                  <div className="space-y-3">
                    {qList.map((q: any, qIdx: number) => {
                      const qKey = `${catIdx}-${qIdx}`;
                      const isVisible = showAnswers[qKey];
                      const ans = q.answer || q.correct_answer;

                      return (
                        <div key={qIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                          <div className="text-xs font-bold text-slate-800">प्रश्नोत्तरी #{qIdx + 1}: {q.question || q.q || JSON.stringify(q)}</div>
                          {ans && (
                            <div className="pt-2 border-t border-slate-200/60">
                              <button
                                onClick={() => toggleAnswer(qKey)}
                                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                              >
                                {isVisible ? 'उत्तर छिपाएँ ▴' : 'उत्तर देखें ▾'}
                              </button>
                              {isVisible && (
                                <div className="mt-2 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-medium">
                                  उत्तर: {typeof ans === 'string' ? ans : JSON.stringify(ans)}
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
        </div>
      )}
    </div>
  );
}
