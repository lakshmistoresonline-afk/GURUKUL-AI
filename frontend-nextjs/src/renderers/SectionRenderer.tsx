import React from 'react';

function renderSafeText(val: any): string {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string') return val;
  if (typeof val === 'number' || typeof val === 'boolean') return String(val);
  if (Array.isArray(val)) {
    return val.map((v) => (typeof v === 'string' ? v : JSON.stringify(v))).join(', ');
  }
  if (typeof val === 'object') {
    return (
      val.lines ||
      val.meaning_and_analysis ||
      val.explanation ||
      val.definition ||
      val.summary ||
      val.details ||
      val.title ||
      val.name ||
      val.heading ||
      val.description ||
      val.text ||
      JSON.stringify(val)
    );
  }
  return String(val);
}

export const SectionRenderer: React.FC<{ data: any; title?: string }> = ({ data, title }) => {
  if (!data) return null;

  // Handle Hindi Grammar Dictionary (sangya, sarvanam, visheshand, kriya, vilom, paryayvachi)
  if (typeof data === 'object' && !Array.isArray(data) && (data.sangya || data.vilom || data.paryayvachi || data.activity || data.character_name)) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between border-b border-slate-200 pb-3">
          <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
            {title || 'व्याकरण एवं भाषा ज्ञान (GRAMMAR & VOCABULARY)'}
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {data.sangya && Array.isArray(data.sangya) && (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm">
              <span className="text-xs font-bold text-indigo-600 uppercase">संज्ञा शब्द (Noun)</span>
              <p className="text-slate-800 text-sm font-medium">{data.sangya.join(', ')}</p>
            </div>
          )}

          {data.sarvanam && Array.isArray(data.sarvanam) && (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm">
              <span className="text-xs font-bold text-indigo-600 uppercase">सर्वनाम शब्द (Pronoun)</span>
              <p className="text-slate-800 text-sm font-medium">{data.sarvanam.join(', ')}</p>
            </div>
          )}

          {data.visheshand && Array.isArray(data.visheshand) && (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm">
              <span className="text-xs font-bold text-indigo-600 uppercase">विशेषण शब्द (Adjective)</span>
              <p className="text-slate-800 text-sm font-medium">{data.visheshand.join(', ')}</p>
            </div>
          )}

          {data.kriya && Array.isArray(data.kriya) && (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm">
              <span className="text-xs font-bold text-indigo-600 uppercase">क्रिया शब्द (Verb)</span>
              <p className="text-slate-800 text-sm font-medium">{data.kriya.join(', ')}</p>
            </div>
          )}

          {data.vilom && Array.isArray(data.vilom) && (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm sm:col-span-2">
              <span className="text-xs font-bold text-indigo-600 uppercase block mb-2">विलोम शब्द (Antonyms)</span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {data.vilom.map((v: any, vIdx: number) => (
                  <div key={vIdx} className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs flex justify-between">
                    <span className="font-bold text-slate-900">{v.word}</span>
                    <span className="text-indigo-700">⇄ {v.opposite}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {data.paryayvachi && Array.isArray(data.paryayvachi) && (
            <div className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm sm:col-span-2">
              <span className="text-xs font-bold text-indigo-600 uppercase block mb-2">पर्यायवाची शब्द (Synonyms)</span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                {data.paryayvachi.map((p: any, pIdx: number) => (
                  <div key={pIdx} className="p-2.5 bg-slate-50 border border-slate-200 rounded-xl text-xs space-y-1">
                    <span className="font-bold text-slate-900">{p.word}: </span>
                    <span className="text-emerald-700">{Array.isArray(p.synonyms) ? p.synonyms.join(', ') : ''}</span>
                  </div>
                ))}
              </div>
            </div>
          )}

          {data.activity && (
            <div className="p-6 bg-white border border-slate-200 rounded-3xl space-y-3 shadow-sm sm:col-span-2">
              <span className="text-xs font-bold text-indigo-600 uppercase">रचनात्मक गतिविधि (Activity)</span>
              <p className="text-slate-900 text-base font-medium">{data.activity}</p>
              {Array.isArray(data.checklist) && data.checklist.length > 0 && (
                <div className="pt-2 border-t border-slate-100 space-y-1.5">
                  <strong className="text-xs font-bold text-slate-600 uppercase">जाँच सूची (Checklist):</strong>
                  <ul className="list-disc list-inside text-slate-800 text-sm space-y-1">
                    {data.checklist.map((chk: string, cIdx: number) => (
                      <li key={cIdx}>{chk}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }

  let headingTitle = title || 'DETAILED LESSON BREAKDOWN';
  let detailsList: any[] = [];

  if (typeof data === 'string') {
    detailsList = [data];
  } else if (Array.isArray(data)) {
    detailsList = data;
  } else if (typeof data === 'object') {
    headingTitle = data.sectionTitle || title || 'DETAILED LESSON BREAKDOWN';
    detailsList = Array.isArray(data.details) ? data.details : [data];
  }

  if (detailsList.length === 0) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
          {headingTitle}
        </h3>
        <span className="text-xs font-mono font-bold text-slate-500">{detailsList.length} Sections</span>
      </div>

      <div className="space-y-5">
        {detailsList.map((item, idx) => {
          if (typeof item === 'string') {
            return (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl space-y-2 shadow-sm">
                <span className="text-xs font-bold text-indigo-600 uppercase">Section #{idx + 1}</span>
                <p className="text-slate-900 text-base leading-relaxed font-normal">{item}</p>
              </div>
            );
          }

          if (typeof item === 'object' && item !== null) {
            const heading =
              item.sectionTitle ||
              item.title ||
              item.name ||
              item.heading ||
              item.term ||
              item.character_name ||
              (item.stanza_number ? `Stanza #${item.stanza_number}` : `Section #${idx + 1}`);

            const lines = item.lines || '';
            const analysis = item.analysis || item.meaning_and_analysis || item.explanation || item.definition || item.summary || item.traits || item.content || '';
            const sign = item.significance || '';
            const poetic = item.poetic_beauty_and_rhyme || '';

            return (
              <div key={idx} className="p-6 md:p-8 bg-white border border-slate-200 rounded-3xl space-y-4 shadow-sm">
                <div className="flex items-center justify-between gap-2 border-b border-slate-100 pb-2">
                  <h4 className="text-base font-extrabold text-slate-900 tracking-tight leading-snug">{heading}</h4>
                  <span className="text-[11px] font-mono text-slate-400">#{idx + 1}</span>
                </div>

                {lines && (
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl whitespace-pre-line text-slate-900 font-serif text-base italic leading-relaxed">
                    {lines}
                  </div>
                )}

                {analysis && (
                  <div className="space-y-1">
                    <strong className="text-xs font-bold text-indigo-700 uppercase tracking-wider">Analysis & Meaning:</strong>
                    <p className="text-slate-800 text-base leading-relaxed font-normal">{analysis}</p>
                  </div>
                )}

                {poetic && (
                  <div className="p-3 bg-indigo-50/60 border border-indigo-200/80 rounded-2xl text-xs text-indigo-950 space-y-1">
                    <strong className="text-indigo-800 font-bold uppercase tracking-wider">Poetic Beauty & Rhyme:</strong>
                    <p>{poetic}</p>
                  </div>
                )}

                {sign && (
                  <div className="p-3 bg-emerald-50/60 border border-emerald-200/80 rounded-2xl text-xs text-emerald-950 space-y-1">
                    <strong className="text-emerald-800 font-bold uppercase tracking-wider">Significance:</strong>
                    <p>{sign}</p>
                  </div>
                )}
              </div>
            );
          }

          return (
            <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl space-y-2 shadow-sm">
              <span className="text-xs font-bold text-indigo-600 uppercase">Section #{idx + 1}</span>
              <p className="text-slate-900 text-base leading-relaxed font-normal">{renderSafeText(item)}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
