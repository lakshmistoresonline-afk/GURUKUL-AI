import React from 'react';

export const VocabularyRenderer: React.FC<{ data: any; title?: string }> = ({ data, title }) => {
  if (!data) return null;

  const items = Array.isArray(data) ? data : [data];
  if (items.length === 0) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
          {title || 'VOCABULARY & SPELLING CORRECTION (शुद्धि-वर्तनी)'}
        </h3>
        <span className="text-xs font-mono font-bold text-slate-500">{items.length} Items</span>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {items.map((item, idx) => {
          const ashuddh = item.ashuddh || item.incorrect || '';
          const shuddh = item.shuddh || item.correct || item.word || '';

          return (
            <div key={idx} className="p-4 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm">
              {ashuddh && (
                <div className="text-xs text-red-600 font-semibold line-through">
                  अशुद्ध: {ashuddh}
                </div>
              )}
              <div className="text-base font-bold text-emerald-700 flex items-center gap-1.5">
                <span>✓ शुद्ध:</span>
                <span>{shuddh}</span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
