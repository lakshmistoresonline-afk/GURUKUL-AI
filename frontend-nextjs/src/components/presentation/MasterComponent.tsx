import React, { useState } from 'react';
import HindiMasterComponent from './HindiMasterComponent';
import MathsMasterComponent from './MathsMasterComponent';
import ScienceMasterComponent from './ScienceMasterComponent';

interface MasterProps {
  data: any;
  subject?: string;
}

export default function MasterComponent({ data, subject }: MasterProps) {
  const [activeSubTab, setActiveSubTab] = useState<string>('summary');

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

  const hasObj = objectiveQ && Object.keys(objectiveQ).length > 0;
  const hasExt = Array.isArray(extracts) && extracts.length > 0;
  const hasPrompts = Array.isArray(prompts) && prompts.length > 0;
  const hasLit = literature && Object.keys(literature).length > 0;
  const hasGrammar = grammar && Object.keys(grammar).length > 0;

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        <button
          onClick={() => setActiveSubTab('summary')}
          className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'summary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
        >
          ⚡ Summary & Theme
        </button>
        {vocab.length > 0 && (
          <button
            onClick={() => setActiveSubTab('vocabulary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'vocabulary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 Vocabulary ({vocab.length})
          </button>
        )}
        {hasObj && (
          <button
            onClick={() => setActiveSubTab('objective')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'objective' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📝 Objective Questions
          </button>
        )}
        {hasExt && (
          <button
            onClick={() => setActiveSubTab('extracts')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'extracts' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📖 Reading Extracts ({extracts.length})
          </button>
        )}
        {hasPrompts && (
          <button
            onClick={() => setActiveSubTab('prompts')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'prompts' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ✍️ Writing Prompts ({prompts.length})
          </button>
        )}
        {(hasLit || hasGrammar) && (
          <button
            onClick={() => setActiveSubTab('literature')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'literature' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📋 Literature & Grammar
          </button>
        )}
      </div>

      {/* Tab 1: Summary & Theme */}
      {activeSubTab === 'summary' && summary && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
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

      {/* Tab 2: Vocabulary */}
      {activeSubTab === 'vocabulary' && Array.isArray(vocab) && vocab.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
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

      {/* Tab 3: Objective Questions */}
      {activeSubTab === 'objective' && hasObj && (
        <div className="space-y-4 animate-in fade-in duration-200">
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
                        {q.explanation && (
                          <div className="text-xs text-slate-500 pt-1 italic">Explanation: {q.explanation}</div>
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

      {/* Tab 4: Reading Extracts */}
      {activeSubTab === 'extracts' && hasExt && (
        <div className="space-y-4 animate-in fade-in duration-200">
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
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 5: Writing Prompts */}
      {activeSubTab === 'prompts' && hasPrompts && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Creative & Writing Prompts</h3>
          <div className="space-y-4">
            {prompts.map((p: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="text-sm font-bold text-slate-900">{p.topic || p.prompt_title || p.title || ''}</div>
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

      {/* Tab 6: Literature & Grammar */}
      {activeSubTab === 'literature' && (hasLit || hasGrammar) && (
        <div className="space-y-6 animate-in fade-in duration-200">
          {hasLit && (
            <div className="space-y-4">
              <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Literature Questions & Answers</h3>
              <div className="space-y-3">
                {Array.isArray(literature) ? (
                  literature.map((lit: any, idx: number) => (
                    <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                      <div className="text-sm font-bold text-slate-900">{lit.question || lit.q || ''}</div>
                      <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
                        <strong className="text-indigo-600">Answer:</strong> {lit.answer || lit.a || ''}
                      </div>
                    </div>
                  ))
                ) : (
                  Object.entries(literature).map(([category, qList]: [string, any], catIdx: number) => (
                    Array.isArray(qList) && qList.length > 0 && (
                      <div key={catIdx} className="space-y-3">
                        <h4 className="text-sm font-extrabold text-indigo-700 uppercase tracking-wider">{category.replace(/_/g, ' ')}</h4>
                        {qList.map((lit: any, idx: number) => (
                          <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                            <div className="text-sm font-bold text-slate-900">{lit.question || lit.q || ''}</div>
                            <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
                              <strong className="text-indigo-600">Answer:</strong> {lit.answer || lit.a || ''}
                            </div>
                          </div>
                        ))}
                      </div>
                    )
                  ))
                )}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
