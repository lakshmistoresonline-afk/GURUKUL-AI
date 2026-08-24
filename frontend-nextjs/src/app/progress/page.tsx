'use client';

import React, { useEffect, useState, useMemo } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import Breadcrumbs from '@/components/Breadcrumbs';
import { TrendingUp, Award, Clock, BookOpen, RefreshCw, CheckCircle2 } from 'lucide-react';
import { useAuth } from '@/context/AuthContext';
import { progressService, MasteryRecord } from '@/services/progress';
import { normalizeClassName, getChapterDisplayData } from '@/utils/chapter';

export default function ProgressPage() {
  const { profile, loading: authLoading } = useAuth();
  const [mastery, setMastery] = useState<MasteryRecord[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (authLoading || !profile) return;

    const fetchData = async () => {
      try {
        const data = await progressService.getStudentMastery();
        const normUserClass = normalizeClassName(profile.className);
        setMastery(data.filter(r => normalizeClassName(r.className) === normUserClass));
      } catch (e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [authLoading, profile]);

  const metrics = useMemo(() => {
    if (mastery.length === 0) return { overall: 0, chapters: 0, weak: [], subjects: [] };

    const sum = mastery.reduce((acc, curr) => acc + (curr.progress || 0), 0);
    const overall = Math.round((sum / mastery.length) * 100);
    const chapters = mastery.filter(m => (m.progress || 0) >= 0.8).length;

    const subjects: Record<string, { total: number, count: number }> = {};
    mastery.forEach(m => {
      if (!subjects[m.subject]) subjects[m.subject] = { total: 0, count: 0 };
      subjects[m.subject].total += (m.progress || 0);
      subjects[m.subject].count += 1;
    });

    const weak: any[] = [];
    mastery.forEach(m => {
      if ((m.progress || 0) < 0.5 && (m.progress || 0) > 0) {
        weak.push({ topic: m.chapterId, subject: m.subject, score: Math.round((m.progress || 0) * 100) });
      }
    });

    return {
      overall,
      chapters,
      weak: weak.slice(0, 3),
      subjects: Object.entries(subjects).map(([name, data]) => ({
        name,
        value: Math.round((data.total / data.count) * 100)
      }))
    };
  }, [mastery]);

  if (authLoading || loading) return (
    <div className="flex min-h-screen items-center justify-center bg-slate-50">
       <RefreshCw className="animate-spin text-primary" size={32} />
    </div>
  );

  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="Analytics & Progress" />

        <div className="max-w-6xl mx-auto p-8">
          <Breadcrumbs items={[{ label: 'Analytics', href: '#' }]} />

          <div className="space-y-8 mt-6">
            <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <StatCard icon={TrendingUp} label="Overall Mastery" value={`${metrics.overall}%`} color="blue" />
              <StatCard icon={BookOpen} label="Chapters Mastered" value={metrics.chapters.toString()} color="emerald" />
              <StatCard icon={Clock} label="Class Level" value={profile?.classId || "?"} color="orange" />
              <StatCard icon={Award} label="Achievements" value={(profile?.xp || 0) > 1000 ? "Level 2" : "Level 1"} color="purple" />
            </section>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 bg-white rounded-[40px] border border-slate-200 p-10 shadow-sm">
                <h3 className="text-xl font-black text-slate-800 mb-10">Subject Performance</h3>
                <div className="space-y-10">
                  {metrics.subjects.length > 0 ? metrics.subjects.map((s, i) => (
                    <ProgressBar key={i} label={s.name.toUpperCase()} value={s.value} color="bg-primary" />
                  )) : (
                    <p className="text-slate-400 font-bold italic">No learning data available for your class yet.</p>
                  )}
                </div>
              </div>

              <div className="bg-white rounded-[40px] border border-slate-200 p-10 shadow-sm">
                <h3 className="text-xl font-black text-slate-800 mb-8 text-center uppercase tracking-widest">Focus Areas</h3>
                <div className="space-y-6">
                  {metrics.weak.length > 0 ? metrics.weak.map((w, i) => (
                    <div key={i} className="p-6 bg-red-50 rounded-[32px] border border-red-100">
                      <p className="text-red-700 font-black text-lg leading-tight uppercase tracking-tight">
                        {getChapterDisplayData(w.topic).name}
                      </p>
                      <p className="text-red-400 text-xs font-bold mt-1 uppercase tracking-widest">{w.subject} • {w.score}% Mastery</p>
                    </div>
                  )) : (
                    <div className="py-12 text-center">
                      <CheckCircle2 size={48} className="mx-auto text-emerald-200 mb-4" />
                      <p className="text-slate-400 font-bold text-sm">No weak topics identified yet. Keep learning!</p>
                    </div>
                  )}
                </div>
                {metrics.weak.length > 0 && (
                   <button className="w-full mt-10 py-4 bg-slate-900 text-white rounded-2xl font-black text-xs uppercase tracking-widest hover:bg-primary transition-all shadow-lg active:scale-95">
                     Start Remedial Practice
                   </button>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color }: any) {
  const colors: any = {
    blue: "text-blue-600 bg-blue-50",
    emerald: "text-emerald-600 bg-emerald-50",
    orange: "text-orange-600 bg-orange-50",
    purple: "text-purple-600 bg-purple-50",
  };
  return (
    <div className="bg-white border border-slate-200 rounded-[32px] p-8 shadow-sm">
      <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mb-6 ${colors[color]}`}>
        <Icon size={24} />
      </div>
      <p className="text-slate-400 text-[10px] font-black uppercase tracking-[0.2em]">{label}</p>
      <h4 className="text-3xl font-black text-slate-900 mt-2">{value}</h4>
    </div>
  );
}

function ProgressBar({ label, value, color }: any) {
  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center text-xs font-black uppercase tracking-widest">
        <span className="text-slate-600">{label}</span>
        <span className="text-primary">{value}%</span>
      </div>
      <div className="h-4 bg-slate-50 border border-slate-100 rounded-full overflow-hidden p-1">
        <div className={`h-full ${color} rounded-full shadow-sm`} style={{ width: `${value}%` }}></div>
      </div>
    </div>
  );
}
