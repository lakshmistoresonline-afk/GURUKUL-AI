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

function formatSectionName(name: string, index: number): string {
  if (!name) return `Section ${String.fromCharCode(65 + index)}`;
  if (name.startsWith('section_') || name.startsWith('sec_')) {
    const letter = name.replace(/section_|sec_/i, '').toUpperCase();
    return `Section ${letter}`;
  }
  return name;
}

function getQuestionCategory(q: any, sectionName: string = ''): string {
  const typeStr = (q.type || q.question_type || sectionName || '').toLowerCase();
  const hasOptions = Array.isArray(q.options) && q.options.length > 0;
  const marks = Number(q.marks || 1);

  if (typeStr.includes('true') || typeStr.includes('false') || 'is_true' in q) {
    return 'True / False';
  }
  if (hasOptions || typeStr.includes('mcq') || typeStr.includes('multiple choice')) {
    return 'MCQ';
  }
  if (typeStr.includes('long') || typeStr.includes('essay') || typeStr.includes('value') || marks >= 4) {
    return 'Long Answer';
  }
  if (typeStr.includes('short') || typeStr.includes('comprehension') || marks <= 3) {
    return 'Short Answer';
  }
  return 'Short Answer';
}

export default function QuestionPapersComponent({ data }: QuestionPapersProps) {
  const [activePaperIdx, setActivePaperIdx] = useState<number>(0);
  const [selectedCategory, setSelectedCategory] = useState<string>('All');
  const [showAnswers, setShowAnswers] = useState<Record<string, boolean>>({});
  const [selectedOptions, setSelectedOptions] = useState<Record<string, string>>({});

  const handleSelectOption = (key: string, opt: string) => {
    setSelectedOptions(prev => ({ ...prev, [key]: opt }));
  };

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

  // Collect all questions across all sections and assign categories
  const allQuestions: Array<{ q: any; sIdx: number; qIdx: number; sectionName: string; category: string }> = [];
  if (Array.isArray(sections)) {
    sections.forEach((sec: any, sIdx: number) => {
      const secName = formatSectionName(sec.section_name || sec.title, sIdx);
      if (Array.isArray(sec.questions)) {
        sec.questions.forEach((q: any, qIdx: number) => {
          const cat = getQuestionCategory(q, secName);
          allQuestions.push({ q, sIdx, qIdx, sectionName: secName, category: cat });
        });
      }
    });
  }

  const categories = ['All', 'MCQ', 'Short Answer', 'Long Answer', 'True / False'];
  const filteredQuestions = selectedCategory === 'All'
    ? allQuestions
    : allQuestions.filter(item => item.category === selectedCategory);

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
            <p className="text-indigo-200 text-sm mt-1">Categorized question bank by question type.</p>
          </div>
          {/* Paper Set Selector Tabs */}
          {Array.isArray(papers) && papers.length > 1 && (
            <div className="flex flex-wrap gap-1.5 bg-indigo-900/80 p-1.5 rounded-2xl border border-indigo-800">
              {papers.map((p: any, idx: number) => (
                <button
                  key={idx}
                  onClick={() => {
                    setActivePaperIdx(idx);
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

        {/* Question Type Filter Tabs */}
        <div className="flex flex-wrap gap-2 pt-2 border-t border-indigo-900">
          {categories.map((cat) => {
            const count = cat === 'All' ? allQuestions.length : allQuestions.filter(item => item.category === cat).length;
            if (count === 0 && cat !== 'All') return null;
            return (
              <button
                key={cat}
                onClick={() => setSelectedCategory(cat)}
                className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                  selectedCategory === cat
                    ? 'bg-indigo-600 text-white shadow-sm border border-indigo-500'
                    : 'bg-indigo-900/60 text-indigo-200 hover:bg-indigo-800 hover:text-white'
                }`}
              >
                {cat} ({count})
              </button>
            );
          })}
        </div>
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

          {/* Render Filtered Questions List */}
          {filteredQuestions.length > 0 ? (
            <div className="space-y-4 pt-2">
              <div className="text-xs font-extrabold text-indigo-700 uppercase tracking-wider bg-indigo-50 p-3 rounded-xl border border-indigo-100 flex items-center justify-between">
                <span>Showing Category: {selectedCategory}</span>
                <span>{filteredQuestions.length} Questions</span>
              </div>
              <div className="space-y-4">
                {filteredQuestions.map(({ q, sIdx, qIdx, sectionName }, index: number) => {
                  const qKey = `${activePaperIdx}-${sIdx}-${qIdx}`;
                  const isAnswerVisible = showAnswers[qKey];
                  const correctAnswer = q.correct_answer || q.marking_scheme_answer || q.answer || q.step_by_step_solution || q.solution;
                  const markingScheme = q.marking_scheme || q.marking_scheme_solution || '';
                  const stepSolution = q.step_by_step_solution || '';
                  const displayQuestionText = cleanQuestionText(q.question_text || q.question || JSON.stringify(q));

                  return (
                    <div key={index} className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-3">
                      <div className="flex items-center justify-between text-xs font-bold text-slate-500">
                        <div className="flex items-center gap-2">
                          <span>Q{index + 1}.</span>
                          <span className="px-2 py-0.5 bg-slate-200 text-slate-700 rounded text-[10px] font-bold">{sectionName}</span>
                        </div>
                        <span className="px-2.5 py-0.5 bg-indigo-50 text-indigo-700 rounded-md font-extrabold">[{q.marks || 1} Mark{q.marks > 1 ? 's' : ''}]</span>
                      </div>

                      <div className="text-sm font-bold text-slate-900 leading-snug">
                        {displayQuestionText}
                      </div>

                      {/* Options if MCQ */}
                      {Array.isArray(q.options) && q.options.length > 0 && (
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pt-1">
                          {q.options.map((opt: string, oIdx: number) => {
                            const selectedOpt = selectedOptions[qKey];
                            const isSelected = selectedOpt === opt;
                            let optStyle = 'bg-white border-slate-200 text-slate-700 hover:border-indigo-400 cursor-pointer';
                            if (isSelected) {
                              optStyle = 'bg-indigo-50 border-indigo-300 text-indigo-900 font-bold shadow-sm';
                            }
                            if (isAnswerVisible) {
                              if (opt === correctAnswer || opt.startsWith(`${correctAnswer})`) || opt === String(correctAnswer)) {
                                optStyle = 'bg-emerald-50 border-emerald-300 text-emerald-900 font-bold';
                              } else if (isSelected && opt !== correctAnswer) {
                                optStyle = 'bg-rose-50 border-rose-300 text-rose-900 font-bold';
                              }
                            }

                            return (
                              <button
                                key={oIdx}
                                type="button"
                                onClick={() => handleSelectOption(qKey, opt)}
                                className={`p-3 rounded-xl text-xs font-medium border text-left transition-all flex items-center justify-between ${optStyle}`}
                              >
                                <span>{opt}</span>
                                {isAnswerVisible && (opt === correctAnswer || opt.startsWith(`${correctAnswer})`) || opt === String(correctAnswer)) && <span className="text-emerald-600 font-black">✓</span>}
                                {isAnswerVisible && isSelected && opt !== correctAnswer && !opt.startsWith(`${correctAnswer})`) && <span className="text-rose-600 font-black">✗</span>}
                              </button>
                            );
                          })}
                        </div>
                      )}

                      {/* Marking Scheme / Step-by-step Solution Toggle */}
                      {(correctAnswer || markingScheme || stepSolution) && (
                        <div className="pt-2 border-t border-slate-200/60 mt-2">
                          <button
                            onClick={() => toggleAnswer(qKey)}
                            className="text-xs font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                          >
                            {isAnswerVisible ? 'Hide Step-by-Step Solution & Marking Scheme ▴' : 'Show Step-by-Step Solution & Marking Scheme ▾'}
                          </button>

                          {isAnswerVisible && (
                            <div className="mt-2 p-4 bg-emerald-50/60 border border-emerald-100 rounded-xl text-xs text-slate-800 leading-relaxed space-y-2">
                              {stepSolution && (
                                <div>
                                  <strong className="text-emerald-900 block mb-1">Step-by-Step Solution:</strong>
                                  <div className="whitespace-pre-line text-slate-700 bg-white p-3 rounded-lg border border-emerald-200/60 font-mono text-[11px]">{stepSolution}</div>
                                </div>
                              )}
                              {markingScheme && (
                                <div>
                                  <strong className="text-teal-900 block mb-1">Marking Scheme:</strong>
                                  <div className="text-slate-700 bg-white p-3 rounded-lg border border-teal-200/60 font-medium">{markingScheme}</div>
                                </div>
                              )}
                              {correctAnswer && !stepSolution && !markingScheme && (
                                <div>
                                  <strong className="text-emerald-900">Answer / Solution:</strong> {String(correctAnswer)}
                                </div>
                              )}
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
            <div className="p-8 text-center text-slate-500">No questions found for category: {selectedCategory}.</div>
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
