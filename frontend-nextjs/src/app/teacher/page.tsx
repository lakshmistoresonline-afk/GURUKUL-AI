'use client';

import React from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { Users, BookCheck, BarChart3, Clock, ChevronRight } from 'lucide-react';

export default function TeacherDashboard() {
  return (
    <div className="flex min-h-screen bg-slate-50">
      <Sidebar />
      <main className="flex-1 overflow-y-auto">
        <TopBar title="Teacher Console" />

        <div className="max-w-7xl mx-auto p-10 space-y-10">

           <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <StatCard icon={Users} label="Total Students" value="42" color="blue" />
              <StatCard icon={BookCheck} label="Active Assignments" value="8" color="emerald" />
              <StatCard icon={Clock} label="Avg. Study Time" value="4.2h" color="orange" />
              <StatCard icon={BarChart3} label="Class Mastery" value="72%" color="purple" />
           </div>

           <div className="grid grid-cols-1 xl:grid-cols-3 gap-10">
              <div className="xl:col-span-2 bg-white rounded-[40px] border border-border p-8 shadow-sm">
                 <h3 className="text-xl font-black text-slate-800 mb-8 uppercase tracking-tight">Classroom Performance</h3>
                 <div className="space-y-6">
                    <StudentRow name="Arjun Singh" progress={85} lastActive="10m ago" />
                    <StudentRow name="Sanya Malhotra" progress={92} lastActive="2h ago" />
                    <StudentRow name="Ishaan Sharma" progress={45} lastActive="1d ago" />
                    <StudentRow name="Riya Patel" progress={78} lastActive="5m ago" />
                 </div>
              </div>

              <div className="bg-slate-900 rounded-[40px] p-8 text-white shadow-xl">
                 <h3 className="text-lg font-black mb-6 uppercase tracking-widest text-blue-400">Quick Tools</h3>
                 <div className="space-y-4">
                    <button className="w-full py-4 bg-white/10 hover:bg-white/20 rounded-2xl text-sm font-bold transition-all text-left px-6 flex items-center justify-between">
                       Assign New Chapter <ChevronRight size={16} />
                    </button>
                    <button className="w-full py-4 bg-white/10 hover:bg-white/20 rounded-2xl text-sm font-bold transition-all text-left px-6 flex items-center justify-between">
                       Generate Class Report <ChevronRight size={16} />
                    </button>
                    <button className="w-full py-4 bg-primary text-white rounded-2xl text-sm font-black uppercase tracking-widest transition-all shadow-lg shadow-blue-500/20">
                       Broadast AI Hint
                    </button>
                 </div>
              </div>
           </div>

        </div>
      </main>
    </div>
  );
}

function StatCard({ icon: Icon, label, value, color }: any) {
  const colors: any = {
    blue: "text-blue-600 bg-blue-50",
    emerald: "text-emerald-600 bg-emerald-50",
    orange: "text-orange-600 bg-orange-50",
    purple: "text-purple-600 bg-purple-50",
  };
  return (
    <div className="bg-white border border-border rounded-3xl p-6 shadow-sm">
       <div className={`w-10 h-10 rounded-xl flex items-center justify-center mb-4 ${colors[color]}`}>
          <Icon size={20} />
       </div>
       <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest">{label}</p>
       <h4 className="text-2xl font-black text-slate-800 mt-1">{value}</h4>
    </div>
  );
}

function StudentRow({ name, progress, lastActive }: any) {
   return (
      <div className="flex items-center justify-between p-4 hover:bg-slate-50 rounded-2xl transition-colors group cursor-pointer">
         <div className="flex items-center gap-4">
            <div className="w-10 h-10 bg-slate-100 rounded-full flex items-center justify-center font-bold text-slate-400 uppercase">
               {name[0]}
            </div>
            <div>
               <h5 className="text-sm font-bold text-slate-800">{name}</h5>
               <p className="text-[10px] text-slate-400 font-medium uppercase tracking-widest">{lastActive}</p>
            </div>
         </div>
         <div className="flex items-center gap-6">
            <div className="w-32 h-2 bg-slate-100 rounded-full overflow-hidden hidden md:block">
               <div className="h-full bg-primary" style={{ width: `${progress}%` }}></div>
            </div>
            <span className="text-xs font-black text-slate-400">{progress}%</span>
            <ChevronRight size={16} className="text-slate-200 group-hover:text-primary transition-all" />
         </div>
      </div>
   );
}
