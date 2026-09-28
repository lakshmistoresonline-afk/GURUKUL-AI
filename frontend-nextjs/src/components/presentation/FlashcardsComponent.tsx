import React, { useState } from 'react';

interface FlashcardsProps {
  flashcards: any[];
}

export default function FlashcardsComponent({ flashcards }: FlashcardsProps) {
  const [viewMode, setViewMode] = useState<'grid' | 'carousel'>('grid');
  const [carouselIdx, setCarouselIdx] = useState<number>(0);
  const [flippedCards, setFlippedCards] = useState<Record<number, boolean>>({});
  const [masteredCards, setMasteredCards] = useState<Record<number, boolean>>({});

  if (!Array.isArray(flashcards) || flashcards.length === 0) {
    return <div className="p-8 text-center text-slate-500">No flashcards available.</div>;
  }

  const toggleFlip = (idx: number) => {
    setFlippedCards(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  const toggleMastered = (idx: number, e: React.MouseEvent) => {
    e.stopPropagation();
    setMasteredCards(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  const speakText = (text: string, e: React.MouseEvent) => {
    e.stopPropagation();
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.9;
      window.speechSynthesis.speak(utterance);
    }
  };

  const currentCard = flashcards[carouselIdx] || flashcards[0];
  const frontText = currentCard.front_question || currentCard.front_prompt || currentCard.front || currentCard.term || currentCard.question || currentCard.question_text || currentCard.prompt || currentCard.front_content || '';
  const backText = currentCard.back_answer || currentCard.back || currentCard.definition || currentCard.answer || currentCard.back_content || '';
  const memoryTip = currentCard.key_takeaway || currentCard.key_memory_tip || currentCard.memory_tip || currentCard.explanation_or_tip || '';
  const category = currentCard.category || currentCard.concept_tag || '';
  const level = currentCard.level || currentCard.difficulty_level || currentCard.difficulty || '';
  const isCarouselFlipped = !!flippedCards[carouselIdx];
  const isCarouselMastered = !!masteredCards[carouselIdx];

  return (
    <div className="space-y-6 bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm">
      <div className="border-b border-slate-100 pb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-black text-slate-900 tracking-tight">
            Flashcards Deck ({flashcards.length} Cards)
          </h3>
          <p className="text-xs text-slate-500 mt-1">Review key terms, concepts, definitions, and memory tips.</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="text-xs font-bold bg-indigo-50 text-indigo-700 px-3 py-1.5 rounded-full border border-indigo-200">
            Mastered: {Object.values(masteredCards).filter(Boolean).length} / {flashcards.length}
          </div>
          <div className="flex bg-slate-100 p-1 rounded-2xl border border-slate-200">
            <button
              onClick={() => setViewMode('grid')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${viewMode === 'grid' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'}`}
            >
              Grid View
            </button>
            <button
              onClick={() => setViewMode('carousel')}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${viewMode === 'carousel' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'}`}
            >
              Focus Mode
            </button>
          </div>
        </div>
      </div>

      {viewMode === 'carousel' ? (
        /* Focus Mode Carousel */
        <div className="max-w-xl mx-auto space-y-6 py-4">
          <div className="flex items-center justify-between text-xs font-bold text-slate-500">
            <span>Card {carouselIdx + 1} of {flashcards.length}</span>
            <span>{category ? `Category: ${category}` : ''}</span>
          </div>

          <div
            onClick={() => toggleFlip(carouselIdx)}
            className={`cursor-pointer min-h-[300px] p-8 rounded-3xl transition-all duration-300 border shadow-md flex flex-col justify-between ${
              isCarouselMastered ? 'bg-emerald-50/50 border-emerald-300' : 'bg-gradient-to-br from-indigo-50/70 to-slate-50 border-indigo-200 hover:border-indigo-400'
            }`}
          >
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-indigo-600 uppercase tracking-wide">{level}</span>
              <button
                onClick={(e) => speakText(isCarouselFlipped ? backText : frontText, e)}
                className="p-2 bg-white rounded-full hover:bg-indigo-100 text-indigo-600 transition-colors shadow-xs"
                title="Pronounce aloud"
              >
                🔊
              </button>
            </div>

            <div className="py-6 space-y-4 my-auto text-center">
              {!isCarouselFlipped ? (
                <div className="text-lg font-bold text-slate-900 leading-snug">
                  <span className="text-indigo-600 font-extrabold mr-1">Q:</span> {frontText}
                </div>
              ) : (
                <div className="space-y-3">
                  <div className="text-sm text-slate-800 font-medium leading-relaxed whitespace-pre-wrap">
                    <span className="text-emerald-600 font-extrabold mr-1">A:</span> {backText}
                  </div>
                  {memoryTip && (
                    <div className="p-3 bg-amber-50 border border-amber-200 rounded-xl text-xs text-amber-900 font-medium text-left">
                      💡 <strong>Tip:</strong> {memoryTip}
                    </div>
                  )}
                </div>
              )}
            </div>

            <div className="flex items-center justify-between pt-4 border-t border-indigo-100 text-xs font-bold text-slate-500">
              <span className="italic">{isCarouselFlipped ? 'Showing Answer (Click to flip)' : 'Click card to flip ➔'}</span>
              <button
                onClick={(e) => toggleMastered(carouselIdx, e)}
                className={`px-4 py-1.5 rounded-full text-xs font-black uppercase transition-all ${
                  isCarouselMastered ? 'bg-emerald-600 text-white shadow-sm' : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                }`}
              >
                {isCarouselMastered ? '✓ Mastered' : 'Mark Mastered'}
              </button>
            </div>
          </div>

          <div className="flex items-center justify-between gap-4">
            <button
              onClick={() => setCarouselIdx(prev => Math.max(0, prev - 1))}
              disabled={carouselIdx === 0}
              className="px-6 py-3 bg-white border border-slate-200 disabled:opacity-40 text-slate-700 font-extrabold rounded-2xl shadow-xs transition-all hover:bg-slate-50"
            >
              ← Previous Card
            </button>
            <button
              onClick={() => setCarouselIdx(prev => Math.min(flashcards.length - 1, prev + 1))}
              disabled={carouselIdx === flashcards.length - 1}
              className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 text-white font-extrabold rounded-2xl shadow-md shadow-indigo-600/20 transition-all"
            >
              Next Card →
            </button>
          </div>
        </div>
      ) : (
        /* Grid View */
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {flashcards.map((fc: any, idx: number) => {
            const fText = fc.front_question || fc.front_prompt || fc.front || fc.term || fc.question || fc.question_text || fc.prompt || fc.front_content || '';
            const bText = fc.back_answer || fc.back || fc.definition || fc.answer || fc.back_content || '';
            const mTip = fc.key_takeaway || fc.key_memory_tip || fc.memory_tip || fc.explanation_or_tip || '';
            const cat = fc.category || fc.concept_tag || '';
            const lev = fc.level || fc.difficulty_level || fc.difficulty || '';
            const isFlipped = !!flippedCards[idx];
            const isMastered = !!masteredCards[idx];

            return (
              <div
                key={idx}
                onClick={() => toggleFlip(idx)}
                className={`relative cursor-pointer min-h-[220px] p-6 rounded-3xl transition-all duration-300 border shadow-sm flex flex-col justify-between ${
                  isMastered ? 'bg-emerald-50/50 border-emerald-200' : 'bg-gradient-to-br from-indigo-50/60 to-slate-50 border-indigo-100 hover:border-indigo-300'
                }`}
              >
                <div className="flex flex-wrap items-center justify-between gap-2">
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wide">
                    Card #{idx + 1} {cat ? `• ${cat}` : ''}
                  </span>
                  <div className="flex items-center gap-2">
                    {lev && (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-800 uppercase">
                        {lev}
                      </span>
                    )}
                    <button
                      onClick={(e) => speakText(isFlipped ? bText : fText, e)}
                      className="p-1.5 bg-white rounded-full hover:bg-indigo-100 text-indigo-600 transition-colors shadow-xs"
                      title="Pronounce aloud"
                    >
                      🔊
                    </button>
                  </div>
                </div>

                <div className="py-4 space-y-2 my-auto">
                  {!isFlipped ? (
                    <div className="text-sm font-bold text-slate-900 leading-snug">
                      <span className="text-indigo-600 font-extrabold mr-1">Q:</span> {fText}
                    </div>
                  ) : (
                    <div className="space-y-2">
                      <div className="text-xs text-slate-800 font-medium leading-relaxed whitespace-pre-wrap">
                        <span className="text-emerald-600 font-extrabold mr-1">A:</span> {bText}
                      </div>
                      {mTip && (
                        <div className="p-2.5 bg-amber-50 border border-amber-200/60 rounded-xl text-[11px] text-amber-900 font-medium">
                          💡 <strong>Tip:</strong> {mTip}
                        </div>
                      )}
                    </div>
                  )}
                </div>

                <div className="flex items-center justify-between pt-3 border-t border-indigo-100/60 text-[11px] font-bold text-slate-500">
                  <span className="italic">{isFlipped ? 'Showing Answer (Click to flip back)' : 'Click card to flip ➔'}</span>
                  <button
                    onClick={(e) => toggleMastered(idx, e)}
                    className={`px-3 py-1 rounded-full text-[10px] font-black uppercase transition-all ${
                      isMastered ? 'bg-emerald-600 text-white shadow-sm' : 'bg-white text-slate-700 border border-slate-200 hover:bg-slate-100'
                    }`}
                  >
                    {isMastered ? '✓ Mastered' : 'Mark Mastered'}
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
