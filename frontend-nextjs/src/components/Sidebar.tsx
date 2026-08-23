'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { GraduationCap } from 'lucide-react';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { navItems } from '@/config/navigation';
import { useLearning } from '@/context/LearningContext';
import { RefreshCw, BookOpen } from 'lucide-react';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function Sidebar() {
  const pathname = usePathname();
  const { isContextComplete, setChapter, clearContext } = useLearning();

  return (
    <aside className="hidden lg:flex flex-col w-72 bg-[#0F172A] h-screen sticky top-0 border-r border-white/5 z-20 flex-shrink-0">
      <div className="p-8 flex flex-col h-full">
        <Link href="/dashboard" className="flex items-center gap-4 mb-12 group">
          <div className="w-12 h-12 bg-primary rounded-2xl flex items-center justify-center text-white shadow-lg shadow-primary/20 group-hover:scale-110 transition-transform">
            <GraduationCap size={28} />
          </div>
          <div className="flex flex-col">
            <span className="text-white font-black text-xl tracking-tighter leading-none">GURUKUL AI</span>
            <span className="text-[11px] font-black text-slate-400 uppercase tracking-[0.15em] mt-1.5">Classroom</span>
          </div>
        </Link>

        <nav className="flex flex-col gap-3">
          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative group flex items-center gap-4 px-6 py-4 rounded-2xl transition-all",
                  isActive
                    ? "bg-primary text-white shadow-[0_12px_24px_rgba(37,99,235,0.3)]"
                    : "text-slate-400 hover:text-white hover:bg-white/5"
                )}
              >
                <item.icon size={22} className={cn(isActive ? "text-white" : "text-slate-400 group-hover:text-white")} />
                <span className="font-black text-sm tracking-tight">{item.label}</span>

                {isActive && (
                   <div className="absolute right-0 w-1.5 h-6 bg-white rounded-l-full" />
                )}
              </Link>
            );
          })}
        </nav>

        <div className="mt-auto space-y-4 pt-10 border-t border-white/5">
          {isContextComplete && (
            <div className="px-2 space-y-2">
              <button
                onClick={() => setChapter(null)}
                className="w-full flex items-center gap-3 px-6 py-3.5 bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-indigo-500/20 transition-all"
              >
                <BookOpen size={14} />
                Change Chapter
              </button>
              <button
                onClick={() => clearContext()}
                className="w-full flex items-center gap-3 px-6 py-3.5 bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded-2xl font-black text-[10px] uppercase tracking-widest hover:bg-emerald-500/20 transition-all"
              >
                <RefreshCw size={14} />
                Change Subject
              </button>
            </div>
          )}

          <div className="p-6 bg-white/5 rounded-3xl space-y-4">
            <div className="flex items-center justify-between">
              <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Version</span>
              <span className="text-[10px] font-black text-primary uppercase tracking-widest">V3.2</span>
            </div>
            <div className="h-1 bg-white/10 rounded-full overflow-hidden">
              <div className="h-full bg-primary w-2/3 rounded-full shadow-[0_0_10px_#2563eb]" />
            </div>
            <p className="text-[10px] font-black text-slate-500 text-center uppercase tracking-widest">Gurukul AI</p>
          </div>
        </div>
      </div>
    </aside>
  );
}
