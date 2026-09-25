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
    item.statement ||
    item.prompt ||
    item.stem ||
    item.q ||
    item.task ||
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

export const StudyQuestionsRenderer: React.FC<{ data: any; title?: string }> = ({ data, title }) => {
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  const [showHints, setShowHints] = useState<Record<string, boolean>>({});

  if (!data) return null;

  // Extract all possible question category arrays from data
  let categories: { categoryTitle: string; items: any[] }[] = [];

  if (typeof data === 'object') {
    const mapping = [
      { key: 'multipleChoice', label: 'Multiple Choice Questions (MCQs)' },
      { key: 'multipleChoiceQuestions', label: 'Multiple Choice Questions (MCQs)' },
      { key: 'mcqs', label: 'Multiple Choice Questions (MCQs)' },
      { key: 'fillInTheBlanks', label: 'Fill in the Blanks' },
      { key: 'fill_in_blanks', label: 'Fill in the Blanks' },
      { key: 'trueFalse', label: 'True or False' },
      { key: 'true_false', label: 'True or False' },
      { key: 'shortAnswer', label: 'Short Answer Questions' },
      { key: 'shortAnswerQuestions', label: 'Short Answer Questions' },
      { key: 'short_questions', label: 'Short Answer Questions' },
      { key: 'reasoning_questions', label: 'Reasoning & Conceptual Questions' },
      { key: 'analyticalProblems', label: 'Analytical Problems' },
      { key: 'ncertComprehension', label: 'NCERT Comprehension & Extracts' },
      { key: 'assertionReason', label: 'Assertion & Reason' },
      { key: 'longAnswer', label: 'Long Answer Questions' },
      { key: 'long_questions', label: 'Long Answer Questions' },
      { key: 'reflectionQuestions', label: 'Reflection & Writing Prompts' },
      { key: 'past_paper_questions', label: 'Past Paper & Model Examination Questions' }
    ];

    for (const m of mapping) {
      if (Array.isArray(data[m.key]) && data[m.key].length > 0) {
        categories.push({ categoryTitle: m.label, items: data[m.key] });
      }
    }

    // If data is a plain array of questions directly
    if (Array.isArray(data) && data.length > 0) {
      categories.push({ categoryTitle: title || 'Practice Questions & Drills', items: data });
    }
  }

  if (categories.length === 0) return null;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
          {title || 'PRACTICE EXERCISES & QUESTION BANK'}
        </h3>
      </div>

      <div className="space-y-8">
        {categories.map((cat, catIdx) => (
          <div key={catIdx} className="space-y-4">
            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 border-b border-slate-100 pb-2">
              {cat.categoryTitle} ({cat.items.length} Questions)
            </h4>

            <div className="space-y-5">
              {cat.items.map((rawItem, qIdx) => {
                const q = normalizeQuestion(rawItem, qIdx);
                const uniqueKey = `${catIdx}-${q.id || qIdx}`;
                const chosen = selectedAnswers[uniqueKey];

                return (
                  <div key={uniqueKey} className="p-6 md:p-8 bg-white border border-slate-200 rounded-3xl space-y-5 shadow-sm">
                    {/* Question Stem */}
                    <h5 className="text-lg sm:text-xl font-extrabold text-slate-900 leading-snug tracking-tight">
                      {qIdx + 1}. {q.stem}
                    </h5>

                    {/* Options Grid */}
                    {q.options.length > 0 ? (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 pt-1">
                        {q.options.map((opt, optIdx) => {
                          const isChosen = chosen === opt;
                          const isCorrect = q.correctAnswer && (opt.trim() === q.correctAnswer.trim() || opt.toLowerCase().includes(q.correctAnswer.toLowerCase()));

                          let btnStyle = 'bg-slate-50 text-slate-800 border-slate-200 hover:bg-slate-100/80';
                          if (chosen) {
                            if (isCorrect) btnStyle = 'bg-emerald-50 text-emerald-900 border-emerald-300 font-bold';
                            else if (isChosen) btnStyle = 'bg-red-50 text-red-900 border-red-300 font-bold';
                          }

                          return (
                            <button
                              key={optIdx}
                              onClick={() => setSelectedAnswers((prev) => ({ ...prev, [uniqueKey]: opt }))}
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
                      /* Fill-in-the-Blank / Short Answer Reveal */
                      <div className="space-y-3 pt-1">
                        {!chosen ? (
                          <button
                            onClick={() => setSelectedAnswers((prev) => ({ ...prev, [uniqueKey]: q.correctAnswer || 'Revealed' }))}
                            className="px-5 py-2.5 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 border border-indigo-200 text-xs font-extrabold rounded-2xl transition-all"
                          >
                            Reveal Answer / Solution 👁
                          </button>
                        ) : (
                          <div className="p-4 bg-emerald-50 border border-emerald-200 rounded-2xl text-xs text-emerald-950 space-y-1">
                            <strong className="text-emerald-800 text-xs font-bold uppercase tracking-wider block">
                              Model Answer / Solution:
                            </strong>
                            <p className="text-emerald-900 font-bold text-sm">{q.correctAnswer || 'Completed Successfully'}</p>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Explanation */}
                    {chosen && q.explanation && (
                      <div className="p-4 bg-indigo-50 border border-indigo-200 rounded-2xl text-xs text-indigo-950 space-y-1">
                        <strong className="text-indigo-700 font-bold">Solution Explanation:</strong>
                        <p className="leading-relaxed">{q.explanation}</p>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
