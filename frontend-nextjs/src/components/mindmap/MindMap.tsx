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
  if (!data || !data.branches) return null;

  return (
    <div className="w-full bg-slate-900 rounded-[40px] p-12 text-white overflow-hidden relative min-h-[600px] flex flex-col items-center justify-center">
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
            <h3 className="text-2xl font-black uppercase tracking-tight leading-none">{data.topic}</h3>
            <p className="text-[10px] font-black text-blue-100 uppercase tracking-widest mt-2 opacity-60">Central Concept</p>
         </motion.div>

         {/* Branches Grid */}
         <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 w-full max-w-5xl">
            {data.branches.map((branch, i) => (
               <motion.div
                  key={i}
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.1 * (i + 1) }}
                  className="bg-white/5 backdrop-blur-xl border border-white/10 rounded-[32px] p-8 hover:bg-white/10 transition-all group"
               >
                  <div className="flex items-center gap-4 mb-6">
                     <div className="w-10 h-10 bg-primary/20 rounded-xl flex items-center justify-center text-primary group-hover:scale-110 transition-transform">
                        <Share2 size={20} />
                     </div>
                     <h4 className="font-black text-lg text-blue-200 leading-tight tracking-tight uppercase">{branch.label}</h4>
                  </div>

                  {branch.details && (
                     <ul className="space-y-3">
                        {branch.details.map((detail, di) => (
                           <li key={di} className="flex items-start gap-3 text-sm text-slate-400 font-medium">
                              <ArrowRight size={14} className="mt-1 shrink-0 text-primary opacity-40" />
                              <span>{detail}</span>
                           </li>
                        ))}
                     </ul>
                  )}
               </motion.div>
            ))}
         </div>

         <div className="flex items-center gap-4 text-slate-500 font-black text-[10px] uppercase tracking-[0.2em] mt-8">
            <div className="w-8 h-px bg-slate-800"></div>
            AI Synthesized Relationship Map
            <div className="w-8 h-px bg-slate-800"></div>
         </div>
      </div>
    </div>
  );
}
