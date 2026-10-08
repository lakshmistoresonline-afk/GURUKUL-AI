'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { buildCurriculumUrl } from '@/lib/curriculumClient';

interface CommandPaletteProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function CommandPalette({ isOpen, onClose }: CommandPaletteProps) {
  const [query, setQuery] = useState('');
  const router = useRouter();

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

  const quickChapters = [
    {
      title: "Papa's Spectacles (Class 5 English)",
      href: buildCurriculumUrl({ grade: '5', subject: 'english', book: 'english', part: 'main', unit: 'U01', chapter_id: 'G5-ENG-U01-C01' })
    },
    {
      title: "किरन (Class 5 Hindi)",
      href: buildCurriculumUrl({ grade: '5', subject: 'hindi', book: 'hindi', part: 'main', unit: 'U01', chapter_id: 'G5-HIN-U01-C01' })
    },
    {
      title: "Travelling, Now and Then (Class 5 Maths)",
      href: buildCurriculumUrl({ grade: '5', subject: 'mathematics', book: 'mathematics', part: 'main', unit: 'U01', chapter_id: 'G5-MAT-U01-C01' })
    },
    {
      title: "Water — The Essence of Life (Class 5 Science)",
      href: buildCurriculumUrl({ grade: '5', subject: 'science', book: 'science', part: 'main', unit: 'U01', chapter_id: 'G5-SCI-U01-C01' })
    },
    {
      title: "A Bottle of Dew (Class 6 English)",
      href: buildCurriculumUrl({ grade: '6', subject: 'english', book: 'english', part: 'main', unit: 'U01', chapter_id: 'G6-ENG-U01-C01' })
    },
    {
      title: "मातृभूमि (Class 6 Hindi)",
      href: buildCurriculumUrl({ grade: '6', subject: 'hindi', book: 'hindi', part: 'main', unit: 'U01', chapter_id: 'G6-HIN-U01-C01' })
    },
    {
      title: "Patterns in Mathematics (Class 6 Maths)",
      href: buildCurriculumUrl({ grade: '6', subject: 'mathematics', book: 'mathematics', part: 'main', unit: 'U01', chapter_id: 'G6-MAT-U01-C01' })
    },
    {
      title: "The Wonderful World of Science (Class 6 Science)",
      href: buildCurriculumUrl({ grade: '6', subject: 'science', book: 'science', part: 'main', unit: 'U01', chapter_id: 'G6-SCI-U01-C01' })
    },
    {
      title: "Locating Places on the Earth (Class 6 Social)",
      href: buildCurriculumUrl({ grade: '6', subject: 'social_science', book: 'social', part: 'main', unit: 'U01', chapter_id: 'G6-SOC-U01-C01' })
    },
  ];

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
          <div className="text-[10px] font-black uppercase tracking-wider text-slate-400 px-3 py-1">Quick Navigation</div>
          {filtered.length > 0 ? (
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
