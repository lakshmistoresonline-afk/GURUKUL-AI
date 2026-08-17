'use client';

import React, { useState } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { chapterService } from '@/services/api';
import {
  FileUp,
  CheckCircle2,
  Loader2,
  AlertCircle,
  FileText
} from 'lucide-react';

export default function ScanPage() {
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState<any>(null);
  const [error, setError] = useState('');

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    setLoading(true);
    setError('');
    const formData = new FormData();
    formData.append('file', file);
    formData.append('student_id', 'scholar_web');
    formData.append('book_id', 'web_custom');
    formData.append('chapter_id', `ch_${Date.now()}`);
    formData.append('class_name', 'class_5');
    formData.append('subject', 'general');

    try {
      const res = await chapterService.processChapter(formData);
      setStatus(res);
      // Start polling status
      pollStatus(res.job_id);
    } catch (err: any) {
      setError(err.response?.data?.detail?.message || 'Upload failed');
      setLoading(false);
    }
  };

  const pollStatus = async (jobId: string) => {
    const check = async () => {
      try {
        const res = await chapterService.getJobStatus(jobId);
        setStatus(res);
        if (res.status === 'COMPLETED' || res.status === 'FAILED') {
          setLoading(false);
          return;
        }
        setTimeout(check, 3000);
      } catch (err) {
        setLoading(false);
      }
    };
    check();
  };

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="AI Content Generator" />

        <div className="max-w-4xl mx-auto p-8 space-y-8">
          <section className="bg-white border border-border rounded-3xl p-10 shadow-sm text-center">
             <div className="w-20 h-20 bg-blue-50 rounded-3xl flex items-center justify-center text-primary mx-auto mb-8 shadow-xl shadow-blue-50">
                <FileUp size={40} />
             </div>
             <h2 className="text-3xl font-black text-slate-800 mb-4">Upload Textbook PDF</h2>
             <p className="text-slate-500 max-w-md mx-auto font-medium mb-10 leading-relaxed">
                Our AI will extract concepts, create summaries, generate quizzes, and build flashcards for you.
             </p>

             <form onSubmit={handleUpload} className="space-y-6">
                <div className="relative group">
                  <input
                    type="file"
                    accept=".pdf"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="absolute inset-0 w-full h-full opacity-0 cursor-pointer z-10"
                  />
                  <div className={`border-2 border-dashed rounded-3xl p-12 transition-all flex flex-col items-center gap-4 ${file ? 'border-primary bg-blue-50/30' : 'border-slate-200 group-hover:border-primary/40 group-hover:bg-slate-50/50'}`}>
                     <FileText size={32} className={file ? 'text-primary' : 'text-slate-300'} />
                     <span className={`font-bold ${file ? 'text-primary' : 'text-slate-500'}`}>
                        {file ? file.name : 'Select a PDF chapter (max 20MB)'}
                     </span>
                  </div>
                </div>

                {error && (
                  <div className="flex items-center gap-3 p-4 bg-red-50 text-red-600 rounded-2xl border border-red-100 text-sm font-bold animate-in fade-in zoom-in duration-300">
                    <AlertCircle size={20} />
                    {error}
                  </div>
                )}

                <button
                  disabled={!file || loading}
                  className="w-full bg-primary text-white py-5 rounded-2xl font-black text-lg shadow-xl shadow-blue-100 hover:bg-blue-700 transition-all disabled:opacity-50 active:scale-[0.98] flex items-center justify-center gap-3"
                >
                  {loading ? (
                    <>
                      <Loader2 className="animate-spin" size={24} />
                      Processing Chapter...
                    </>
                  ) : (
                    'Enrich with Gurukul AI'
                  )}
                </button>
             </form>
          </section>

          {status && (
            <section className="bg-white border border-border rounded-3xl p-10 shadow-sm animate-in slide-in-from-bottom-4 duration-500">
               <div className="flex items-center justify-between mb-10">
                  <h3 className="text-xl font-black text-slate-800">Job Progress</h3>
                  <span className={`px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest ${status.status === 'COMPLETED' ? 'bg-emerald-100 text-emerald-600' : 'bg-blue-100 text-primary'}`}>
                    {status.status}
                  </span>
               </div>

               <div className="space-y-8">
                  <div className="h-4 bg-slate-100 rounded-full overflow-hidden">
                     <div
                        className="h-full bg-primary transition-all duration-1000 ease-out"
                        style={{ width: `${status.progress * 100}%` }}
                     ></div>
                  </div>

                  <div className="flex items-center gap-4 p-5 bg-slate-50 rounded-2xl border border-slate-100 font-bold text-slate-600 text-sm">
                     {status.status === 'COMPLETED' ? (
                       <CheckCircle2 size={20} className="text-emerald-500" />
                     ) : (
                       <Loader2 size={20} className="animate-spin text-primary" />
                     )}
                     Current Stage: <span className="text-primary">{status.current_stage || 'Initializing'}</span>
                  </div>

                  {status.status === 'COMPLETED' && (
                    <button className="w-full py-4 bg-slate-900 text-white rounded-2xl font-black hover:bg-black transition-all">
                       Open Generated Lesson
                    </button>
                  )}
               </div>
            </section>
          )}
        </div>
      </main>
    </div>
  );
}
