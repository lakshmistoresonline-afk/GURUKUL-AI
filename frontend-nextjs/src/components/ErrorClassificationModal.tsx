'use client';

import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { HelpCircle, Brain, Target, MessageSquare, AlertTriangle, Zap, X } from 'lucide-react';

interface ErrorClassificationModalProps {
  isOpen: boolean;
  onClose: () => void;
  onClassify: (type: string) => void;
  question: string;
}

const ERROR_TYPES = [
  { id: 'CONCEPTUAL', label: "I don't understand the concept", icon: Brain, color: 'text-red-500 bg-red-50' },
  { id: 'PROCEDURAL', label: "I knew it but used the wrong method", icon: Target, color: 'text-orange-500 bg-orange-50' },
  { id: 'READING', label: "I misunderstood the question", icon: MessageSquare, color: 'text-blue-500 bg-blue-50' },
  { id: 'CARELESS', label: "I made a small mistake", icon: Zap, color: 'text-amber-500 bg-amber-50' },
  { id: 'GUESS', label: "I guessed", icon: HelpCircle, color: 'text-purple-500 bg-purple-50' },
  { id: 'OTHER', label: "Not sure", icon: AlertTriangle, color: 'text-slate-500 bg-slate-50' },
];

export default function ErrorClassificationModal({ isOpen, onClose, onClassify, question }: ErrorClassificationModalProps) {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-950/80 backdrop-blur-md">
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className="bg-white rounded-[40px] shadow-2xl max-w-xl w-full overflow-hidden border border-slate-100"
        >
          <div className="p-8 border-b border-slate-50 flex items-center justify-between">
            <div className="flex items-center gap-3">
               <div className="w-10 h-10 rounded-2xl bg-primary/10 flex items-center justify-center text-primary">
                  <HelpCircle size={24} />
               </div>
               <h3 className="text-xl font-black text-slate-800 uppercase tracking-tight">What happened?</h3>
            </div>
            <button onClick={onClose} className="p-2 hover:bg-slate-50 rounded-full text-slate-400 transition-all">
               <X size={20} />
            </button>
          </div>

          <div className="p-8 space-y-6">
            <div className="p-5 bg-slate-50 rounded-2xl border border-slate-100">
               <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest mb-2">Question Context</p>
               <p className="text-sm font-bold text-slate-600 line-clamp-2 italic">&quot;{question}&quot;</p>
            </div>

            <div className="grid gap-3">
               {ERROR_TYPES.map((type) => (
                 <button
                   key={type.id}
                   onClick={() => onClassify(type.id)}
                   className="flex items-center gap-4 p-5 rounded-2xl border-2 border-slate-50 hover:border-primary/20 hover:bg-slate-50 transition-all group text-left"
                 >
                    <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${type.color} group-hover:scale-110 transition-transform`}>
                       <type.icon size={20} />
                    </div>
                    <span className="text-sm font-bold text-slate-700">{type.label}</span>
                 </button>
               ))}
            </div>
          </div>

          <div className="p-8 bg-slate-50 text-center">
             <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest leading-relaxed">
                Help Gurukul adapt to your learning style.<br/>Your privacy is strictly isolated.
             </p>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
