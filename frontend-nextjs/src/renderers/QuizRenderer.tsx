import React, { useState } from 'react';

export interface QuestionPresentationModel {
  id: string;
  stem: string;
  options: string[];
  correctAnswer: string;
  explanation: string;
  hints?: string[];
}

function normalizeQuestion(item: any, idx: number): QuestionPresentationModel {
  if (typeof item === 'string') {
    return {
      id: `q-${idx + 1}`,
      stem: item,
      options: [],
      correctAnswer: '',
      explanation: ''
    };
  }

  if (typeof item !== 'object' || item === null) {
    return {
      id: `q-${idx + 1}`,
      stem: `Question ${idx + 1}`,
      options: [],
      correctAnswer: '',
      explanation: ''
    };
  }

  const stem =
    item.question ||
    item.question_text ||
    item.questionText ||
    item.prompt ||
    item.stem ||
    item.q ||
    item.task ||
    item.statement ||
    item.topic ||
    item.title ||
    `Question ${idx + 1}`;

  let rawOpts = item.options || item.choices || item.opts || [];
  if (!Array.isArray(rawOpts) && typeof rawOpts === 'object') {
    rawOpts = Object.values(rawOpts);
  }

  const correctAnswer =
    item.correctAnswer ||
    item.correct_answer ||
    item.correct_option ||
    item.correctOption ||
    item.answer ||
    item.modelAnswer ||
    item.model_answer ||
    item.solution ||
    item.correct ||
    '';

  const explanation =
    item.explanation ||
    item.detailed_explanation ||
    item.step_by_step_solution ||
    item.justification ||
    item.reasoning ||
    '';

  const hints = Array.isArray(item.hints)
    ? item.hints.map((h: any) => (typeof h === 'string' ? h : h.hint || JSON.stringify(h)))
    : [];

  return {
    id: item.id || item.question_id || item.q_id || `q-${idx + 1}`,
    stem: String(stem),
    options: Array.isArray(rawOpts) ? rawOpts.map((o: any) => (typeof o === 'string' ? o : o.text || JSON.stringify(o))) : [],
    correctAnswer: String(correctAnswer),
    explanation: String(explanation),
    hints
  };
}

export const QuizRenderer: React.FC<{ data: any; title?: string }> = ({ data, title }) => {
  const [selectedOptions, setSelectedOptions] = useState<Record<number, any>>({});

  if (!data) return null;

  const rawList: any[] = Array.isArray(data) ? data : [data];
  if (rawList.length === 0) return null;

  const questions: QuestionPresentationModel[] = rawList.map((item, idx) => normalizeQuestion(item, idx));

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <div>
          <span className="text-xs font-black uppercase tracking-widest text-amber-600 block">
            FINAL CHAPTER ASSESSMENT • STEP 6 OF 6
          </span>
          <h3 className="text-lg font-bold text-slate-900">
            {title || 'CHAPTER PRACTICE QUIZ'}
          </h3>
        </div>
        <span className="text-xs font-mono font-bold text-slate-500">
          {questions.length} Questions
        </span>
      </div>

      <div className="space-y-6">
        {questions.map((q, qIdx) => {
          const selected = selectedOptions[qIdx];
          const isAnswered = selected !== undefined;

          return (
            <div key={q.id || qIdx} className="p-6 md:p-8 bg-white border border-slate-200 rounded-3xl space-y-5 shadow-sm">
              {/* Question Stem (18--20px font-extrabold) */}
              <h4 className="text-lg sm:text-xl font-extrabold text-slate-900 leading-snug tracking-tight">
                {qIdx + 1}. {q.stem}
              </h4>

              {/* Options Grid */}
              {q.options.length > 0 ? (
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
                  {q.options.map((opt, optIdx) => {
                    const isThisSelected = selected === optIdx || selected === opt;
                    const isCorrect = q.correctAnswer && (opt.trim() === q.correctAnswer.trim() || opt.toLowerCase().includes(q.correctAnswer.toLowerCase()));

                    let btnStyle = 'bg-slate-50 text-slate-800 border-slate-200 hover:bg-slate-100/80';
                    if (isAnswered) {
                      if (isCorrect) btnStyle = 'bg-emerald-50 text-emerald-900 border-emerald-300 font-bold';
                      else if (isThisSelected) btnStyle = 'bg-red-50 text-red-900 border-red-300 font-bold';
                    }

                    return (
                      <button
                        key={optIdx}
                        disabled={isAnswered}
                        onClick={() => setSelectedOptions((prev) => ({ ...prev, [qIdx]: opt }))}
                        className={`p-4 rounded-2xl text-base border text-left transition-all leading-snug font-medium flex items-center gap-3 ${btnStyle}`}
                      >
                        <span className="inline-flex items-center justify-center w-7 h-7 rounded-xl bg-slate-200/80 text-slate-800 text-xs font-black shrink-0">
                          {String.fromCharCode(65 + optIdx)}
                        </span>
                        <span className="flex-1">{opt}</span>
                      </button>
                    );
                  })}
                </div>
              ) : (
                /* Fill-in-the-Blank / Open Response Reveal Option */
                <div className="space-y-3 pt-1">
                  {!isAnswered ? (
                    <button
                      onClick={() => setSelectedOptions((prev) => ({ ...prev, [qIdx]: true }))}
                      className="px-5 py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 text-xs font-extrabold rounded-2xl transition-all"
                    >
                      Reveal Correct Answer 👁
                    </button>
                  ) : (
                    <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-950 space-y-1">
                      <strong className="text-emerald-800 text-xs font-bold uppercase tracking-wider block">
                        Correct Answer:
                      </strong>
                      <p className="text-emerald-900 font-extrabold text-sm">{q.correctAnswer}</p>
                    </div>
                  )}
                </div>
              )}

              {/* Solution Explanation */}
              {isAnswered && q.explanation && (
                <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl text-xs text-indigo-950 space-y-1">
                  <strong className="text-indigo-700 font-bold">Explanation & Reasoning:</strong>
                  <p className="leading-relaxed">{q.explanation}</p>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
