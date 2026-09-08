'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { GraduationCap, User, LogOut, ChevronDown, BookOpen } from 'lucide-react';
import { useAuth } from '@/core/context/AuthContext';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuth();
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setDropdownOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const classNameStr = user?.class_id === 'class_6' ? 'Class 6' : 'Class 5';

  return (
    <div className="min-h-screen bg-white flex flex-col font-sans">
      <header className="h-20 border-b border-slate-100 flex items-center justify-between px-6 lg:px-12 sticky top-0 bg-white/90 backdrop-blur-md z-50">
        <Link href="/" className="flex items-center gap-3">
          <div className="w-10 h-10 bg-blue-600 rounded-xl flex items-center justify-center text-white shadow-md">
             <GraduationCap size={22} />
          </div>
          <span className="text-2xl font-black tracking-tighter text-slate-900 uppercase italic">Gurukul <span className="text-blue-600">AI</span></span>
        </Link>

        {user && (
           <div className="relative" ref={dropdownRef}>
              <button
                onClick={() => setDropdownOpen(!dropdownOpen)}
                className="flex items-center gap-3 bg-slate-50 border border-slate-200 px-4 py-2.5 rounded-2xl hover:bg-slate-100 transition-all text-left"
              >
                 <div className="w-8 h-8 rounded-full bg-blue-600 text-white font-bold flex items-center justify-center text-xs">
                    {(user.name || user.username || 'S').charAt(0).toUpperCase()}
                 </div>
                 <div className="hidden sm:flex flex-col text-left leading-tight">
                    <span className="text-xs font-black text-slate-900 uppercase tracking-wide">{user.name || user.username}</span>
                    <span className="text-[10px] font-bold text-blue-600 uppercase tracking-widest">{classNameStr}</span>
                 </div>
                 <ChevronDown size={14} className="text-slate-400" />
              </button>

              {dropdownOpen && (
                 <div className="absolute right-0 mt-2 w-56 bg-white border border-slate-100 rounded-2xl shadow-xl py-2 z-50 animate-in fade-in slide-in-from-top-2 duration-200">
                    <div className="px-4 py-3 border-b border-slate-100">
                       <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Signed in as</p>
                       <p className="text-sm font-extrabold text-slate-900 truncate">{user.name || user.username}</p>
                       <p className="text-[11px] font-bold text-blue-600 mt-0.5">{classNameStr} Curriculum</p>
                    </div>

                    <div className="py-1">
                       <button
                         onClick={() => {
                            setDropdownOpen(false);
                            alert(`Current Profile:\nName: ${user.name || user.username}\nAssigned Class: ${classNameStr}\nRole: ${user.role}`);
                         }}
                         className="w-full px-4 py-2.5 text-left text-xs font-bold text-slate-700 hover:bg-slate-50 flex items-center gap-2.5 transition-colors"
                       >
                          <User size={14} className="text-slate-400" /> My Profile
                       </button>

                       <button
                         onClick={() => {
                            setDropdownOpen(false);
                            window.location.href = '/';
                         }}
                         className="w-full px-4 py-2.5 text-left text-xs font-bold text-slate-700 hover:bg-slate-50 flex items-center gap-2.5 transition-colors"
                       >
                          <BookOpen size={14} className="text-slate-400" /> Current Dashboard ({classNameStr})
                       </button>
                    </div>

                    <div className="border-t border-slate-100 pt-1">
                       <button
                         onClick={() => {
                            setDropdownOpen(false);
                            logout();
                         }}
                         className="w-full px-4 py-2.5 text-left text-xs font-bold text-red-600 hover:bg-red-50 flex items-center gap-2.5 transition-colors"
                       >
                          <LogOut size={14} className="text-red-500" /> Logout
                       </button>
                    </div>
                 </div>
              )}
           </div>
        )}
      </header>

      <main className="flex-1">
        {children}
      </main>

      <footer className="py-12 bg-slate-50 border-t border-slate-100 text-center">
        <p className="text-[10px] font-black text-slate-300 uppercase tracking-widest">
           &copy; 2026 Gurukul AI V1.5 — Multi-Class Certified Production Baseline
        </p>
      </footer>
    </div>
  );
};
