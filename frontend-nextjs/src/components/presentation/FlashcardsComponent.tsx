import React from 'react';

interface FlashcardsProps {
  flashcards: any[];
}

export default function FlashcardsComponent({ flashcards }: FlashcardsProps) {
  if (!Array.isArray(flashcards) || flashcards.length === 0) {
    return <div className="p-8 text-center text-slate-500">No flashcards available.</div>;
  }

  return (
    <div className="space-y-6 bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm">
      <div className="border-b border-slate-100 pb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-black text-slate-900 tracking-tight">
            Flashcards Deck ({flashcards.length} Cards)
          </h3>
          <p className="text-xs text-slate-500 mt-1">Review key terms, concepts, definitions, and memory tips.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {flashcards.map((fc: any, idx: number) => {
          const frontText = fc.front || fc.term || fc.question || fc.front_content || '';
          const backText = fc.back || fc.definition || fc.answer || fc.back_content || '';
          const memoryTip = fc.key_memory_tip || fc.memory_tip || fc.explanation_or_tip || '';
          const category = fc.category || fc.concept_tag || '';
          const level = fc.level || fc.difficulty_level || '';

          return (
            <div key={idx} className="p-6 bg-gradient-to-br from-indigo-50/60 to-slate-50 border border-indigo-100 rounded-2xl space-y-3 shadow-sm hover:border-indigo-300 transition-all">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-wide">
                  Card #{idx + 1} {category ? `• ${category}` : ''}
                </span>
                {level && (
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-indigo-100 text-indigo-800 uppercase">
                    {level}
                  </span>
                )}
              </div>

              <div className="space-y-2">
                <div className="text-sm font-bold text-slate-900 leading-snug">{frontText}</div>
                <div className="text-xs text-slate-700 border-t border-indigo-100/60 pt-2 leading-relaxed whitespace-pre-wrap">{backText}</div>

                {memoryTip && (
                  <div className="mt-2 p-3 bg-amber-50/70 border border-amber-200/60 rounded-xl text-[11px] text-amber-900 font-medium">
                    💡 <strong>Concept Explanation / Tip:</strong> {memoryTip}
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
