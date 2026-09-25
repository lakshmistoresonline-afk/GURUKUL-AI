import React from 'react';

interface QuestionProps {
  data: any;
}

export const QuestionRenderer: React.FC<QuestionProps> = ({ data }) => {
  const questions = Array.isArray(data) ? data : [data];

  return (
    <div className="space-y-4">
      {questions.map((q, idx) => (
        <div key={idx} className="p-5 bg-slate-900 border border-slate-800 rounded-xl space-y-3">
          <p className="font-semibold text-slate-100">{q.question || q.prompt || JSON.stringify(q)}</p>
          {q.options && (
            <div className="grid grid-cols-1 gap-2 pt-2">
              {q.options.map((opt: string, oIdx: number) => (
                <div key={oIdx} className="p-3 bg-slate-950 border border-slate-800 rounded-lg text-sm text-slate-300">
                  {opt}
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};
