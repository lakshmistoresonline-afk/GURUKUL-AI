import React from 'react';

function renderSafeText(val: any): string {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string') return val;
  if (typeof val === 'number' || typeof val === 'boolean') return String(val);
  if (typeof val === 'object') {
    return val.definition || val.meaning || val.description || val.explanation || val.details || val.text || JSON.stringify(val);
  }
  return String(val);
}

interface TerminologyItem {
  term?: string;
  word?: string;
  concept?: string;
  topic?: string;
  name?: string;
  title?: string;
  definition?: string;
  meaning?: string;
  description?: string;
  explanation?: string;
  usageExample?: string;
  example_sentence?: string;
  synonyms?: string[];
  antonyms?: string[];
  ashuddhCorrection?: string;
}

export const TerminologyRenderer: React.FC<{ data: any; title?: string }> = ({ data, title }) => {
  if (!data) return null;

  const rawList: any[] = Array.isArray(data) ? data : [data];
  if (rawList.length === 0) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
          {title || 'KEY TERMINOLOGY & CORE DEFINITIONS'}
        </h3>
        <span className="text-xs font-mono font-bold text-slate-500">
          {rawList.length} Items
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {rawList.map((item, idx) => {
          let termWord = `Definition #${idx + 1}`;
          let definitionText = '';
          let exampleText = '';
          let ashuddhCorrection = '';
          let synonyms: string[] = [];

          if (typeof item === 'string') {
            definitionText = item;
          } else if (typeof item === 'object' && item !== null) {
            termWord = item.term || item.word || item.concept || item.topic || item.name || item.title || `Definition #${idx + 1}`;
            definitionText = renderSafeText(item.definition || item.meaning || item.description || item.explanation || item.details || item.content || item);
            exampleText = renderSafeText(item.usageExample || item.example_sentence || item.example || '');
            ashuddhCorrection = item.ashuddhCorrection || '';
            synonyms = Array.isArray(item.synonyms) ? item.synonyms : [];
          }

          return (
            <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl space-y-3 shadow-sm">
              <div className="flex items-center justify-between gap-2 border-b border-slate-100 pb-2">
                <h4 className="text-base font-bold text-slate-900">{termWord}</h4>
                {ashuddhCorrection && (
                  <span className="px-2 py-0.5 text-[11px] font-bold bg-red-50 text-red-700 border border-red-200 rounded-md">
                    अशुद्ध: {ashuddhCorrection}
                  </span>
                )}
              </div>

              {definitionText && (
                <p className="text-slate-800 text-sm leading-relaxed">{definitionText}</p>
              )}

              {exampleText && (
                <div className="p-3 bg-slate-50 border border-slate-200/80 rounded-xl text-xs text-slate-700 italic">
                  Usage Example: &quot;{exampleText}&quot;
                </div>
              )}

              {synonyms.length > 0 && (
                <div className="text-xs text-slate-600 space-x-1">
                  <span className="font-bold text-slate-700">Synonyms:</span>
                  <span>{synonyms.join(', ')}</span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
