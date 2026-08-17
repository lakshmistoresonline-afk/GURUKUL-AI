'use client';

import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  X,
  Sparkles,
  Brain,
  Network,
  Info,
  ChevronRight,
  Target
} from 'lucide-react';

interface MindMapNode {
  label: string;
  details: string[];
}

interface ConceptGalaxyProps {
  data: {
    topic: string;
    branches: MindMapNode[];
  };
  onClose: () => void;
}

export default function ConceptGalaxy({ data, onClose }: ConceptGalaxyProps) {
  const [selectedNode, setSelectedNode] = useState<MindMapNode | null>(null);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-[100] bg-[#0F172A]/95 backdrop-blur-2xl flex flex-col p-6 md:p-12 overflow-hidden"
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-12">
        <div className="flex items-center gap-6">
          <div className="w-16 h-16 bg-primary rounded-3xl flex items-center justify-center text-white shadow-xl shadow-primary/20">
            <Network size={32} />
          </div>
          <div>
            <p className="text-xs font-black uppercase tracking-[0.25em] text-primary mb-1">Knowledge Visualization</p>
            <h2 className="text-3xl font-black text-white uppercase tracking-tight">{data.topic}</h2>
          </div>
        </div>
        <button
          onClick={onClose}
          className="p-4 bg-white/5 hover:bg-white/10 text-white rounded-2xl transition-all border border-white/5"
        >
          <X size={24} />
        </button>
      </div>

      <div className="flex-1 relative flex items-center justify-center">
        {/* The Galaxy Map */}
        <div className="relative w-full h-full max-w-5xl mx-auto flex items-center justify-center">
           {/* Central Core */}
           <motion.div
             animate={{ scale: [1, 1.05, 1], rotate: 360 }}
             transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
             className="w-48 h-48 bg-primary/20 rounded-full border-2 border-primary/40 flex items-center justify-center relative z-10 shadow-[0_0_100px_rgba(37,99,235,0.2)]"
           >
             <div className="w-32 h-32 bg-primary/40 rounded-full flex items-center justify-center backdrop-blur-xl border border-primary/50">
               <Brain size={48} className="text-white" />
             </div>
           </motion.div>

           {/* Branches */}
           {data.branches.map((branch, idx) => {
             const angle = (idx / data.branches.length) * (2 * Math.PI);
             const radius = 300; // Distance from center
             const x = Math.cos(angle) * radius;
             const y = Math.sin(angle) * radius;

             return (
               <React.Fragment key={idx}>
                 {/* Connection Line */}
                 <svg className="absolute inset-0 w-full h-full pointer-events-none">
                    <line
                      x1="50%" y1="50%"
                      x2={`calc(50% + ${x}px)`} y2={`calc(50% + ${y}px)`}
                      stroke="rgba(37,99,235,0.2)"
                      strokeWidth="2"
                      strokeDasharray="4 4"
                    />
                 </svg>

                 <motion.button
                   whileHover={{ scale: 1.1, y: -5 }}
                   onClick={() => setSelectedNode(branch)}
                   initial={{ x: 0, y: 0, opacity: 0 }}
                   animate={{ x, y, opacity: 1 }}
                   transition={{ delay: idx * 0.1, type: "spring", stiffness: 100 }}
                   className={`absolute p-6 bg-slate-800/80 border border-white/10 rounded-[32px] backdrop-blur-xl shadow-2xl flex flex-col items-center gap-3 w-48 text-center group ${selectedNode?.label === branch.label ? 'border-primary shadow-primary/20 ring-4 ring-primary/10' : ''}`}
                 >
                    <div className="w-10 h-10 bg-primary/10 rounded-xl flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all">
                       <Target size={20} />
                    </div>
                    <span className="text-xs font-black text-white uppercase tracking-wider line-clamp-2 leading-tight">
                       {branch.label}
                    </span>
                 </motion.button>
               </React.Fragment>
             );
           })}
        </div>

        {/* Side Detail Panel */}
        <AnimatePresence>
          {selectedNode && (
            <motion.div
              initial={{ x: 400, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              exit={{ x: 400, opacity: 0 }}
              className="absolute right-0 top-0 bottom-0 w-[400px] bg-slate-900 border-l border-white/5 p-10 flex flex-col shadow-[-40px_0_80px_rgba(0,0,0,0.5)] z-50 overflow-y-auto custom-scrollbar"
            >
               <button
                 onClick={() => setSelectedNode(null)}
                 className="self-end p-2 text-slate-500 hover:text-white mb-8"
               >
                 <X size={24} />
               </button>

               <div className="space-y-10">
                  <div className="space-y-4">
                     <div className="inline-flex items-center gap-2 px-3 py-1 bg-primary/20 text-primary rounded-full text-[10px] font-black uppercase tracking-widest border border-primary/20">
                        Concept Node
                     </div>
                     <h3 className="text-3xl font-black text-white leading-tight">{selectedNode.label}</h3>
                  </div>

                  <div className="space-y-6">
                     <div className="flex items-center gap-3 text-slate-400">
                        <Info size={18} className="text-primary" />
                        <span className="text-xs font-black uppercase tracking-[0.15em]">Detailed Insights</span>
                     </div>

                     <div className="space-y-4">
                        {selectedNode.details.map((detail, dIdx) => (
                           <motion.div
                             key={dIdx}
                             initial={{ opacity: 0, x: 20 }}
                             animate={{ opacity: 1, x: 0 }}
                             transition={{ delay: dIdx * 0.1 }}
                             className="p-5 bg-white/5 border border-white/5 rounded-2xl flex gap-4 items-start group/detail hover:bg-white/10 transition-all"
                           >
                              <ChevronRight size={16} className="text-primary mt-1 shrink-0 group-hover/detail:translate-x-1 transition-transform" />
                              <p className="text-sm font-medium text-slate-300 leading-relaxed italic">
                                 {detail}
                              </p>
                           </motion.div>
                        ))}
                     </div>
                  </div>

                  <div className="pt-10 border-t border-white/5">
                     <button
                       className="w-full py-5 bg-primary text-white rounded-2xl font-black text-xs uppercase tracking-[0.2em] flex items-center justify-center gap-3 shadow-xl shadow-primary/20 hover:scale-[1.02] active:scale-[0.98] transition-all"
                     >
                        Deep Dive into Content <Sparkles size={16} />
                     </button>
                  </div>
               </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      <style jsx global>{`
         .custom-scrollbar::-webkit-scrollbar { width: 4px; }
         .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
      `}</style>
    </motion.div>
  );
}
