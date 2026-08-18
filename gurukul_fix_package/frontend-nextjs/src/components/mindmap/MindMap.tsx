'use client';

import React from 'react';
import { motion } from 'framer-motion';
import { Share2, Network, ArrowRight } from 'lucide-react';

interface MindMapProps {
  data: {
    topic: string;
    branches: Array<{
      label: string;
      details?: string[];
    }>;
  };
}

export default function MindMap({ data }: MindMapProps) {
  const branches = data?.branches || [];
  const topic = data?.topic || "Concept Map";

  return (
    <div className="w-full bg-slate-900 rounded-[48px] p-10 md:p-20 text-white overflow-hidden relative flex flex-col items-center">
      {/* Background decoration */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none opacity-20">
         <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] border border-blue-500/30 rounded-full animate-pulse"></div>
         <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] border border-indigo-500/20 rounded-full"></div>
         <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[400px] h-[400px] border border-purple-500/10 rounded-full"></div>
      </div>

      <div className="relative z-10 w-full flex flex-col items-center gap-16">

         {/* Central Node */}
         <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="px-10 py-6 bg-primary rounded-[32px] shadow-2xl shadow-blue-500/40 text-center border-4 border-white/20 relative group"
         >
            <Network className="absolute -top-4 -right-4 text-blue-300 animate-bounce" size={32} />
            <h3 className="text-2xl font-black uppercase tracking-tight leading-none">{topic}</h3>
            <p className="text-[10px] font-black text-blue-100 uppercase tracking-widest mt-2 opacity-60">Central Concept</p>
         </motion.div>

         {/* Branches Grid */}
         {branches.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 w-full max-w-6xl">
               {branches.map((branch, i) => (
                  <motion.div
                     key={i}
                     initial={{ y: 20, opacity: 0 }}
                     animate={{ y: 0, opacity: 1 }}
                     transition={{ delay: 0.1 * (i + 1) }}
                     className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-[40px] p-8 hover:bg-white/10 transition-all group flex flex-col h-full"
                  >
                     <div className="flex items-center gap-4 mb-4 shrink-0">
                        <div className="w-12 h-12 bg-primary/20 rounded-2xl flex items-center justify-center text-primary group-hover:scale-110 transition-transform shadow-inner">
                           <Share2 size={24} />
                        </div>
                        <h4 className="font-black text-base text-blue-100 leading-tight tracking-tight uppercase line-clamp-2">{branch.label}</h4>
                     </div>

                     <div className="flex-1">
                        {branch.details && branch.details.length > 0 && (
                           <ul className="space-y-3">
                              {branch.details.slice(0, 4).map((detail, di) => (
                                 <li key={di} className="flex items-start gap-3 text-[13px] text-slate-400 font-medium leading-relaxed">
                                    <ArrowRight size={12} className="mt-1 shrink-0 text-primary opacity-40" />
                                    <span className="line-clamp-2">{detail}</span>
                                 </li>
                              ))}
                           </ul>
                        )}
                     </div>
                  </motion.div>
               ))}
            </div>
         ) : (
            <div className="text-center py-20 bg-white/5 rounded-[40px] w-full border border-white/10">
               <Share2 size={48} className="mx-auto text-slate-500 mb-4 opacity-50" />
               <p className="text-slate-400 font-bold uppercase tracking-widest text-sm">Visualizing relationships...</p>
            </div>
         )}

         <div className="flex items-center gap-4 text-slate-500 font-black text-[10px] uppercase tracking-[0.2em] mt-8">
            <div className="w-8 h-px bg-slate-800"></div>
            AI Synthesized Relationship Map
            <div className="w-8 h-px bg-slate-800"></div>
         </div>
      </div>
    </div>
  );
}
