'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { CurriculumApiClient, buildCurriculumUrl } from '@/lib/curriculumClient';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
  hierarchy?: any[];
}

export default function CommandPalette({ isOpen, onClose, hierarchy }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const [hierarchyData, setHierarchyData] = useState<any[]>(hierarchy || []);
  const [loading, setLoading] = useState<boolean>(false);
  const [loadError, setLoadError] = useState<string | null>(null);
  const router = useRouter();

  // Defect B: Fallback fetch with lifecycle protection & sync with prop hierarchy
  useEffect(() => {
    let isMounted = true;
    if (hierarchy && hierarchy.length > 0) {
      setHierarchyData(hierarchy);
      setLoading(false);
      setLoadError(null);
    } else if (isOpen && (!hierarchy || hierarchy.length === 0) && hierarchyData.length === 0) {
      setLoading(true);
      setLoadError(null);
      CurriculumApiClient.fetchHierarchy()
        .then(data => {
          if (!isMounted) return;
          setHierarchyData(data);
          setLoading(false);
        })
        .catch(err => {
          if (!isMounted) return;
          setLoadError(err.message || 'Failed to fetch authoritative hierarchy.');
          setLoading(false);
        });
    }
    return () => {
      isMounted = false;
    };
  }, [hierarchy, isOpen, hierarchyData.length]);

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        if (isOpen) onClose();
      } else if (e.key === 'Escape' && isOpen) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Build Quick Navigation exclusively from authoritative hierarchy data
  const quickChapters: Array<{ title: string; href: string }> = [];
  for (const g of hierarchyData) {
    for (const s of g.subjects || []) {
      for (const b of s.books || []) {
        for (const u of b.units || []) {
          for (const ch of u.chapters || []) {
            quickChapters.push({
              title: `${ch.chapter_title || ch.title} (Class ${g.grade} • ${s.subject})`,
              href: buildCurriculumUrl({
                grade: String(g.grade),
                subject: s.canonical_subject,
                book: b.book_id,
                part: b.part,
                unit: u.unit_id,
                chapter_id: ch.chapter_id
              })
            });
          }
        }
      }
    }
  }

  const filtered = quickChapters.filter(c => c.title.toLowerCase().includes(query.toLowerCase()));

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-start justify-center pt-20 px-4">
      <div className="bg-white border border-slate-200 rounded-3xl shadow-2xl max-w-2xl w-full overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        <div className="p-4 border-b border-slate-100 flex items-center gap-3">
          <span className="text-xl">🔍</span>
          <input
            type="text"
            autoFocus
            placeholder="Type a chapter or topic to jump instantly..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-slate-900 placeholder:text-slate-400 text-base focus:outline-none font-medium"
          />
          <kbd className="hidden sm:inline-block px-2 py-1 bg-slate-100 border border-slate-200 rounded-lg text-[10px] font-mono text-slate-500">ESC</kbd>
        </div>

        <div className="max-h-96 overflow-y-auto p-3 space-y-1">
          <div className="text-[10px] font-black uppercase tracking-wider text-slate-400 px-3 py-1">Authoritative Quick Navigation</div>
          {loading ? (
            <div className="p-8 text-center text-slate-500 text-xs">Loading authoritative hierarchy...</div>
          ) : loadError ? (
            <div className="p-8 text-center text-rose-600 text-xs font-bold">Failed to load authoritative hierarchy: {loadError}</div>
          ) : hierarchyData.length === 0 ? (
            <div className="p-8 text-center text-slate-400 text-xs">Authoritative curriculum hierarchy is empty.</div>
          ) : filtered.length > 0 ? (
            filtered.map((item, idx) => (
              <button
                key={idx}
                onClick={() => {
                  router.push(item.href);
                  onClose();
                }}
                className="w-full text-left px-4 py-3 rounded-2xl hover:bg-indigo-50 hover:text-indigo-950 text-slate-700 text-sm font-bold transition-all flex items-center justify-between group"
              >
                <span>{item.title}</span>
                <span className="text-xs text-slate-400 group-hover:text-indigo-600">Jump ➔</span>
              </button>
            ))
          ) : (
            <div className="p-8 text-center text-slate-400 text-xs">No matching chapters found.</div>
          )}
        </div>

        <div className="p-3 bg-slate-50 border-t border-slate-100 text-[11px] text-slate-400 flex items-center justify-between px-4">
          <span>Tip: Press <kbd className="px-1.5 py-0.5 bg-white border border-slate-200 rounded text-[10px]">Ctrl + K</kbd> anywhere</span>
          <span className="font-bold text-indigo-600">Gurukul AI Command Center</span>
        </div>
      </div>
    </div>
  );
}
