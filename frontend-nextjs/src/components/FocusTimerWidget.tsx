import React, { useState, useEffect } from 'react';

interface TimerProps {
  onComplete: () => void;
}

export default function FocusTimerWidget({ onComplete }: TimerProps) {
  const [timeLeft, setTimeLeft] = useState<number>(25 * 60);
  const [isRunning, setIsRunning] = useState<boolean>(false);
  const [mode, setMode] = useState<'focus' | 'break'>('focus');

  useEffect(() => {
    let timer: any = null;
    if (isRunning && timeLeft > 0) {
      timer = setInterval(() => {
        setTimeLeft(prev => prev - 1);
      }, 1000);
    } else if (timeLeft === 0) {
      setIsRunning(false);
      onComplete();
    }
    return () => clearInterval(timer);
  }, [isRunning, timeLeft, onComplete]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="p-5 bg-white border border-slate-200 rounded-3xl shadow-sm space-y-4">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="text-xs font-black uppercase tracking-wider text-indigo-600">
          ⏱️ Pomodoro Focus Timer ({mode === 'focus' ? 'Study' : 'Break'})
        </div>
        <div className="flex gap-1">
          <button
            onClick={() => { setMode('focus'); setTimeLeft(25 * 60); setIsRunning(false); }}
            className={`px-2.5 py-1 rounded-xl text-[10px] font-bold ${mode === 'focus' ? 'bg-indigo-600 text-white' : 'bg-slate-100 text-slate-600'}`}
          >
            25m
          </button>
          <button
            onClick={() => { setMode('break'); setTimeLeft(5 * 60); setIsRunning(false); }}
            className={`px-2.5 py-1 rounded-xl text-[10px] font-bold ${mode === 'break' ? 'bg-teal-600 text-white' : 'bg-slate-100 text-slate-600'}`}
          >
            5m
          </button>
        </div>
      </div>

      <div className="text-center space-y-2">
        <div className="text-4xl font-black font-mono text-slate-900 tracking-tight">
          {formatTime(timeLeft)}
        </div>
        <p className="text-xs text-slate-500 font-medium">
          {mode === 'focus' ? 'Deep focus session. Stay curious!' : 'Relax and recharge your mind.'}
        </p>
      </div>

      <div className="flex items-center justify-center gap-3 pt-2">
        <button
          onClick={() => setIsRunning(!isRunning)}
          className={`px-6 py-2.5 rounded-2xl text-xs font-extrabold shadow-sm transition-all ${isRunning ? 'bg-amber-600 hover:bg-amber-500 text-white' : 'bg-indigo-600 hover:bg-indigo-500 text-white'}`}
        >
          {isRunning ? 'Pause Timer' : 'Start Focus'}
        </button>
        <button
          onClick={() => { setIsRunning(false); setTimeLeft(mode === 'focus' ? 25 * 60 : 5 * 60); }}
          className="px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-bold rounded-2xl transition-all"
        >
          Reset
        </button>
      </div>
    </div>
  );
}
