import React from 'react';

interface GrammarItem {
  topic: string;
  explanation: string;
}

interface GrammarProps {
  data: GrammarItem[] | { topics: GrammarItem[] };
}

export const GrammarRenderer: React.FC<GrammarProps> = ({ data }) => {
  const items = Array.isArray(data) ? data : (data as any).topics || [];

  return (
    <div className="space-y-4">
      {items.map((item: GrammarItem, idx: number) => (
        <div key={idx} className="p-5 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
          <h4 className="text-lg font-bold text-sky-400">{item.topic}</h4>
          <p className="text-slate-300 text-sm">{item.explanation}</p>
        </div>
      ))}
    </div>
  );
};
