import React from 'react';

interface SocialMindmapProps {
  data: any;
}

export default function Class6SocialMindmapComponent({ data }: SocialMindmapProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No mindmap available.</div>;
  }

  const mapData = data.mind_map || data.mindmap || data;
  const rootNode = mapData.chapter_title || mapData.central_topic || 'Social Concept Tree';
  const nodes = mapData.nodes || [];

  return (
    <div className="space-y-8">
      {/* Root / Central Theme Card */}
      <div className="p-8 bg-gradient-to-br from-indigo-600 to-indigo-800 rounded-3xl text-white shadow-xl text-center space-y-3">
        <div className="inline-block px-3 py-1 rounded-full bg-indigo-500/50 border border-indigo-400/40 text-indigo-100 text-xs font-bold uppercase tracking-widest">
          Mindmap Root
        </div>
        <h2 className="text-3xl font-black tracking-tight">{rootNode}</h2>
        {mapData.central_topic && (
          <p className="text-indigo-100 text-sm max-w-2xl mx-auto opacity-90 leading-relaxed">
            {mapData.central_topic}
          </p>
        )}
      </div>

      {/* Nodes */}
      {Array.isArray(nodes) && nodes.length > 0 ? (
        <div className="space-y-6">
          <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Concept Nodes & Topics</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {nodes.map((node: any, idx: number) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-3 hover:border-indigo-300 transition-all">
                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                  <span className="text-xs font-bold text-indigo-600 uppercase">{node.topic_level || `Node #${idx + 1}`}</span>
                  <span className="text-xs font-mono bg-indigo-50 px-2 py-0.5 rounded text-indigo-700">{node.node_id}</span>
                </div>
                <h4 className="text-lg font-black text-slate-900">{node.title}</h4>
                {node.summary && <p className="text-xs text-slate-600 leading-relaxed">{node.summary}</p>}

                {Array.isArray(node.details_and_keywords) && node.details_and_keywords.length > 0 && (
                  <div className="flex flex-wrap gap-1 pt-1">
                    {node.details_and_keywords.map((kw: string, kIdx: number) => (
                      <span key={kIdx} className="px-2 py-0.5 bg-slate-100 text-slate-700 text-[10px] font-bold rounded-md">{kw}</span>
                    ))}
                  </div>
                )}
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
