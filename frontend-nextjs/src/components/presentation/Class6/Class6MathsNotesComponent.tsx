import React, { useState } from 'react';

function renderSafeText(val: any): React.ReactNode {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string' || typeof val === 'number') return val;
  if (Array.isArray(val)) {
    return val.map((item, idx) => (
      <div key={idx} className="my-1">{renderSafeText(item)}</div>
    ));
  }
  if (typeof val === 'object') {
    if (val.text) return val.text;
    if (val.definition) return `${val.term || val.word || ''}: ${val.definition}`;
    return Object.entries(val).map(([k, v], idx) => (
      <div key={idx} className="text-xs space-y-0.5">
        <strong className="capitalize text-indigo-700">{k.replace(/_/g, ' ')}:</strong> {renderSafeText(v)}
      </div>
    ));
  }
  return String(val);
}

interface MathsNotesProps {
  data: any;
}

export default function Class6MathsNotesComponent({ data }: MathsNotesProps) {
  const [activeSubTab, setActiveSubTab] = useState<string>('notes');

  if (!data) {
    return <div className="p-8 text-center text-slate-500">कोई गणित नोट्स उपलब्ध नहीं हैं।</div>;
  }

  const sec1 = data.section_1_complete_textbook_notes || {};
  const sec2 = data.section_2_step_by_step_algorithms || [];
  const sec3 = data.section_3_in_text_boxes_and_try_these || [];
  const sec4 = data.section_4_complete_textbook_exercise_solutions || [];

  const hasNotes = sec1 && Object.keys(sec1).length > 0;
  const hasAlgos = Array.isArray(sec2) && sec2.length > 0;
  const hasBoxes = Array.isArray(sec3) && sec3.length > 0;
  const hasSolutions = Array.isArray(sec4) && sec4.length > 0;

  return (
    <div className="space-y-6">
      {/* Sub-Section Selector Tabs Bar */}
      <div className="flex flex-wrap gap-2 bg-white p-2 rounded-2xl border border-slate-200 shadow-sm">
        {hasNotes && (
          <button
            onClick={() => setActiveSubTab('notes')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'notes' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📖 Complete Notes
          </button>
        )}
        {hasAlgos && (
          <button
            onClick={() => setActiveSubTab('algos')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'algos' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            ⚙️ Step-by-Step Algorithms ({sec2.length})
          </button>
        )}
        {hasBoxes && (
          <button
            onClick={() => setActiveSubTab('boxes')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'boxes' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            💡 Try These ({sec3.length})
          </button>
        )}
        {hasSolutions && (
          <button
            onClick={() => setActiveSubTab('solutions')}
            className={`px-4 py-2.5 rounded-xl text-xs font-extrabold transition-all ${activeSubTab === 'solutions' ? 'bg-indigo-600 text-white shadow-md' : 'text-slate-600 hover:bg-slate-100'}`}
          >
            📋 Exercise Solutions ({sec4.length})
          </button>
        )}
      </div>

      {/* Tab 1: Complete Textbook Notes */}
      {activeSubTab === 'notes' && hasNotes && (
        <div className="p-6 sm:p-8 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-100 pb-3">अध्याय नोट्स (Complete Textbook Notes)</h3>
          <div className="text-slate-700 text-sm leading-relaxed space-y-4">
            {typeof sec1 === 'string' ? sec1 : Object.entries(sec1).map(([key, val]: [string, any], idx: number) => (
              <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                <div className="text-xs font-black uppercase text-indigo-700 tracking-wider">{key.replace(/_/g, ' ')}</div>
                <div className="text-xs text-slate-700 leading-relaxed">{renderSafeText(val)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 2: Algorithms */}
      {activeSubTab === 'algos' && hasAlgos && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">चरण-दर-चरण एल्गोरिथ्म (Step-by-Step Algorithms)</h3>
          <div className="space-y-3">
            {sec2.map((algo: any, idx: number) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                <div className="text-xs font-bold text-indigo-600 uppercase">Algorithm #{idx + 1}</div>
                <div className="text-sm font-bold text-slate-900">{algo.title || algo.name || ''}</div>
                <div className="text-xs text-slate-700 leading-relaxed">{renderSafeText(algo.description || algo.steps || algo)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 3: Try These */}
      {activeSubTab === 'boxes' && hasBoxes && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">प्रयास कीजिए (Try These / In-Text Boxes)</h3>
          <div className="space-y-3">
            {sec3.map((box: any, idx: number) => (
              <div key={idx} className="p-5 bg-amber-50/50 border border-amber-100 rounded-2xl space-y-2">
                <div className="text-xs font-bold text-amber-900 uppercase">Box Problem #{idx + 1}</div>
                <div className="text-xs text-slate-800 font-medium">{renderSafeText(box.question || box.problem || box)}</div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tab 4: Solutions */}
      {activeSubTab === 'solutions' && hasSolutions && (
        <div className="space-y-4 animate-in fade-in duration-200">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">प्रश्नावली हल (Exercise Solutions)</h3>
          <div className="space-y-3">
            {sec4.map((sol: any, idx: number) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl shadow-sm space-y-2">
                <div className="text-xs font-bold text-slate-500">Exercise Item #{idx + 1}</div>
                <div className="text-sm font-bold text-slate-900">{sol.question || sol.q || ''}</div>
                <div className="text-xs text-emerald-800 bg-emerald-50 p-3 rounded-xl border border-emerald-100 font-semibold">
                  Solution: {renderSafeText(sol.solution || sol.answer || sol)}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
