import React, { useState } from 'react';

interface QuizProps {
  quiz: any[];
}

export default function QuizComponent({ quiz }: QuizProps) {
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [showExplanation, setShowExplanation] = useState<Record<number, boolean>>({});

  if (!Array.isArray(quiz) || quiz.length === 0) {
    return <div className="p-8 text-center text-slate-500">No quiz items available.</div>;
  }

  const handleSelectOption = (qIdx: number, opt: string) => {
    setSelectedAnswers(prev => ({ ...prev, [qIdx]: opt }));
  };

  const toggleExplanation = (qIdx: number) => {
    setShowExplanation(prev => ({ ...prev, [qIdx]: !prev[qIdx] }));
  };

  return (
    <div className="space-y-6 bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm">
      <div className="border-b border-slate-100 pb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-black text-slate-900 tracking-tight">
            Master Quiz Assessment ({quiz.length} Questions)
          </h3>
          <p className="text-xs text-slate-500 mt-1">Test your comprehension, vocabulary, and grammar knowledge.</p>
        </div>
      </div>

      <div className="space-y-6">
        {quiz.map((q: any, idx: number) => {
          const qText = q.question || q.question_text || q.prompt || q.statement || '';
          const correctAnswer = q.correct_answer || q.answer;
          const explanation = q.explanation || q.detailed_explanation || '';
          const userAnswer = selectedAnswers[idx];
          const isAnswered = userAnswer !== undefined;
          const isExpanded = showExplanation[idx];

          return (
            <div key={idx} className="p-6 bg-slate-50 border border-slate-200 rounded-3xl space-y-4 shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-wide">
                  Question #{idx + 1} {q.category ? `• ${q.category}` : ''}
                </span>
                {(q.difficulty_level || q.difficulty) && (
                  <span className={`text-[10px] font-bold px-2.5 py-1 rounded-full uppercase ${
                    (q.difficulty_level || q.difficulty).includes('Easy') || (q.difficulty_level || q.difficulty) === 'Level 1' ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'
                  }`}>
                    {q.difficulty_level || q.difficulty}
                  </span>
                )}
              </div>

              <div className="text-base font-bold text-slate-900 leading-snug">
                {qText}
              </div>

              {/* Options */}
              {Array.isArray(q.options) && q.options.length > 0 && (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                  {q.options.map((opt: string, oIdx: number) => {
                    let btnStyle = "bg-white border-slate-200 text-slate-700 hover:border-indigo-400";
                    if (isAnswered) {
                      if (opt === correctAnswer) {
                        btnStyle = "bg-emerald-50 border-emerald-300 text-emerald-900 font-bold";
                      } else if (opt === userAnswer) {
                        btnStyle = "bg-rose-50 border-rose-300 text-rose-900 font-bold";
                      }
                    }

                    return (
                      <button
                        key={oIdx}
                        onClick={() => handleSelectOption(idx, opt)}
                        className={`p-4 rounded-2xl text-xs sm:text-sm text-left border transition-all flex items-center justify-between ${btnStyle}`}
                      >
                        <span>{opt}</span>
                        {isAnswered && opt === correctAnswer && <span className="text-emerald-600 font-black">✓</span>}
                        {isAnswered && opt === userAnswer && opt !== correctAnswer && <span className="text-rose-600 font-black">✗</span>}
                      </button>
                    );
                  })}
                </div>
              )}

              {/* Explanation Toggle */}
              {correctAnswer && (
                <div className="pt-2 flex flex-col items-start gap-2 border-t border-slate-200/60 mt-4">
                  <button
                    onClick={() => toggleExplanation(idx)}
                    className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                  >
                    {isExpanded ? 'Hide Explanation ▴' : 'Show Explanation ▾'}
                  </button>

                  {isExpanded && (
                    <div className="w-full p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl text-xs text-slate-700 leading-relaxed space-y-1">
                      <div><strong className="text-indigo-900">Correct Answer:</strong> {String(correctAnswer)}</div>
                      {explanation && <div><strong className="text-indigo-900">Explanation:</strong> {explanation}</div>}
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
