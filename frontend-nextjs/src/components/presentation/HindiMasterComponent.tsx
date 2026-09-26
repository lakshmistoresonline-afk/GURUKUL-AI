import React from 'react';

interface HindiMasterProps {
  data: any;
}

export default function HindiMasterComponent({ data }: HindiMasterProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई मास्टर सामग्री उपलब्ध नहीं है।</div>;
  }

  const summary = data.summary || '';
  const poemMeaning = data.poem_meaning || '';
  const characterSketches = data.character_sketches || [];
  const vocab = data.vocabulary || [];
  const grammar = data.grammar || {};
  const spellingPractice = data.spelling_practice || [];
  const questionBank = data.question_bank || [];
  const creativeWriting = data.creative_writing || [];

  return (
    <div className="space-y-8">
      {/* Summary & Poem Meaning */}
      {(summary || poemMeaning) && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
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

      {/* Vocabulary */}
      {Array.isArray(vocab) && vocab.length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
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

      {/* Grammar Practice */}
      {grammar && Object.keys(grammar).length > 0 && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">संपूर्ण व्याकरण अभ्यास (Comprehensive Grammar)</h3>

          {/* Nouns */}
          {Array.isArray(grammar.nouns) && grammar.nouns.length > 0 && (
            <div className="space-y-1">
              <div className="text-xs font-bold text-indigo-700 uppercase">संज्ञा (Nouns):</div>
              <div className="flex flex-wrap gap-2 pt-1">
                {grammar.nouns.map((n: string, i: number) => (
                  <span key={i} className="px-3 py-1 bg-indigo-50 border border-indigo-200 rounded-xl text-xs font-bold text-indigo-900">{n}</span>
                ))}
              </div>
            </div>
          )}

          {/* Pronouns */}
          {Array.isArray(grammar.pronouns) && grammar.pronouns.length > 0 && (
            <div className="space-y-1 pt-2">
              <div className="text-xs font-bold text-indigo-700 uppercase">सर्वनाम (Pronouns):</div>
              <div className="flex flex-wrap gap-2 pt-1">
                {grammar.pronouns.map((p: string, i: number) => (
                  <span key={i} className="px-3 py-1 bg-emerald-50 border border-emerald-200 rounded-xl text-xs font-bold text-emerald-900">{p}</span>
                ))}
              </div>
            </div>
          )}

          {/* Adjectives */}
          {Array.isArray(grammar.adjectives) && grammar.adjectives.length > 0 && (
            <div className="space-y-1 pt-2">
              <div className="text-xs font-bold text-indigo-700 uppercase">विशेषण (Adjectives):</div>
              <div className="flex flex-wrap gap-2 pt-1">
                {grammar.adjectives.map((a: string, i: number) => (
                  <span key={i} className="px-3 py-1 bg-amber-50 border border-amber-200 rounded-xl text-xs font-bold text-amber-900">{a}</span>
                ))}
              </div>
            </div>
          )}

          {/* Verbs */}
          {Array.isArray(grammar.verbs) && grammar.verbs.length > 0 && (
            <div className="space-y-1 pt-2">
              <div className="text-xs font-bold text-indigo-700 uppercase">क्रिया (Verbs):</div>
              <div className="flex flex-wrap gap-2 pt-1">
                {grammar.verbs.map((vb: string, i: number) => (
                  <span key={i} className="px-3 py-1 bg-purple-50 border border-purple-200 rounded-xl text-xs font-bold text-purple-900">{vb}</span>
                ))}
              </div>
            </div>
          )}

          {/* Idioms */}
          {Array.isArray(grammar.idioms) && grammar.idioms.length > 0 && (
            <div className="space-y-2 pt-3 border-t border-slate-100">
              <div className="text-xs font-bold text-indigo-700 uppercase">मुहावरे एवं प्रयोग (Idioms):</div>
              <div className="space-y-2">
                {grammar.idioms.map((idm: any, i: number) => (
                  <div key={i} className="p-3 bg-slate-50 border border-slate-100 rounded-xl text-xs space-y-1">
                    <div className="font-bold text-slate-900">{idm.idiom} — {idm.meaning}</div>
                    {idm.sentence_usage && <div className="font-serif italic text-slate-600">वाक्य: &ldquo;{idm.sentence_usage}&rdquo;</div>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
