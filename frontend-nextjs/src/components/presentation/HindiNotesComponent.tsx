import React from 'react';

interface HindiNotesProps {
  data: any;
}

export default function HindiNotesComponent({ data }: HindiNotesProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई नोट्स उपलब्ध नहीं हैं।</div>;
  }

  const genre = data.genre || '';
  const author = data.author || '';
  const coreTheme = data.core_theme_and_moral || {};
  const detailedSummary = data.detailed_summary_and_explanation || {};
  const stanzas = detailedSummary.stanza_wise_explanation || [];
  const characters = data.character_and_element_sketches || [];
  const vocabulary = data.exhaustive_vocabulary || {};
  const wordMeanings = vocabulary.word_meanings || [];
  const synonyms = vocabulary.synonyms || [];
  const antonyms = vocabulary.antonyms || [];
  const grammar = data.comprehensive_grammar || {};
  const extracts = data.comprehension_and_extracts || [];
  const activities = data.activities_and_projects || [];

  return (
    <div className="space-y-8">
      {/* Chapter Metadata & Core Theme */}
      <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
        <div className="flex flex-wrap items-center gap-3">
          {genre && <span className="px-3 py-1 bg-indigo-50 text-indigo-700 text-xs font-bold rounded-full border border-indigo-200">विधा (Genre): {genre}</span>}
          {author && <span className="px-3 py-1 bg-slate-100 text-slate-700 text-xs font-bold rounded-full">रचनाकार (Author): {author}</span>}
        </div>

        {coreTheme.central_theme && (
          <div className="space-y-2 pt-2">
            <h4 className="text-xs font-black uppercase tracking-widest text-indigo-600">केंद्रीय भाव (Central Theme)</h4>
            <p className="text-slate-800 text-sm leading-relaxed font-medium bg-slate-50 p-4 rounded-2xl border border-slate-100">
              {coreTheme.central_theme}
            </p>
          </div>
        )}

        {coreTheme.moral_lesson && (
          <div className="space-y-2 pt-2">
            <h4 className="text-xs font-black uppercase tracking-widest text-amber-600">नैतिक शिक्षा एवं संदेश (Moral Lesson)</h4>
            <p className="text-slate-800 text-sm leading-relaxed font-medium bg-amber-50/50 p-4 rounded-2xl border border-amber-100">
              {coreTheme.moral_lesson}
            </p>
          </div>
        )}

        {Array.isArray(coreTheme.pedagogical_objectives) && coreTheme.pedagogical_objectives.length > 0 && (
          <div className="space-y-2 pt-2">
            <h4 className="text-xs font-black uppercase tracking-widest text-emerald-600">शैक्षणिक उद्देश्य (Pedagogical Objectives)</h4>
            <ul className="list-disc list-inside space-y-1 text-xs text-slate-700 p-3 bg-emerald-50/40 rounded-2xl border border-emerald-100">
              {coreTheme.pedagogical_objectives.map((obj: string, idx: number) => (
                <li key={idx}>{obj}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Overview & Stanza-wise Explanations */}
      {(detailedSummary.overview || stanzas.length > 0) && (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">पद्यांश / गद्यांश व्याख्या (Stanza Explanations)</h3>
          {detailedSummary.overview && (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm text-sm text-slate-700 leading-relaxed">
              {detailedSummary.overview}
            </div>
          )}
          <div className="space-y-4">
            {stanzas.map((st: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3">
                <div className="text-xs font-black uppercase tracking-wider text-indigo-600">पद्यांश / खंड #{st.stanza_number || idx + 1}</div>
                {st.lines && (
                  <div className="p-4 bg-slate-50 border border-slate-100 rounded-2xl font-serif text-slate-900 text-sm leading-relaxed whitespace-pre-wrap">
                    {st.lines}
                  </div>
                )}
                <div className="space-y-1 pt-1">
                  <div className="text-xs font-bold text-slate-700">व्याख्या (Meaning & Analysis):</div>
                  <p className="text-slate-700 text-sm leading-relaxed">{st.meaning_and_analysis}</p>
                </div>
                {st.poetic_beauty_and_rhyme && (
                  <div className="text-xs font-serif text-indigo-900 bg-indigo-50/50 p-3 rounded-xl border border-indigo-100">
                    <strong>काव्य-सौंदर्य (Poetic Beauty):</strong> {st.poetic_beauty_and_rhyme}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Character & Element Sketches */}
      {Array.isArray(characters) && characters.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">पात्र एवं तत्व परिचय (Character & Element Sketches)</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {characters.map((ch: any, idx: number) => (
              <div key={idx} className="p-5 bg-indigo-50/40 border border-indigo-100 rounded-2xl space-y-2">
                <div className="text-sm font-extrabold text-indigo-700">{ch.element || ch.character}</div>
                <div className="text-xs text-slate-800 font-medium">विशेषताएँ: {ch.traits}</div>
                <div className="text-xs text-slate-600">महत्व: {ch.significance}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Exhaustive Vocabulary (Word Meanings, Synonyms, Antonyms) */}
      {Array.isArray(wordMeanings) && wordMeanings.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">शब्दार्थ एवं शब्दावली (Word Meanings)</h3>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {wordMeanings.map((v: any, idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-1">
                <div className="text-sm font-extrabold text-indigo-600">{v.word}</div>
                <div className="text-xs text-slate-700">अर्थ: {v.meaning}</div>
                {v.sentence && <div className="text-xs font-serif italic text-slate-500 pt-1">वाक्य प्रयोग: &ldquo;{v.sentence}&rdquo;</div>}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Activities & Projects */}
      {Array.isArray(activities) && activities.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">रचनात्मक गतिविधियाँ (Activities & Projects)</h3>
          <div className="space-y-3">
            {activities.map((act: any, idx: number) => (
              <div key={idx} className="p-4 bg-amber-50/50 border border-amber-100 rounded-2xl space-y-1">
                <div className="text-xs font-bold text-amber-900">{act.activity_name || act.title || `गतिविधि #${idx + 1}`}</div>
                <div className="text-xs text-slate-700 leading-relaxed">{act.description || act.details || JSON.stringify(act)}</div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
