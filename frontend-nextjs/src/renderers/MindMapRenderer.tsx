import React from 'react';

function renderSafeText(val: any): string {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string') return val;
  if (typeof val === 'number' || typeof val === 'boolean') return String(val);
  if (typeof val === 'object') {
    return val.prompt || val.task || val.title || val.topic || val.details || val.text || val.description || JSON.stringify(val);
  }
  return String(val);
}

export const MindMapRenderer: React.FC<{ data: any }> = ({ data }) => {
  if (!data || typeof data !== 'object') return null;

  const rootNode = data.root_node || data.title || '';
  const centralTheme = data.central_theme || data.theme || '';

  // Extract Sub Nodes / Branches
  const subNodes: any[] = Array.isArray(data.sub_nodes)
    ? data.sub_nodes
    : Array.isArray(data.branches)
    ? data.branches
    : [];

  const grammarList = Array.isArray(data.keyGrammarConcepts) ? data.keyGrammarConcepts : [];
  const phoneticsList = Array.isArray(data.phonetics) ? data.phonetics : [];
  const activitiesList = Array.isArray(data.practicalActivities) ? data.practicalActivities : [];

  // Extract Story Mindmap
  const storyMindmap = data.story_mindmap;
  let storyStart = '';
  let storyEvents: string[] = [];
  let storyConclusion = '';

  if (typeof storyMindmap === 'object' && storyMindmap !== null) {
    storyStart = renderSafeText(storyMindmap.start || storyMindmap.aarambh);
    if (Array.isArray(storyMindmap.events)) {
      storyEvents = storyMindmap.events.map((e: any) => renderSafeText(e));
    } else if (Array.isArray(storyMindmap.ghatna)) {
      storyEvents = storyMindmap.ghatna.map((e: any) => renderSafeText(e));
    } else if (typeof storyMindmap.events === 'string') {
      storyEvents = [storyMindmap.events];
    }
    storyConclusion = renderSafeText(storyMindmap.conclusion || storyMindmap.nishkarsh);
  }

  const hasStory = storyStart || storyEvents.length > 0 || storyConclusion;
  const hasContent = rootNode || centralTheme || subNodes.length > 0 || grammarList.length > 0 || phoneticsList.length > 0 || activitiesList.length > 0 || hasStory;

  if (!hasContent) return null;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
          CONCEPT MIND MAP & STRUCTURE
        </h3>
        {rootNode && (
          <span className="px-3 py-1 bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-bold uppercase rounded-lg">
            {rootNode}
          </span>
        )}
      </div>

      {/* Central Theme Banner */}
      {centralTheme && (
        <div className="p-6 bg-indigo-50 border border-indigo-200 rounded-3xl space-y-2 shadow-sm">
          <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-700">
            Central Theme & Core Objective
          </h4>
          <p className="text-indigo-950 text-base md:text-lg font-medium leading-relaxed">
            {centralTheme}
          </p>
        </div>
      )}

      {/* Hierarchical Sub-Nodes Grid */}
      {subNodes.length > 0 && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {subNodes.map((node: any, nIdx: number) => {
            const nodeTitle = node.title || node.branch_title || `Branch #${nIdx + 1}`;
            const childNodes: any[] = Array.isArray(node.child_nodes) ? node.child_nodes : Array.isArray(node.subbranches) ? node.subbranches : [];

            return (
              <div key={nIdx} className="p-6 bg-white border border-slate-200 rounded-3xl space-y-3 shadow-sm">
                <div className="flex items-center justify-between border-b border-slate-100 pb-2">
                  <h4 className="text-base font-extrabold text-slate-900 tracking-tight">{nodeTitle}</h4>
                  <span className="text-[11px] font-mono text-slate-400">Node #{nIdx + 1}</span>
                </div>

                {childNodes.length > 0 ? (
                  <div className="space-y-2.5 pt-1">
                    {childNodes.map((child: any, cIdx: number) => {
                      const cTitle = child.title || child.topic || '';
                      const cDetails = child.details || child.description || renderSafeText(child);

                      return (
                        <div key={cIdx} className="p-3.5 bg-slate-50 border border-slate-200/80 rounded-2xl space-y-1">
                          {cTitle && <div className="text-xs font-bold text-indigo-700 uppercase">{cTitle}</div>}
                          <p className="text-slate-800 text-sm leading-relaxed">{cDetails}</p>
                        </div>
                      );
                    })}
                  </div>
                ) : (
                  <p className="text-slate-700 text-sm leading-relaxed">{renderSafeText(node)}</p>
                )}
              </div>
            );
          })}
        </div>
      )}

      {/* Grammar & Language Node Card */}
      {grammarList.length > 0 && (
        <div className="p-6 bg-white border border-slate-200 rounded-3xl space-y-3 shadow-sm">
          <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-600 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-indigo-600" />
            <span>Key Grammar & Language Focus</span>
          </h4>
          <ul className="space-y-2 pt-1">
            {grammarList.map((item: any, idx: number) => (
              <li key={idx} className="p-3 bg-slate-50 border border-slate-200 rounded-xl text-slate-800 text-sm font-medium">
                {renderSafeText(item)}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Story Mindmap Node Tree */}
      {hasStory && (
        <div className="p-6 bg-white border border-slate-200 rounded-3xl space-y-4 shadow-sm">
          <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-600 flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-indigo-600" />
            <span>Narrative Progression & Story Structure</span>
          </h4>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-1">
            {storyStart && (
              <div className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-2">
                <span className="text-xs font-extrabold uppercase tracking-wider text-emerald-700">
                  Beginning
                </span>
                <p className="text-slate-900 text-sm font-medium leading-relaxed">{storyStart}</p>
              </div>
            )}

            {storyEvents.length > 0 && (
              <div className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-2 sm:col-span-2">
                <span className="text-xs font-extrabold uppercase tracking-wider text-indigo-700">
                  Key Narrative Events
                </span>
                <ul className="space-y-1.5 list-disc list-inside text-slate-900 text-sm font-medium pl-1">
                  {storyEvents.map((ev: any, eIdx: number) => (
                    <li key={eIdx}>{ev}</li>
                  ))}
                </ul>
              </div>
            )}

            {storyConclusion && (
              <div className="p-5 bg-slate-50 border border-slate-200 rounded-2xl space-y-2 sm:col-span-3">
                <span className="text-xs font-extrabold uppercase tracking-wider text-amber-700">
                  Conclusion & Moral Message
                </span>
                <p className="text-slate-900 text-sm font-medium leading-relaxed">{storyConclusion}</p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
