import React from 'react';

interface GenericProps {
  title: string;
  data: any;
}

export const GenericStructuredRenderer: React.FC<GenericProps> = ({ title, data }) => {
  return (
    <div className="p-6 bg-slate-900 border border-slate-800 rounded-2xl space-y-4">
      <div className="flex items-center gap-3">
        <span className="px-2.5 py-1 text-xs font-semibold uppercase tracking-wider bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-md">
          Extensible Content Block
        </span>
        <h3 className="text-xl font-bold text-slate-100">{title}</h3>
      </div>
      <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 overflow-x-auto text-sm text-slate-300">
        <pre className="font-mono whitespace-pre-wrap">
          {typeof data === 'string' ? data : JSON.stringify(data, null, 2)}
        </pre>
      </div>
    </div>
  );
};
