import React from 'react';

interface Exercise {
  sentence: string;
  answer?: string;
}

interface FillInTheBlanksData {
  wordBank?: string[];
  exercises?: Exercise[];
}

export const FillInTheBlanksRenderer: React.FC<{ data: FillInTheBlanksData }> = ({ data }) => {
  if (!data || typeof data !== 'object') return null;

  const wordBank = data.wordBank || [];
  const exercises = data.exercises || [];

  if (wordBank.length === 0 && exercises.length === 0) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-400">
          FILL IN THE BLANKS PRACTICE
        </h3>
        <span className="text-xs font-bold text-slate-500">{exercises.length} Exercises</span>
      </div>

      {/* Word Bank */}
      {wordBank.length > 0 && (
        <div className="p-5 bg-indigo-500/10 border border-indigo-500/20 rounded-2xl space-y-2">
          <div className="text-xs font-bold uppercase tracking-wider text-indigo-400">
            Word Bank
          </div>
          <div className="flex flex-wrap gap-2 pt-1">
            {wordBank.map((word, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-slate-900 border border-indigo-500/30 text-indigo-300 rounded-xl text-sm font-semibold shadow-sm"
              >
                {word}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Sentences List */}
      {exercises.length > 0 && (
        <div className="space-y-3">
          {exercises.map((item, idx) => (
            <div key={idx} className="p-5 bg-slate-900/90 border border-slate-800 rounded-2xl space-y-2 shadow-md">
              <p className="text-slate-200 text-base md:text-lg font-medium leading-relaxed">
                {idx + 1}. {item.sentence}
              </p>
              {item.answer && (
                <div className="text-xs text-emerald-400 font-semibold pt-1">
                  Answer: <span className="underline underline-offset-2">{item.answer}</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
