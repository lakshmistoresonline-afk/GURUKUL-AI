import React from 'react';

interface QuestionPapersProps {
  data: any;
}

export default function QuestionPapersComponent({ data }: QuestionPapersProps) {
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

  return (
    <div className="space-y-8">
      <div className="p-6 sm:p-8 bg-indigo-900 rounded-3xl text-white shadow-xl space-y-2">
        <h3 className="text-2xl font-black tracking-tight">Examination Question Bank</h3>
        <p className="text-indigo-200 text-sm">Practice model question papers and summative assessments for this chapter.</p>
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
                  {paper.total_marks && <span className="px-3 py-1 bg-slate-100 rounded-full text-slate-700">Marks: {paper.total_marks}</span>}
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
                    {Array.isArray(sec.questions) && sec.questions.map((q: any, qIdx: number) => (
                      <div key={qIdx} className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-2">
                        <div className="text-xs font-bold text-slate-500">Q{qIdx + 1}. ({q.marks || 1} Marks)</div>
                        <div className="text-sm font-bold text-slate-900">{q.question_text || q.question || JSON.stringify(q)}</div>
                        {Array.isArray(q.options) && (
                          <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 pt-1">
                            {q.options.map((opt: string, oIdx: number) => (
                              <li key={oIdx}>{opt}</li>
                            ))}
                          </ul>
                        )}
                      </div>
                    ))}
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
