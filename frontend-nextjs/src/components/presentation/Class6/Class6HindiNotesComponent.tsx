import React, { useState } from 'react';

interface HindiNotesProps {
  data: any;
}

function renderSafeHindiText(val: any): React.ReactNode {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string' || typeof val === 'number') return val;
  if (Array.isArray(val)) {
    return val.map((item, idx) => (
      <div key={idx} className="my-1">{renderSafeHindiText(item)}</div>
    ));
  }
  if (typeof val === 'object') {
    if (val.question_text) return val.question_text;
    if (val.detailed_answer) return val.detailed_answer;
    if (val.answer) return val.answer;
    if (val.question) return val.question;
    if (val.word && val.meaning) return `${val.word} — ${val.meaning}`;
    if (val.term && val.definition) return `${val.term} — ${val.definition}`;
    if (val.original_text_snippet) return val.original_text_snippet;
    if (val.detailed_explanation_भावार्थ_व्याख्या) return val.detailed_explanation_भावार्थ_व्याख्या;

    return Object.entries(val).map(([k, v], idx) => (
      <div key={idx} className="text-xs">
        <strong className="text-indigo-700 capitalize">{k.replace(/_/g, ' ')}:</strong> {renderSafeHindiText(v)}
      </div>
    ));
  }
  return String(val);
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
                        <div key={vIdx}><strong className="text-indigo-600 capitalize">{k.replace(/_/g, ' ')}:</strong> {renderSafeHindiText(v)}</div>
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
            <div className="text-xs text-slate-700 leading-relaxed">{renderSafeHindiText(val)}</div>
          </div>
        );
      })}
    </div>
  );
}

export default function Class6HindiNotesComponent({ data }: HindiNotesProps) {
  const [activeSubTab, setActiveSubTab] = useState<string>('summary');

  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई नोट्स उपलब्ध नहीं हैं।</div>;
  }

  const genre = data.genre || '';
  const author = data.author_or_poet || '';
  const sec1 = data.section_1_about_author_and_theme || {};
  const sec2 = data.section_2_exhaustive_word_meanings || {};
  const sec3 = data.section_3_stanza_or_paragraph_explanations || [];
  const sec4 = data.section_4_language_and_grammar_भाषा_की_बात || {};
  const sec5 = data.section_5_textbook_exercise_solutions_प्रश्न_उत्तर || [];

  const hasSec1 = sec1 && (typeof sec1 === 'string' || Object.keys(sec1).length > 0);
  const hasSec2 = sec2 && (Array.isArray(sec2) ? sec2.length > 0 : Object.keys(sec2).length > 0);
  const hasSec3 = Array.isArray(sec3) && sec3.length > 0;
  const hasSec4 = sec4 && Object.keys(sec4).length > 0;
  const hasSec5 = Array.isArray(sec5) && sec5.length > 0;

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        {hasSec1 && (
          <button
            onClick={() => setActiveSubTab('summary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'summary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📖 लेखक परिचय एवं व्याख्या
          </button>
        )}
        {hasSec2 && (
          <button
            onClick={() => setActiveSubTab('vocabulary')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'vocabulary' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📚 शब्दार्थ (Vocabulary)
          </button>
        )}
        {hasSec4 && (
          <button
            onClick={() => setActiveSubTab('grammar')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'grammar' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ✍️ भाषा की बात (Grammar)
          </button>
        )}
        {hasSec5 && (
          <button
            onClick={() => setActiveSubTab('qa')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'qa' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📋 प्रश्न-उत्तर (Q&A)
          </button>
        )}
      </div>

      {/* Tab 1: Author & Explanations */}
      {activeSubTab === 'summary' && hasSec1 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <div className="flex flex-wrap items-center gap-3">
            {genre && <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full border border-indigo-200">विधा: {genre}</span>}
            {author && <span className="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full">रचनाकार: {author}</span>}
          </div>

          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">लेखक परिचय एवं केंद्रीय भाव</h3>
          <div className="text-slate-700 text-sm leading-relaxed space-y-2 bg-slate-50 p-4 rounded-2xl border border-slate-100">
            {typeof sec1 === 'string' ? sec1 : (
              <>
                {sec1.author_intro && <p>{sec1.author_intro}</p>}
                {sec1.central_theme && <p className="font-bold text-indigo-900">केंद्रीय भाव: {sec1.central_theme}</p>}
              </>
            )}
          </div>

          {hasSec3 && (
            <div className="space-y-4 pt-4 border-t border-slate-100">
              <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">पद्यांश / गद्यांश व्याख्या</h4>
              {sec3.map((st: any, idx: number) => {
                const textSnippet = st.original_text_snippet || st.text || '';
                const contextStr = st.context_प्रसंग || st.context || '';
                const explanationStr = st.detailed_explanation_भावार्थ_व्याख्या || st.explanation || '';
                const specialties = st.poetic_or_literary_specialties_काव्य_सौंदर्य || st.specialties || [];

                return (
                  <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-3">
                    <div className="text-xs font-bold text-indigo-600 uppercase">गद्यांश / पद्यांश #{idx + 1}</div>
                    {textSnippet && <div className="p-3 bg-slate-50 rounded-xl font-serif text-xs text-slate-900">&ldquo;{textSnippet}&rdquo;</div>}
                    {contextStr && <div className="text-xs text-slate-800 font-medium">{renderSafeHindiText(contextStr)}</div>}
                    {explanationStr && <div className="text-xs text-slate-700 leading-relaxed">{renderSafeHindiText(explanationStr)}</div>}
                    {Array.isArray(specialties) && specialties.length > 0 && (
                      <div className="flex flex-wrap gap-1 pt-1">
                        {specialties.map((sp: string, sIdx: number) => (
                          <span key={sIdx} className="px-2 py-0.5 bg-indigo-50 text-indigo-800 text-[10px] font-bold rounded">{sp}</span>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Tab 2: Vocabulary */}
      {activeSubTab === 'vocabulary' && hasSec2 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">शब्दार्थ एवं शब्दावली (Vocabulary)</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {Array.isArray(sec2) ? (
              sec2.map((v: any, idx: number) => (
                <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                  <div className="text-sm font-extrabold text-indigo-600">{v.word || v.term}</div>
                  <div className="text-xs text-slate-700">अर्थ: {v.meaning || v.definition}</div>
                  {v.sentence_usage && <div className="text-xs font-serif italic text-slate-500">वाक्य: &ldquo;{v.sentence_usage}&rdquo;</div>}
                </div>
              ))
            ) : (
              Object.entries(sec2).map(([word, meaning]: [string, any], idx: number) => (
                <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                  <div className="text-sm font-extrabold text-indigo-600">{word}</div>
                  <div className="text-xs text-slate-700">अर्थ: {renderSafeHindiText(meaning)}</div>
                </div>
              ))
            )}
          </div>
        </div>
      )}

      {/* Tab 3: Grammar */}
      {activeSubTab === 'grammar' && hasSec4 && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">भाषा की बात (Grammar & Language)</h3>
          {renderHindiGrammar(sec4)}
        </div>
      )}

      {/* Tab 4: Q&A */}
      {activeSubTab === 'qa' && hasSec5 && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">पाठ्यपुस्तक प्रश्न-उत्तर (Textbook Solutions)</h3>
          <div className="space-y-3">
            {sec5.map((qa: any, idx: number) => {
              const qText = qa.question_text || qa.question || qa.q || '';
              const aText = qa.detailed_answer || qa.answer || qa.a || '';

              return (
                <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                  <div className="text-xs font-bold text-slate-500">{qa.question_number || `प्रश्न #${idx + 1}`}</div>
                  <div className="text-sm font-bold text-slate-900">{renderSafeHindiText(qText)}</div>
                  <div className="text-xs text-slate-700 bg-slate-50 p-3 rounded-xl border border-slate-100">
                    <strong className="text-indigo-600">उत्तर:</strong> {renderSafeHindiText(aText)}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}
    </div>
  );
}
