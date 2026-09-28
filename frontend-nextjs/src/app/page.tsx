'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import CommandPalette from '../components/CommandPalette';

interface CurricularGoal {
  code: string;
  name: string;
  description: string;
}

interface Chapter {
  id: string;
  chapterNumber: number;
  title: string;
  resourceCount?: number;
  contentTypes?: string[];
}

interface Unit {
  id: string;
  title: string;
  unitNumber: number;
  theme?: string;
  chapters: Chapter[];
}

interface SubjectDetails {
  grade: string;
  subject: string;
  curriculumFramework?: string;
  curricularGoals?: CurricularGoal[];
  totalChapters: number;
  units: Unit[];
}

interface ClassDiscovery {
  grade: string;
  subjects: string[];
}

interface ApiDiagnostics {
  endpoint: string;
  status?: number;
  error: string;
}

const FALLBACK_CLASS5_ENGLISH: SubjectDetails = {
  grade: '5',
  subject: 'English',
  curriculumFramework: 'NEP 2020 & NCF-SE 2023',
  curricularGoals: [
    {
      code: 'CG1',
      name: 'Communication',
      description: 'Develops effective oral communication skills through interactive sections.',
    },
    {
      code: 'CG2',
      name: 'Reading Comprehension',
      description: 'Enhances reading fluency and text comprehension across diverse literary genres.',
    },
    {
      code: 'CG3',
      name: 'Expressive Writing',
      description: 'Guides learners from structured writing towards independent creative expression.',
    },
    {
      code: 'CG4',
      name: 'Vocabulary Expansion',
      description: 'Develops contextual vocabulary integrated across literature, science, and social life.',
    },
  ],
  totalChapters: 10,
  units: [
    {
      id: 'U01',
      unitNumber: 1,
      title: 'Let’s Have Fun',
      theme: 'Empathy, family bonds, and observing everyday life with humor and joy.',
      chapters: [
        {
          id: 'G5-ENG-U01-C01',
          chapterNumber: 1,
          title: 'Papa’s Spectacles',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
        {
          id: 'G5-ENG-U01-C02',
          chapterNumber: 2,
          title: 'Gone with the Scooter',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
      ],
    },
  ],
};

export default function Dashboard() {
  const [classes, setClasses] = useState<ClassDiscovery[]>([
    { grade: '5', subjects: ['English', 'Hindi', 'Maths', 'Science'] },
    { grade: '6', subjects: ['English', 'Hindi', 'Maths', 'Science', 'Social'] },
  ]);
  const [selectedGrade, setSelectedGrade] = useState<string>('5');
  const [selectedSubject, setSelectedSubject] = useState<string>('English');
  const [availableSubjects, setAvailableSubjects] = useState<string[]>(['English', 'Hindi', 'Maths', 'Science']);
  const [subjectData, setSubjectData] = useState<SubjectDetails | null>(FALLBACK_CLASS5_ENGLISH);
  const [selectedGoalModal, setSelectedGoalModal] = useState<CurricularGoal | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [apiError, setApiError] = useState<ApiDiagnostics | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [streak, setStreak] = useState<number>(5);
  const [isCommandOpen, setIsCommandOpen] = useState<boolean>(false);

  useEffect(() => {
    const savedStreak = localStorage.getItem('gurukul_streak');
    if (savedStreak) {
      setStreak(parseInt(savedStreak, 10));
    } else {
      localStorage.setItem('gurukul_streak', '5');
    }

    const savedGrade = localStorage.getItem('gurukul_selected_grade');
    if (savedGrade && (savedGrade === '5' || savedGrade === '6')) {
      setSelectedGrade(savedGrade);
      if (savedGrade === '6') {
        setAvailableSubjects(['English', 'Hindi', 'Maths', 'Science', 'Social']);
      }
    }

    const handleGlobalKey = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === 'k') {
        e.preventDefault();
        setIsCommandOpen(prev => !prev);
      }
    };
    window.addEventListener('keydown', handleGlobalKey);
    return () => window.removeEventListener('keydown', handleGlobalKey);
  }, []);

  const handleGradeChange = (grade: string) => {
    setSelectedGrade(grade);
    localStorage.setItem('gurukul_selected_grade', grade);
    const activeClass = classes.find((c) => c.grade === grade) || classes[0];
    setAvailableSubjects(activeClass.subjects);
    if (!activeClass.subjects.includes(selectedSubject)) {
      setSelectedSubject(activeClass.subjects[0]);
    }
  };

  // Discovery Fetch
  useEffect(() => {
    async function loadDiscovery() {
      try {
        const primaryUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
        let res: Response | null = null;
        try {
          res = await fetch(`${primaryUrl}/api/v1/classes`);
        } catch {
          res = await fetch('http://127.0.0.1:8080/api/v1/classes');
        }

        if (res && res.ok) {
          const classList: ClassDiscovery[] = await res.json();
          if (classList && classList.length > 0) {
            setClasses(classList);
            const activeClass = classList.find((c) => c.grade === selectedGrade) || classList[0];
            setAvailableSubjects(activeClass.subjects);
          }
        }
      } catch (err) {
        console.warn('Class discovery API offline, using fallback catalog:', err);
      }
    }
    loadDiscovery();
  }, [selectedGrade]);

  // Subject Details Fetch
  useEffect(() => {
    async function fetchSubjectData() {
      try {
        setLoading(true);
        setApiError(null);

        const primaryUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8080';
        const fallbackUrl = 'http://127.0.0.1:8080';
        let targetUrl = primaryUrl;

        let res: Response | null = null;
        try {
          res = await fetch(`${targetUrl}/api/v1/classes/${selectedGrade}/subjects/${selectedSubject}`);
        } catch {
          targetUrl = fallbackUrl;
          try {
            res = await fetch(`${targetUrl}/api/v1/classes/${selectedGrade}/subjects/${selectedSubject}`);
          } catch (retryErr: any) {
            setApiError({
              endpoint: `${primaryUrl}/api/v1/classes/${selectedGrade}/subjects/${selectedSubject}`,
              error: retryErr.message || 'TypeError: Failed to fetch (Connection Refused)',
            });
            setSubjectData(FALLBACK_CLASS5_ENGLISH);
            setLoading(false);
            return;
          }
        }

        if (res && res.ok) {
          const data: SubjectDetails = await res.json();
          setSubjectData(data);
        } else {
          setApiError({
            endpoint: `${targetUrl}/api/v1/classes/${selectedGrade}/subjects/${selectedSubject}`,
            status: res?.status,
            error: `API returned HTTP ${res?.status}: ${res?.statusText}`,
          });
          setSubjectData(FALLBACK_CLASS5_ENGLISH);
        }
      } catch (err: any) {
        console.warn('Subject API offline, using fallback catalog:', err);
        setApiError({
          endpoint: `http://localhost:8080/api/v1/classes/${selectedGrade}/subjects/${selectedSubject}`,
          error: err.message || 'TypeError: Failed to fetch',
        });
        setSubjectData(FALLBACK_CLASS5_ENGLISH);
      } finally {
        setLoading(false);
      }
    }

    fetchSubjectData();
  }, [selectedGrade, selectedSubject]);

  // Get first chapter for Continue Learning hero card
  const firstChapter = subjectData?.units?.[0]?.chapters?.[0];

  // Filtered units based on live search query
  const filteredUnits = subjectData?.units?.map(unit => ({
    ...unit,
    chapters: unit.chapters.filter(ch => ch.title.toLowerCase().includes(searchQuery.toLowerCase()) || ch.id.toLowerCase().includes(searchQuery.toLowerCase()))
  })).filter(unit => unit.chapters.length > 0) || [];

  return (
    <div className="min-h-screen bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-indigo-50/50 via-slate-50 to-white text-[#0F172A] selection:bg-indigo-500 selection:text-white">
      <CommandPalette isOpen={isCommandOpen} onClose={() => setIsCommandOpen(false)} />

      <main className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 pt-10 pb-16 md:pt-14 md:pb-20 space-y-10">
        {/* Calm Welcome Header with Command Palette Trigger */}
        <header className="space-y-4 border-b border-slate-200/80 pb-6 pt-2">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-700 text-xs font-bold uppercase tracking-wider">
              <span>Gurukul AI Classroom</span>
            </div>
            <button
              onClick={() => setIsCommandOpen(true)}
              className="inline-flex items-center gap-3 px-4 py-2 bg-white/80 backdrop-blur-md border border-slate-200 hover:border-indigo-400 rounded-2xl shadow-xs text-xs font-bold text-slate-600 transition-all group hover:scale-[1.02]"
            >
              <span>🔍 Quick Search & Command</span>
              <kbd className="px-2 py-0.5 bg-slate-100 border border-slate-200 rounded-lg text-[10px] font-mono text-slate-500 group-hover:border-indigo-300">Ctrl + K</kbd>
            </button>
          </div>

          <div className="flex flex-wrap items-center justify-between gap-6">
            <div className="space-y-2 max-w-3xl">
              <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-slate-900 leading-tight">
                Good morning, Explorer 👋
              </h1>
              <p className="text-slate-600 text-base sm:text-lg leading-relaxed">
                Welcome to your personal learning journey. Explore curriculum units, lessons, practice exercises, flashcards, and quizzes.
              </p>
            </div>
            <div className="p-5 bg-white/80 backdrop-blur-xl border border-slate-200/80 rounded-3xl shadow-lg shadow-slate-900/5 flex items-center gap-4 hover:scale-[1.02] transition-all">
              <span className="text-3xl">🔥</span>
              <div>
                <div className="text-xl font-black text-slate-900">{streak} Day Streak</div>
                <div className="text-xs text-slate-500 font-bold">Keep learning daily!</div>
              </div>
            </div>
          </div>
        </header>

        {/* 1. CONTINUE LEARNING HERO CARD */}
        {firstChapter && (
          <section className="p-6 md:p-8 bg-gradient-to-r from-indigo-900 via-slate-900 to-indigo-950 text-white rounded-3xl shadow-2xl space-y-4 hover:scale-[1.005] transition-all">
            <div className="flex items-center justify-between gap-2">
              <span className="px-3 py-1 text-xs font-black uppercase tracking-widest bg-indigo-500/30 text-indigo-300 rounded-lg border border-indigo-400/20">
                Continue Learning
              </span>
              <span className="text-xs font-mono text-slate-400">Class {selectedGrade} • {selectedSubject}</span>
            </div>

            <div className="space-y-1">
              <h2 className="text-2xl sm:text-3xl font-black tracking-tight text-white">
                {firstChapter.title}
              </h2>
              <p className="text-slate-300 text-sm">
                Chapter {firstChapter.chapterNumber} • {subjectData?.units?.[0]?.title || 'Unit 1'}
              </p>
            </div>

            <div className="pt-2 flex justify-end">
              <Link
                href={`/${selectedGrade}/${selectedSubject}/${firstChapter.id}`}
                className="inline-flex items-center gap-2 px-6 py-3 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-extrabold rounded-2xl shadow-lg shadow-indigo-600/30 transition-all hover:translate-x-1"
              >
                <span>Continue Learning</span>
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M14 5l7 7-7 7M3 12h18" />
                </svg>
              </Link>
            </div>
          </section>
        )}

        {/* 2. YOUR SUBJECTS SELECTOR */}
        <section className="space-y-4 bg-white/80 backdrop-blur-2xl p-6 md:p-8 rounded-3xl border border-slate-200/80 shadow-xl shadow-slate-900/5">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-black tracking-widest text-slate-500 uppercase">
              YOUR SUBJECTS
            </h2>
            <div className="flex items-center gap-2">
              <span className="text-xs font-bold text-slate-400">Grade:</span>
              <div className="flex gap-1">
                {classes.map((c) => (
                  <button
                    key={`class-select-${c.grade}`}
                    onClick={() => handleGradeChange(c.grade)}
                    className={`px-3 py-1 rounded-xl text-xs font-extrabold transition-all ${
                      selectedGrade === c.grade
                        ? 'bg-slate-900 text-white shadow-xs'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    Class {c.grade}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
            {availableSubjects.map((sub) => {
              const isActive = selectedSubject === sub;
              return (
                <button
                  key={sub}
                  onClick={() => setSelectedSubject(sub)}
                  className={`p-4 rounded-2xl text-left border transition-all flex flex-col justify-between gap-2 hover:-translate-y-0.5 ${
                    isActive
                      ? 'bg-indigo-600 text-white border-indigo-500 shadow-lg shadow-indigo-600/30'
                      : 'bg-slate-50/80 text-slate-700 hover:bg-slate-100 border-slate-200/80'
                  }`}
                >
                  <span className="text-xl">
                    {sub === 'English' ? '📚' : sub === 'Hindi' ? '🌸' : sub === 'Maths' ? '📐' : sub === 'Science' ? '🔬' : '🌍'}
                  </span>
                  <div>
                    <div className="text-sm font-extrabold">{sub}</div>
                    <div className={`text-[10px] font-bold ${isActive ? 'text-indigo-200' : 'text-slate-400'}`}>
                      {selectedGrade === '6' ? 'Class 6 Curriculum' : 'Class 5 Curriculum'}
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </section>

        {/* API Connection Warning Banner if Offline */}
        {apiError && (
          <div className="p-4 bg-amber-50 border border-amber-200 rounded-2xl text-amber-900 text-xs flex items-center justify-between gap-4">
            <div>
              <strong>⚠️ Backend API Connection Notice:</strong> {apiError.error}. Operating with local fallback catalog. Ensure FastAPI server is running (`python backend/src/main.py`).
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

        {/* 4. CHAPTERS LIST BY UNIT */}
        <section className="space-y-6">
          <div className="flex items-center justify-between">
            <h2 className="text-xs font-black tracking-widest text-slate-500 uppercase">
              Curriculum Chapters • {selectedSubject} (Class {selectedGrade})
            </h2>
            <span className="text-xs font-bold text-slate-400">
              {subjectData?.totalChapters || 0} Chapters Total
            </span>
          </div>

          {loading ? (
            <div className="flex items-center justify-center py-16 text-slate-500 bg-white/80 backdrop-blur-xl rounded-3xl border border-slate-200/80">
              <div className="animate-spin w-6 h-6 border-2 border-indigo-600 border-t-transparent rounded-full mr-3" />
              <span className="font-bold text-sm">Loading Curriculum Units...</span>
            </div>
          ) : filteredUnits.length > 0 ? (
            filteredUnits.map((unit) => (
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
                  {unit.chapters.map((ch) => (
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
                          href={`/${selectedGrade}/${selectedSubject}/${ch.id}`}
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
              <h3 className="text-lg font-bold text-slate-900">No chapters found</h3>
              <p className="text-xs text-slate-400">Try adjusting your live search term.</p>
            </div>
          )}
        </section>

        {/* 5. NEP 2020 PEDAGOGICAL GOALS */}
        <section className="p-6 md:p-8 bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white rounded-3xl shadow-2xl space-y-6">
          <div className="space-y-2">
            <span className="px-3 py-1 text-xs font-black uppercase tracking-widest bg-teal-500/20 text-teal-300 rounded-lg border border-teal-400/30">
              National Education Policy 2020
            </span>
            <h2 className="text-2xl font-black tracking-tight">
              Curricular Goals & Pedagogical Principles
            </h2>
            <p className="text-slate-300 text-sm max-w-2xl leading-relaxed">
              Gurukul AI aligns fully with NCF-SE 2023 guidelines, fostering holistic, experiential, inquiry-driven, and multi-disciplinary learning.
            </p>
          </div>

          <div className="grid grid-classes sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {subjectData?.curricularGoals?.map((goal) => (
              <div
                key={goal.code}
                onClick={() => setSelectedGoalModal(goal)}
                className="cursor-pointer p-5 bg-white/5 hover:bg-white/10 border border-white/10 rounded-2xl transition-all space-y-2 group"
              >
                <div className="text-xs font-black text-indigo-400">{goal.code}</div>
                <div className="text-sm font-bold text-white group-hover:text-teal-300 transition-colors">{goal.name}</div>
                <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">{goal.description}</p>
              </div>
            ))}
          </div>
        </section>
      </main>
    </div>
  );
}
