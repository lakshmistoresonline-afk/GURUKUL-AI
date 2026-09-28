import React, { useState } from 'react';

interface QuizProps {
  quiz: any[];
}

export default function QuizComponent({ quiz }: QuizProps) {
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [textInputs, setTextInput] = useState<Record<number, string>>({});
  const [submittedText, setSubmittedText] = useState<Record<number, boolean>>({});
  const [showExplanation, setShowExplanation] = useState<Record<number, boolean>>({});

  let quizList = quiz;
  if (quiz && !Array.isArray(quiz) && typeof quiz === 'object') {
    if (Array.isArray((quiz as any).questions)) {
      quizList = (quiz as any).questions;
    } else {
      quizList = Object.values(quiz);
    }
  }

  if (!Array.isArray(quizList) || quizList.length === 0) {
    return <div className="p-8 text-center text-slate-500">No quiz items available.</div>;
  }

  const handleSelectOption = (qIdx: number, opt: string) => {
    setSelectedAnswers(prev => ({ ...prev, [qIdx]: opt }));
  };

  const handleTextChange = (qIdx: number, val: string) => {
    setTextInput(prev => ({ ...prev, [qIdx]: val }));
  };

  const handleSubmitText = (qIdx: number) => {
    setSubmittedText(prev => ({ ...prev, [qIdx]: true }));
  };

  const toggleExplanation = (qIdx: number) => {
    setShowExplanation(prev => ({ ...prev, [qIdx]: !prev[qIdx] }));
  };

  return (
    <div className="space-y-6 bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm">
      <div className="border-b border-slate-100 pb-4 flex flex-wrap items-center justify-between gap-4">
        <div>
          <h3 className="text-xl font-black text-slate-900 tracking-tight">
            Master Quiz Assessment ({quizList.length} Questions)
          </h3>
          <p className="text-xs text-slate-500 mt-1">Test your comprehension, vocabulary, and subject knowledge.</p>
        </div>
      </div>

      <div className="space-y-6">
        {quizList.map((q: any, idx: number) => {
          const qText = q.question || q.question_text || q.prompt || q.statement || '';
          const rawCorrect = q.correct_option || q.correct_answer || q.answer;
          const qType = q.type || q.question_type || '';

          let optionsArr: string[] = [];
          if (Array.isArray(q.options)) {
            optionsArr = q.options;
          } else if (q.options && typeof q.options === 'object') {
            optionsArr = Object.entries(q.options).map(([k, v]) => `${k}) ${v}`);
          }

          let correctAnswer = rawCorrect;
          if (rawCorrect && optionsArr.length > 0) {
            const matchedOpt = optionsArr.find(opt => opt.startsWith(`${rawCorrect})`) || opt.startsWith(`${rawCorrect}:`) || opt === rawCorrect);
            if (matchedOpt) correctAnswer = matchedOpt;
          }

          const explanation = q.explanation || q.detailed_explanation || '';
          const userAnswer = selectedAnswers[idx];
          const textVal = textInputs[idx] || '';
          const isSubmitted = submittedText[idx];
          const isAnswered = userAnswer !== undefined || isSubmitted;
          const isExpanded = showExplanation[idx];

          return (
            <div key={idx} className="p-6 bg-slate-50 border border-slate-200 rounded-3xl space-y-4 shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-wide">
                  Question #{idx + 1} {qType ? `• ${qType}` : ''} {q.category || q.qid ? `• ${q.category || q.qid}` : ''}
                </span>
                {(q.difficulty_level || q.difficulty || q.blooms_level) && (
                  <span className="text-[10px] font-bold px-2.5 py-1 rounded-full uppercase bg-emerald-100 text-emerald-800">
                    {q.difficulty_level || q.difficulty || q.blooms_level}
                  </span>
                )}
              </div>

              <div className="text-base font-bold text-slate-900 leading-snug">
                {qText}
              </div>

              {/* Options if available */}
              {optionsArr.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                  {optionsArr.map((opt: string, oIdx: number) => {
                    let btnStyle = "bg-white border-slate-200 text-slate-700 hover:border-indigo-400";
                    if (isAnswered) {
                      if (opt === correctAnswer || opt.startsWith(`${rawCorrect})`) || opt === String(rawCorrect)) {
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
                        {isAnswered && (opt === correctAnswer || opt.startsWith(`${rawCorrect})`) || opt === String(rawCorrect)) && <span className="text-emerald-600 font-black">✓</span>}
                        {isAnswered && opt === userAnswer && opt !== correctAnswer && !opt.startsWith(`${rawCorrect})`) && <span className="text-rose-600 font-black">✗</span>}
                      </button>
                    );
                  })}
                </div>
              ) : (
                /* Text Input for Fill-in-the-Blank / Reasoning / Descriptive */
                <div className="space-y-3 pt-2">
                  <div className="flex gap-2">
                    <input
                      type="text"
                      placeholder="Type your answer here..."
                      value={textVal}
                      onChange={(e) => handleTextChange(idx, e.target.value)}
                      disabled={isSubmitted}
                      className="flex-1 px-4 py-3 bg-white border border-slate-200 rounded-xl text-xs sm:text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <button
                      onClick={() => handleSubmitText(idx)}
                      disabled={isSubmitted || !textVal.trim()}
                      className="px-5 py-3 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-55 text-white text-xs font-bold rounded-xl shadow-sm transition-all"
                    >
                      {isSubmitted ? 'Submitted ✓' : 'Submit Answer'}
                    </button>
                  </div>
                  {isSubmitted && correctAnswer && (
                    <div className="p-3 bg-emerald-50 border border-emerald-200 rounded-xl text-xs text-emerald-900 font-semibold">
                      Expected Answer Key: {String(correctAnswer)}
                    </div>
                  )}
                </div>
              )}

              {/* Explanation Toggle */}
              {(correctAnswer || explanation) && (
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
