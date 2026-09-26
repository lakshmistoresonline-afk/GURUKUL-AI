import React from 'react';

interface MindmapProps {
  data: any;
}

export default function MindmapComponent({ data }: MindmapProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No mindmap available.</div>;
  }

  const rootNode = data.root_node || data.root || 'Central Concept';
  const centralTheme = data.central_theme || data.theme || '';
  const subNodes = data.sub_nodes || data.branches || data.nodes || [];

  return (
    <div className="space-y-8">
      {/* Root / Central Theme Card */}
      <div className="p-8 bg-gradient-to-br from-indigo-600 to-indigo-800 rounded-3xl text-white shadow-xl text-center space-y-3">
        <div className="inline-block px-3 py-1 rounded-full bg-indigo-500/50 border border-indigo-400/40 text-indigo-100 text-xs font-bold uppercase tracking-widest">
          Mindmap Root
        </div>
        <h2 className="text-3xl font-black tracking-tight">{rootNode}</h2>
        {centralTheme && (
          <p className="text-indigo-100 text-sm max-w-2xl mx-auto opacity-90 leading-relaxed">
            {centralTheme}
          </p>
        )}
      </div>

      {/* Sub Nodes / Branches */}
      {Array.isArray(subNodes) && subNodes.length > 0 ? (
        <div className="space-y-4">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Concept Branches</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {subNodes.map((node: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3 hover:border-indigo-300 transition-all">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-black uppercase tracking-wider text-indigo-600">Branch #{idx + 1}</span>
                  {node.node_id && <span className="text-xs font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-500">{node.node_id}</span>}
                </div>
                <h4 className="text-lg font-bold text-slate-900">{node.title || node.name}</h4>
                <p className="text-slate-600 text-sm leading-relaxed">{node.detail || node.description || node.details || ''}</p>
              </div>
            ))}
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
