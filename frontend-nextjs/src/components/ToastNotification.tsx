import React, { useEffect } from 'react';

interface ToastProps {
  message: string;
  subMessage?: string;
  isOpen: boolean;
  onClose: () => void;
}

export default function ToastNotification({ message, subMessage, isOpen, onClose }: ToastProps) {
  useEffect(() => {
    if (isOpen) {
      const timer = setTimeout(() => {
        onClose();
      }, 4000);
      return () => clearTimeout(timer);
    }
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return (
    <div className="fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-6 py-4 rounded-3xl shadow-2xl border border-indigo-500/30 flex items-center gap-4 animate-in slide-in-from-bottom-5 duration-300 backdrop-blur-xl bg-slate-900/90">
      <div className="w-10 h-10 bg-indigo-600 rounded-2xl flex items-center justify-center text-xl shadow-md">
        🎉
      </div>
      <div>
        <div className="text-sm font-black text-white">{message}</div>
        {subMessage && <div className="text-xs text-indigo-200 font-medium">{subMessage}</div>}
      </div>
      <button onClick={onClose} className="ml-4 text-slate-400 hover:text-white font-bold text-xs">✕</button>
    </div>
  );
}
