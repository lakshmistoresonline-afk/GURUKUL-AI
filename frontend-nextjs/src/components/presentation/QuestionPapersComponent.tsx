import React, { useState } from 'react';

interface QuestionPapersProps {
  data: any;
}

export default function QuestionPapersComponent({ data }: QuestionPapersProps) {
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});

  if (!data) {
    return (
      <div className="p-12 text-center text-slate-600 bg-white rounded-3xl border border-slate-200 space-y-3 shadow-sm">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold uppercase tracking-wider">
          <span>Section Ready</span>
        </div>
        <h3 className="text-xl font-black text-slate-900 tracking-tight">Question Papers</h3>
        <p className="text-slate-600 text-sm leading-relaxed max-w-md mx-auto">
          No question papers are available for this chapter yet.
        </p>
      </div>
    );
  }

  const papers = data.question_papers || data.papers || [data];

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-8">
      <div className="p-6 sm:p-8 bg-indigo-900 rounded-3xl text-white shadow-xl space-y-2">
        <h3 className="text-2xl font-black tracking-tight">Examination Question Bank</h3>
        <p className="text-indigo-200 text-sm">Practice model question papers and summative assessments for this chapter with complete marking schemes.</p>
      </div>

      {Array.isArray(papers) && papers.length > 0 ? (
        <div className="space-y-6">
          {papers.map((paper: any, pIdx: number) => (
            <div key={pIdx} className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-6">
              <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-4">
                <div>
                  <div className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Model Question Paper #{pIdx + 1}</div>
                  <h4 className="text-xl font-black text-slate-900">{paper.paper_title || paper.title || 'Practice Assessment'}</h4>
                </div>
                <div className="flex items-center gap-3 text-xs font-bold">
                  {paper.total_marks && <span className="px-3 py-1 bg-slate-100 rounded-full text-slate-700">Total Marks: {paper.total_marks}</span>}
                  {paper.time_allowed_minutes && <span className="px-3 py-1 bg-slate-100 rounded-full text-slate-700">Time: {paper.time_allowed_minutes} mins</span>}
                </div>
              </div>

              {/* Sections / Questions */}
              {Array.isArray(paper.sections) && paper.sections.map((sec: any, sIdx: number) => (
                <div key={sIdx} className="space-y-4 pt-2">
                  <h5 className="text-sm font-black uppercase text-indigo-800 tracking-wider bg-indigo-50 p-3 rounded-xl border border-indigo-100">
                    {sec.section_name || sec.title || `Section ${sIdx + 1}`}
                  </h5>
                  <div className="space-y-4">
                    {Array.isArray(sec.questions) && sec.questions.map((q: any, qIdx: number) => {
                      const qKey = `${pIdx}-${sIdx}-${qIdx}`;
                      const isAnswerVisible = showAnswers[qKey];
                      const correctAnswer = q.correct_answer || q.marking_scheme_answer || q.answer;

                      return (
                        <div key={qIdx} className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-3">
                          <div className="flex items-center justify-between text-xs font-bold text-slate-500">
                            <span>Q{q.question_number || qIdx + 1}.</span>
                            <span className="px-2.5 py-0.5 bg-indigo-50 text-indigo-700 rounded-md font-extrabold">[{q.marks || 1} Mark{q.marks > 1 ? 's' : ''}]</span>
                          </div>

                          <div className="text-sm font-bold text-slate-900 leading-snug">
                            {q.question_text || q.question || JSON.stringify(q)}
                          </div>

                          {/* Options if MCQ */}
                          {Array.isArray(q.options) && q.options.length > 0 && (
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                              {q.options.map((opt: string, oIdx: number) => (
                                <div key={oIdx} className={`p-3 rounded-xl text-xs font-medium border ${isAnswerVisible && opt === correctAnswer ? 'bg-emerald-50 border-emerald-300 text-emerald-900 font-bold' : 'bg-white border-slate-200 text-slate-700'}`}>
                                  {opt} {isAnswerVisible && opt === correctAnswer ? '✓' : ''}
                                </div>
                              ))}
                            </div>
                          )}

                          {/* Marking Scheme / Answer Key Toggle */}
                          {correctAnswer && (
                            <div className="pt-2 border-t border-slate-200/60 mt-2">
                              <button
                                onClick={() => toggleAnswer(qKey)}
                                className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                              >
                                {isAnswerVisible ? 'Hide Marking Scheme / Answer ▴' : 'Show Marking Scheme / Answer ▾'}
                              </button>

                              {isAnswerVisible && (
                                <div className="mt-2 p-4 bg-emerald-50/60 border border-emerald-100 rounded-xl text-xs text-slate-800 leading-relaxed space-y-1">
                                  <strong className="text-emerald-900">Marking Scheme / Answer:</strong> {correctAnswer}
                                  {q.explanation && <div className="text-slate-600 pt-1"><em>Explanation:</em> {q.explanation}</div>}
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          ))}
        </div>
      ) : (
        <div className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm">
          <pre className="whitespace-pre-wrap font-sans text-sm text-slate-700 leading-relaxed overflow-x-auto">
            {JSON.stringify(data, null, 2)}
          </pre>
        </div>
      )}
    </div>
  );
}
