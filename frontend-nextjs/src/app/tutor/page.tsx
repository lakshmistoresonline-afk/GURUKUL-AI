'use client';

import React, { useState, useRef, useEffect, Suspense } from 'react';
import Sidebar from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import { aiService, feynmanService, chapterService } from '@/services/api';
import { progressService } from '@/services/progress';
import { useSearchParams } from 'next/navigation';
import { getChapterDisplayData } from '@/utils/chapter';
import FormattedText from '@/components/FormattedText';
import { Send, Bot, User, Sparkles, RefreshCcw, Plus, BookOpen, ChevronRight, Terminal, Cpu, Brain, MessageSquare, Award, Zap } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';

function TutorContent() {
  const { profile } = useAuth();
  const searchParams = useSearchParams();
  const chapterId = searchParams.get('chapter');
  const className = searchParams.get('class');
  const subject = searchParams.get('subject');

  const [messages, setMessages] = useState<any[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<'CHAT' | 'FEYNMAN'>('CHAT');
  const [chapterName, setChapterName] = useState<string | null>(null);
  const [feynmanState, setFeynmanState] = useState<{
    concept: string;
    stage: 'START' | 'WAITING_FOR_EXPLANATION' | 'EVALUATED';
    evaluation?: any;
    level: number;
  } | null>(null);

  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  useEffect(() => {
    const initContext = async () => {
      if (chapterId && className && subject) {
        try {
          const pkg = await chapterService.getPackage(className, subject, chapterId);
          const name = getChapterDisplayData(chapterId, pkg).name;
          setChapterName(name);
          setMessages([
            { role: 'assistant', content: `Greetings, Scholar. I have loaded the context for **${name}**. How can I assist your understanding of this module?` }
          ]);
        } catch (e) {
          setMessages([
            { role: 'assistant', content: `Greetings, Scholar. I have loaded the context for **${chapterId.split('_').pop()?.toUpperCase()}**. How can I assist your understanding of this module?` }
          ]);
        }
      } else {
        const classId = className?.split('_')[1] || profile?.classId || '5';
        const counts: any = { '5': 47, '6': 54, '7': 62 };
        const nodeCount = counts[classId] || 'all';
        setMessages([
          { role: 'assistant', content: `System initialized. I am your Gurukul AI Intelligence. Accessing **${nodeCount}** verified national curriculum modules for your grade. What shall we explore today?` }
        ]);
      }
    };
    initContext();
  }, [chapterId, className, subject, profile?.classId]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const startFeynmanMode = async () => {
    if (!chapterId || !className || !subject) {
      alert("Please select a chapter from the Library first to enter Mastery Mode.");
      return;
    }
    setMode('FEYNMAN');
    setLoading(true);
    const currentLevel = feynmanState?.level || 1;
    try {
      const challenge = await feynmanService.getChallenge(className, subject, chapterId, currentLevel);
      setFeynmanState({
        concept: challenge.concept,
        stage: 'WAITING_FOR_EXPLANATION',
        level: currentLevel
      });
      setMessages(prev => [...prev, { role: 'assistant', isFeynman: true, content: challenge.question }]);
    } catch (e) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Failed to initialize Feynman Mode. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async (e?: React.FormEvent) => {
    e?.preventDefault();
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
    setLoading(true);

    try {
      if (mode === 'FEYNMAN' && feynmanState?.stage === 'WAITING_FOR_EXPLANATION') {
        const evalRes = await feynmanService.evaluate(className!, subject!, chapterId!, feynmanState.concept, userMsg, feynmanState.level);

        const isSuccess = evalRes.score >= 70;
        const nextLevel = isSuccess ? Math.min(6, feynmanState.level + 1) : feynmanState.level;

        setFeynmanState({ ...feynmanState, stage: 'EVALUATED', evaluation: evalRes, level: nextLevel });

        // Record Feynman Mastery Evidence
        if (evalRes.is_accurate) {
           progressService.recordFeynmanScore(chapterId!, subject!, className!, evalRes.score);
        }

        setMessages(prev => [...prev, {
          role: 'assistant',
          isEvaluation: true,
          content: evalRes.feedback,
          score: evalRes.score
        }]);
      } else {
        const res = await aiService.generate(userMsg);
        setMessages(prev => [...prev, { role: 'assistant', content: res.response }]);
      }
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: "Error in neural processing. Please retry." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex min-h-screen bg-[#F8FAFC] text-slate-900">
      <Sidebar />
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        <TopBar title={mode === 'FEYNMAN' ? "Mastery Mode: Feynman" : "AI Intelligence Hub"} />

        <div className="flex-1 overflow-y-auto p-6 md:p-12 scrollbar-hide">
           <div className="max-w-4xl mx-auto space-y-8">

              {/* Header Toggles */}
              <div className="flex items-center justify-between">
                <div className="flex gap-4">
                  <button
                    onClick={() => setMode('CHAT')}
                    className={`px-6 py-3 rounded-2xl font-black text-[10px] uppercase tracking-widest flex items-center gap-2 transition-all ${mode === 'CHAT' ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/20' : 'bg-slate-200/50 text-slate-500 hover:bg-slate-200'}`}
                  >
                    <MessageSquare size={16} /> Neural Chat
                  </button>
                  <button
                    onClick={startFeynmanMode}
                    className={`px-6 py-3 rounded-2xl font-black text-[10px] uppercase tracking-widest flex items-center gap-2 transition-all ${mode === 'FEYNMAN' ? 'bg-amber-500 text-white shadow-lg shadow-amber-500/20' : 'bg-slate-200/50 text-slate-500 hover:bg-slate-200'}`}
                  >
                    <Brain size={16} /> Feynman Mastery
                  </button>
                </div>
                {chapterId && (
                  <div className="px-4 py-2 bg-emerald-50 border border-emerald-100 rounded-xl flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                    <span className="text-[10px] font-black uppercase tracking-widest text-emerald-600">{chapterName || chapterId.split('_').pop()} Ready</span>
                  </div>
                )}
              </div>

              <div className="space-y-8 pt-10">
                <AnimatePresence>
                  {messages.map((m, i) => (
                    <motion.div
                      key={i}
                      initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
                      className={`flex ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
                    >
                      <div className={`flex gap-5 max-w-[85%] ${m.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                        <div className={`w-12 h-12 rounded-2xl flex-shrink-0 flex items-center justify-center shadow-lg ${
                          m.role === 'user' ? 'bg-blue-600 text-white' :
                          m.isEvaluation ? 'bg-amber-100 text-amber-600 border border-amber-200' : 'bg-white border border-slate-200/60 text-blue-600'
                        }`}>
                           {m.role === 'user' ? <User size={24} /> : m.isEvaluation ? <Award size={24} /> : <Bot size={24} />}
                        </div>
                        <div className={`p-8 rounded-[32px] text-base leading-relaxed font-medium shadow-sm relative ${
                          m.role === 'user' ? 'bg-blue-600 text-white rounded-tr-none' :
                          m.isEvaluation ? 'bg-amber-50 border border-amber-100 text-amber-900 rounded-tl-none' :
                          'bg-white border border-slate-200/60 text-slate-800 rounded-tl-none'
                        }`}>
                           {m.isEvaluation && (
                             <div className="absolute -top-4 -right-4 w-12 h-12 bg-amber-500 rounded-full flex items-center justify-center font-black text-xs text-white border-4 border-[#F8FAFC] shadow-xl">
                                {m.score}%
                             </div>
                           )}
                           <FormattedText
                             content={m.content}
                             className={m.role === 'user' ? 'prose-p:text-white prose-strong:text-white' : 'prose-slate'}
                           />

                           {m.isEvaluation && m.score >= 80 && (
                             <div className="mt-4 flex items-center gap-2 text-[10px] font-black uppercase text-amber-600 tracking-[0.2em]">
                                <Zap size={14} className="fill-current" /> Mastery Achievement Unlocked
                             </div>
                           )}
                        </div>
                      </div>
                    </motion.div>
                  ))}
                </AnimatePresence>

                {loading && (
                  <div className="flex justify-start">
                    <div className="flex gap-5">
                       <div className="w-12 h-12 rounded-2xl bg-white border border-slate-200/60 text-blue-600 flex items-center justify-center animate-pulse shadow-sm">
                          <Sparkles size={24} />
                       </div>
                       <div className="bg-white border border-slate-200/60 p-8 rounded-[32px] shadow-sm">
                          <div className="flex gap-2">
                             <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                             <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:0.2s]"></div>
                             <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce [animation-delay:0.4s]"></div>
                          </div>
                       </div>
                    </div>
                  </div>
                )}
              </div>
              <div ref={messagesEndRef} className="h-40" />
           </div>
        </div>

        {/* Input Area */}
        <div className="p-10 bg-white border-t border-slate-200 shadow-[0_-4px_20px_-5px_rgba(0,0,0,0.05)]">
           <div className="max-w-4xl mx-auto">
              <form onSubmit={handleSend} className="relative group">
                <div className="absolute left-6 top-1/2 -translate-y-1/2 text-slate-400 group-focus-within:text-blue-600 transition-colors">
                   <Terminal size={20} />
                </div>
                <input
                   type="text"
                   value={input}
                   onChange={(e) => setInput(e.target.value)}
                   placeholder={mode === 'FEYNMAN' ? "Explain the concept simply..." : "Enter query for neural processing..."}
                   className="w-full pl-16 pr-32 py-6 bg-slate-50 border border-slate-200 rounded-3xl focus:outline-none focus:ring-2 focus:ring-blue-600/10 focus:border-blue-600/30 text-sm font-bold transition-all shadow-sm text-slate-900 placeholder:text-slate-400"
                />
                <div className="absolute right-3 top-1/2 -translate-y-1/2 flex items-center gap-3">
                   <button
                      type="button"
                      onClick={() => {
                        setMessages([{ role: 'assistant', content: 'Session reset. Awaiting next command.' }]);
                        setMode('CHAT');
                        setFeynmanState(null);
                      }}
                      className="p-3 text-slate-400 hover:text-slate-600 transition-colors"
                   >
                      <RefreshCcw size={20} />
                   </button>
                   <button
                      type="submit"
                      disabled={loading || !input.trim()}
                      className="bg-blue-600 text-white p-4 rounded-2xl hover:bg-blue-700 transition-all disabled:opacity-30 shadow-lg shadow-blue-600/20 active:scale-95"
                   >
                      <Send size={20} />
                   </button>
                </div>
              </form>

              <div className="mt-6 flex flex-wrap gap-3">
                 {mode === 'CHAT' ? (
                   <>
                     <QuickCmd label="Simplify context" onClick={() => setInput('Explain this like I am 5')} />
                     <QuickCmd label="Real-world example" onClick={() => setInput('Give me a real-life example')} />
                     <QuickCmd label="Mastery Challenge" onClick={startFeynmanMode} />
                   </>
                 ) : (
                   <div className="flex items-center gap-2 text-[10px] font-black uppercase text-slate-500 tracking-widest">
                      <Brain size={14} className="text-amber-500" /> Currently in Feynman Mastery Mode
                   </div>
                 )}
              </div>
           </div>
        </div>
      </main>
    </div>
  );
}

function QuickCmd({ label, onClick }: any) {
   return (
      <button
        onClick={onClick}
        className="px-4 py-2 bg-slate-100 border border-slate-200 rounded-xl text-[9px] font-black uppercase tracking-widest text-slate-600 hover:bg-slate-200 hover:text-blue-600 hover:border-blue-300 transition-all"
      >
         {label}
      </button>
   );
}

export default function TutorPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center font-black text-slate-400 uppercase tracking-widest text-xs animate-pulse">Initializing Neural Link...</div>}>
      <TutorContent />
    </Suspense>
  );
}
