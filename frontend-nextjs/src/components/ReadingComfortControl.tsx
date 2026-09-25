'use client';

import React, { useState } from 'react';

export type ReadingTheme = 'light' | 'warm' | 'dark';
export type TextSize = 'medium' | 'large' | 'xlarge';
export type LineSpacing = 'normal' | 'comfortable' | 'spacious';

interface ReadingComfortControlProps {
  theme: ReadingTheme;
  textSize: TextSize;
  lineSpacing: LineSpacing;
  onThemeChange: (theme: ReadingTheme) => void;
  onTextSizeChange: (size: TextSize) => void;
  onLineSpacingChange: (spacing: LineSpacing) => void;
}

export const ReadingComfortControl: React.FC<ReadingComfortControlProps> = ({
  theme,
  textSize,
  lineSpacing,
  onThemeChange,
  onTextSizeChange,
  onLineSpacingChange,
}) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative inline-block text-left">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center gap-2 px-4 py-2 rounded-2xl bg-slate-800/90 hover:bg-slate-700/90 text-slate-200 text-sm font-bold border border-slate-700/80 shadow-md transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
        aria-label="Reading Comfort Controls"
        title="Adjust text size, line spacing, and theme"
      >
        <span className="text-base font-black font-serif">Aa</span>
        <span>Reading Comfort</span>
      </button>

      {isOpen && (
        <div
          className="origin-top-right absolute right-0 mt-2 w-72 rounded-3xl bg-slate-900 border border-slate-800 shadow-2xl p-5 z-50 space-y-5 backdrop-blur-md"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <span className="text-xs font-black uppercase tracking-widest text-indigo-400">
              Reading Controls
            </span>
            <button
              onClick={() => setIsOpen(false)}
              className="text-slate-400 hover:text-white text-xs font-bold"
            >
              ✕
            </button>
          </div>

          {/* Theme Selector */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase">Theme</label>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => onThemeChange('dark')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  theme === 'dark'
                    ? 'bg-slate-950 text-indigo-400 border-indigo-500 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                Dark
              </button>
              <button
                onClick={() => onThemeChange('warm')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  theme === 'warm'
                    ? 'bg-[#FFFBEB] text-[#D97706] border-[#F59E0B] shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                Warm
              </button>
              <button
                onClick={() => onThemeChange('light')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  theme === 'light'
                    ? 'bg-[#F8FAFC] text-[#4F46E5] border-[#6366F1] shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                Light
              </button>
            </div>
          </div>

          {/* Text Size Selector */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase">Text Size</label>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => onTextSizeChange('medium')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  textSize === 'medium'
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                Medium
              </button>
              <button
                onClick={() => onTextSizeChange('large')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  textSize === 'large'
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                Large
              </button>
              <button
                onClick={() => onTextSizeChange('xlarge')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  textSize === 'xlarge'
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                XL
              </button>
            </div>
          </div>

          {/* Line Spacing Selector */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-slate-400 uppercase">Line Spacing</label>
            <div className="grid grid-cols-3 gap-2">
              <button
                onClick={() => onLineSpacingChange('normal')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  lineSpacing === 'normal'
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                1.5
              </button>
              <button
                onClick={() => onLineSpacingChange('comfortable')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  lineSpacing === 'comfortable'
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                1.7
              </button>
              <button
                onClick={() => onLineSpacingChange('spacious')}
                className={`py-2 text-xs font-bold rounded-xl border transition-all ${
                  lineSpacing === 'spacious'
                    ? 'bg-indigo-600 text-white border-indigo-500 shadow-sm'
                    : 'bg-slate-900 text-slate-400 border-slate-800 hover:bg-slate-800'
                }`}
              >
                1.9
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
