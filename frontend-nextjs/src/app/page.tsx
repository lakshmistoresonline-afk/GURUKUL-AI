'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

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
    {
      id: 'U02',
      unitNumber: 2,
      title: 'My Colourful World',
      theme: 'Wonder of nature, animals, and clever problem-solving.',
      chapters: [
        {
          id: 'G5-ENG-U02-C03',
          chapterNumber: 3,
          title: 'The Rainbow',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
        {
          id: 'G5-ENG-U02-C04',
          chapterNumber: 4,
          title: 'The Wise Parrot',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
      ],
    },
    {
      id: 'U03',
      unitNumber: 3,
      title: 'Water and Nature',
      theme: 'Environmental consciousness, biodiversity, and conservation.',
      chapters: [
        {
          id: 'G5-ENG-U03-C05',
          chapterNumber: 5,
          title: 'My Frog’s World',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
        {
          id: 'G5-ENG-U03-C06',
          chapterNumber: 6,
          title: 'What a Tank!',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
      ],
    },
    {
      id: 'U04',
      unitNumber: 4,
      title: 'Ups and Downs',
      theme: 'Sportsmanship, traditional games, justice, and community wisdom.',
      chapters: [
        {
          id: 'G5-ENG-U04-C07',
          chapterNumber: 7,
          title: 'Gilli Danda',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
        {
          id: 'G5-ENG-U04-C08',
          chapterNumber: 8,
          title: 'The Decision of the Panchayat',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
      ],
    },
    {
      id: 'U05',
      unitNumber: 5,
      title: 'Work Is Worship',
      theme: 'Dignity of labor, traditional crafts, and choosing life callings.',
      chapters: [
        {
          id: 'G5-ENG-U05-C09',
          chapterNumber: 9,
          title: 'Vocation',
          resourceCount: 8,
          contentTypes: ['Overview', 'Learn', 'Practice', 'Quiz', 'Flashcards', 'Mind Map'],
        },
        {
          id: 'G5-ENG-U05-C10',
          chapterNumber: 10,
          title: 'Glass Bangles',
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
    { grade: '6', subjects: ['English', 'Hindi', 'Maths', 'Science'] },
    { grade: '7', subjects: ['English', 'Hindi', 'Maths', 'Science'] },
  ]);
  const [selectedGrade, setSelectedGrade] = useState<string>('5');
  const [selectedSubject, setSelectedSubject] = useState<string>('English');
  const [availableSubjects, setAvailableSubjects] = useState<string[]>(['English', 'Hindi', 'Maths', 'Science']);
  const [subjectData, setSubjectData] = useState<SubjectDetails | null>(FALLBACK_CLASS5_ENGLISH);
  const [selectedGoalModal, setSelectedGoalModal] = useState<CurricularGoal | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [apiError, setApiError] = useState<ApiDiagnostics | null>(null);

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
            status: res?.status || 500,
            error: `API returned HTTP ${res?.status || 500}: ${res?.statusText || 'Internal Server Error'}`,
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

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-[#0F172A] selection:bg-indigo-500 selection:text-white">
      <main className="mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 pt-10 pb-16 md:pt-14 md:pb-20 space-y-10">
        {/* Calm Welcome Header with Generous Top Padding */}
        <header className="space-y-3 border-b border-slate-200 pb-6 pt-2">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-teal-500/10 border border-teal-500/20 text-teal-700 text-xs font-bold uppercase tracking-wider">
            <span>Gurukul AI Classroom</span>
          </div>
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-slate-900 leading-tight pt-1">
            Good morning, Learner 👋
          </h1>
          <p className="text-slate-600 text-base sm:text-lg max-w-2xl leading-relaxed">
            Welcome to your personal learning journey. Explore curriculum units, lessons, practice exercises, flashcards, and quizzes.
          </p>
        </header>

        {/* 1. CONTINUE LEARNING HERO CARD */}
        {firstChapter && (
          <section className="p-6 md:p-8 bg-gradient-to-r from-indigo-900 to-slate-900 text-white rounded-3xl shadow-xl space-y-4">
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
        <section className="space-y-4 bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm">
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
                    onClick={() => {
                      setSelectedGrade(c.grade);
                      setAvailableSubjects(c.subjects);
                      if (!c.subjects.includes(selectedSubject) && c.subjects.length > 0) {
                        setSelectedSubject(c.subjects[0]);
                      }
                    }}
                    className={`px-3 py-1 rounded-lg text-xs font-bold transition-all ${
                      selectedGrade === c.grade
                        ? 'bg-slate-900 text-white'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    Class {c.grade}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            {availableSubjects.map((sub, sIdx) => {
              const isSelected = selectedSubject === sub;
              return (
                <button
                  key={`subject-btn-${sub}-${sIdx}`}
                  onClick={() => setSelectedSubject(sub)}
                  className={`p-4 rounded-2xl text-base font-extrabold transition-all text-center border ${
                    isSelected
                      ? 'bg-indigo-600 text-white border-indigo-600 shadow-lg shadow-indigo-600/20 scale-[1.02]'
                      : 'bg-slate-50 text-slate-700 hover:bg-slate-100 border-slate-200'
                  }`}
                >
                  {sub}
                </button>
              );
            })}
          </div>
        </section>

        {/* API Connection Warning Diagnostic Banner */}
        {apiError && (
          <div className="p-6 bg-red-500/10 border border-red-500/30 rounded-3xl space-y-2 text-xs font-mono text-red-600">
            <div className="font-bold text-red-700 text-sm">⚠️ Backend API Connection Warning:</div>
            <div>Endpoint: {apiError.endpoint}</div>
            <div>Error: {apiError.error}</div>
            <div className="text-slate-600 font-sans pt-1">
              Ensure FastAPI is running: <code className="bg-white px-1 py-0.5 rounded text-indigo-700 font-mono border border-slate-200">python backend/src/main.py</code> on port 8080.
            </div>
          </div>
        )}

        {/* 3. YOUR CHAPTERS LIST (Units & Chapters Grid) */}
        {loading ? (
          <div className="flex items-center justify-center py-24 text-slate-500 space-x-3">
            <div className="animate-spin w-8 h-8 border-2 border-indigo-600 border-t-transparent rounded-full" />
            <span className="text-base font-semibold">Loading Subject Content...</span>
          </div>
        ) : subjectData && subjectData.units && subjectData.units.length > 0 ? (
          <div className="space-y-10">
            <div className="text-xs font-black tracking-widest text-slate-500 uppercase">
              YOUR CHAPTERS • {selectedSubject}
            </div>

            {subjectData.units.map((unit, uIdx) => {
              const rawTitle = unit.title || `Unit ${unit.unitNumber || (uIdx + 1)}`;
              const cleanUnitTitle = typeof rawTitle === 'string' ? rawTitle.replace(/^Unit \d+:\s*/i, '') : `Unit ${unit.unitNumber || (uIdx + 1)}`;
              const unitKey = `unit-sec-${selectedSubject}-${unit.id || unit.unitNumber || uIdx}-${uIdx}`;

              return (
                <section key={unitKey} className="space-y-5 bg-white p-6 md:p-8 rounded-3xl border border-slate-200 shadow-sm">
                  {/* Unit Section Header */}
                  <div className="space-y-1 border-b border-slate-100 pb-4">
                    <div className="text-xs font-black tracking-widest text-indigo-600 uppercase">
                      UNIT {unit.unitNumber || (uIdx + 1)}
                    </div>
                    <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
                      {cleanUnitTitle}
                    </h2>
                    {unit.theme && (
                      <p className="text-slate-500 text-sm italic font-normal">
                        Theme: {unit.theme}
                      </p>
                    )}
                  </div>

                  {/* Clean Chapter Cards Grid (No Tiny Button Clutter) */}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                    {unit.chapters && unit.chapters.map((ch, cIdx) => {
                      const chapterKey = `chapter-card-${selectedSubject}-${ch.id || ch.chapterNumber || cIdx}-${cIdx}`;
                      return (
                        <Link
                          key={chapterKey}
                          href={`/${selectedGrade}/${selectedSubject}/${ch.id}`}
                          className="group p-6 bg-slate-50 hover:bg-slate-100/80 border border-slate-200/80 hover:border-indigo-400 rounded-2xl flex flex-col justify-between space-y-4 transition-all hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500"
                          aria-label={`Open Chapter ${ch.chapterNumber}: ${ch.title}`}
                        >
                          <div className="space-y-3">
                            {/* Card Top Badge Row */}
                            <div className="flex items-center justify-between gap-2">
                              <span className="px-2.5 py-0.5 text-[11px] font-extrabold uppercase tracking-wider bg-indigo-50 text-indigo-700 border border-indigo-200 rounded-md">
                                CHAPTER {ch.chapterNumber}
                              </span>
                              <span className="text-[11px] font-mono text-slate-400">
                                {ch.id}
                              </span>
                            </div>

                            {/* Chapter Title */}
                            <h3 className="text-xl font-bold text-slate-900 group-hover:text-indigo-600 transition-colors tracking-tight leading-snug">
                              {ch.title}
                            </h3>
                          </div>

                          {/* Clean CTA Footer */}
                          <div className="flex items-center justify-between text-xs font-bold text-indigo-600 group-hover:text-indigo-700 transition-colors pt-3 border-t border-slate-200/60">
                            <span>Open Chapter</span>
                            <svg
                              className="w-4 h-4 group-hover:translate-x-1 transition-transform"
                              fill="none"
                              stroke="currentColor"
                              viewBox="0 0 24 24"
                            >
                              <path
                                strokeLinecap="round"
                                strokeLinejoin="round"
                                strokeWidth={2.5}
                                d="M14 5l7 7-7 7M3 12h18"
                              />
                            </svg>
                          </div>
                        </Link>
                      );
                    })}
                  </div>
                </section>
              );
            })}
          </div>
        ) : (
          <div className="p-12 text-center text-slate-500 bg-white rounded-3xl border border-slate-200">
            No chapters discovered for Class {selectedGrade} {selectedSubject}.
          </div>
        )}

        {/* 4. CURRICULUM FRAMEWORK OBJECTIVES (Secondary Footer Section) */}
        {subjectData?.curricularGoals && subjectData.curricularGoals.length > 0 && (
          <section className="p-6 md:p-8 bg-white border border-slate-200 rounded-3xl space-y-5 shadow-sm">
            <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div className="space-y-0.5">
                <div className="text-xs font-black uppercase tracking-widest text-teal-600">
                  CURRICULUM FRAMEWORK ({subjectData.curriculumFramework || 'NEP 2020 & NCF-SE 2023'})
                </div>
                <h2 className="text-lg font-bold text-slate-900 tracking-tight">
                  Subject Framework Objectives
                </h2>
              </div>
              <span className="text-xs font-bold px-2.5 py-0.5 bg-slate-100 border border-slate-200 text-slate-600 rounded-md">
                4 Core Goals
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              {subjectData.curricularGoals.map((cg, gIdx) => (
                <div
                  key={`goal-card-${selectedSubject}-${cg.code || gIdx}-${gIdx}`}
                  onClick={() => setSelectedGoalModal(cg)}
                  className="group p-4 bg-slate-50 border border-slate-200/80 hover:border-teal-500/60 rounded-2xl space-y-2 flex flex-col justify-between cursor-pointer transition-all hover:shadow-md focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500"
                  tabIndex={0}
                  role="button"
                  aria-label={`View details for ${cg.code}: ${cg.name || cg.code}`}
                >
                  <div className="space-y-1.5">
                    <span className="inline-block px-2 py-0.5 text-[10px] font-black uppercase bg-teal-50 text-teal-700 border border-teal-200 rounded-md">
                      {cg.code}
                    </span>
                    <h3 className="text-sm font-bold text-slate-900 group-hover:text-teal-700 transition-colors leading-snug">
                      {cg.name || cg.code}
                    </h3>
                    <p className="text-xs text-slate-600 leading-relaxed font-normal line-clamp-2">
                      {cg.description}
                    </p>
                  </div>

                  <div className="flex items-center text-[11px] font-bold text-teal-600 group-hover:text-teal-700 transition-colors pt-2 border-t border-slate-200/60">
                    <span>Goal Details</span>
                    <svg className="w-3.5 h-3.5 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                    </svg>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>

      {/* Navigable Curricular Goal Detail Modal */}
      {selectedGoalModal && (
        <div
          className="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm flex items-center justify-center p-4 sm:p-6"
          onClick={() => setSelectedGoalModal(null)}
        >
          <div
            className="p-6 md:p-8 bg-white border border-slate-200 rounded-3xl max-w-xl w-full space-y-5 shadow-2xl relative"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-slate-100 pb-4">
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 text-xs font-black uppercase bg-teal-50 text-teal-700 border border-teal-200 rounded-lg">
                  {selectedGoalModal.code}
                </span>
                <span className="text-xs font-bold text-slate-500">
                  {subjectData?.curriculumFramework || 'NEP 2020 & NCF-SE 2023'}
                </span>
              </div>
              <button
                onClick={() => setSelectedGoalModal(null)}
                className="w-8 h-8 rounded-full bg-slate-100 text-slate-500 hover:text-slate-900 flex items-center justify-center transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500"
                aria-label="Close goal details"
              >
                ✕
              </button>
            </div>

            <div className="space-y-2">
              <h3 className="text-2xl font-extrabold text-slate-900 tracking-tight">
                {selectedGoalModal.name || selectedGoalModal.code}
              </h3>
              <p className="text-slate-700 text-base md:text-lg leading-relaxed font-normal">
                {selectedGoalModal.description}
              </p>
            </div>

            <div className="pt-2 border-t border-slate-100 flex justify-end">
              <button
                onClick={() => setSelectedGoalModal(null)}
                className="px-6 py-2.5 bg-teal-600 hover:bg-teal-500 text-white text-sm font-bold rounded-2xl shadow-md transition-all focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-teal-500"
              >
                Close Goal Details
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
