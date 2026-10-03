import React from 'react';

export function renderSafeText(val: any): string {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string') return val;
  if (typeof val === 'number' || typeof val === 'boolean') return String(val);
  if (Array.isArray(val)) {
    return val.map(renderSafeText).filter(Boolean).join(' | ');
  }
  if (typeof val === 'object') {
    try {
      if (typeof val.text === 'string') return val.text;
      if (typeof val.summary === 'string') return val.summary;
      if (typeof val.overview === 'string') return val.overview;
      if (typeof val.description === 'string') return val.description;
      if (typeof val.title === 'string') return val.title;
      if (typeof val.name === 'string') return val.name;
      if (typeof val.question_text === 'string') return val.question_text;
      if (typeof val.question === 'string') return val.question;
      if (typeof val.front_content === 'string') return val.front_content;
      if (typeof val.back_content === 'string') return val.back_content;
      if (typeof val.big_idea_summary === 'string') return val.big_idea_summary;
      if ('term' in val && 'definition' in val) {
        return `${val.term}: ${val.definition}`;
      }
      if ('heading' in val && 'content' in val) {
        return `${val.heading}: ${val.content}`;
      }

      const keys = Object.keys(val);
      if (keys.length === 0) return '';
      for (const k of keys) {
        if (typeof val[k] === 'string' && val[k].length > 0) {
          return val[k];
        }
      }
      return '';
    } catch {
      return '';
    }
  }
  return String(val);
}

export function SafeStructuredCard({ item }: { item: any }) {
  if (!item) return null;
  if (typeof item === 'string') {
    return <p className="text-slate-700 text-xs leading-relaxed">{item}</p>;
  }
  if (typeof item === 'object') {
    const term = item.term || item.word || item.heading || item.title || '';
    const def = item.definition || item.meaning || item.content || item.description || '';
    const example = item.example || item.contextual_importance || '';

    if (term || def) {
      return (
        <div className="p-4 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-1.5">
          {term && <div className="text-sm font-extrabold text-indigo-700">{term}</div>}
          {def && <div className="text-xs text-slate-700 leading-relaxed">{def}</div>}
          {example && <div className="text-[11px] font-serif italic text-slate-500 pt-1">Example: &ldquo;{example}&rdquo;</div>}
        </div>
      );
    }

    if (item.big_idea_summary) {
      return (
        <div className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-3">
          <p className="text-slate-700 text-xs leading-relaxed">{item.big_idea_summary}</p>
          {Array.isArray(item.topic_hierarchy) && item.topic_hierarchy.map((th: any, idx: number) => (
            <div key={idx} className="p-3 bg-slate-50 rounded-xl space-y-1">
              <div className="text-xs font-bold text-indigo-800">{th.topic}</div>
              {Array.isArray(th.subtopics) && (
                <ul className="list-disc list-inside text-[11px] text-slate-600 space-y-0.5">
                  {th.subtopics.map((st: string, sIdx: number) => (
                    <li key={sIdx}>{st}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      );
    }
  }
  return <pre className="text-xs text-slate-700 font-sans">{renderSafeText(item)}</pre>;
}
