import React, { useState } from 'react';

interface Flashcard {
  term?: string;
  term_or_question?: string;
  front?: string;
  front_content?: string;
  question?: string;
  topic?: string;
  concept_tag?: string;
  definition?: string;
  definition_or_answer?: string;
  back?: string;
  back_content?: string;
  answer?: string;
  explanation_or_tip?: string;
  key_memory_tip?: string;
  key_takeaway?: string;
}

export const FlashcardDeck: React.FC<{ data: any; title?: string }> = ({ data, title }) => {
  const cards: Flashcard[] = (Array.isArray(data) ? data : []).filter(
    (c) =>
      c &&
      (c.front_content || c.front || c.term || c.term_or_question || c.question || c.topic || c.concept_tag) &&
      (c.back_content || c.back || c.definition || c.definition_or_answer || c.answer || c.explanation_or_tip || c.key_memory_tip || c.key_takeaway)
  );

  const [currentIndex, setCurrentIndex] = useState<number>(0);
  const [isFlipped, setIsFlipped] = useState<boolean>(false);

  if (cards.length === 0) return null;

  const currentCard = cards[currentIndex];
  const termText =
    currentCard.front_content ||
    currentCard.front ||
    currentCard.term ||
    currentCard.term_or_question ||
    currentCard.question ||
    currentCard.topic ||
    currentCard.concept_tag ||
    '';

  const defText =
    currentCard.back_content ||
    currentCard.back ||
    currentCard.definition ||
    currentCard.definition_or_answer ||
    currentCard.answer ||
    currentCard.explanation_or_tip ||
    currentCard.key_memory_tip ||
    currentCard.key_takeaway ||
    '';

  const handleNext = () => {
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev + 1) % cards.length);
  };

  const handlePrev = () => {
    setIsFlipped(false);
    setCurrentIndex((prev) => (prev - 1 + cards.length) % cards.length);
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
          {title || 'REVISION FLASHCARDS'}
        </h3>
        <span className="text-xs font-mono font-bold text-slate-500">
          Card {currentIndex + 1} of {cards.length}
        </span>
      </div>

      {/* Interactive Card */}
      <div
        onClick={() => setIsFlipped(!isFlipped)}
        className="group relative min-h-[280px] w-full cursor-pointer rounded-3xl bg-white border border-slate-200 p-8 shadow-sm transition-all duration-300 hover:border-indigo-400 flex flex-col items-center justify-between text-center space-y-6"
        tabIndex={0}
        role="button"
        aria-label="Click to flip flashcard"
      >
        {/* Top Badge */}
        <div className="w-full flex justify-center pt-2">
          <span className="text-[11px] font-bold uppercase tracking-wider px-3 py-1 bg-slate-100 border border-slate-200 text-slate-600 rounded-lg">
            {isFlipped ? 'ANSWER / DEFINITION' : 'QUESTION / TERM'}
          </span>
        </div>

        {/* Center Term / Definition Text */}
        <div className="my-auto px-4 py-2">
          <p className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight leading-snug">
            {isFlipped ? defText : termText}
          </p>
        </div>

        {/* Flip Instruction Hint */}
        <div className="pb-1">
          <span className="text-xs text-indigo-600 font-bold group-hover:text-indigo-700 transition-colors">
            {isFlipped ? '↺ Click to view question' : '↻ Click to reveal answer'}
          </span>
        </div>
      </div>

      {/* Control Buttons */}
      <div className="flex items-center justify-between gap-4 pt-2">
        <button
          onClick={handlePrev}
          disabled={cards.length <= 1}
          className="px-6 py-2.5 bg-white hover:bg-slate-50 text-slate-700 text-sm font-bold rounded-2xl border border-slate-200 shadow-sm transition-all disabled:opacity-50"
        >
          ← Previous
        </button>

        <button
          onClick={() => setIsFlipped(!isFlipped)}
          className="px-6 py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 text-sm font-bold rounded-2xl transition-all font-extrabold"
        >
          {isFlipped ? 'Show Front' : 'Flip Card'}
        </button>

        <button
          onClick={handleNext}
          disabled={cards.length <= 1}
          className="px-6 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-bold rounded-2xl shadow-md shadow-indigo-600/20 transition-all disabled:opacity-50"
        >
          Next →
        </button>
      </div>
    </div>
  );
};
