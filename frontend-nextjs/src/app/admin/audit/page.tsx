'use client';

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Layout } from '@/presentation/components/common/Layout';
import { ShieldAlert, CheckCircle, AlertTriangle, ChevronRight, Search } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000/api/v1/system';

export default function AdminAuditPage() {
  const [summary, setSummary] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get(`${API_BASE}/audits`).then(res => {
      setSummary(res.data);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  if (loading) return <Layout><div className="p-20 text-center font-black animate-pulse">Loading System Audits...</div></Layout>;
  if (!summary) return <Layout><div className="p-20 text-center text-red-600 font-black">Audit Data Not Available</div></Layout>;

  return (
    <Layout>
      <div className="max-w-7xl mx-auto px-6 py-12 space-y-12">
        <header className="flex items-center justify-between border-b-4 border-slate-900 pb-6">
           <h1 className="text-5xl font-black italic uppercase tracking-tighter text-slate-900">System <span className="text-blue-600">QA Audit</span></h1>
           <div className="bg-slate-900 text-white px-6 py-2 rounded-full font-black text-xs uppercase tracking-widest flex items-center gap-2">
              <ShieldAlert size={14} className="text-red-400" /> Admin Access Only
           </div>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
           {Object.entries(summary.classes).map(([className, data]: [string, any]) => (
              <div key={className} className="bg-white border-4 border-slate-100 rounded-[40px] p-8 space-y-6 hover:shadow-2xl transition-all">
                 <div className="flex items-center justify-between">
                    <h2 className="text-3xl font-black uppercase italic tracking-tighter">{className}</h2>
                    <CheckCircle className="text-emerald-500" />
                 </div>

                 <div className="grid grid-cols-2 gap-4">
                    <div className="bg-slate-50 p-4 rounded-2xl">
                       <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Processed</p>
                       <p className="text-2xl font-black text-slate-900">{data.totals.processed}</p>
                    </div>
                    <div className="bg-slate-50 p-4 rounded-2xl">
                       <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Subjects</p>
                       <p className="text-2xl font-black text-slate-900">{Object.keys(data.subjects).length}</p>
                    </div>
                 </div>

                 <div className="space-y-3">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Subject Integrity:</p>
                    {Object.entries(data.subjects).map(([subj, sdata]: [string, any]) => (
                       <div key={subj} className="flex items-center justify-between text-xs font-bold border-b border-slate-50 pb-2">
                          <span className="text-slate-700">{subj}</span>
                          <span className="bg-blue-50 text-blue-600 px-2 py-0.5 rounded uppercase">{Object.keys(sdata.chapters).length} Chapters</span>
                       </div>
                    ))}
                 </div>
              </div>
           ))}
        </div>
      </div>
    </Layout>
  );
}
