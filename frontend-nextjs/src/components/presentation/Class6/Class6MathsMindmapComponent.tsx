import React from 'react';

interface MathsMindmapProps {
  data: any;
}

export default function Class6MathsMindmapComponent({ data }: MathsMindmapProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No mindmap available.</div>;
  }

  const mapData = data.mind_map || data.mindmap || data;
  const rootNode = mapData.root_node || mapData.central_node || mapData.chapter_title || 'Mathematical Concept Tree';
  const subNodes = mapData.sub_nodes || mapData.branches || mapData.nodes || mapData.main_branches || [];

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

      {/* Sub Nodes / Branches */}
      {Array.isArray(subNodes) && subNodes.length > 0 ? (
        <div className="space-y-6">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Concept Branches</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {subNodes.map((node: any, idx: number) => {
              const children = node.child_nodes || node.children || node.sub_nodes || node.sub_topics || node.sub_branches || [];
              const branchTitle = node.title || node.name || node.branch_title || node.branch_name || `Branch #${idx + 1}`;
              return (
                <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 hover:border-indigo-300 transition-all">
                  <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                    <span className="text-xs font-black uppercase tracking-wider text-indigo-600">Branch #{idx + 1}</span>
                  </div>
                  <h4 className="text-lg font-black text-slate-900">{branchTitle}</h4>

                  {Array.isArray(children) && children.length > 0 && (
                    <div className="space-y-3 pt-2">
                      {children.map((child: any, cIdx: number) => (
                        <div key={cIdx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl space-y-2">
                          <div className="text-xs font-bold text-indigo-900">{child.title || child.name || child.topic || child.sub_title || ''}</div>
                          {child.details && <div className="text-xs text-slate-600 leading-relaxed">{child.details}</div>}

                          {Array.isArray(child.key_nodes) && child.key_nodes.length > 0 && (
                            <ul className="list-disc list-inside text-xs text-slate-700 space-y-1 pt-1">
                              {child.key_nodes.map((kn: string, knIdx: number) => (
                                <li key={knIdx}>{kn}</li>
                              ))}
                            </ul>
                          )}

                          {child.misconception_alert && (
                            <div className="text-[11px] font-medium text-rose-700 bg-rose-50 p-2.5 rounded-xl border border-rose-100">
                              <strong>⚠️ Note:</strong> {child.misconception_alert}
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
