import React from 'react';
import HindiMasterComponent from './HindiMasterComponent';
import MathsMasterComponent from './MathsMasterComponent';
import ScienceMasterComponent from './ScienceMasterComponent';

interface MasterProps {
  data: any;
  subject?: string;
}

export default function MasterComponent({ data, subject }: MasterProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No master practice content available.</div>;
  }

  // Check if this is Hindi schema
  if (data.poem_meaning || (data.summary && typeof data.summary === 'string' && data.vocabulary && data.grammar)) {
    return <HindiMasterComponent data={data} />;
  }

  // Check if this is Maths schema
  if (data.core_concepts || data.key_competencies) {
    return <MathsMasterComponent data={data} />;
  }

  // Check if this is Science schema
  if (Array.isArray(data.concepts) || data.experiments_and_activities) {
    return <ScienceMasterComponent data={data} />;
  }

  const summary = data.summary_and_theme || data.summary || {};
  const characterSketches = summary.character_sketches || [];
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
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Master Summary & Theme</h3>
          <p className="text-slate-700 text-sm leading-relaxed">
            {typeof summary === 'string' ? summary : summary.summary || summary.overview || JSON.stringify(summary)}
          </p>
          {summary.core_theme && (
            <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl text-indigo-900 text-xs font-bold">
              Core Theme: {typeof summary.core_theme === 'string' ? summary.core_theme : JSON.stringify(summary.core_theme)}
            </div>
          )}

          {/* Character Sketches */}
          {Array.isArray(characterSketches) && characterSketches.length > 0 && (
            <div className="pt-4 space-y-3 border-t border-slate-100">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">Character Profiles</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {characterSketches.map((cs: any, cIdx: number) => (
                  <div key={cIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                    <div className="text-sm font-extrabold text-slate-900">{cs.name || cs.character}</div>
                    <div className="text-xs text-slate-700 leading-relaxed">{cs.profile || cs.traits}</div>
                  </div>
                ))}
              </div>
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
                {v.phonics && <div className="text-[11px] font-mono text-slate-400">Phonics: {v.phonics}</div>}
                {v.sentence || v.example ? (
                  <div className="text-xs font-serif italic text-slate-500 pt-1">Example: &ldquo;{v.sentence || v.example}&rdquo;</div>
                ) : null}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Objective Question Bank (MCQs, Fill in blanks, True/False, Match Following) */}
      {objectiveQ && Object.keys(objectiveQ).length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Objective Question Bank</h3>
          {Object.entries(objectiveQ).map(([qType, qArr]: [string, any], tIdx: number) => (
            Array.isArray(qArr) && qArr.length > 0 && (
              <div key={tIdx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
                <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">{qType.replace(/_/g, ' ')}</h4>
                <div className="space-y-4">
                  {qArr.map((q: any, qIdx: number) => {
                    const qText = q.question || q.statement || (qType === 'match_following' ? 'Match the following columns:' : null);
                    return (
                      <div key={qIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                        {qText && <div className="text-xs font-bold text-slate-700">Q{qIdx + 1}: {qText}</div>}

                        {/* Match Following Columns / Pairs */}
                        {qType === 'match_following' && (
                          <div className="space-y-2 pt-1">
                            {Array.isArray(q.pairs) ? (
                              <div className="grid grid-cols-2 gap-2 text-xs">
                                {q.pairs.map((pair: any, pIdx: number) => (
                                  <React.Fragment key={pIdx}>
                                    <div className="p-2 bg-white border border-slate-200 rounded-xl font-semibold">{pair.a || pair.column_a}</div>
                                    <div className="p-2 bg-indigo-50 border border-indigo-100 rounded-xl font-semibold text-indigo-900">{pair.b || pair.column_b}</div>
                                  </React.Fragment>
                                ))}
                              </div>
                            ) : (
                              <div className="grid grid-cols-2 gap-2 text-xs">
                                <div>
                                  <strong>Column A:</strong>
                                  <ul className="list-disc list-inside">{q.column_a?.map((item: string, i: number) => <li key={i}>{item}</li>)}</ul>
                                </div>
                                <div>
                                  <strong>Column B:</strong>
                                  <ul className="list-disc list-inside">{q.column_b?.map((item: string, i: number) => <li key={i}>{item}</li>)}</ul>
                                </div>
                              </div>
                            )}
                          </div>
                        )}

                        {/* Options */}
                        {Array.isArray(q.options) && (
                          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                            {q.options.map((opt: string, oIdx: number) => (
                              <div key={oIdx} className={`p-2.5 rounded-xl text-xs font-medium border ${opt === q.correct_answer ? 'bg-emerald-50 border-emerald-200 text-emerald-900' : 'bg-white border-slate-200 text-slate-700'}`}>
                                {opt} {opt === q.correct_answer ? '✓' : ''}
                              </div>
                            ))}
                          </div>
                        )}

                        {q.correct_answer && !q.options && qType !== 'match_following' && (
                          <div className="text-xs text-emerald-700 font-semibold pt-1">Answer: {String(q.correct_answer)}</div>
                        )}
                        {q.is_true !== undefined && (
                          <div className="text-xs text-indigo-700 font-semibold pt-1">Answer: {q.is_true ? 'True' : 'False'}</div>
                        )}
                        {q.explanation && (
                          <div className="text-xs text-slate-500 pt-1 italic">Explanation: {q.explanation}</div>
                        )}
                        {q.justification && (
                          <div className="text-xs text-slate-500 pt-1 italic">Justification: {q.justification}</div>
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

      {/* Writing Prompts */}
      {Array.isArray(prompts) && prompts.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Creative & Writing Prompts</h3>
          <div className="space-y-4">
            {prompts.map((p: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="flex items-center justify-between">
                  <div className="text-xs font-bold text-purple-600 uppercase">Prompt #{idx + 1}</div>
                  {p.format && <span className="text-[11px] font-bold bg-purple-50 text-purple-700 px-2.5 py-1 rounded-full border border-purple-200">{p.format}</span>}
                </div>
                <div className="text-sm font-bold text-slate-900">{p.topic || p.prompt_title || p.title || ''}</div>

                {/* Hints */}
                {Array.isArray(p.hints) && p.hints.length > 0 && (
                  <div className="p-4 bg-purple-50/50 border border-purple-100 rounded-2xl space-y-1">
                    <div className="text-xs font-bold text-purple-800 uppercase tracking-wider">Guiding Hints:</div>
                    <ul className="list-disc list-inside text-xs text-slate-700 space-y-1">
                      {p.hints.map((h: string, hIdx: number) => (
                        <li key={hIdx}>{h}</li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Model Answer */}
                {p.model_answer && (
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl space-y-1">
                    <div className="text-xs font-bold text-slate-600 uppercase tracking-wider">Model Answer / Example:</div>
                    <p className="text-xs text-slate-700 font-serif leading-relaxed">{p.model_answer}</p>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Literature Questions */}
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
                  <div className="text-sm font-bold text-slate-900">{g.exercise_title || g.title || g.topic || g.type || ''}</div>
                  {g.instruction && <p className="text-xs font-medium text-slate-800">{g.instruction}</p>}

                  {/* Grammar Items / Sub-questions */}
                  {Array.isArray(g.items) && g.items.length > 0 && (
                    <div className="space-y-2 pt-2">
                      {g.items.map((item: any, iIdx: number) => (
                        <div key={iIdx} className="p-3 bg-slate-50 border border-slate-100 rounded-xl space-y-1">
                          <div className="text-xs font-bold text-slate-700">Item #{iIdx + 1}: {item.q || item.question || item.statement || ''}</div>
                          {item.a && <div className="text-xs text-emerald-700 font-semibold">Answer: {item.a}</div>}
                          {item.answer && <div className="text-xs text-emerald-700 font-semibold">Answer: {item.answer}</div>}
                          {item.explanation && <div className="text-xs text-slate-500 italic">Explanation: {item.explanation}</div>}
                        </div>
                      ))}
                    </div>
                  )}
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
