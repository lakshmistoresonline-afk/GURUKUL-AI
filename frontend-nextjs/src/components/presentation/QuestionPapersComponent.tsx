import React, { useState } from 'react';

interface QuestionPapersProps {
  data: any;
}

function cleanQuestionText(text: string): string {
  if (!text) return '';
  if (text.includes("is tested in Set")) {
    return text.replace(/is tested in Set \d+ Q\d+\?/i, "is central to this chapter's core learning objectives?");
  }
  return text;
}

export default function QuestionPapersComponent({ data }: QuestionPapersProps) {
  const [activePaperIdx, setActivePaperIdx] = useState<number>(0);
  const [activeSectionIdx, setActiveSectionIdx] = useState<number>(0);
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
  const currentPaper = Array.isArray(papers) && papers.length > 0 ? papers[activePaperIdx] || papers[0] : null;
  const sections = currentPaper?.sections || [];
  const currentSection = sections[activeSectionIdx] || sections[0] || null;

  const toggleAnswer = (key: string) => {
    setShowAnswers(prev => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="space-y-8">
      {/* Header & Set Selector */}
      <div className="p-6 sm:p-8 bg-indigo-950 rounded-3xl text-white shadow-xl space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h3 className="text-2xl font-black tracking-tight">Examination Question Bank</h3>
            <p className="text-indigo-200 text-sm mt-1">Practice distinct model question papers set by set, section by section.</p>
          </div>
          {/* Paper Set Selector Tabs */}
          {Array.isArray(papers) && papers.length > 1 && (
            <div className="flex flex-wrap gap-1.5 bg-indigo-900/80 p-1.5 rounded-2xl border border-indigo-800">
              {papers.map((p: any, idx: number) => (
                <button
                  key={idx}
                  onClick={() => {
                    setActivePaperIdx(idx);
                    setActiveSectionIdx(0);
                    setShowAnswers({});
                  }}
                  className={`px-4 py-2 rounded-xl text-xs font-extrabold transition-all ${
                    activePaperIdx === idx
                      ? 'bg-white text-indigo-950 shadow-md'
                      : 'text-indigo-200 hover:text-white hover:bg-indigo-800/50'
                  }`}
                >
                  Set {idx + 1}
                </button>
              ))}
            </div>
          )}
        </div>

        {/* Dynamic Section Selector Tabs (Strictly bound to activePaperIdx) */}
        {Array.isArray(sections) && sections.length > 0 && (
          <div className="flex flex-wrap gap-2 pt-2 border-t border-indigo-900">
            {sections.map((sec: any, sIdx: number) => (
              <button
                key={`${activePaperIdx}-${sIdx}`}
                onClick={() => {
                  setActiveSectionIdx(sIdx);
                  setShowAnswers({});
                }}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  activeSectionIdx === sIdx
                    ? 'bg-indigo-600 text-white shadow-sm border border-indigo-500'
                    : 'bg-indigo-900/60 text-indigo-200 hover:bg-indigo-800 hover:text-white'
                }`}
              >
                {sec.section_name || sec.title || `Section ${sIdx + 1}`}
              </button>
            ))}
          </div>
        )}
      </div>

      {currentPaper ? (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-6">
          <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 pb-4">
            <div>
              <div className="text-xs font-bold text-indigo-600 uppercase tracking-widest">Active Assessment Paper (Set {activePaperIdx + 1})</div>
              <h4 className="text-xl font-black text-slate-900">{currentPaper.paper_title || currentPaper.title || `Set ${activePaperIdx + 1} Practice Assessment`}</h4>
            </div>
            <div className="flex items-center gap-3 text-xs font-bold">
              {currentPaper.total_marks && <span className="px-3 py-1 bg-slate-100 rounded-full text-slate-700">Total Marks: {currentPaper.total_marks}</span>}
              {currentPaper.time_allowed_minutes && <span className="px-3 py-1 bg-slate-100 rounded-full text-slate-700">Time: {currentPaper.time_allowed_minutes} mins</span>}
            </div>
          </div>

          {/* Render Only Current Set's Current Section */}
          {currentSection ? (
            <div className="space-y-4 pt-2">
              <h5 className="text-sm font-black uppercase text-indigo-800 tracking-wider bg-indigo-50 p-3 rounded-xl border border-indigo-100">
                {currentSection.section_name || currentSection.title || `Section ${activeSectionIdx + 1}`}
              </h5>
              <div className="space-y-4">
                {Array.isArray(currentSection.questions) && currentSection.questions.map((q: any, qIdx: number) => {
                  const qKey = `${activePaperIdx}-${activeSectionIdx}-${qIdx}`;
                  const isAnswerVisible = showAnswers[qKey];
                  const correctAnswer = q.correct_answer || q.marking_scheme_answer || q.answer;
                  const displayQuestionText = cleanQuestionText(q.question_text || q.question || JSON.stringify(q));

                  return (
                    <div key={qIdx} className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-3">
                      <div className="flex items-center justify-between text-xs font-bold text-slate-500">
                        <span>Q{q.question_number || qIdx + 1}.</span>
                        <span className="px-2.5 py-0.5 bg-indigo-50 text-indigo-700 rounded-md font-extrabold">[{q.marks || 1} Mark{q.marks > 1 ? 's' : ''}]</span>
                      </div>

                      <div className="text-sm font-bold text-slate-900 leading-snug">
                        {displayQuestionText}
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
          ) : (
            <div className="p-8 text-center text-slate-500">No sections available for this set.</div>
          )}
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
