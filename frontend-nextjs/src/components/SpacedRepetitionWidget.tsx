'use client';

import React, { useEffect, useState } from 'react';
import { srsService } from '@/services/api';
import { getChapterDisplayData } from '@/utils/chapter';
import { Brain, Zap, ArrowRight, Sparkles, Clock, CheckCircle2, ChevronRight } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

interface SRSItem {
  id: string;
  content_id: string;
  content_type: string;
  easiness_factor: number;
  interval: number;
  repetitions: number;
  next_review: string;
}

export default function SpacedRepetitionWidget({ studentId }: { studentId: string }) {
  const [dueItems, setDueItems] = useState<SRSItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!studentId) return;

    const fetchDue = async () => {
      try {
        const items = await srsService.getDueItems(studentId, undefined, 3);
        setDueItems(items);
      } catch (err) {
        console.error("SRS Fetch error", err);
      } finally {
        setLoading(false);
      }
    };

    fetchDue();
  }, [studentId]);

  if (loading) return (
    <div className="h-64 bg-slate-50 border border-slate-200 rounded-[50px] animate-pulse flex items-center justify-center">
       <Brain className="text-slate-300" size={32} />
    </div>
  );

  return (
    <div className="bg-white border border-slate-200 rounded-[50px] p-10 shadow-xl relative overflow-hidden group">
      <div className="relative z-10 space-y-8">
        <div className="flex items-center justify-between">
           <div className="flex items-center gap-4">
              <div className="w-12 h-12 rounded-2xl bg-indigo-50 flex items-center justify-center text-indigo-600 border border-indigo-100">
                 <Brain size={24} />
              </div>
              <div>
                 <h3 className="text-xl font-black tracking-tight text-slate-900">Daily Revision</h3>
                 <p className="text-[10px] font-black text-slate-600 uppercase tracking-widest">Strengthen Your Memory</p>
              </div>
           </div>
           {dueItems.length > 0 && (
             <span className="px-3 py-1.5 bg-amber-500 text-white text-[10px] font-black uppercase rounded-lg shadow-lg shadow-amber-500/10">
                {dueItems.length} Due
             </span>
           )}
        </div>

        <div className="space-y-4">
           {dueItems.length > 0 ? (
             dueItems.map((item, idx) => {
               const display = getChapterDisplayData(item.content_id);
               // Calculate "Memory Strength" based on repetitions and interval
               const strength = Math.min(100, (item.repetitions * 20) + (item.interval > 0 ? 20 : 0));

               return (
                 <div key={item.id} className="p-6 bg-slate-50 border border-slate-200 rounded-3xl hover:bg-white hover:border-indigo-200 transition-all flex items-center justify-between group/item">
                    <div className="flex items-center gap-5">
                       <div className="w-10 h-10 rounded-xl bg-white border border-slate-200 flex items-center justify-center text-slate-400 group-hover/item:text-indigo-600 transition-colors">
                          <Zap size={20} className={strength > 70 ? "fill-amber-500 text-amber-500" : ""} />
                       </div>
                       <div>
                          <h4 className="text-sm font-black text-slate-900 line-clamp-1">{display.name}</h4>
                          <div className="flex items-center gap-3 mt-1">
                             <div className="w-20 h-2 bg-slate-200 rounded-full overflow-hidden">
                                <div
                                  className="h-full bg-indigo-600 rounded-full"
                                  style={{ width: `${strength}%` }}
                                />
                             </div>
                             <span className="text-[10px] font-black text-slate-700 uppercase tracking-tight">Strength: {strength}%</span>
                          </div>
                       </div>
                    </div>
                    <Link
                      href={`/quiz/${item.content_id}`}
                      className="p-3 rounded-2xl bg-indigo-50 text-indigo-600 opacity-0 group-hover/item:opacity-100 transition-all hover:bg-indigo-600 hover:text-white"
                    >
                       <ArrowRight size={18} />
                    </Link>
                 </div>
               )
             })
           ) : (
             <div className="py-10 text-center space-y-4">
                <div className="w-16 h-16 bg-emerald-50 rounded-full flex items-center justify-center mx-auto text-emerald-600 border border-emerald-100">
                   <CheckCircle2 size={32} />
                </div>
                <div className="space-y-1">
                   <p className="text-sm font-black text-slate-900">Memory Bank Full</p>
                   <p className="text-xs font-bold text-slate-600 uppercase tracking-tight">No revisions due today. Explore new chapters!</p>
                </div>
                <Link href="/library" className="inline-flex items-center gap-2 text-[10px] font-black text-indigo-600 uppercase tracking-widest hover:underline pt-2">
                   Open Knowledge Index <ChevronRight size={12} />
                </Link>
             </div>
           )}
        </div>

        {dueItems.length > 0 && (
          <button className="w-full py-5 bg-indigo-600 text-white rounded-2xl font-black text-xs uppercase tracking-[0.2em] shadow-xl shadow-indigo-500/10 hover:bg-indigo-700 transition-all flex items-center justify-center gap-2">
             Start Rapid Fire Session <Sparkles size={14} />
          </button>
        )}
      </div>

      <Brain className="absolute -right-20 -bottom-20 w-80 h-80 text-slate-50 -rotate-12 group-hover:rotate-0 transition-transform duration-1000 pointer-events-none" />
    </div>
  );
}
