'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import { chapterService } from '@/services/api';
import { getChapterDisplayData } from '@/utils/chapter';
import {
  ChevronLeft,
  RotateCw,
  History,
  ChevronRight,
  CheckCircle2,
  BookMarked,
  AlertCircle
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';

export default function FlashcardsClient() {
  const { profile, loading: authLoading } = useAuth();
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const chapterId = params.chapterId as string;
  const className = searchParams.get('class') || profile?.className || 'class_5';
  const subject = searchParams.get('subject') || 'mathematics';

  const [cards, setCards] = useState<any[]>([]);
  const [pkg, setPackage] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [flipped, setFlipped] = useState(false);
  const [isComplete, setIsComplete] = useState(false);

  const displayData = getChapterDisplayData(chapterId, pkg);

  useEffect(() => {
    if (authLoading) return;

    // Data Isolation Check
    if (profile?.className && className !== profile.className) {
      console.warn("Unauthorized flashcards access attempt");
      router.replace('/library');
      return;
    }

    const loadCards = async () => {
      try {
        const data = await chapterService.getPackage(className, subject, chapterId);
        setPackage(data);
        const cardData = data?.content?.flashcards || [];
        setCards(cardData);
      } catch (error) {
        console.error("Failed to load flashcards", error);
      } finally {
        setLoading(false);
      }
    };
    loadCards();
  }, [chapterId, className, subject, authLoading, profile, router]);

  const handleNext = () => {
    if (currentIndex < cards.length - 1) {
      setCurrentIndex(prev => prev + 1);
      setFlipped(false);
    } else {
      setIsComplete(true);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(prev => prev - 1);
      setFlipped(false);
    }
  };

  if (loading || authLoading) return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center font-bold text-slate-400 uppercase tracking-widest text-xs">
       Reviewing cards...
    </div>
  );

  if (cards.length === 0) return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6 text-center">
       <div className="bg-white p-12 rounded-[40px] shadow-xl border border-border max-w-md w-full">
          <AlertCircle className="mx-auto text-pink-400 mb-6" size={64} />
          <h2 className="text-2xl font-black text-slate-800 mb-4">No Cards Available</h2>
          <p className="text-slate-500 font-medium mb-8">This chapter doesn&apos;t have generated flashcards yet.</p>
          <button onClick={() => router.back()} className="w-full py-4 bg-slate-900 text-white rounded-2xl font-bold">Go Back</button>
       </div>
    </div>
  );

  if (isComplete) return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center p-6">
       <motion.div
          initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }}
          className="bg-white p-12 rounded-[40px] shadow-2xl border border-border text-center max-w-md w-full"
       >
          <div className="w-20 h-20 bg-pink-50 text-pink-500 rounded-3xl flex items-center justify-center mx-auto mb-8 shadow-xl shadow-pink-100">
             <CheckCircle2 size={40} />
          </div>
          <h2 className="text-4xl font-black text-slate-800 mb-2">Well Done!</h2>
          <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px] mb-10">Revision Session Complete</p>
          <p className="text-slate-600 font-medium leading-relaxed mb-10 px-4">
             You have reviewed all <span className="text-pink-500 font-bold">{cards.length} key concepts</span> for this chapter.
          </p>
          <div className="flex flex-col gap-3">
             <button onClick={() => window.location.reload()} className="w-full py-4 bg-pink-500 text-white rounded-2xl font-black uppercase tracking-widest text-xs shadow-lg shadow-pink-100 hover:bg-pink-600 transition-all">Restart Review</button>
             <button onClick={() => router.back()} className="w-full py-4 bg-slate-50 text-slate-500 border border-slate-100 rounded-2xl font-black uppercase tracking-widest text-xs hover:bg-white transition-all">Finish</button>
          </div>
       </motion.div>
    </div>
  );

  const current = cards[currentIndex];

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12 overflow-hidden flex flex-col">
      <div className="max-w-4xl mx-auto w-full flex-1 flex flex-col gap-10">

        <div className="flex items-center justify-between">
          <button
            onClick={() => router.back()}
            className="flex items-center gap-2 text-slate-500 hover:text-primary transition-colors group"
          >
            <ChevronLeft size={20} className="group-hover:-translate-x-1 transition-transform" />
            <div>
               <p className="text-[8px] font-black text-slate-300 uppercase tracking-[0.2em] leading-none mb-1">{subject} • Class {className.split('_').pop()}</p>
               <span className="font-bold uppercase tracking-widest text-[10px] text-slate-800">{displayData.fullName}</span>
            </div>
          </button>
          <div className="px-6 py-2 bg-white border border-border rounded-full text-[10px] font-black uppercase tracking-widest text-slate-400 shadow-sm">
             Revision • Card {currentIndex + 1} of {cards.length}
          </div>
        </div>

        <div className="flex-1 flex flex-col items-center justify-center gap-12">

          <div
            onClick={() => setFlipped(!flipped)}
            className="relative w-full max-w-lg h-[450px] cursor-pointer perspective-2000 group"
          >
             <motion.div
                className="relative w-full h-full transform-style-3d preserve-3d"
                initial={false}
                animate={{ rotateY: flipped ? 180 : 0 }}
                transition={{ duration: 0.6, type: "spring", stiffness: 260, damping: 20 }}
             >
                {/* Front Side */}
                <div className="absolute inset-0 bg-white border border-border rounded-[48px] shadow-2xl flex flex-col items-center justify-center p-12 backface-hidden border-b-8 border-b-slate-100">
                   <div className="w-14 h-14 bg-pink-50 text-pink-500 rounded-2xl flex items-center justify-center mb-10 group-hover:scale-110 transition-transform">
                      <History size={28} />
                   </div>
                   <h3 className="text-[10px] font-black text-pink-500 uppercase tracking-[0.2em] mb-4">Key Concept</h3>
                   <p className="text-3xl font-black text-slate-800 text-center leading-tight tracking-tight">
                      {current.front}
                   </p>
                   <div className="mt-16 flex items-center gap-3 text-slate-300 font-black text-[10px] uppercase tracking-widest">
                      <RotateCw size={12} className="animate-spin-slow" /> Tap to reveal definition
                   </div>
                </div>

                {/* Back Side */}
                <div className="absolute inset-0 bg-gradient-to-br from-pink-500 to-rose-600 border border-pink-400 rounded-[48px] shadow-2xl shadow-pink-200 flex flex-col items-center justify-center p-12 backface-hidden rotate-y-180 border-b-8 border-b-pink-700/30">
                   <div className="w-14 h-14 bg-white/20 text-white rounded-2xl flex items-center justify-center mb-10">
                      <BookMarked size={28} />
                   </div>
                   <h3 className="text-[10px] font-black text-white/60 uppercase tracking-[0.2em] mb-4">Definition</h3>
                   <p className="text-xl font-bold text-white text-center leading-relaxed italic">
                      {current.back}
                   </p>
                   <div className="mt-16 px-8 py-2.5 bg-white/10 backdrop-blur-md rounded-full text-white font-black text-[10px] uppercase tracking-widest border border-white/20">
                      Concept Explained
                   </div>
                </div>
             </motion.div>
          </div>

          <div className="flex items-center gap-6">
             <button
               onClick={handlePrevious}
               disabled={currentIndex === 0}
               className="w-14 h-14 bg-white border border-border rounded-full flex items-center justify-center text-slate-400 hover:text-primary hover:border-primary/30 transition-all shadow-sm active:scale-90 disabled:opacity-30"
             >
                <ChevronLeft size={24} />
             </button>

             <button
                onClick={handleNext}
                className="px-12 py-4 bg-slate-900 text-white rounded-3xl font-black uppercase tracking-widest text-xs hover:bg-black shadow-xl shadow-slate-200 flex items-center gap-3 transition-all active:scale-95"
             >
                {currentIndex === cards.length - 1 ? 'Finish Session' : 'Next Concept'}
                <ChevronRight size={18} />
             </button>
          </div>
        </div>
      </div>

      <style jsx global>{`
        .perspective-2000 { perspective: 2000px; }
        .transform-style-3d { transform-style: preserve-3d; }
        .backface-hidden { backface-visibility: hidden; }
        .rotate-y-180 { transform: rotateY(180deg); }
        .preserve-3d { transform-style: preserve-3d; }
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
        .animate-spin-slow { animation: spin-slow 8s linear infinite; }
      `}</style>
    </div>
  );
}
