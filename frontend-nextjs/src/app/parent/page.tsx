'use client';

import React from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { Heart, Trophy, BarChart3, Clock, ChevronRight, BellRing } from 'lucide-react';

export default function ParentDashboard() {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="Parent Portal" />

        <div className="max-w-7xl mx-auto p-10 space-y-10">

           {/* Child Summary Hero */}
           <section className="bg-white border border-border rounded-[48px] p-12 shadow-sm flex flex-col md:flex-row items-center gap-12">
              <div className="w-32 h-32 bg-blue-50 rounded-full flex items-center justify-center border-4 border-white shadow-xl ring-4 ring-blue-100">
                 <img src="https://api.dicebear.com/7.x/avataaars/svg?seed=Scholar" alt="Child" className="w-24 h-24" />
              </div>
              <div className="flex-1 space-y-4 text-center md:text-left">
                 <div className="inline-flex items-center gap-2 px-3 py-1 bg-blue-50 text-blue-600 rounded-full text-[10px] font-black uppercase tracking-widest">
                    Class 5 Scholar
                 </div>
                 <h2 className="text-4xl font-black text-slate-800 tracking-tight leading-none">Arjun&apos;s Learning Journey</h2>
                 <p className="text-slate-500 font-medium max-w-md">Arjun has mastered 3 new concepts today! His strongest subject is <span className="text-primary font-bold">Mathematics</span>.</p>
              </div>
              <div className="flex gap-4">
                 <button className="p-4 bg-slate-50 text-slate-400 rounded-3xl hover:text-primary transition-all border border-border"><BellRing size={24} /></button>
                 <button className="px-8 py-4 bg-primary text-white rounded-3xl font-black text-sm uppercase tracking-widest hover:bg-blue-600 transition-all shadow-xl shadow-blue-100">Encourage Arjun</button>
              </div>
           </section>

           <div className="grid grid-cols-1 lg:grid-cols-3 gap-10">
              <div className="lg:col-span-2 space-y-8">
                 <h3 className="text-xs font-black text-slate-400 uppercase tracking-[0.2em] px-4">Performance Insights</h3>
                 <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <InsightCard icon={Trophy} label="Weekly Goal" value="85%" desc="Completed 12/14 modules" color="amber" />
                    <InsightCard icon={Clock} label="Focus Time" value="1.2h" desc="20% more than last week" color="blue" />
                    <InsightCard icon={BarChart3} label="Quiz Accuracy" value="92%" desc="Excellent understanding" color="emerald" />
                    <InsightCard icon={Heart} label="Learning Streak" value="5 Days" desc="Keep the momentum!" color="rose" />
                 </div>
              </div>

              <div className="bg-white border border-border rounded-[40px] p-8 shadow-sm">
                 <h3 className="text-lg font-black text-slate-800 mb-8 uppercase tracking-tight">Active Chapters</h3>
                 <div className="space-y-6">
                    <ChapterProgress name="Large Numbers" subject="Math" progress={65} />
                    <ChapterProgress name="Super Senses" subject="EVS" progress={88} />
                    <ChapterProgress name="The Fish Tale" subject="Math" progress={40} />
                 </div>
                 <button className="w-full mt-10 py-4 bg-slate-900 text-white rounded-2xl font-bold text-sm hover:bg-black transition-all">View All Results</button>
              </div>
           </div>

        </div>
      </main>
    </div>
  );
}

function InsightCard({ icon: Icon, label, value, desc, color }: any) {
   const colors: any = {
      amber: "bg-amber-50 text-amber-600",
      blue: "bg-blue-50 text-blue-600",
      emerald: "bg-emerald-50 text-emerald-600",
      rose: "bg-rose-50 text-rose-600",
   };
   return (
      <div className="bg-white border border-border rounded-[32px] p-8 hover:border-primary/20 transition-all shadow-sm group">
         <div className={`w-12 h-12 rounded-2xl flex items-center justify-center mb-6 group-hover:scale-110 transition-transform ${colors[color]}`}>
            <Icon size={24} />
         </div>
         <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest mb-1">{label}</p>
         <h4 className="text-2xl font-black text-slate-800">{value}</h4>
         <p className="text-slate-400 text-[10px] font-medium mt-2">{desc}</p>
      </div>
   );
}

function ChapterProgress({ name, subject, progress }: any) {
   return (
      <div className="space-y-3">
         <div className="flex justify-between items-end">
            <div>
               <h5 className="text-sm font-bold text-slate-800 leading-none">{name}</h5>
               <p className="text-[10px] font-black text-slate-400 uppercase mt-1">{subject}</p>
            </div>
            <span className="text-xs font-black text-primary">{progress}%</span>
         </div>
         <div className="h-2 bg-slate-50 rounded-full overflow-hidden border border-slate-100">
            <div className="h-full bg-primary" style={{ width: `${progress}%` }}></div>
         </div>
      </div>
   );
}
