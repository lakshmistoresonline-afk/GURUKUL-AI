import React, { useState } from 'react';

interface HindiMasterProps {
  data: any;
}

function renderHindiGrammar(grammar: any): React.ReactNode {
  if (!grammar || typeof grammar !== 'object') return null;
  return (
    <div className="space-y-4">
      {Object.entries(grammar).map(([key, val]: [string, any], idx: number) => {
        if (Array.isArray(val)) {
          return (
            <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-3">
              <div className="text-xs font-black uppercase tracking-wider text-indigo-700">{key.replace(/_/g, ' ')}</div>
              <div className="flex flex-wrap gap-2">
                {val.map((item: any, i: number) => {
                  if (typeof item === 'string') {
                    return <span key={i} className="px-3 py-1.5 bg-indigo-50 border border-indigo-200 rounded-xl text-xs font-bold text-indigo-900">{item}</span>;
                  }
                  return (
                    <div key={i} className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1 w-full sm:w-[48%]">
                      {Object.entries(item).map(([k, v], vIdx) => (
                        <div key={vIdx}><strong className="text-indigo-600 capitalize">{k.replace(/_/g, ' ')}:</strong> {String(v)}</div>
                      ))}
                    </div>
                  );
                })}
              </div>
            </div>
          );
        }
        return (
          <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-1">
            <div className="text-xs font-black uppercase tracking-wider text-indigo-700">{key.replace(/_/g, ' ')}</div>
            <div className="text-xs text-slate-700 leading-relaxed">{String(val)}</div>
          </div>
        );
      })}
    </div>
  );
}

export default function HindiMasterComponent({ data }: HindiMasterProps) {
  const [activeSubTab, setActiveSubTab] = useState<string>('summary');

  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई मास्टर सामग्री उपलब्ध नहीं है।</div>;
  }

  const summary = data.summary || '';
  const poemMeaning = data.poem_meaning || '';
  const characterSketches = data.character_sketches || [];
  const vocab = data.vocabulary || [];
  const grammar = data.grammar || {};
  const questionBank = data.question_bank || [];

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        <button
          onClick={() => setActiveSubTab('summary')}
          className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'summary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
        >
          📖 सारांश एवं भावार्थ (Summary)
        </button>
        {Array.isArray(vocab) && vocab.length > 0 && (
          <button
            onClick={() => setActiveSubTab('vocabulary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'vocabulary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 शब्दार्थ ({vocab.length})
          </button>
        )}
        {grammar && Object.keys(grammar).length > 0 && (
          <button
            onClick={() => setActiveSubTab('grammar')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'grammar' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ✍️ व्याकरण अभ्यास (Grammar)
          </button>
        )}
        {Array.isArray(questionBank) && questionBank.length > 0 && (
          <button
            onClick={() => setActiveSubTab('qa')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'qa' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📋 प्रश्न बैंक ({questionBank.length})
          </button>
        )}
      </div>

      {/* Tab 1: Summary & Poem Meaning */}
      {activeSubTab === 'summary' && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">अध्याय सारांश एवं भावार्थ (Summary & Meaning)</h3>
          {summary && (
            <div className="space-y-1">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">सारांश (Summary)</h4>
              <p className="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap">{summary}</p>
            </div>
          )}
          {poemMeaning && (
            <div className="space-y-1 pt-2">
              <h4 className="text-xs font-black uppercase tracking-widest text-emerald-600">काव्य अर्थ / व्याख्या (Poem Meaning)</h4>
              <p className="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap">{poemMeaning}</p>
            </div>
          )}

          {/* Character Sketches */}
          {Array.isArray(characterSketches) && characterSketches.length > 0 && (
            <div className="pt-4 space-y-3 border-t border-slate-100">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">पात्र परिचय (Character Sketches)</h4>
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
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">शब्दार्थ, पर्यायवाची एवं विलोम (Vocabulary & Meanings)</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {vocab.map((v: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{v.word || v.term}</div>
                <div className="text-xs text-slate-700">अर्थ: {v.meaning || v.definition}</div>
                {v.synonym && <div className="text-xs text-slate-600">पर्यायवाची: {v.synonym}</div>}
                {v.antonym && <div className="text-xs text-slate-600">विलोम: {v.antonym}</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Grammar */}
      {activeSubTab === 'grammar' && grammar && Object.keys(grammar).length > 0 && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">संपूर्ण व्याकरण अभ्यास (Comprehensive Grammar)</h3>
          {renderHindiGrammar(grammar)}
        </div>
      )}

      {/* Tab 4: Question Bank */}
      {activeSubTab === 'qa' && Array.isArray(questionBank) && questionBank.length > 0 && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">प्रश्न बैंक (Question Bank)</h3>
          <div className="space-y-3">
            {questionBank.map((q: any, idx: number) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                <div className="text-xs font-bold text-slate-500">प्रश्न #{idx + 1}</div>
                <div className="text-sm font-bold text-slate-900">{q.question || q.q}</div>
                <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <strong className="text-indigo-600">उत्तर:</strong> {q.answer || q.a}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
