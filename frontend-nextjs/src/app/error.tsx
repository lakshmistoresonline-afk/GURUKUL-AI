'use client';

import { useEffect } from 'react';

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    console.error('GLOBAL ERROR BOUNDARY:', error);
  }, [error]);

  return (
    <div className="min-h-screen bg-white flex flex-col items-center justify-center p-6 text-center">
      <div className="space-y-6 max-w-md">
        <div className="w-20 h-20 bg-red-50 text-red-600 rounded-full flex items-center justify-center mx-auto">
           <svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
        </div>
        <h1 className="text-4xl font-black text-slate-900 uppercase italic italic underline decoration-red-100 decoration-8 underline-offset-8">Critical Error</h1>
        <p className="text-slate-500 font-medium">The educational stream has encountered a technical anomaly. Our auditors have been notified.</p>
        <div className="p-4 bg-slate-50 rounded-2xl border border-slate-100 text-left">
           <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-1">Diagnostic Info</p>
           <p className="text-xs font-mono text-slate-600 break-all">{error.message || 'Unknown stream disruption'}</p>
           {error.digest && <p className="text-[10px] text-slate-400 mt-2 italic">Digest: {error.digest}</p>}
        </div>
        <button
          onClick={() => reset()}
          className="w-full py-4 bg-blue-600 text-white rounded-2xl font-black uppercase text-xs hover:bg-blue-700 transition-all shadow-xl"
        >
          Attempt Stream Recovery
        </button>
      </div>
    </div>
  );
}
