'use client';

import React from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import Breadcrumbs from '@/components/Breadcrumbs';
import { OFFICIAL_PORTALS, QUESTION_PAPER_REPOSITORIES } from '@/data/externalResources';
import {
  ExternalLink,
  Book,
  Video,
  Mic2,
  Gamepad2,
  GraduationCap,
  FileText,
  ShieldCheck,
  Search,
  ArrowRight,
  Sparkles,
  Download,
  FileQuestion
} from 'lucide-react';
import Link from 'next/link';

export default function ResourcesPage() {
  const [activeTab, setActiveTab] = React.useState('Official Portals');

  const categories = [
    { label: 'Textbooks', icon: Book },
    { label: 'Videos', icon: Video },
    { label: 'Audio', icon: Mic2 },
    { label: 'Interactive', icon: Gamepad2 },
    { label: 'Courses', icon: GraduationCap },
    { label: 'Curriculum', icon: FileText },
  ];

  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto pb-20">
        <TopBar title="Official Educational Resources" />

        <div className="max-w-7xl mx-auto p-10">
           <Breadcrumbs items={[{ label: 'Resources', href: '#' }]} />

           <div className="space-y-12">
              {/* Premium Resource Hero */}
              <section className="bg-slate-900 rounded-[64px] p-16 text-white relative overflow-hidden flex flex-col md:flex-row items-center gap-16 shadow-2xl">
                 <div className="relative z-10 flex-1 space-y-8">
                    <div className="inline-flex items-center gap-2 px-4 py-1.5 bg-blue-500/20 text-blue-400 rounded-full border border-blue-500/20 text-[10px] font-black uppercase tracking-[0.2em]">
                       <ShieldCheck size={14} /> Authoritative Learning Hub
                    </div>
                    <h2 className="text-5xl lg:text-6xl font-black tracking-tighter leading-[1.1]">
                       Verified<br />National Content
                    </h2>
                    <p className="text-slate-400 font-medium max-w-xl text-xl leading-relaxed">
                       Access 10,000+ official learning resources from NCERT, DIKSHA, and the Ministry of Education,
                       seamlessly integrated into your Gurukul AI journey.
                    </p>
                    <div className="flex flex-wrap gap-4 pt-4">
                       <button className="px-10 py-5 bg-primary text-white rounded-[32px] font-black text-sm uppercase tracking-widest hover:bg-blue-600 transition-all shadow-xl shadow-blue-500/20 flex items-center gap-3">
                          Browse DIKSHA <ArrowRight size={18} />
                       </button>
                       <button className="px-10 py-5 bg-white/5 border border-white/10 rounded-[32px] font-black text-sm uppercase tracking-widest hover:bg-white/10 transition-all">
                          NCERT Catalog
                       </button>
                    </div>
                 </div>
                 <div className="relative z-10 w-full md:w-[400px] aspect-square bg-blue-600/10 rounded-[48px] border border-white/5 flex items-center justify-center p-12 group overflow-hidden">
                    <img
                      src="https://api.dicebear.com/7.x/shapes/svg?seed=resource&backgroundColor=0ea5e9"
                      alt="Resource Hub"
                      className="w-full h-full opacity-60 group-hover:scale-110 transition-transform duration-700"
                    />
                    <Sparkles className="absolute bottom-10 right-10 text-blue-400 animate-pulse" size={48} />
                 </div>
                 <div className="absolute -left-20 -bottom-20 w-96 h-96 bg-primary/20 rounded-full blur-[120px]"></div>
              </section>

              {/* Resource Tabs */}
              <div className="flex items-center justify-between border-b border-slate-200">
                 <div className="flex gap-10">
                    {['Official Portals', 'Question Papers', 'Imported Content', 'Subject Resources'].map((tab) => (
                       <button
                         key={tab}
                         onClick={() => setActiveTab(tab)}
                         className={`pb-6 text-xs font-black uppercase tracking-[0.2em] transition-all relative ${activeTab === tab ? 'text-primary' : 'text-slate-400 hover:text-slate-600'}`}
                       >
                          {tab}
                          {activeTab === tab && <div className="absolute bottom-0 left-0 right-0 h-1 bg-primary rounded-full" />}
                       </button>
                    ))}
                 </div>
                 <div className="relative hidden md:block">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-300" size={16} />
                    <input type="text" placeholder="Search external index..." className="pl-10 pr-6 py-2 bg-white border border-border rounded-2xl text-xs font-bold focus:outline-none focus:ring-2 focus:ring-primary/20 w-64 shadow-sm" />
                 </div>
              </div>

              {activeTab === 'Official Portals' && (
                 <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {OFFICIAL_PORTALS.map((portal) => (
                       <ResourceCard key={portal.id} portal={portal} />
                    ))}
                 </div>
              )}

              {activeTab === 'Question Papers' && (
                 <div className="space-y-10">
                    <div className="p-8 bg-blue-50 border border-blue-100 rounded-3xl flex gap-6 items-center">
                       <div className="w-12 h-12 bg-primary rounded-2xl flex items-center justify-center text-white shrink-0">
                          <FileQuestion size={24} />
                       </div>
                       <div>
                          <h4 className="font-black text-slate-800 uppercase tracking-tight">External Question Paper Resources</h4>
                          <p className="text-slate-600 text-sm font-medium mt-1">
                             Gurukul does not download, store, or host these question papers. The resources are provided by external repositories.
                             Click &quot;Visit Repository&quot; to access them directly from the original source.
                          </p>
                       </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                       {QUESTION_PAPER_REPOSITORIES.map((repo) => (
                          <div key={repo.id} className="bg-white border border-border rounded-[32px] p-8 hover:shadow-2xl hover:shadow-slate-200 transition-all group flex flex-col h-full relative">
                             <div className="flex items-start justify-between mb-8">
                                <div className="w-14 h-14 bg-slate-50 rounded-2xl flex items-center justify-center text-slate-400 group-hover:bg-primary/10 group-hover:text-primary transition-all">
                                   <FileQuestion size={28} />
                                </div>
                                <span className="text-[9px] font-black text-slate-300 uppercase tracking-[0.2em]">{repo.organization}</span>
                             </div>

                             <h4 className="text-xl font-black text-slate-800 mb-2 leading-tight">{repo.title}</h4>
                             <p className="text-[10px] font-black text-primary uppercase tracking-widest mb-4">{repo.classLevel}</p>
                             <p className="text-sm text-slate-500 font-medium mb-8 flex-1 leading-relaxed line-clamp-2">{repo.description}</p>

                             <div className="flex items-center justify-between pt-6 border-t border-slate-50">
                                <span className="text-[9px] font-black uppercase tracking-widest text-emerald-600 bg-emerald-50 px-3 py-1 rounded-md border border-emerald-100">FREE ACCESS</span>
                                <a
                                  href={repo.url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="flex items-center gap-2 text-primary font-black text-[10px] uppercase tracking-widest hover:underline"
                                >
                                   VISIT REPOSITORY <ExternalLink size={14} />
                                </a>
                             </div>
                          </div>
                       ))}
                    </div>
                 </div>
              )}

              {activeTab === 'Imported Content' && (
                 <div className="py-20 text-center space-y-6">
                    <div className="w-20 h-20 bg-emerald-50 text-emerald-500 rounded-3xl flex items-center justify-center mx-auto shadow-xl shadow-emerald-100">
                       <ShieldCheck size={40} />
                    </div>
                    <h3 className="text-2xl font-black text-slate-800">Licensed Repository</h3>
                    <p className="text-slate-500 max-w-md mx-auto font-medium mb-10">
                       These resources have been legally imported into Gurukul for offline access and AI Tutor context.
                    </p>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 text-left">
                        <ImportedTile title="Knowing Our Numbers" type="Video" source="DIKSHA" license="CC BY 4.0" />
                        <ImportedTile title="Mathematics Class 6 Exemplar" type="PDF" source="NCERT" license="Official" />
                    </div>
                 </div>
              )}
           </div>
        </div>
      </main>
    </div>
  );
}

function ResourceCard({ portal }: { portal: any }) {
   return (
      <a
        href={portal.url}
        target="_blank"
        rel="noopener noreferrer"
        className="bg-white border border-border rounded-[32px] p-8 hover:shadow-2xl hover:shadow-slate-200 transition-all group flex flex-col h-full relative"
      >
         <div className="flex items-start justify-between mb-8">
            <div className="w-14 h-14 bg-slate-50 rounded-2xl flex items-center justify-center text-slate-400 group-hover:bg-primary/10 group-hover:text-primary transition-all">
               <ExternalLink size={28} />
            </div>
            <span className="text-[9px] font-black text-slate-300 uppercase tracking-[0.2em]">{portal.organization}</span>
         </div>

         <h4 className="text-xl font-black text-slate-800 mb-4 leading-tight">{portal.title}</h4>
         <p className="text-sm text-slate-500 font-medium mb-8 flex-1 leading-relaxed line-clamp-2">{portal.description}</p>

         <div className="flex items-center justify-between pt-6 border-t border-slate-50">
            <span className="text-[9px] font-black uppercase tracking-widest text-primary bg-blue-50 px-3 py-1 rounded-md border border-blue-100">{portal.category}</span>
            <div className="flex items-center gap-2 text-primary font-black text-[10px] uppercase tracking-widest">
               GO TO SOURCE <ExternalLink size={14} />
            </div>
         </div>
      </a>
   );
}

function ImportedTile({ title, type, source, license }: any) {
   return (
      <div className="p-6 bg-white border border-border rounded-3xl hover:border-primary/30 transition-all group flex items-center justify-between shadow-sm">
         <div className="flex items-center gap-5">
            <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center">
               <Download size={24} />
            </div>
            <div>
               <h5 className="text-sm font-bold text-slate-800 leading-tight">{title}</h5>
               <p className="text-[9px] font-black text-slate-400 uppercase mt-1 tracking-widest">{source} • {license}</p>
            </div>
         </div>
         <span className="px-3 py-1 bg-emerald-100 text-emerald-700 text-[9px] font-black uppercase tracking-tighter rounded-md">IMPORTED</span>
      </div>
   );
}
