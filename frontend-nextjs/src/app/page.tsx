'use client';

import React, { useEffect, useState } from 'react';
import { useAuth } from '@/core/context/AuthContext';
import { Layout } from '@/presentation/components/common/Layout';
import { studentApi, Class, Subject } from '@/services/api/student_api';
import { GraduationCap, ArrowRight, Book, Layers, ShieldCheck, Zap, Target, HelpCircle, RefreshCw, Globe, ChevronRight, Search } from 'lucide-react';
import Link from 'next/link';

export default function HomePage() {
  const { user, login, loading: authLoading } = useAuth();
  const [classes, setClasses] = useState<Class[]>([]);
  const [selectedClass, setSelectedClass] = useState<Class | null>(null);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any[]>([]);
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    if (searchQuery.length > 2) {
      setIsSearching(true);
      studentApi.search(searchQuery).then(res => {
        setSearchResults(res);
        setIsSearching(false);
      });
    } else {
      setSearchResults([]);
    }
  }, [searchQuery]);

  // Form State
  const [username, setUsername] = useState('tester_v1');
  const [password, setPassword] = useState('password123');
  const [loginError, setLoginError] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    studentApi.getClasses().then(data => {
      setClasses(data);
      setLoading(false);
      // Auto-select class based on user if logged in
      if (user) {
        const userClassId = user.class_id || (user.username.includes('6') ? 'class_6' : 'class_5');
        const found = data.find(c => c.id === userClassId);
        if (found) setSelectedClass(found);
      }
    }).catch(() => setLoading(false));
  }, [user]);

  const handleLogin = async (e: React.FormEvent) => {
     e.preventDefault();
     setLoginError('');
     setSubmitting(true);
     try {
        await login(username, password);
     } catch (err: any) {
        setLoginError('Invalid username or password.');
        setSubmitting(false);
     }
  };

  if (authLoading) return <Layout><div className="p-20 text-center font-black text-slate-300 uppercase animate-pulse">Establishing Secure Link...</div></Layout>;

  if (!user) {
    return (
      <Layout>
        <div className="min-h-[80vh] flex flex-col items-center justify-center px-4 sm:px-6 py-12 sm:py-20 relative overflow-hidden">
           <div className="max-w-md w-full space-y-8 sm:space-y-12 relative z-10">
              <div className="text-center space-y-4">
                 <div className="inline-flex items-center gap-3 px-5 sm:px-6 py-2 bg-slate-900 text-white rounded-full font-black text-[10px] uppercase tracking-[0.3em]">
                    <ShieldCheck size={14} className="text-blue-400" /> Gurukul AI Unified System
                 </div>
                 <h1 className="text-4xl sm:text-6xl font-black tracking-tighter text-slate-900 uppercase italic">Student Login</h1>
                 <p className="text-sm text-slate-500 font-medium">Class 5, 6, and 7 Universal Access</p>
              </div>

              <div className="bg-white border-2 border-slate-100 rounded-[36px] p-6 sm:p-10 shadow-2xl space-y-6">
                 <form onSubmit={handleLogin} className="space-y-4">
                    {loginError && (
                       <div className="p-4 bg-red-50 border border-red-200 rounded-2xl text-xs font-bold text-red-600">{loginError}</div>
                    )}
                    <div>
                       <label className="block text-[11px] font-black uppercase tracking-wider text-slate-500 mb-2">Username</label>
                       <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} className="w-full px-6 py-4 bg-slate-50 border-2 border-slate-200 rounded-2xl font-bold text-slate-900 outline-none transition-all text-sm" required />
                    </div>
                    <div>
                       <label className="block text-[11px] font-black uppercase tracking-wider text-slate-500 mb-2">Password</label>
                       <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="w-full px-6 py-4 bg-slate-50 border-2 border-slate-200 rounded-2xl font-bold text-slate-900 outline-none transition-all text-sm" required />
                    </div>
                    <button type="submit" disabled={submitting} className="w-full py-5 bg-blue-600 text-white rounded-2xl font-black uppercase text-xs hover:bg-blue-700 transition-all shadow-xl disabled:opacity-50">
                      {submitting ? 'Authenticating...' : 'Authorize Access'}
                    </button>
                 </form>
                 <div className="border-t border-slate-100 pt-6 space-y-3">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest text-center">Quick Credentials:</p>
                    <div className="grid grid-cols-3 gap-2">
                       {['tester_v1', 'class6_user', 'class7_user'].map(u => (
                          <button key={u} type="button" onClick={() => { setUsername(u); setPassword('password123'); }} className="p-2 bg-slate-50 border border-slate-200 rounded-xl text-[10px] font-black hover:bg-blue-50 transition-all uppercase">{u.split('_')[0]}</button>
                       ))}
                    </div>
                 </div>
              </div>
           </div>
        </div>
      </Layout>
    );
  }

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 sm:py-12 space-y-12">
        <header className="space-y-4">
           <h1 className="text-3xl sm:text-5xl font-black tracking-tighter text-slate-900 uppercase italic">Gurukul <span className="text-blue-600">Unified</span> Dashboard</h1>
           <p className="text-lg text-slate-500 font-medium">Select your class to begin your learning journey.</p>

           <div className="pt-4 max-w-xl">
              <div className="relative group">
                 <Search className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-300 group-focus-within:text-blue-600 transition-colors" size={20} />
                 <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="Search for lessons, questions, or definitions..."
                    className="w-full pl-16 pr-6 py-5 bg-slate-50 border-2 border-slate-100 rounded-[24px] font-bold text-slate-900 outline-none focus:border-blue-600 focus:bg-white transition-all shadow-inner"
                 />
              </div>
              {searchResults.length > 0 && (
                 <div className="absolute mt-2 w-full bg-white border-2 border-slate-100 rounded-[24px] shadow-2xl z-50 p-4 space-y-2 max-h-[400px] overflow-y-auto">
                    {searchResults.map((res: any) => (
                       <Link key={res.id} href={`/chapter/${res.chapter_id}`} className="block p-4 hover:bg-slate-50 rounded-2xl border border-transparent hover:border-slate-100 transition-all">
                          <div className="flex items-center justify-between mb-1">
                             <span className="text-[8px] font-black text-blue-600 uppercase tracking-widest bg-blue-50 px-2 py-0.5 rounded">{res.layer}</span>
                             <span className="text-[8px] font-bold text-slate-400 uppercase">{res.class} • {res.subject}</span>
                          </div>
                          <p className="text-sm font-black text-slate-900 leading-tight">{res.title || 'Untitled Block'}</p>
                          <p className="text-[10px] text-slate-500 line-clamp-1 mt-1 font-medium">{res.text}</p>
                       </Link>
                    ))}
                 </div>
              )}
           </div>
        </header>

        {/* CLASS SELECTOR */}
        <section className="grid grid-cols-1 sm:grid-cols-3 gap-6">
           {classes.map((cls) => (
              <button
                key={cls.id}
                onClick={() => setSelectedClass(cls)}
                className={`p-8 rounded-[40px] border-4 transition-all text-left space-y-4 group relative overflow-hidden ${selectedClass?.id === cls.id ? 'border-blue-600 bg-blue-50' : 'border-slate-100 bg-white hover:border-slate-200'}`}
              >
                 <div className={`w-12 h-12 rounded-2xl flex items-center justify-center font-black ${selectedClass?.id === cls.id ? 'bg-blue-600 text-white' : 'bg-slate-100 text-slate-400 group-hover:bg-slate-200'}`}>
                    <GraduationCap size={24} />
                 </div>
                 <div>
                    <h3 className="text-2xl font-black uppercase italic tracking-tighter">{cls.name}</h3>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{cls.subjects.length} Subjects Available</p>
                 </div>
                 {selectedClass?.id === cls.id && <div className="absolute top-4 right-8 text-blue-600 font-black text-xs uppercase tracking-widest animate-pulse italic">Active</div>}
              </button>
           ))}
        </section>

        {/* SUBJECT GRID */}
        {selectedClass && (
           <section className="space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
              <div className="flex items-center gap-4 border-b-2 border-slate-100 pb-4">
                 <h2 className="text-2xl font-black uppercase italic tracking-tighter text-slate-900">{selectedClass.name} Streams</h2>
                 <ArrowRight className="text-blue-600" />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
                 {selectedClass.subjects.map((subj) => (
                    <Link key={subj.id} href={`/subject/${subj.id}`} className="bg-white border-2 border-slate-100 rounded-[32px] p-6 hover:border-blue-600 hover:shadow-xl transition-all group flex flex-col gap-6">
                       <div className="w-10 h-10 bg-slate-50 rounded-xl flex items-center justify-center text-slate-300 group-hover:bg-blue-600 group-hover:text-white transition-all">
                          <Book size={18} />
                       </div>
                       <div>
                          <h3 className="text-xl font-black text-slate-900 uppercase italic leading-tight">{subj.name}</h3>
                          <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mt-1">{subj.chapters.length} Chapters</p>
                       </div>
                       <span className="text-[10px] font-black text-blue-600 uppercase tracking-widest mt-auto">Explore &rarr;</span>
                    </Link>
                 ))}
              </div>
           </section>
        )}
      </div>
    </Layout>
  );
}
