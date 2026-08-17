'use client';

import React, { useState, useRef, useEffect } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Bell, Search, User, ChevronLeft, ChevronRight, LogOut, GraduationCap, ChevronDown, Menu, X } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { auth } from '@/lib/firebase';
import { signOut } from 'firebase/auth';
import { motion, AnimatePresence } from 'framer-motion';
import { navItems } from '@/config/navigation';
import { usePathname } from 'next/navigation';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export default function TopBar({ title }: { title: string }) {
  const router = useRouter();
  const pathname = usePathname();
  const { profile } = useAuth();
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsProfileOpen(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleLogout = async () => {
    try {
      await signOut(auth);
      router.push('/login');
    } catch (error) {
      console.error('Logout error', error);
    }
  };

  return (
    <header className="h-20 bg-slate-50/80 backdrop-blur-xl border-b border-black/[0.03] flex items-center justify-between px-6 md:px-10 sticky top-0 z-30">
      <div className="flex items-center gap-4 md:gap-6">
        <button
          onClick={() => setIsMobileMenuOpen(true)}
          className="lg:hidden p-2 hover:bg-white rounded-xl text-slate-500 transition-all border border-black/[0.05] shadow-sm"
        >
          <Menu size={20} />
        </button>

        <div className="hidden md:flex items-center gap-2 mr-4 bg-white/50 p-1.5 rounded-2xl border border-black/[0.05]">
          <button
            onClick={() => router.back()}
            className="p-2 hover:bg-white rounded-xl text-slate-500 hover:text-primary hover:shadow-sm transition-all"
            title="Go Back"
          >
            <ChevronLeft size={18} />
          </button>
          <button
            onClick={() => router.forward()}
            className="p-2 hover:bg-white rounded-xl text-slate-500 hover:text-primary hover:shadow-sm transition-all"
            title="Go Forward"
          >
            <ChevronRight size={18} />
          </button>
        </div>
        <h1 className="text-lg font-black text-slate-900 uppercase tracking-tight">{title}</h1>
      </div>

      <div className="flex items-center gap-6">
        <Link href="/search" className="relative hidden lg:block group">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 group-hover:text-primary transition-colors" size={16} />
          <div className="pl-12 pr-6 py-3 bg-white border border-black/[0.05] rounded-2xl text-xs text-slate-400 font-bold w-72 cursor-pointer hover:border-primary/20 transition-all shadow-sm">
            Search curriculum...
          </div>
        </Link>

        <button className="text-slate-500 hover:text-primary transition-colors relative">
          <Bell size={20} />
          <span className="absolute -top-1 -right-1 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
        </button>

        <div className="relative" ref={dropdownRef}>
          <button
            onClick={() => setIsProfileOpen(!isProfileOpen)}
            className="flex items-center gap-3 pl-4 border-l border-border hover:opacity-80 transition-opacity"
          >
            <div className="text-right hidden sm:block">
              <p className="text-sm font-black text-slate-900 leading-tight truncate max-w-[150px]">
                {profile?.name || 'Scholar'}
              </p>
              <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest mt-0.5">
                Class {profile?.classId || '...'} Student
              </p>
            </div>
            <div className="w-10 h-10 bg-primary/10 rounded-2xl flex items-center justify-center text-primary border border-primary/20 shadow-glow shadow-primary/5 relative">
              <User size={20} />
              <div className="absolute -bottom-1 -right-1 w-4 h-4 bg-white rounded-full flex items-center justify-center shadow-sm border border-slate-100">
                <ChevronDown size={10} className={cn("transition-transform duration-300", isProfileOpen && "rotate-180")} />
              </div>
            </div>
          </button>

          <AnimatePresence>
            {isProfileOpen && (
              <motion.div
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                className="absolute right-0 mt-4 w-72 bg-white border border-slate-200 rounded-[32px] shadow-[0_20px_50px_rgba(0,0,0,0.1)] overflow-hidden z-50"
              >
                <div className="p-6 bg-slate-50/50 border-b border-slate-100">
                   <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-primary rounded-2xl flex items-center justify-center text-white shadow-lg shadow-primary/20">
                         <GraduationCap size={24} />
                      </div>
                      <div className="flex-1 min-w-0">
                         <p className="text-sm font-black text-slate-900 truncate">{profile?.name || 'Scholar'}</p>
                         <p className="text-[10px] font-bold text-slate-400 truncate uppercase tracking-tight">{profile?.email || 'student@gurukul.ai'}</p>
                      </div>
                   </div>
                </div>

                <div className="p-3">
                   <Link
                     href="/profile"
                     className="flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-slate-50 text-slate-600 hover:text-primary transition-all font-bold text-xs"
                     onClick={() => setIsProfileOpen(false)}
                   >
                      <User size={18} /> View Profile
                   </Link>
                   <button
                     onClick={handleLogout}
                     className="w-full flex items-center gap-3 px-4 py-3 rounded-2xl hover:bg-red-50 text-slate-600 hover:text-red-600 transition-all font-bold text-xs mt-1"
                   >
                      <LogOut size={18} /> Sign Out Session
                   </button>
                </div>

                <div className="p-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between">
                   <span className="text-[9px] font-black text-slate-500 uppercase tracking-widest">Class {profile?.classId || '...'}</span>
                   <span className="text-[9px] font-black text-emerald-600 uppercase tracking-widest bg-emerald-50 px-2.5 py-1 rounded-lg border border-emerald-100">Active</span>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>

      <AnimatePresence>
        {isMobileMenuOpen && (
          <>
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsMobileMenuOpen(false)}
              className="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] lg:hidden"
            />
            <motion.div
              initial={{ x: "-100%" }}
              animate={{ x: 0 }}
              exit={{ x: "-100%" }}
              transition={{ type: "spring", damping: 25, stiffness: 200 }}
              className="fixed inset-y-0 left-0 w-80 bg-[#0F172A] z-[101] lg:hidden p-8 flex flex-col shadow-2xl"
            >
              <div className="flex items-center justify-between mb-12">
                <Link href="/dashboard" className="flex items-center gap-3">
                  <div className="w-10 h-10 bg-primary rounded-xl flex items-center justify-center text-white shadow-lg shadow-primary/20">
                    <GraduationCap size={24} />
                  </div>
                  <span className="text-white font-black text-lg tracking-tighter">GURUKUL AI</span>
                </Link>
                <button onClick={() => setIsMobileMenuOpen(false)} className="p-2 text-slate-500 hover:text-white transition-colors">
                  <X size={24} />
                </button>
              </div>

              <nav className="flex flex-col gap-2">
                {navItems.map((item) => {
                  const isActive = pathname === item.href || (item.href !== '/dashboard' && pathname.startsWith(item.href));
                  return (
                    <Link
                      key={item.href}
                      href={item.href}
                      onClick={() => setIsMobileMenuOpen(false)}
                      className={cn(
                        "flex items-center gap-4 px-6 py-4 rounded-2xl transition-all font-bold text-sm",
                        isActive ? "bg-primary text-white" : "text-slate-400 hover:text-white hover:bg-white/5"
                      )}
                    >
                      <item.icon size={20} />
                      {item.label}
                    </Link>
                  );
                })}
              </nav>

              <div className="mt-auto p-6 bg-white/5 rounded-3xl text-center">
                 <p className="text-[10px] font-black text-slate-500 uppercase tracking-widest">Gurukul V3.2</p>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </header>
  );
}
