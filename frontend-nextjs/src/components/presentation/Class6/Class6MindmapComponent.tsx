import React from 'react';

interface Class6MindmapProps {
  data: any;
}

export default function Class6MindmapComponent({ data }: Class6MindmapProps) {
  if (!data) {
    return <div className="p-8 text-center text-slate-500">No mindmap available.</div>;
  }

  const mapData = data.mind_map || data.mindmap || data;
  const rootNode = mapData.root_node || mapData.central_node || mapData.chapter_title || 'Central Concept';

  // Extract Class 6 node categories
  const categories = [
    { key: 'plot_summary_nodes', title: 'Plot & Summary' },
    { key: 'character_arc_nodes', title: 'Character Arcs' },
    { key: 'theme_and_moral_nodes', title: 'Theme & Morals' },
    { key: 'key_grammar_nodes', title: 'Grammar & Language' },
    { key: 'sub_nodes', title: 'Sub Nodes' },
    { key: 'main_branches', title: 'Main Branches' }
  ];

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

      {/* Categories / Branches */}
      <div className="space-y-6">
        <h3 className="text-xl font-black text-slate-900 border-b border-slate-200 pb-3">Concept Branches</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {categories.map((cat) => {
            const items = mapData[cat.key];
            if (!Array.isArray(items) || items.length === 0) return null;

            return (
              <div key={cat.key} className="p-6 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4 hover:border-indigo-300 transition-all">
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                  <span className="text-xs font-black uppercase tracking-wider text-indigo-600">{cat.title}</span>
                </div>
                <div className="space-y-3 pt-2">
                  {items.map((item: any, idx: number) => (
                    <div key={idx} className="p-4 bg-slate-50 border border-slate-100 rounded-2xl text-xs text-slate-800 leading-relaxed font-medium">
                      {typeof item === 'string' ? item : item.title || item.details || JSON.stringify(item)}
                    </div>
                  ))}
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
