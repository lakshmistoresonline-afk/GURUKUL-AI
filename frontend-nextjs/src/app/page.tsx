'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { onAuthStateChanged, signOut } from 'firebase/auth';
import { doc, getDoc } from 'firebase/firestore';
import { auth, db } from '../lib/firebase';
import LoginScreen from '../components/LoginScreen';
import CommandPalette from '../components/CommandPalette';
import ExplorerLockerModal from '../components/ExplorerLockerModal';
import { CurriculumApiClient, buildCurriculumUrl } from '../lib/curriculumClient';

interface CurricularGoal {
  code: string;
  name: string;
  description: string;
}

interface ApiDiagnostics {
  endpoint: string;
  status?: number;
  error: string;
}

export default function Dashboard() {
  const [currentUser, setCurrentUser] = useState<any>(null);
  const [userRole, setUserRole] = useState<string>('student');
  const [userClassId, setUserClassId] = useState<string>('all');
  const [authChecking, setAuthChecking] = useState<boolean>(true);

  const [hierarchy, setHierarchy] = useState<any[]>([]);
  const [selectedGrade, setSelectedGrade] = useState<string>('5');
  const [selectedSubject, setSelectedSubject] = useState<string>('english');
  const [selectedBook, setSelectedBook] = useState<string>('english');
  const [selectedPart, setSelectedPart] = useState<string>('main');

  const [loading, setLoading] = useState<boolean>(true);
  const [apiError, setApiError] = useState<ApiDiagnostics | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');

  // Truthful progress state
  const [streak, setStreak] = useState<number>(0);
  const [xp, setXp] = useState<number>(0);
  const [recentChapter, setRecentChapter] = useState<any>(null);

  const [isCommandOpen, setIsCommandOpen] = useState<boolean>(false);
  const [isLockerOpen, setIsLockerOpen] = useState<boolean>(false);
  const [viewMode, setViewMode] = useState<'grid' | 'constellation'>('grid');

  useEffect(() => {
    // eslint-disable-next-line react-hooks/exhaustive-deps
    const demoUserStr = localStorage.getItem('gurukul_demo_user');
    const isDevMode = process.env.NODE_ENV !== 'production' && process.env.NEXT_PUBLIC_ENABLE_DEMO_AUTH === 'true';
    if (demoUserStr && isDevMode) {
      try {
        const u = JSON.parse(demoUserStr);
        setCurrentUser(u);
        setUserRole(u.role || 'student');
        setAuthChecking(false);
        return;
      } catch {}
    }

    const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        setCurrentUser(user);
        try {
          const userDoc = await getDoc(doc(db, 'users', user.uid));
          if (userDoc.exists()) {
            const data = userDoc.data();
            setUserRole(data.role || 'student');
            setUserClassId(data.classId || 'all');
          }
        } catch (e) {
          console.warn('Could not fetch user metadata from Firestore:', e);
        }
      } else {
        setCurrentUser(null);
      }
      setAuthChecking(false);
    });

    return () => unsubscribe();
  }, []);

  // Load authoritative hierarchy
  useEffect(() => {
    async function loadHierarchy() {
      try {
        setLoading(true);
        setApiError(null);
        const data = await CurriculumApiClient.fetchHierarchy();
        setHierarchy(data);

        if (data && data.length > 0) {
          const defaultGradeNode = data.find((g: any) => String(g.grade) === String(selectedGrade)) || data[0];
          setSelectedGrade(String(defaultGradeNode.grade));
          if (defaultGradeNode.subjects && defaultGradeNode.subjects.length > 0) {
            const defaultSubj = defaultGradeNode.subjects[0];
            setSelectedSubject(defaultSubj.canonical_subject);
            if (defaultSubj.books && defaultSubj.books.length > 0) {
              setSelectedBook(defaultSubj.books[0].book_id);
              setSelectedPart(defaultSubj.books[0].part);
            }
          }
        }
      } catch (err: any) {
        setApiError({
          endpoint: '/api/v1/curriculum/hierarchy',
          error: err.message || 'Failed to connect to authoritative curriculum hierarchy API.'
        });
        setHierarchy([]);
      } finally {
        setLoading(false);
      }
    }

    loadHierarchy();
  }, [selectedGrade]);

  // Load and defensively validate recent history against authoritative hierarchy
  useEffect(() => {
    try {
      const recent = JSON.parse(localStorage.getItem('gurukul_recent_chapters') || '[]');
      if (Array.isArray(recent) && recent.length > 0 && hierarchy.length > 0) {
        const validRecord = recent.find((r: any) => {
          if (!r || !r.grade || !r.subject || !r.book || !r.part || !r.unit || !r.chapterId) return false;
          const gObj = hierarchy.find((g: any) => String(g.grade) === String(r.grade));
          if (!gObj) return false;
          const sObj = (gObj.subjects || []).find((s: any) => s.canonical_subject?.toLowerCase() === r.subject.toLowerCase() || s.subject?.toLowerCase() === r.subject.toLowerCase());
          if (!sObj) return false;
          const bObj = (sObj.books || []).find((b: any) => b.book_id?.toLowerCase() === r.book.toLowerCase() && b.part?.toLowerCase() === r.part.toLowerCase());
          if (!bObj) return false;
          const uObj = (bObj.units || []).find((u: any) => u.unit_id?.toUpperCase() === r.unit.toUpperCase());
          if (!uObj) return false;
          const chObj = (uObj.chapters || []).find((c: any) => c.chapter_id?.toLowerCase() === r.chapterId.toLowerCase());
          return Boolean(chObj);
        });
        setRecentChapter(validRecord || null);
      } else {
        setRecentChapter(null);
      }
    } catch {
      setRecentChapter(null);
    }
  }, [hierarchy]);

  const currentGradeObj = hierarchy.find((g: any) => String(g.grade) === String(selectedGrade));
  const availableSubjects = currentGradeObj?.subjects || [];
  const currentSubjectObj = availableSubjects.find((s: any) => s.canonical_subject.toLowerCase() === selectedSubject.toLowerCase());
  const availableBooks = currentSubjectObj?.books || [];
  const currentBookObj = availableBooks.find((b: any) => b.book_id.toLowerCase() === selectedBook.toLowerCase() && b.part.toLowerCase() === selectedPart.toLowerCase()) || availableBooks[0];

  const handleGradeChange = (g: string) => {
    setSelectedGrade(g);
    const gObj = hierarchy.find((item: any) => String(item.grade) === String(g));
    if (gObj && gObj.subjects.length > 0) {
      const sub = gObj.subjects[0];
      setSelectedSubject(sub.canonical_subject);
      if (sub.books && sub.books.length > 0) {
        setSelectedBook(sub.books[0].book_id);
        setSelectedPart(sub.books[0].part);
      }
    }
  };

  const handleSubjectChange = (canonicalSubj: string) => {
    setSelectedSubject(canonicalSubj);
    const subObj = availableSubjects.find((s: any) => s.canonical_subject.toLowerCase() === canonicalSubj.toLowerCase());
    if (subObj && subObj.books && subObj.books.length > 0) {
      setSelectedBook(subObj.books[0].book_id);
      setSelectedPart(subObj.books[0].part);
    }
  };

  const getRankInfo = (score: number) => {
    if (score < 500) return { title: '🌱 Curious Novice', color: 'text-emerald-600 bg-emerald-50 border-emerald-200' };
    if (score < 1500) return { title: '🚀 Active Explorer', color: 'text-indigo-600 bg-indigo-50 border-indigo-200' };
    if (score < 3000) return { title: '⭐ Curriculum Scholar', color: 'text-amber-600 bg-amber-50 border-amber-200' };
    return { title: '👑 Master Academic', color: 'text-purple-600 bg-purple-50 border-purple-200' };
  };

  const rank = getRankInfo(xp);

  const getSubjectAtmosphere = (subj: string) => {
    const s = subj.toLowerCase();
    if (s.includes('english')) return 'from-amber-500/20 via-orange-500/10 to-transparent border-amber-500/30 text-amber-900';
    if (s.includes('hindi')) return 'from-rose-500/20 via-pink-500/10 to-transparent border-rose-500/30 text-rose-900';
    if (s.includes('maths')) return 'from-blue-500/20 via-indigo-500/10 to-transparent border-blue-500/30 text-blue-900';
    if (s.includes('science')) return 'from-teal-500/20 via-emerald-500/10 to-transparent border-teal-500/30 text-teal-900';
    return 'from-purple-500/20 via-indigo-500/10 to-transparent border-purple-500/30 text-purple-900';
  };

  const unitsList = currentBookObj?.units || [];
  const filteredUnits = unitsList.map((unit: any) => ({
    ...unit,
    chapters: unit.chapters.filter((ch: any) =>
      ch.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      ch.id.toLowerCase().includes(searchQuery.toLowerCase())
    )
  })).filter((unit: any) => unit.chapters.length > 0);

  const totalChaptersCount = unitsList.reduce((acc: number, u: any) => acc + u.chapters.length, 0);

  if (authChecking) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center text-white">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full mr-3" />
        <span className="font-bold">Loading Gurukul AI Session...</span>
      </div>
    );
  }

  if (!currentUser) {
    return <LoginScreen onLoginSuccess={() => window.location.reload()} />;
  }

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 selection:bg-indigo-500 selection:text-white">
      {/* Command Palette Modal (Passes authoritative hierarchy) */}
      <CommandPalette isOpen={isCommandOpen} onClose={() => setIsCommandOpen(false)} hierarchy={hierarchy} />

      {/* Explorer Locker Modal */}
      <ExplorerLockerModal isOpen={isLockerOpen} onClose={() => setIsLockerOpen(false)} xp={xp} streak={streak} />

      {/* TOP NAVIGATION HEADER */}
      <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-2xl border-b border-slate-200/80 shadow-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-20 flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-indigo-600 to-violet-600 flex items-center justify-center text-white font-black text-2xl shadow-lg shadow-indigo-600/30">
              G
            </div>
            <div>
              <h1 className="text-lg font-black tracking-tight bg-gradient-to-r from-indigo-600 to-violet-600 bg-clip-text text-transparent">
                Gurukul AI
              </h1>
              <p className="text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                NCERT • NEP 2020 • Authoritative
              </p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            {/* Command Palette Trigger */}
            <button
              onClick={() => setIsCommandOpen(true)}
              className="hidden sm:flex items-center gap-3 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-600 text-xs font-bold rounded-2xl border border-slate-200/85 transition-all"
            >
              <span>🔍 Quick Search...</span>
              <kbd className="px-2 py-0.5 bg-white text-slate-500 rounded-lg text-[10px] font-mono shadow-xs">Cmd K</kbd>
            </button>

            {/* Streak & XP Badges */}
            <button
              onClick={() => setIsLockerOpen(true)}
              className="flex items-center gap-3 px-4 py-2.5 bg-indigo-50 hover:bg-indigo-100/80 border border-indigo-200/80 rounded-2xl transition-all shadow-xs"
            >
              <div className="flex items-center gap-1.5 text-orange-600 font-extrabold text-xs">
                <span>🔥</span>
                <span>{streak} Days</span>
              </div>
              <div className="w-px h-4 bg-indigo-200" />
              <div className="flex items-center gap-1.5 text-indigo-700 font-extrabold text-xs">
                <span>⭐</span>
                <span>{xp} XP</span>
              </div>
            </button>

            {/* Sign Out */}
            <button
              onClick={() => {
                localStorage.removeItem('gurukul_demo_user');
                signOut(auth);
              }}
              className="p-2.5 text-slate-400 hover:text-rose-600 hover:bg-rose-50 rounded-2xl transition-all"
              title="Sign Out"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
              </svg>
            </button>
          </div>
        </div>
      </header>

      {/* MAIN DASHBOARD CONTAINER */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">

        {/* WELCOME BANNER */}
        <div className="p-8 md:p-10 rounded-3xl bg-gradient-to-r from-indigo-950 via-indigo-900 to-slate-900 text-white shadow-2xl relative overflow-hidden flex flex-col md:flex-row items-start md:items-center justify-between gap-6">
          <div className="absolute -right-16 -top-16 w-64 h-64 bg-indigo-500/20 rounded-full blur-3xl pointer-events-none" />

          <div className="space-y-3 z-10">
            <div className="inline-flex items-center gap-2 px-3 py-1 bg-white/10 backdrop-blur-md rounded-full text-xs font-bold text-indigo-200 border border-white/10">
              <span>{rank.title}</span>
            </div>
            <h2 className="text-3xl sm:text-4xl font-black tracking-tight">
              Welcome back, {currentUser?.displayName || currentUser?.email?.split('@')[0] || 'Scholar'}!
            </h2>
            <p className="text-slate-300 text-sm max-w-xl font-medium leading-relaxed">
              Your authoritative NCERT digital companion. Explore interactive chapters, practice exercises, flashcards, and verified assessments.
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-3 z-10 w-full md:w-auto">
            <button
              onClick={() => setIsLockerOpen(true)}
              className="px-6 py-3.5 bg-white text-indigo-950 text-xs font-black rounded-2xl shadow-lg hover:bg-slate-100 transition-all text-center"
            >
              🏆 View Achievements
            </button>
          </div>
        </div>

        {/* 1. CONTINUE LEARNING BANNER */}
        {recentChapter && (
          <section className="p-6 md:p-8 rounded-3xl bg-gradient-to-r from-indigo-600 to-violet-600 text-white shadow-xl space-y-4">
            <div className="flex items-center justify-between">
              <span className="px-3 py-1 bg-white/20 rounded-full text-[10px] font-black uppercase tracking-wider">
                Continue Learning • Unit {recentChapter.unit}
              </span>
              <span className="text-xs font-bold text-indigo-100">Class {recentChapter.grade} • {recentChapter.subject}</span>
            </div>

            <div className="space-y-1">
              <h2 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
                Chapter: {recentChapter.chapterId}
              </h2>
              <p className="text-slate-200 text-sm">
                Book: {recentChapter.book} • Part: {recentChapter.part}
              </p>
            </div>

            <div className="pt-2 flex justify-end">
              <Link
                href={buildCurriculumUrl({
                  grade: recentChapter.grade,
                  subject: recentChapter.subject,
                  book: recentChapter.book,
                  part: recentChapter.part,
                  unit: recentChapter.unit,
                  chapter_id: recentChapter.chapterId
                })}
                className="inline-flex items-center gap-2 px-6 py-3 bg-white text-indigo-900 hover:bg-slate-100 text-sm font-extrabold rounded-2xl shadow-lg transition-all hover:translate-x-1"
              >
                <span>Resume Lesson</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14 5l7 7-7 7M3 12h18" />
                </svg>
              </Link>
            </div>
          </section>
        )}

        {/* 2. YOUR SUBJECTS SELECTOR & VIEW MODE TOGGLE */}
        <section className="space-y-4 bg-white/80 backdrop-blur-2xl p-6 md:p-8 rounded-3xl border border-slate-200/80 shadow-xl shadow-slate-900/5">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <h2 className="text-xs font-black tracking-widest text-slate-500 uppercase">
              YOUR SUBJECTS & ATMOSPHERE
            </h2>
            <div className="flex items-center gap-4">
              <div className="flex bg-slate-100 p-1 rounded-2xl border border-slate-200 text-xs font-bold">
                <button
                  onClick={() => setViewMode('grid')}
                  className={`px-3 py-1.5 rounded-xl transition-all ${viewMode === 'grid' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'}`}
                >
                  Grid View
                </button>
                <button
                  onClick={() => setViewMode('constellation')}
                  className={`px-3 py-1.5 rounded-xl transition-all ${viewMode === 'constellation' ? 'bg-white text-slate-900 shadow-xs' : 'text-slate-500 hover:text-slate-900'}`}
                >
                  ✨ Constellation Map
                </button>
              </div>

              <div className="flex items-center gap-2">
                <span className="text-xs font-bold text-slate-400">Grade:</span>
                <div className="flex gap-1">
                  {hierarchy.map((g: any) => (
                    <button
                      key={`class-select-${g.grade}`}
                      onClick={() => handleGradeChange(g.grade)}
                      className={`px-3 py-1 rounded-xl text-xs font-extrabold transition-all ${
                        selectedGrade === g.grade
                          ? 'bg-slate-900 text-white shadow-xs'
                          : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                      }`}
                    >
                      Class {g.grade}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-7 gap-3">
            {availableSubjects.map((sub: any) => {
              const isActive = selectedSubject.toLowerCase() === sub.canonical_subject.toLowerCase();
              return (
                <button
                  key={sub.canonical_subject}
                  onClick={() => handleSubjectChange(sub.canonical_subject)}
                  className={`p-4 rounded-2xl text-left border transition-all flex flex-col justify-between gap-2 hover:-translate-y-0.5 ${
                    isActive
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow-lg shadow-indigo-600/30'
                      : 'bg-slate-50/80 text-slate-700 hover:bg-slate-100 border-slate-200/80'
                  }`}
                >
                  <span className="text-xl">
                    {sub.subject.toLowerCase().includes('english') ? '📚' : sub.subject.toLowerCase().includes('hindi') ? '🌸' : sub.subject.toLowerCase().includes('maths') ? '📐' : sub.subject.toLowerCase().includes('science') ? '🔬' : '🌍'}
                  </span>
                  <div>
                    <div className="text-sm font-extrabold">{sub.subject}</div>
                    <div className={`text-[10px] font-bold ${isActive ? 'text-indigo-200' : 'text-slate-400'}`}>
                      Class {selectedGrade}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </section>

        {/* API Connection Warning Banner if Offline */}
        {apiError && (
          <div className="p-4 bg-rose-50 border border-rose-200 rounded-2xl text-rose-900 text-xs flex items-center justify-between gap-4">
            <div>
              <strong>⚠️ Curriculum Loading Notice:</strong> {apiError.error}. Ensure backend FastAPI server is running (`python backend/src/main.py`).
            </div>
          </div>
        )}

        {/* 3. LIVE SEARCH BAR */}
        <div className="relative">
          <input
            type="text"
            placeholder="🔍 Search any chapter by name or ID..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full px-6 py-4 bg-white/80 backdrop-blur-xl border border-slate-200/80 rounded-2xl shadow-sm text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
          />
        </div>

        {/* 4. CHAPTERS LIST BY UNIT OR CONSTELLATION MAP */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-black tracking-widest text-slate-500 uppercase">
              Curriculum Chapters • {currentSubjectObj?.subject || selectedSubject} (Class {selectedGrade}) {viewMode === 'constellation' ? '• Star Map' : ''}
            </h2>
            <span className="text-xs font-bold text-slate-400">
              {totalChaptersCount} Chapters Total
            </span>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-16 text-slate-500 bg-white/80 backdrop-blur-xl rounded-3xl border border-slate-200/80">
              <div className="animate-spin w-6 h-6 border-2 border-indigo-600 border-t-transparent rounded-full mr-3" />
              <span className="font-bold text-sm">Loading Authoritative Curriculum Hierarchy...</span>
            </div>
          ) : hierarchy.length === 0 ? (
            <div className="p-12 text-center text-slate-500 bg-white/80 backdrop-blur-xl rounded-3xl border border-slate-200 space-y-3">
              <h3 className="text-lg font-bold text-slate-900">We couldn&apos;t load the curriculum.</h3>
              <p className="text-xs text-slate-500">Please ensure the backend server is running and try again.</p>
              <button
                onClick={() => window.location.reload()}
                className="px-6 py-2.5 bg-indigo-600 text-white text-xs font-bold rounded-xl shadow-md hover:bg-indigo-500 transition-all"
              >
                Retry ↻
              </button>
            </div>
          ) : viewMode === 'constellation' ? (
            /* Constellation Star Map View */
            <div className={`p-8 rounded-3xl bg-gradient-to-br ${getSubjectAtmosphere(selectedSubject)} shadow-2xl space-y-8 border`}>
              <div className="text-center space-y-2">
                <span className="px-3 py-1 bg-white/10 rounded-full text-xs font-bold uppercase tracking-widest">✨ Celestial Constellation Map</span>
                <h3 className="text-2xl font-black text-white">{currentSubjectObj?.subject || selectedSubject} Star Trail</h3>
                <p className="text-xs text-slate-300">Click any shining star node to warp directly into the chapter workspace.</p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 pt-4">
                {filteredUnits.flatMap((u: any) => u.chapters).map((ch: any, idx: number) => {
                  const unitObj = filteredUnits.find((u: any) => u.chapters.some((c: any) => c.id === ch.id));
                  return (
                    <Link
                      key={ch.id}
                      href={buildCurriculumUrl({
                        grade: selectedGrade,
                        subject: selectedSubject,
                        book: currentBookObj?.book_id || selectedSubject.toLowerCase(),
                        part: currentBookObj?.part || 'main',
                        unit: unitObj?.id || 'U01',
                        chapter_id: ch.id
                      })}
                      className="group relative p-6 rounded-3xl bg-white/10 hover:bg-white/20 border border-white/20 backdrop-blur-xl transition-all hover:scale-105 hover:shadow-2xl flex flex-col justify-between gap-4"
                    >
                      <div className="flex items-center justify-between">
                        <span className="text-2xl">⭐</span>
                        <span className="text-xs font-mono font-bold opacity-70">Node #{idx + 1}</span>
                      </div>
                      <div className="space-y-1">
                        <div className="text-xs font-bold opacity-80">Chapter {ch.chapterNumber}</div>
                        <h4 className="text-base font-black text-white group-hover:text-teal-300 transition-colors">{ch.title}</h4>
                      </div>
                      <div className="text-[11px] font-bold text-teal-300 flex items-center gap-1">
                        <span>Explore Constellation ➔</span>
                      </div>
                    </Link>
                  );
                })}
              </div>
            </div>
          ) : filteredUnits.length > 0 ? (
            filteredUnits.map((unit: any) => (
              <div key={unit.id} className="p-6 md:p-8 bg-white/80 backdrop-blur-2xl border border-slate-200/80 rounded-3xl shadow-xl shadow-slate-900/5 space-y-6">
                <div className="border-b border-slate-100 pb-4">
                  <div className="text-xs font-black uppercase tracking-widest text-indigo-600">
                    Unit {unit.unitNumber}
                  </div>
                  <h3 className="text-xl font-black text-slate-900 tracking-tight">
                    {unit.title}
                  </h3>
                  {unit.theme && (
                    <p className="text-xs text-slate-500 mt-1">{unit.theme}</p>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {unit.chapters.map((ch: any) => (
                    <div
                      key={ch.id}
                      className="group p-5 bg-[#F8FAFC]/80 backdrop-blur-md border border-slate-200/80 hover:border-indigo-300 rounded-2xl transition-all duration-300 hover:-translate-y-0.5 hover:shadow-lg flex flex-col justify-between gap-4"
                    >
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="px-2.5 py-1 bg-indigo-50 text-indigo-700 text-[10px] font-black uppercase tracking-wider rounded-lg border border-indigo-100">
                            Chapter {ch.chapterNumber}
                          </span>
                          <span className="text-[11px] font-mono text-slate-400">
                            {ch.id}
                          </span>
                        </div>
                        <h4 className="text-base font-bold text-slate-900 group-hover:text-indigo-600 transition-colors leading-snug">
                          {ch.title}
                        </h4>
                      </div>

                      <div className="pt-3 border-t border-slate-200/60 flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-500 group-hover:text-slate-700">
                          Open Chapter Experience
                        </span>
                        <Link
                          href={buildCurriculumUrl({
                            grade: selectedGrade,
                            subject: selectedSubject,
                            book: currentBookObj?.book_id || selectedSubject.toLowerCase(),
                            part: currentBookObj?.part || 'main',
                            unit: unit.id,
                            chapter_id: ch.id
                          })}
                          className="inline-flex items-center gap-1.5 px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-extrabold rounded-xl shadow-md shadow-indigo-600/20 transition-all group-hover:translate-x-0.5"
                        >
                          <span>Explore</span>
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M9 5l7 7-7 7" />
                          </svg>
                        </Link>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            ))
          ) : (
            <div className="p-12 text-center text-slate-500 bg-white/80 backdrop-blur-xl rounded-3xl border border-slate-200 space-y-2">
              <h3 className="text-lg font-bold text-slate-900">No chapters found matching &quot;{searchQuery}&quot;</h3>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}
