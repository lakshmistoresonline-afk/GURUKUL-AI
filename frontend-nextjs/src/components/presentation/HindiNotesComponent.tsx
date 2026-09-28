import React, { useState } from 'react';

interface HindiNotesProps {
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

export default function HindiNotesComponent({ data }: HindiNotesProps) {
  const [activeSubTab, setActiveSubTab] = useState<string>('summary');

  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई नोट्स उपलब्ध नहीं हैं।</div>;
  }

  const genre = data.genre || '';
  const author = data.author || '';
  const themeAndMoral = data.core_theme_and_moral || {};
  const summaryAndExp = data.detailed_summary_and_explanation || {};
  const characterSketches = data.character_and_element_sketches || [];
  const vocabulary = data.exhaustive_vocabulary || data.vocabulary || [];
  const grammar = data.comprehensive_grammar || data.grammar || {};
  const questionBank = data.question_bank || data.comprehension_and_extracts || [];

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
        {vocabulary.length > 0 && (
          <button
            onClick={() => setActiveSubTab('vocabulary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'vocabulary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 शब्दार्थ ({vocabulary.length})
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
        {questionBank.length > 0 && (
          <button
            onClick={() => setActiveSubTab('qa')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'qa' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📋 प्रश्न बैंक ({questionBank.length})
          </button>
        )}
      </div>

      {/* Tab 1: Summary & Theme */}
      {activeSubTab === 'summary' && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <div className="flex flex-wrap items-center gap-3">
            {genre && <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full border border-indigo-200">विधा: {genre}</span>}
            {author && <span className="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full">रचनाकार: {author}</span>}
          </div>

          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">अध्याय सारांश एवं व्याख्या</h3>

          {themeAndMoral && (
            <div className="p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl text-indigo-900 text-xs space-y-1">
              {themeAndMoral.central_theme && <div><strong>केंद्रीय भाव:</strong> {themeAndMoral.central_theme}</div>}
              {themeAndMoral.moral_lesson && <div><strong>नैतिक शिक्षा:</strong> {themeAndMoral.moral_lesson}</div>}
            </div>
          )}

          {summaryAndExp.overview && (
            <div className="space-y-1">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">अवलोकन (Overview)</h4>
              <p className="text-slate-700 text-sm leading-relaxed whitespace-pre-wrap">{summaryAndExp.overview}</p>
            </div>
          )}

          {Array.isArray(characterSketches) && characterSketches.length > 0 && (
            <div className="pt-4 space-y-3 border-t border-slate-100">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">पात्र परिचय (Character Sketches)</h4>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {characterSketches.map((cs: any, cIdx: number) => (
                  <div key={cIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                    <div className="text-sm font-extrabold text-slate-900">{cs.name || cs.character}</div>
                    <div className="text-xs text-slate-700 leading-relaxed">{cs.traits || cs.profile}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Vocabulary */}
      {activeSubTab === 'vocabulary' && Array.isArray(vocabulary) && vocabulary.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">शब्दार्थ एवं पर्यायवाची (Vocabulary)</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {vocabulary.map((v: any, idx: number) => (
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
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">संपूर्ण व्याकरण (Comprehensive Grammar)</h3>
          {renderHindiGrammar(grammar)}
        </div>
      )}

      {/* Tab 4: Q&A */}
      {activeSubTab === 'qa' && Array.isArray(questionBank) && questionBank.length > 0 && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">प्रश्न बैंक एवं अभ्यास (Question Bank)</h3>
          <div className="space-y-3">
            {questionBank.map((qa: any, idx: number) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                <div className="text-xs font-bold text-slate-500">प्रश्न #{idx + 1}</div>
                <div className="text-sm font-bold text-slate-900">{qa.question || qa.q}</div>
                <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
                  <strong className="text-indigo-600">उत्तर:</strong> {qa.answer || qa.a}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
