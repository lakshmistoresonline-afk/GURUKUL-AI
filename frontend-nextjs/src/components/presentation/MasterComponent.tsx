import React from 'react';

interface MasterProps {
  data: any;
}

export default function MasterComponent({ data }: MasterProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No master practice content available.</div>;
  }

  const summary = data.summary_and_theme || data.summary || {};
  const vocab = data.vocabulary || [];
  const objectiveQ = data.objective_questions || {};
  const extracts = data.reading_extracts || [];
  const prompts = data.writing_prompts || [];
  const grammar = data.grammar_exercises || [];
  const literature = data.literature_questions || {};

  return (
    <div className="space-y-8">
      {/* Summary & Theme */}
      {summary && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Master Summary & Theme</h3>
          <p className="text-slate-700 text-sm leading-relaxed">
            {typeof summary === 'string' ? summary : summary.summary || summary.overview || JSON.stringify(summary)}
          </p>
          {summary.core_theme && (
            <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl text-indigo-900 text-xs font-bold">
              Core Theme: {typeof summary.core_theme === 'string' ? summary.core_theme : JSON.stringify(summary.core_theme)}
            </div>
          )}
        </div>
      )}

      {/* Vocabulary */}
      {Array.isArray(vocab) && vocab.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Vocabulary & Meanings</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {vocab.map((v: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{v.word || v.term || ''}</div>
                <div className="text-xs text-slate-700">{v.meaning || v.definition || ''}</div>
                {v.sentence || v.example ? (
                  <div className="text-xs font-serif italic text-slate-500 pt-1">Example: &ldquo;{v.sentence || v.example}&rdquo;</div>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Reading Extracts */}
      {Array.isArray(extracts) && extracts.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Reading Extracts & Comprehension</h3>
          <div className="space-y-4">
            {extracts.map((ex: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-600">Extract #{idx + 1}</div>
                {ex.extract_text && (
                  <div className="p-4 bg-slate-50 border border-slate-100 rounded-2xl font-serif italic text-slate-800 text-sm leading-relaxed">
                    &ldquo;{ex.extract_text}&rdquo;
                  </div>
                )}
                {Array.isArray(ex.questions) && (
                  <div className="space-y-2 pt-2">
                    {ex.questions.map((q: any, qIdx: number) => (
                      <div key={qIdx} className="p-3 bg-indigo-50/40 border border-indigo-100 rounded-xl text-xs text-slate-800 font-medium">
                        Q{qIdx + 1}: {typeof q === 'string' ? q : q.question || q.q || JSON.stringify(q)}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Literature Questions (Handling Object with short_answer / long_answer or Array) */}
      {literature && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Literature Questions & Answers</h3>
          {Array.isArray(literature) ? (
            <div className="space-y-3">
              {literature.map((lit: any, idx: number) => (
                <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                  <div className="text-xs font-bold text-slate-500">Question #{idx + 1}</div>
                  <div className="text-sm font-bold text-slate-900">{lit.question || lit.q || ''}</div>
                  <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <strong className="text-indigo-600">Answer:</strong> {lit.answer || lit.a || ''}
                  </div>
                </div>
              ))}
            </div>
          ) : typeof literature === 'object' ? (
            <div className="space-y-6">
              {Object.entries(literature).map(([category, qList]: [string, any], catIdx: number) => (
                Array.isArray(qList) && qList.length > 0 && (
                  <div key={catIdx} className="space-y-3">
                    <h4 className="text-sm font-extrabold text-indigo-700 uppercase tracking-wider">{category.replace(/_/g, ' ')}</h4>
                    <div className="space-y-3">
                      {qList.map((lit: any, idx: number) => (
                        <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                          <div className="text-xs font-bold text-slate-500">Question #{idx + 1}</div>
                          <div className="text-sm font-bold text-slate-900">{lit.question || lit.q || ''}</div>
                          <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100 space-y-1">
                            <div><strong className="text-indigo-600">Answer:</strong> {lit.answer || lit.a || ''}</div>
                            {lit.explanation && <div className="text-slate-500 pt-1"><em>Explanation:</em> {lit.explanation}</div>}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )
              ))}
            </div>
          ) : null}
        </div>
      )}

      {/* Grammar Exercises */}
      {grammar && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Grammar & Language Practice</h3>
          {Array.isArray(grammar) && grammar.length > 0 ? (
            <div className="space-y-3">
              {grammar.map((g: any, idx: number) => (
                <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                  <div className="text-xs font-bold text-emerald-600 uppercase">Exercise #{idx + 1}</div>
                  <div className="text-sm font-bold text-slate-900">{g.exercise_title || g.title || g.topic || ''}</div>
                  <p className="text-xs text-slate-700">{g.description || g.instruction || JSON.stringify(g)}</p>
                </div>
              ))}
            </div>
          ) : typeof grammar === 'object' ? (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm">
              <pre className="whitespace-pre-wrap font-sans text-xs text-slate-700 leading-relaxed overflow-x-auto">
                {JSON.stringify(grammar, null, 2)}
              </pre>
            </div>
          ) : null}
        </div>
      )}
    </div>
  );
}
