import React from 'react';

interface HindiMindmapProps {
  data: any;
}

export default function Class6HindiMindmapComponent({ data }: HindiMindmapProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No mindmap available.</div>;
  }

  const mapData = data.mind_map || data.mindmap || data;
  const rootNode = mapData.root_topic || mapData.root_node || mapData.central_node || mapData.chapter_title || 'केंद्रीय संकल्पना (Central Concept)';
  const branches = mapData.branches || mapData.sub_nodes || mapData.main_branches || [];

  return (
    <div className="space-y-8">
      {/* Root / Central Theme Card */}
      <div className="p-8 bg-gradient-to-br from-indigo-600 to-indigo-800 rounded-3xl text-white shadow-xl text-center space-y-3">
        <div className="inline-block px-3 py-1 rounded-full bg-indigo-500/50 border border-indigo-400/40 text-indigo-100 text-xs font-bold uppercase tracking-widest">
          Mindmap Root
        </div>
        <h2 className="text-3xl font-black tracking-tight">
          {typeof rootNode === 'string' ? rootNode : rootNode.title || JSON.stringify(rootNode)}
        </h2>
      </div>

      {/* Concept Branches */}
      {Array.isArray(branches) && branches.length > 0 ? (
        <div className="space-y-6">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">विचार शाखाएँ (Concept Branches)</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {branches.map((branch: any, idx: number) => {
              const subBranches = branch.sub_branches || branch.child_nodes || branch.children || [];
              const branchTitle = branch.theme || branch.title || branch.name || `शाखा #${idx + 1}`;
              return (
                <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 hover:border-indigo-300 transition-all">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                    <span className="text-xs font-black uppercase tracking-wider text-indigo-600">शाखा #{idx + 1}</span>
                  </div>
                  <h4 className="text-lg font-black text-slate-900">{branchTitle}</h4>

                  {Array.isArray(subBranches) && subBranches.length > 0 && (
                    <div className="space-y-3 pt-2">
                      {subBranches.map((sub: any, sIdx: number) => (
                        <div key={sIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                          <div className="text-xs font-bold text-indigo-900">{sub.concept_or_event || sub.title || sub.topic || ''}</div>

                          {Array.isArray(sub.detailed_explanation) && sub.detailed_explanation.length > 0 && (
                            <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 pt-1">
                              {sub.detailed_explanation.map((det: string, dIdx: number) => (
                                <li key={dIdx}>{det}</li>
                              ))}
                            </ul>
                          )}

                          {Array.isArray(sub.associated_vocabulary) && sub.associated_vocabulary.length > 0 && (
                            <div className="flex flex-wrap gap-1 pt-1">
                              {sub.associated_vocabulary.map((av: string, avIdx: number) => (
                                <span key={avIdx} className="px-2 py-0.5 bg-indigo-50 text-indigo-700 text-[10px] font-bold rounded-md border border-indigo-200">{av}</span>
                              ))}
                            </div>
                          )}

                          {Array.isArray(sub.associated_grammar) && sub.associated_grammar.length > 0 && (
                            <div className="text-[11px] font-serif italic text-emerald-800 bg-emerald-50/50 p-2 rounded-xl">
                              <strong>व्याकरण:</strong> {sub.associated_grammar.join(' | ')}
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      ) : null}
    </div>
  );
}
