import React, { useState, useEffect } from 'react';

interface QuestProps {
  onClaimReward: (xp: number) => void;
}

export default function DailyQuestWidget({ onClaimReward }: QuestProps) {
  const [completed, setCompleted] = useState<boolean>(false);

  useEffect(() => {
    const isDone = localStorage.getItem('gurukul_daily_quest_done') === 'true';
    setCompleted(isDone);
  }, []);

  const handleCompleteQuest = () => {
    if (!completed) {
      setCompleted(true);
      localStorage.setItem('gurukul_daily_quest_done', 'true');
      onClaimReward(75);
    }
  };

  return (
    <div className="p-6 bg-gradient-to-br from-amber-500/10 via-amber-500/5 to-white border border-amber-500/20 rounded-3xl shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-amber-500/10 pb-3">
        <div className="text-xs font-black uppercase tracking-wider text-amber-800">
          📜 Daily Learning Quest
        </div>
        <span className="text-[10px] font-extrabold px-2.5 py-1 bg-amber-100 text-amber-900 rounded-full">+75 XP Reward</span>
      </div>

      <div className="space-y-1">
        <h4 className="text-base font-bold text-slate-900">Explore Today&apos;s Curriculum Milestone</h4>
        <p className="text-xs text-slate-600">Review any chapter notes or complete a quick quiz to earn your daily quest bonus.</p>
      </div>

      <div className="pt-2 flex items-center justify-between">
        <span className="text-xs font-bold text-slate-500">{completed ? 'Status: Completed ✓' : 'Status: In Progress ⏱️'}</span>
        <button
          onClick={handleCompleteQuest}
          disabled={completed}
          className="px-5 py-2.5 bg-amber-600 hover:bg-amber-500 disabled:opacity-50 text-white text-xs font-extrabold rounded-xl shadow-md transition-all"
        >
          {completed ? 'Reward Claimed ✓' : 'Claim Quest Reward'}
        </button>
      </div>
    </div>
  );
}
