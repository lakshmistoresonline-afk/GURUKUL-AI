'use client';

import React, { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import api, { chapterService, resourceService, mediaService } from '@/services/api';
import {
  Database,
  Cpu,
  Users,
  Settings,
  RefreshCw,
  Server,
  Terminal,
  ShieldCheck,
  AlertTriangle,
  Globe,
  Play,
  ExternalLink,
  CheckCircle2,
  XCircle,
  Eye
} from 'lucide-react';

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>({
    activeJobs: 2,
    totalChapters: 0,
    systemHealth: 'Optimal',
    cpuUsage: '12%',
    activeUsers: 42
  });

  const [externalStats, setExternalStats] = useState<any>(null);
  const [pendingResources, setPendingResources] = useState<any[]>([]);
  const [activeAdminTab, setActiveAdminTab] = useState<'system' | 'multimedia'>('system');

  const [collectionId, setCollectionId] = useState('do_31310347505669734411282');
  const [providerId, setProviderId] = useState('DIKSHA');
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [integrityReport, setIntegrityReport] = useState<any>(null);
  const [collectionJobs, setCollectionJobs] = useState<any[]>([]);

  const handleRetryRAG = async (id: string) => {
    try {
      // Assuming 'api' is available or use resourceService
      // await api.post(`/api/resources/retry-rag/${id}`);
      if (analysisResult) {
        const updated = analysisResult.ingested_resources.map((r: any) =>
          r.id === id ? { ...r, rag_status: 'INDEXING' } : r
        );
        setAnalysisResult({ ...analysisResult, ingested_resources: updated });
      }
    } catch (e) {
      console.error(e);
    }
  };

  const runAnalysis = async () => {
    setLoading(true);
    try {
      const res = await resourceService.analyzeCollection(providerId, collectionId);
      setAnalysisResult(res);
      fetchJobs(); // Refresh job list
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchJobs = async () => {
    try {
      const response = await resourceService.getCollections();
      setCollectionJobs(response.data || []);
    } catch (e) {
      console.error(e);
    }
  };

  const checkIntegrity = async () => {
    setLoading(true);
    try {
      const res = await resourceService.runIntegrityCheck();
      setIntegrityReport(res);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const fetchExternalData = async () => {
    try {
      const [s, p] = await Promise.all([
        mediaService.getExternalStats(),
        mediaService.getAdminPending({})
      ]);
      setExternalStats(s);
      setPendingResources(p);
    } catch (e) {
      console.error(e);
    }
  };

  const handleVerify = async (id: string) => {
    try {
      await mediaService.verifyExternal(id);
      fetchExternalData();
    } catch (e) {
      console.error(e);
    }
  };

  const handleReject = async (id: string) => {
    try {
      await mediaService.rejectExternal(id);
      fetchExternalData();
    } catch (e) {
      console.error(e);
    }
  };

  const fetchCount = async () => {
    try {
      const h = await chapterService.getHierarchy();
      let count = 0;
      Object.values(h).forEach((subjects: any) => {
        Object.values(subjects).forEach((chapters: any) => {
          count += chapters.length;
        });
      });
      setStats((prev: any) => ({ ...prev, totalChapters: count }));
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => {
    fetchCount();
    fetchJobs();
    fetchExternalData();
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-900 text-slate-300">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-20">
        <header className="h-16 bg-slate-800 border-b border-slate-700 flex items-center justify-between px-8 sticky top-0 z-10">
          <div className="flex items-center gap-8">
            <h1 className="text-sm font-black text-white uppercase tracking-widest flex items-center gap-3">
              <ShieldCheck className="text-emerald-500" size={18} /> Gurukul System Audit
            </h1>
            <div className="flex p-1 bg-slate-900 rounded-xl">
               <button
                onClick={() => setActiveAdminTab('system')}
                className={`px-4 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${activeAdminTab === 'system' ? 'bg-slate-700 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
               >
                 Core System
               </button>
               <button
                onClick={() => setActiveAdminTab('multimedia')}
                className={`px-4 py-1.5 rounded-lg text-[10px] font-black uppercase tracking-widest transition-all ${activeAdminTab === 'multimedia' ? 'bg-slate-700 text-white shadow-lg' : 'text-slate-500 hover:text-slate-300'}`}
               >
                 Multimedia Lab
               </button>
            </div>
          </div>
          <div className="flex items-center gap-4">
            <span className="px-3 py-1 bg-slate-700 rounded-full text-[10px] font-black uppercase text-emerald-400">Live</span>
            <button className="p-2 hover:bg-slate-700 rounded-lg text-slate-400"><Settings size={18} /></button>
          </div>
        </header>

        <div className="max-w-7xl mx-auto p-10 space-y-10">
          {activeAdminTab === 'system' ? (
            <>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                <AdminStat icon={Database} label="Indexed Chapters" value={stats.totalChapters} color="blue" />
                <AdminStat icon={Cpu} label="System Load" value={stats.cpuUsage} color="emerald" />
                <AdminStat icon={Users} label="Active Scholars" value={stats.activeUsers} color="purple" />
                <AdminStat icon={Server} label="Backend Status" value={stats.systemHealth} color="orange" />
              </div>

              <div className="flex items-center gap-4">
                <button
                  onClick={checkIntegrity}
                  className="px-6 py-3 bg-slate-800 border border-slate-700 rounded-2xl text-xs font-black uppercase tracking-widest text-slate-400 hover:text-white transition-all flex items-center gap-3"
                >
                  <ShieldCheck size={16} /> Run Integrity Audit
                </button>
                {integrityReport && (
                  <div className="flex gap-6 px-6 py-3 bg-slate-800/50 rounded-2xl border border-slate-700 text-[10px] font-black uppercase tracking-tighter">
                    <span className="text-emerald-500">Healthy: {integrityReport.healthy}</span>
                    <span className="text-red-500">Missing: {integrityReport.missing}</span>
                    <span className="text-amber-500">Mismatch: {integrityReport.mismatch}</span>
                  </div>
                )}
              </div>

              {/* Authoritative Resource Analyzer */}
              <section className="bg-slate-800 rounded-[40px] border border-slate-700 p-10 space-y-8">
                <div className="flex items-center justify-between">
                  <div>
                    <h2 className="text-xl font-black text-white flex items-center gap-3"><Globe size={24} className="text-blue-500" /> Resource Ingestion Pipeline</h2>
                    <p className="text-slate-500 text-xs font-bold uppercase tracking-widest mt-1">Discover and verify authoritative external collections</p>
                  </div>
                  <button
                    onClick={runAnalysis}
                    disabled={loading}
                    className="px-8 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-2xl font-black text-xs uppercase tracking-[0.2em] transition-all flex items-center gap-3"
                  >
                    {loading ? <RefreshCw className="animate-spin" size={16} /> : <Play size={16} fill="currentColor" />}
                    {loading ? 'Analyzing...' : 'Run Discovery'}
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-2">
                    <label className="text-[10px] font-black uppercase text-slate-500 px-4">Provider</label>
                    <select
                      value={providerId}
                      onChange={(e) => setProviderId(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-6 py-4 text-sm font-bold text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                    >
                      <option value="DIKSHA">DIKSHA (Sunbird)</option>
                      <option value="NCERT">NCERT e-Resources</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-[10px] font-black uppercase text-slate-500 px-4">Collection ID</label>
                    <input
                      type="text"
                      value={collectionId}
                      onChange={(e) => setCollectionId(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-2xl px-6 py-4 text-sm font-bold text-white focus:outline-none focus:ring-2 focus:ring-blue-500/20"
                      placeholder="e.g. do_313..."
                    />
                  </div>
                </div>

                {analysisResult && (
                  <div className="bg-slate-900/50 rounded-3xl p-8 border border-slate-700/50 animate-in fade-in slide-in-from-top-4 duration-500">
                    <div className="flex items-start justify-between mb-8">
                      <div>
                        <h3 className="text-2xl font-black text-white">{analysisResult.title}</h3>
                        <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px] mt-2">{analysisResult.publisher} • {analysisResult.stats?.discovered} Resources Discovered</p>
                      </div>
                      <span className="px-4 py-1.5 bg-emerald-500/10 text-emerald-400 rounded-full text-[10px] font-black uppercase tracking-widest border border-emerald-500/20">Analysis Complete</span>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
                      <MiniStat label="Import Allowed" value={analysisResult.stats?.eligible} color="emerald" />
                      <MiniStat label="Imported" value={analysisResult.stats?.imported} color="blue" />
                      <MiniStat label="Review Required" value={analysisResult.stats?.review} color="amber" />
                      <MiniStat label="Link Only" value={analysisResult.stats?.link_only} color="slate" />
                    </div>

                    <div className="grid grid-cols-1 gap-3">
                      {analysisResult.ingested_resources?.map((res: any) => (
                        <div key={res.id} className="p-4 bg-slate-800 rounded-xl flex items-center justify-between border border-slate-700 hover:border-slate-500 transition-all">
                          <div className="flex items-center gap-6">
                            <div className="w-10 h-10 bg-slate-700 rounded-xl flex items-center justify-center text-slate-400 font-black text-[10px]">
                              {res.type.slice(0, 3).toUpperCase()}
                            </div>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-3">
                                <p className="text-xs font-bold text-white truncate max-w-[200px]">{res.title}</p>
                                {res.license_verified && (
                                  <span className="text-[8px] bg-emerald-500/10 text-emerald-500 px-1.5 py-0.5 rounded uppercase font-black">Verified</span>
                                )}
                                <span className="text-[8px] text-slate-500 font-bold">PID: {res.collection_id?.slice(0, 8)}</span>
                              </div>
                              <p className="text-[9px] text-slate-500 font-black uppercase mt-1">
                                ID: {res.original_resource_id} → {res.resolved_resource_id?.slice(0, 10)}... • {res.reuse_decision} • {res.import_status} • {res.rag_status}
                              </p>
                              {res.rag_status === 'FAILED' && (
                                <p className="text-[8px] text-red-400 font-bold mt-1">Error: {res.rag_error_message}</p>
                              )}
                              {res.content_hash && (
                                <p className="text-[8px] text-slate-600 font-mono mt-0.5 truncate max-w-[400px]">Hash: {res.content_hash}</p>
                              )}
                            </div>
                          </div>
                          <div className="flex items-center gap-4">
                            {res.import_status === 'IMPORTED' && (
                              <button
                                onClick={() => handleRetryRAG(res.id)}
                                className="p-2 hover:bg-slate-700 rounded-lg text-slate-500 hover:text-white transition-colors"
                                title="Retry RAG Indexing"
                              >
                                <RefreshCw size={14} className={res.rag_status === 'INDEXING' ? 'animate-spin' : ''} />
                              </button>
                            )}
                            {res.import_status === 'IMPORTED' && <ShieldCheck size={14} className="text-emerald-500" />}
                            <a href={res.url} target="_blank" rel="noopener" className="p-2 hover:bg-slate-700 rounded-lg text-blue-400 transition-colors"><ExternalLink size={14} /></a>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </section>

              <div className="grid grid-cols-1 lg:grid-cols-2 gap-10">
                <div className="bg-slate-800 rounded-3xl border border-slate-700 p-8">
                  <div className="flex items-center justify-between mb-10">
                    <h3 className="text-lg font-black text-white flex items-center gap-3"><Terminal size={20} className="text-slate-500" /> Collection Ingestion Jobs</h3>
                    <button onClick={fetchJobs} className="p-2 hover:bg-slate-700 rounded-lg text-slate-400">
                      <RefreshCw size={16} />
                    </button>
                  </div>
                  <div className="space-y-4">
                    {collectionJobs.length > 0 ? collectionJobs.map(job => (
                      <div key={job.id} className="p-5 bg-slate-900/50 rounded-2xl border border-slate-700/50">
                        <div className="flex justify-between items-start mb-4">
                          <div>
                            <p className="text-white font-bold text-sm">{job.title}</p>
                            <p className="text-[10px] text-slate-500 font-black uppercase mt-1">{job.external_id}</p>
                          </div>
                          <span className={`px-2 py-0.5 rounded text-[8px] font-black uppercase ${job.status === 'COMPLETED' ? 'bg-emerald-500/10 text-emerald-500' : 'bg-blue-500/10 text-blue-500'}`}>{job.status}</span>
                        </div>
                        {job.stats && (
                          <div className="flex gap-4 text-[9px] font-black text-slate-400 uppercase">
                            <span>Disc: {job.stats.discovered}</span>
                            <span>Imp: {job.stats.imported}</span>
                            <span>Fail: {job.stats.failed}</span>
                          </div>
                        )}
                      </div>
                    )) : (
                      <p className="text-xs text-slate-600 italic">No collection jobs recorded.</p>
                    )}
                  </div>
                </div>

                <div className="bg-slate-800 rounded-3xl border border-slate-700 p-8">
                  <h3 className="text-lg font-black text-white mb-8">Incident Report</h3>
                  <div className="space-y-4">
                    <div className="p-5 bg-red-950/30 rounded-2xl border border-red-900/50 flex gap-4">
                      <AlertTriangle className="text-red-500 shrink-0" size={20} />
                      <div>
                        <p className="text-red-200 font-bold text-sm">Ollama Latency High</p>
                        <p className="text-red-900 text-xs mt-1">Provider &apos;Gemini&apos; triggered circuit breaker at 18:20.</p>
                      </div>
                    </div>
                    <div className="p-5 bg-amber-950/30 rounded-2xl border border-amber-900/50 flex gap-4 opacity-50">
                      <AlertTriangle className="text-amber-500 shrink-0" size={20} />
                      <div>
                        <p className="text-amber-200 font-bold text-sm">Quota Alert</p>
                        <p className="text-amber-900 text-xs mt-1">OpenRouter at 85% of daily limits.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </>
          ) : (
            <div className="space-y-10">
               {/* Multimedia External Verification View */}
               <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  <AdminStat icon={Globe} label="Total Resources" value={externalStats?.total_resources || 0} color="blue" />
                  <AdminStat icon={ShieldCheck} label="Verified" value={externalStats?.verified || 0} color="emerald" />
                  <AdminStat icon={RefreshCw} label="Pending" value={externalStats?.pending || 0} color="amber" />
                  <AdminStat icon={XCircle} label="Rejected" value={externalStats?.rejected || 0} color="rose" />
               </div>

               <div className="bg-slate-800 rounded-[40px] border border-slate-700 p-10 space-y-10">
                  <div className="flex items-center justify-between">
                     <div>
                        <h2 className="text-2xl font-black text-white">External Multimedia Verification</h2>
                        <p className="text-slate-500 text-sm font-bold uppercase tracking-widest mt-1">Review and approve supplementary learning nodes</p>
                     </div>
                     <button
                        onClick={() => mediaService.reloadExternalCatalogs().then(() => fetchExternalData())}
                        className="px-6 py-3 bg-slate-700 hover:bg-slate-600 text-white rounded-2xl font-black text-[10px] uppercase tracking-widest transition-all flex items-center gap-2"
                     >
                        <RefreshCw size={14} /> Reload Catalogs
                     </button>
                  </div>

                  <div className="space-y-6">
                     <h3 className="text-xs font-black text-slate-500 uppercase tracking-[0.2em] px-4">Pending Approval ({pendingResources.length})</h3>
                     <div className="grid grid-cols-1 gap-4">
                        {pendingResources.map((res) => (
                           <div key={res.id} className="p-8 bg-slate-900/50 border border-slate-700/50 rounded-3xl flex items-center justify-between group hover:border-blue-500/30 transition-all">
                              <div className="flex items-center gap-8 flex-1">
                                 <div className="w-16 h-16 bg-slate-800 rounded-2xl flex items-center justify-center text-slate-500 group-hover:text-blue-400 transition-colors shadow-inner border border-slate-700">
                                    <Globe size={32} />
                                 </div>
                                 <div className="space-y-2 flex-1">
                                    <div className="flex items-center gap-3">
                                       <span className="text-[10px] font-black text-blue-400 uppercase tracking-widest bg-blue-400/10 px-2 py-0.5 rounded">{res.provider}</span>
                                       <span className="text-[10px] font-black text-slate-500 uppercase tracking-widest">{res.class_name?.replace('_', ' ')} • {res.subject}</span>
                                    </div>
                                    <h4 className="text-lg font-bold text-white leading-tight">{res.title}</h4>
                                    <p className="text-[10px] font-black text-slate-600 uppercase tracking-tighter">Chapter: {res.chapter_id} • Type: {res.resource_types?.join(', ')}</p>
                                 </div>
                              </div>

                              <div className="flex items-center gap-3 ml-12">
                                 <a
                                    href={res.url}
                                    target="_blank"
                                    rel="noopener"
                                    className="p-4 bg-slate-800 hover:bg-slate-700 text-blue-400 rounded-2xl transition-all"
                                    title="View Resource"
                                 >
                                    <Eye size={20} />
                                 </a>
                                 <button
                                    onClick={() => handleReject(res.id)}
                                    className="p-4 bg-slate-800 hover:bg-rose-500/20 text-slate-500 hover:text-rose-500 rounded-2xl transition-all"
                                    title="Reject"
                                 >
                                    <XCircle size={20} />
                                 </button>
                                 <button
                                    onClick={() => handleVerify(res.id)}
                                    className="p-4 bg-slate-800 hover:bg-emerald-500/20 text-slate-500 hover:text-emerald-500 rounded-2xl transition-all"
                                    title="Verify"
                                 >
                                    <CheckCircle2 size={20} />
                                 </button>
                              </div>
                           </div>
                        ))}
                        {pendingResources.length === 0 && (
                           <div className="py-20 text-center bg-slate-900/30 rounded-3xl border border-dashed border-slate-700">
                              <ShieldCheck size={48} className="mx-auto text-slate-800 mb-4" />
                              <p className="text-slate-600 font-bold uppercase tracking-widest text-xs">All external nodes verified</p>
                           </div>
                        )}
                     </div>
                  </div>
               </div>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

function AdminStat({ icon: Icon, label, value, color }: any) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-3xl p-8 shadow-2xl">
      <div className="flex items-center justify-between mb-4">
        <p className="text-slate-500 text-[10px] font-black uppercase tracking-widest">{label}</p>
        <Icon size={20} className="text-slate-600" />
      </div>
      <h4 className="text-4xl font-black text-white">{value}</h4>
    </div>
  );
}

function MiniStat({ label, value, color }: any) {
  const colors: any = {
    emerald: "text-emerald-400 bg-emerald-500/10",
    blue: "text-blue-400 bg-blue-500/10",
    amber: "text-amber-400 bg-amber-500/10",
    slate: "text-slate-400 bg-slate-500/10",
  };
  return (
    <div className={`p-4 rounded-2xl border border-white/5 ${colors[color]}`}>
      <p className="text-[8px] font-black uppercase tracking-widest opacity-60 mb-1">{label}</p>
      <p className="text-xl font-black">{value}</p>
    </div>
  );
}
