import React, { useState } from 'react';

interface Class6MasterProps {
  data: any;
}

function renderSafeText(val: any): React.ReactNode {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string' || typeof val === 'number') return val;
  if (Array.isArray(val)) {
    return val.map((item, idx) => (
      <div key={idx} className="my-1">{renderSafeText(item)}</div>
    ));
  }
  if (typeof val === 'object') {
    if (val.text) return (
      <div className="space-y-1">
        <p>{val.text}</p>
        {Array.isArray(val.takeaways) && val.takeaways.length > 0 && (
          <div className="text-[11px] font-medium text-amber-800 bg-amber-50 p-2 rounded-xl">
            <strong>Takeaways:</strong> {val.takeaways.join(' | ')}
          </div>
        )}
      </div>
    );
    if (val.name && val.role) return (
      <div className="space-y-1">
        <strong>{val.name}</strong> ({val.role})
        {val.traits && <div><em>Traits:</em> {Array.isArray(val.traits) ? val.traits.join(', ') : val.traits}</div>}
        {val.arc && <div><em>Arc:</em> {val.arc}</div>}
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

export default function Class6MasterComponent({ data }: Class6MasterProps) {
  const [activeSubTab, setActiveSubTab] = useState<string>('overview');
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return <div className="p-8 text-center text-slate-500">No master content available.</div>;
  }

  const overview = data.m1_overview || {};
  const vocabulary = data.m2_vocabulary || {};
  const textual = data.m3_textual || {};
  const questionBank = data.m4_question_bank || {};
  const grammar = data.m5_grammar || {};
  const extensions = data.m6_extensions || {};

  const hasOverview = overview && Object.keys(overview).length > 0;
  const hasVocab = vocabulary && Object.keys(vocabulary).length > 0;
  const hasTextual = textual && Object.keys(textual).length > 0;
  const hasQBank = questionBank && Object.keys(questionBank).length > 0;
  const hasGrammar = grammar && Object.keys(grammar).length > 0;

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        {hasOverview && (
          <button
            onClick={() => setActiveSubTab('overview')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'overview' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ⚡ Summary & Theme
          </button>
        )}
        {hasVocab && (
          <button
            onClick={() => setActiveSubTab('vocabulary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'vocabulary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 Vocabulary ({Object.keys(vocabulary).length})
          </button>
        )}
        {hasTextual && (
          <button
            onClick={() => setActiveSubTab('textual')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'textual' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📖 Textual Analysis
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
        {hasGrammar && (
          <button
            onClick={() => setActiveSubTab('grammar')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'grammar' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ✍️ Grammar Practice
          </button>
        )}
      </div>

      {/* Tab 1: Overview / Summary */}
      {activeSubTab === 'overview' && hasOverview && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Master Summary & Theme</h3>

          {Array.isArray(overview.summary) && (
            <div className="space-y-3">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">Chapter Synopsis</h4>
              {overview.summary.map((sumItem: any, sIdx: number) => (
                <div key={sIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl text-xs text-slate-800 leading-relaxed space-y-1">
                  {renderSafeText(sumItem)}
                </div>
              ))}
            </div>
          )}

          {Array.isArray(overview.characters) && overview.characters.length > 0 && (
            <div className="space-y-3 pt-3 border-t border-slate-100">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">Character Profiles</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {overview.characters.map((char: any, cIdx: number) => (
                  <div key={cIdx} className="p-4 bg-indigo-50/40 border border-indigo-100 rounded-2xl text-xs space-y-1">
                    {renderSafeText(char)}
                  </div>
                ))}
              </div>
            </div>
          )}

          {overview.thematic_analysis && (
            <div className="space-y-2 pt-3 border-t border-slate-100">
              <h4 className="text-xs font-black uppercase tracking-widest text-amber-600">Thematic Analysis</h4>
              <div className="p-4 bg-amber-50/50 border border-amber-100 rounded-2xl text-xs text-slate-800 space-y-1">
                {renderSafeText(overview.thematic_analysis)}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Vocabulary */}
      {activeSubTab === 'vocabulary' && hasVocab && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Vocabulary & Key Terms</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Object.entries(vocabulary).map(([term, def]: [string, any], idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{term}</div>
                <div className="text-xs text-slate-700">{renderSafeText(def)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Textual Analysis */}
      {activeSubTab === 'textual' && hasTextual && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Textual Analysis</h3>
          <div className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-2xl">
            {renderSafeText(textual)}
          </div>
        </div>
      )}

      {/* Tab 4: Question Bank */}
      {activeSubTab === 'qbank' && hasQBank && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Master Question Bank</h3>
          <div className="space-y-4">
            {Object.entries(questionBank).map(([qCat, qList]: [string, any], catIdx: number) => (
              Array.isArray(qList) && qList.length > 0 && (
                <div key={catIdx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                  <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">{qCat.replace(/_/g, ' ')}</h4>
                  <div className="space-y-3">
                    {qList.map((q: any, qIdx: number) => {
                      const qKey = `${catIdx}-${qIdx}`;
                      const isVisible = showAnswers[qKey];
                      const ans = q.answer || q.correct_answer || q.solution;

                      return (
                        <div key={qIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                          <div className="text-xs font-bold text-slate-800">Q{qIdx + 1}: {renderSafeText(q.question || q.q || q.statement || q)}</div>
                          {ans && (
                            <div className="pt-2 border-t border-slate-200/60">
                              <button
                                onClick={() => toggleAnswer(qKey)}
                                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                              >
                                {isVisible ? 'Hide Answer ▴' : 'Show Answer ▾'}
                              </button>
                              {isVisible && (
                                <div className="mt-2 p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-medium">
                                  Answer: {renderSafeText(ans)}
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

      {/* Tab 5: Grammar */}
      {activeSubTab === 'grammar' && hasGrammar && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">Grammar & Language Practice</h3>
          <div className="text-xs text-slate-700 leading-relaxed bg-slate-50 p-4 rounded-2xl">
            {renderSafeText(grammar)}
          </div>
        </div>
      )}
    </div>
  );
}
