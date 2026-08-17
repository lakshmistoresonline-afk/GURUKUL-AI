'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X, Zap, Target, Brain, Award, RotateCcw, ArrowRight } from 'lucide-react';

interface PracticeSessionModalProps {
  isOpen: boolean;
  onClose: () => void;
  chapterId: string;
  className: string;
  subject: string;
  onStart: (type: string, count: number, conceptId?: string) => void;
  concepts: any[];
}

const SESSION_TYPES = [
  { id: 'quick', title: 'Quick Practice', desc: '10 balanced questions for a fast check-in.', count: 10, icon: Zap, color: 'blue' },
  { id: 'chapter', title: 'Chapter Drill', desc: '15 questions covering all concepts.', count: 15, icon: Target, color: 'emerald' },
  { id: 'mastery', title: 'Mastery Challenge', desc: '20 difficult questions to prove your knowledge.', count: 20, icon: Award, color: 'orange' },
  { id: 'remediation', title: 'Concept Review', desc: 'Focused on your weak areas (5-8 questions).', count: 8, icon: RotateCcw, color: 'red' },
];

export default function PracticeSessionModal({ isOpen, onClose, onStart, concepts }: PracticeSessionModalProps) {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/40 backdrop-blur-md">
        <motion.div
          initial={{ scale: 0.9, opacity: 0, y: 20 }}
          animate={{ scale: 1, opacity: 1, y: 0 }}
          exit={{ scale: 0.9, opacity: 0, y: 20 }}
          className="bg-white rounded-[40px] shadow-2xl w-full max-w-4xl overflow-hidden flex flex-col border border-slate-200/60"
        >
          {/* Header */}
          <div className="p-10 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
            <div>
               <h3 className="text-4xl font-black text-slate-900 uppercase italic tracking-tight">Practice Lab</h3>
               <p className="text-slate-600 text-sm font-bold uppercase tracking-widest mt-1">Select your training intensity</p>
            </div>
            <button
              onClick={onClose}
              className="p-4 hover:bg-slate-100 rounded-3xl transition-all text-slate-400 hover:text-slate-900 border border-transparent hover:border-slate-200"
              aria-label="Close modal"
            >
              <X size={32} />
            </button>
          </div>

          {/* Content */}
          <div className="p-10 grid grid-cols-1 md:grid-cols-2 gap-6 overflow-y-auto max-h-[65vh] custom-scrollbar">
            {SESSION_TYPES.map((type) => (
              <button
                key={type.id}
                onClick={() => onStart(type.id, type.count)}
                className="flex items-start gap-6 p-8 bg-slate-50 border border-slate-200/60 rounded-[32px] hover:border-primary/40 hover:bg-white hover:shadow-xl hover:shadow-slate-200/50 transition-all group text-left relative overflow-hidden"
              >
                 {/* Icon Container */}
                 <div className="w-16 h-16 rounded-2xl bg-white border border-slate-200 flex items-center justify-center text-primary group-hover:scale-110 transition-transform shadow-sm">
                    <type.icon size={32} strokeWidth={2.5} />
                 </div>

                 <div className="flex-1 space-y-2">
                    <div className="flex items-center justify-between">
                       <h4 className="font-black text-slate-900 text-2xl uppercase tracking-tight">{type.title}</h4>
                       <span className="text-xs font-black text-primary uppercase tracking-widest bg-primary/5 px-3 py-1 rounded-full">{type.count} Questions</span>
                    </div>
                    <p className="text-base text-slate-600 font-medium leading-relaxed">{type.desc}</p>
                 </div>

                 {/* Hover Arrow */}
                 <div className="absolute top-6 right-6 opacity-0 group-hover:opacity-100 translate-x-4 group-hover:translate-x-0 transition-all">
                    <ArrowRight size={24} className="text-primary" />
                 </div>
              </button>
            ))}

            {/* Concept Specific Section */}
            <div className="md:col-span-2 pt-8 border-t border-slate-100 mt-6">
               <h4 className="text-xs font-black text-slate-500 uppercase tracking-[0.3em] mb-6 px-2">Targeted Concept Practice</h4>
               <div className="flex flex-wrap gap-3 px-2">
                  {concepts.map((c, i) => (
                    <button
                       key={i}
                       onClick={() => onStart('concept', 5, c.id)}
                       className="px-6 py-4 bg-white border border-slate-200 rounded-2xl text-xs font-bold text-slate-600 hover:text-slate-900 hover:border-primary/40 hover:shadow-md transition-all"
                    >
                       {c.name}
                    </button>
                  ))}
               </div>
            </div>
          </div>

          {/* Footer */}
          <div className="p-8 bg-slate-50/50 border-t border-slate-100 text-center">
             <p className="text-xs font-black text-slate-500 uppercase tracking-widest">
               Powered by Gurukul AI Smart Question Bank
             </p>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
