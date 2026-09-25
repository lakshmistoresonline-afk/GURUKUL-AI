import React from 'react';

function renderSafeText(val: any): string {
  if (val === null || val === undefined) return '';
  if (typeof val === 'string') return val;
  if (typeof val === 'number' || typeof val === 'boolean') return String(val);
  if (typeof val === 'object') {
    return val.explanation || val.overview || val.summary || val.text || val.details || val.title || val.description || '';
  }
  return String(val);
}

export const OverviewRenderer: React.FC<{ data: any; title?: string }> = ({ data }) => {
  if (!data) return null;

  let summaryText = '';
  let themeText = '';
  let themesList: string[] = [];
  let keySectionsList: { heading: string; summary: string; key_terms?: string[] }[] = [];
  let characterList: { name: string; traits: string }[] = [];
  let poeticInfo: { scheme?: string; pairs?: string[]; devices?: string[] } | null = null;
  let takeawaysList: string[] = [];
  let stanzaSummaries: { stanza: number; summary: string }[] = [];

  if (typeof data === 'string') {
    summaryText = data;
  } else if (Array.isArray(data)) {
    // Handle array of concept/topic dicts: [{"topic": "...", "explanation": "...", "key_terms": [...]}]
    keySectionsList = data.map((item: any) => {
      if (typeof item === 'string') return { heading: 'Topic', summary: item };
      return {
        heading: item.topic || item.heading || item.title || 'Core Topic',
        summary: item.explanation || item.summary || item.details || renderSafeText(item),
        key_terms: Array.isArray(item.key_terms) ? item.key_terms : []
      };
    });
  } else if (typeof data === 'object') {
    if (typeof data.overview === 'string') {
      summaryText = data.overview;
    } else if (typeof data.summary === 'string') {
      summaryText = data.summary;
    } else if (typeof data.overview === 'object' && data.overview !== null) {
      summaryText = renderSafeText(data.overview);
    } else if (typeof data.summary === 'object' && data.summary !== null) {
      summaryText = renderSafeText(data.summary);
    }

    if (typeof data.centralTheme === 'string') {
      themeText = data.centralTheme;
    } else if (typeof data.theme_and_moral === 'string') {
      themeText = data.theme_and_moral;
    } else if (typeof data.theme_and_moral === 'object' && data.theme_and_moral !== null) {
      themeText = [data.theme_and_moral.theme, data.theme_and_moral.moral].filter(Boolean).join(' • ');
    }

    if (Array.isArray(data.coreThemes)) {
      themesList = data.coreThemes;
    } else if (Array.isArray(data.conceptual_foundation)) {
      themesList = data.conceptual_foundation;
    }

    // Extract Science Key Sections or Topic Lists
    if (Array.isArray(data.keySections)) {
      keySectionsList = data.keySections.map((s: any) => ({
        heading: s.heading || s.title || s.topic || 'Key Section',
        summary: s.summary || s.overview || s.explanation || s.details || s.content || (Array.isArray(s.points) ? s.points.join(' ') : ''),
        key_terms: Array.isArray(s.key_terms) ? s.key_terms : []
      }));
    } else if (Array.isArray(data.concepts)) {
      keySectionsList = data.concepts.map((s: any) => ({
        heading: s.topic || s.heading || s.title || 'Core Concept',
        summary: s.explanation || s.summary || s.details || renderSafeText(s),
        key_terms: Array.isArray(s.key_terms) ? s.key_terms : []
      }));
    }

    // Extract Character Analysis
    if (Array.isArray(data.characterAnalysis)) {
      characterList = data.characterAnalysis.map((c: any) => ({
        name: c.character || c.character_name || 'Character',
        traits: c.traits || ''
      }));
    }

    // Extract Poetic Devices
    if (data.poeticDevices && typeof data.poeticDevices === 'object') {
      poeticInfo = {
        scheme: data.poeticDevices.rhymeScheme,
        pairs: Array.isArray(data.poeticDevices.rhymingPairs) ? data.poeticDevices.rhymingPairs : [],
        devices: Array.isArray(data.poeticDevices.poeticDevices) ? data.poeticDevices.poeticDevices : []
      };
    }

    // Extract Takeaways
    if (Array.isArray(data.importantTakeaways)) {
      takeawaysList = data.importantTakeaways;
    }

    // Extract Stanza Summaries if present
    if (Array.isArray(data.detailedBreakdown)) {
      stanzaSummaries = data.detailedBreakdown.filter((s: any) => s && s.stanza && s.summary);
    }
  }

  const hasAnyContent =
    summaryText ||
    themeText ||
    themesList.length > 0 ||
    keySectionsList.length > 0 ||
    characterList.length > 0 ||
    poeticInfo ||
    takeawaysList.length > 0 ||
    stanzaSummaries.length > 0;

  if (!hasAnyContent) return null;

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between border-b border-slate-200 pb-3">
        <h3 className="text-xs font-black uppercase tracking-widest text-indigo-600">
          COMPLETE CHAPTER OVERVIEW & ANALYSIS
        </h3>
      </div>

      {/* Summary Text */}
      {summaryText && (
        <div className="p-6 md:p-8 bg-white border border-slate-200 rounded-3xl space-y-3 shadow-sm">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Chapter Summary & Overview
          </h4>
          <p className="text-slate-900 text-base md:text-lg leading-relaxed font-normal">
            {summaryText}
          </p>
        </div>
      )}

      {/* Key Sections & Concepts Grid (No Raw JSON Strings!) */}
      {keySectionsList.length > 0 && (
        <div className="space-y-4">
          <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-600">
            Key Sections & Core Scientific Concepts
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {keySectionsList.map((sec, idx) => (
              <div key={idx} className="p-6 bg-white border border-slate-200 rounded-3xl space-y-3 shadow-sm">
                <div className="flex items-center justify-between gap-2 border-b border-slate-100 pb-2">
                  <h5 className="text-base font-extrabold text-slate-900 tracking-tight leading-snug">{sec.heading}</h5>
                  <span className="text-[11px] font-mono text-slate-400">#{idx + 1}</span>
                </div>

                <p className="text-slate-800 text-sm leading-relaxed">{renderSafeText(sec.summary)}</p>

                {sec.key_terms && sec.key_terms.length > 0 && (
                  <div className="pt-2 flex flex-wrap gap-1.5 border-t border-slate-100">
                    <span className="text-[11px] font-bold text-slate-400 uppercase mr-1">Key Terms:</span>
                    {sec.key_terms.map((term, tIdx) => (
                      <span key={tIdx} className="px-2 py-0.5 bg-slate-100 text-slate-700 border border-slate-200 rounded-md text-[11px] font-medium">
                        {term}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Central Theme & Moral */}
      {themeText && (
        <div className="p-6 md:p-8 bg-indigo-50 border border-indigo-200/80 rounded-3xl space-y-2 shadow-sm">
          <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-700">
            Central Theme & Moral Message
          </h4>
          <p className="text-indigo-950 text-base md:text-lg font-medium leading-relaxed">
            {themeText}
          </p>
        </div>
      )}

      {/* Character Analysis Grid */}
      {characterList.length > 0 && (
        <div className="space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Character Analysis & Key Traits
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {characterList.map((c, idx) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm">
                <span className="px-2.5 py-0.5 text-[11px] font-bold uppercase bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-md">
                  Character #{idx + 1}
                </span>
                <h5 className="text-lg font-bold text-slate-900">{c.name}</h5>
                <p className="text-slate-700 text-sm italic">Traits: {c.traits}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Stanza-by-Stanza Outline */}
      {stanzaSummaries.length > 0 && (
        <div className="space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Stanza-by-Stanza Narrative Outline
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {stanzaSummaries.map((s, idx) => (
              <div key={idx} className="p-5 bg-white border border-slate-200 rounded-2xl space-y-2 shadow-sm">
                <span className="text-xs font-bold text-indigo-600 uppercase">
                  Stanza {s.stanza}
                </span>
                <p className="text-slate-800 text-sm leading-relaxed">{s.summary}</p>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Poetic Devices Analysis */}
      {poeticInfo && (
        <div className="p-6 md:p-8 bg-white border border-slate-200 rounded-3xl space-y-4 shadow-sm">
          <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-600">
            Poetic Devices & Literary Structure
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
            {poeticInfo.scheme && (
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl space-y-1">
                <span className="text-xs font-bold text-slate-500 uppercase">Rhyme Scheme</span>
                <p className="text-indigo-700 font-extrabold text-base">{poeticInfo.scheme}</p>
              </div>
            )}
            {poeticInfo.pairs && poeticInfo.pairs.length > 0 && (
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl space-y-1">
                <span className="text-xs font-bold text-slate-500 uppercase">Rhyming Pairs</span>
                <p className="text-emerald-700 font-medium text-xs">{poeticInfo.pairs.join(', ')}</p>
              </div>
            )}
            {poeticInfo.devices && poeticInfo.devices.length > 0 && (
              <div className="p-4 bg-slate-50 border border-slate-200 rounded-2xl space-y-1">
                <span className="text-xs font-bold text-slate-500 uppercase">Literary Devices</span>
                <p className="text-amber-700 font-medium text-xs">{poeticInfo.devices.join(', ')}</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Important Takeaways */}
      {takeawaysList.length > 0 && (
        <div className="space-y-3">
          <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500">
            Important Takeaways & Core Lessons
          </h4>
          <div className="space-y-2">
            {takeawaysList.map((item, idx) => (
              <div key={idx} className="p-4 bg-white border border-slate-200 rounded-2xl flex items-center gap-3 shadow-sm">
                <span className="w-2 h-2 rounded-full bg-emerald-500 shrink-0" />
                <p className="text-slate-800 text-sm md:text-base font-medium">{renderSafeText(item)}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
