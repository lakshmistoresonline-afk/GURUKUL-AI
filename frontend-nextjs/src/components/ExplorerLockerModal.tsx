import React from 'react';

interface LockerProps {
  isOpen: boolean;
  onClose: () => void;
  xp: number;
  streak: number;
}

export default function ExplorerLockerModal({ isOpen, onClose, xp, streak }: LockerProps) {
  if (!isOpen) return null;

  const badges = [
    { title: '🌱 Curious Novice', unlocked: true, desc: 'Started your learning journey.' },
    { title: '🔥 5-Day Streak', unlocked: streak >= 5, desc: 'Learned 5 days in a row.' },
    { title: '⚡ Quiz Ace', unlocked: xp >= 1000, desc: 'Scored high on multiple quizzes.' },
    { title: '👑 Master Academic', unlocked: xp >= 3000, desc: 'Reached 3,000+ XP milestone.' },
  ];

  return (
    <div className="fixed inset-0 z-50 bg-slate-900/65 backdrop-blur-sm flex items-center justify-center p-4">
      <div className="bg-white border border-slate-200 rounded-3xl shadow-2xl max-w-lg w-full overflow-hidden p-6 sm:p-8 space-y-6 animate-in fade-in zoom-in-95 duration-200">
        <div className="flex items-center justify-between border-b border-slate-100 pb-4">
          <div>
            <h3 className="text-xl font-black text-slate-900">🏆 Explorer Locker</h3>
            <p className="text-xs text-slate-500">Your personal achievements and companion avatar.</p>
          </div>
          <button onClick={onClose} className="p-2 bg-slate-100 hover:bg-slate-200 rounded-full text-slate-600 font-bold text-xs">✕</button>
        </div>

        <div className="flex items-center gap-4 p-4 bg-indigo-50/60 border border-indigo-100 rounded-2xl">
          <div className="w-14 h-14 bg-indigo-600 rounded-2xl flex items-center justify-center text-white text-2xl shadow-md">
            🚀
          </div>
          <div>
            <div className="text-sm font-black text-slate-900">Explorer Scholar</div>
            <div className="text-xs font-bold text-indigo-700">{xp} Total XP • {streak} Day Streak</div>
          </div>
        </div>

        <div className="space-y-3">
          <div className="text-xs font-black uppercase tracking-wider text-slate-400">Unlocked Badges</div>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {badges.map((b, idx) => (
              <div key={idx} className={`p-4 rounded-2xl border text-left space-y-1 ${b.unlocked ? 'bg-emerald-50/50 border-emerald-200 text-emerald-950' : 'bg-slate-50 border-slate-200 opacity-50'}`}>
                <div className="text-sm font-black">{b.title} {b.unlocked ? '✓' : '🔒'}</div>
                <div className="text-[11px] text-slate-600">{b.desc}</div>
              </div>
            ))}
          </div>
        </div>

        <button
          onClick={onClose}
          className="w-full py-3 bg-indigo-600 hover:bg-indigo-500 text-white font-bold rounded-2xl shadow-lg shadow-indigo-600/20 transition-all text-sm"
        >
          Back to Classroom
        </button>
      </div>
    </div>
  );
}
