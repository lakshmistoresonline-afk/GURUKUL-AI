import React from 'react';

interface PhoneticsItem {
  sound: string;
  words: string[];
}

interface PhoneticsProps {
  data: PhoneticsItem[];
}

export const PhoneticsRenderer: React.FC<PhoneticsProps> = ({ data }) => {
  const items = Array.isArray(data) ? data : [];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
      {items.map((item, idx) => (
        <div key={idx} className="p-5 bg-slate-900 border border-slate-800 rounded-xl space-y-2">
          <span className="text-xl font-bold text-indigo-400 font-mono">{item.sound}</span>
          <div className="flex flex-wrap gap-2 pt-2">
            {item.words?.map((w, wIdx) => (
              <span key={wIdx} className="px-2.5 py-1 text-xs bg-slate-800 text-slate-300 rounded-md">
                {w}
              </span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
};
