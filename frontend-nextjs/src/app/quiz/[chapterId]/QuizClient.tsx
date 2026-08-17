'use client';

import React, { useState, useEffect } from 'react';
import { useParams, useRouter, useSearchParams } from 'next/navigation';
import api, { chapterService, quizService, srsService } from '@/services/api';
import { progressService } from '@/services/progress';
import { getChapterDisplayData } from '@/utils/chapter';
import {
  ChevronLeft,
  ChevronRight,
  Zap,
  CheckCircle2,
  XCircle,
  ArrowRight,
  Info,
  Trophy,
  AlertCircle,
  Sparkles,
  RefreshCw,
  Bot,
  Star,
  HelpCircle,
  Brain
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { useAuth } from '@/context/AuthContext';
import { featureFlags } from '@/config/featureFlags';
import ErrorClassificationModal from '@/components/ErrorClassificationModal';
import FormattedText from '@/components/FormattedText';

export default function QuizClient() {
  const { profile, loading: authLoading } = useAuth();
  const params = useParams();
  const searchParams = useSearchParams();
  const router = useRouter();

  const chapterId = params.chapterId as string;
  const className = searchParams.get('class') || profile?.className;
  const subject = searchParams.get('subject') || 'mathematics';

  const [questions, setQuestions] = useState<any[]>([]);
  const [pkg, setPackage] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [isAnswered, setIsAnswered] = useState(false);
  const [score, setScore] = useState(0);
  const [responses, setResponses] = useState<any[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [textAnswer, setTextAnswer] = useState('');
  const [confidence, setConfidence] = useState<number | null>(null);
  const [showMetacognitive, setShowMetacognitive] = useState(false);
  const [strategy, setStrategy] = useState<string | null>(null);
  const [errorModalOpen, setErrorModalOpen] = useState(false);
  const [pendingError, setPendingError] = useState<any>(null);
  const [hint, setHint] = useState<string | null>(null);
  const [detailedErrorExpl, setDetailedErrorExpl] = useState<string | null>(null);
  const [hintLevel, setHintLevel] = useState(1);
  const [hintLoading, setHintLoading] = useState(false);

  const displayData = getChapterDisplayData(chapterId, pkg);

  useEffect(() => {
    if (authLoading || !profile || !className) return;

    if (profile?.className && className !== profile.className) {
      console.warn("Unauthorized quiz access attempt");
      router.replace('/library');
      return;
    }

    const loadQuiz = async () => {
      try {
        const type = searchParams.get('type') || 'quick';
        const count = parseInt(searchParams.get('count') || '10');
        const conceptId = searchParams.get('conceptId');

        if (chapterId === 'interleaved') {
           const allMastery = await progressService.getStudentMastery();
           const interleavedQuestions = await quizService.getInterleaved(className, subject, count, allMastery);
           setQuestions(interleavedQuestions);
           setPackage({ metadata: { chapter_name: "Mixed Practice" } });
        } else {
           const sessionQuestions = await quizService.getSession({
              type: type as any,
              classId: parseInt(className.split('_').pop() || '5'),
              subject,
              chapterId,
              conceptId: conceptId || undefined,
              count
           });
           setQuestions(sessionQuestions);
           const data = await chapterService.getPackage(className, subject, chapterId);
           setPackage(data);
        }
      } catch (error) {
        console.error("Failed to load quiz data", error);
      } finally {
        setLoading(false);
      }
    };
    loadQuiz();
  }, [chapterId, className, subject, authLoading, profile, router, searchParams]);

  const handleMasteryChallenge = async (difficulty: string = 'Hard') => {
    if (!className) return;
    setIsGenerating(true);
    try {
      const newQuestions = await quizService.generateDynamic(className, subject, chapterId, 5, difficulty);
      if (newQuestions && newQuestions.length > 0) {
        setQuestions(newQuestions);
        setCurrentIndex(0);
        setSelectedOption(null);
        setIsAnswered(false);
        setScore(0);
        setShowResults(false);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleSubmit = () => {
    const current = questions[currentIndex];
    const isTextBased = !current.options || current.options.length === 0;

    if (isAnswered) return;
    if (!isTextBased && !selectedOption) return;
    if (isTextBased && !textAnswer.trim()) return;

    let isCorrect = false;
    if (isTextBased) {
      isCorrect = textAnswer.toLowerCase().trim() === current.correctAnswer.toLowerCase().trim();
      if (!current.correctAnswer) isCorrect = true;
    } else {
      isCorrect = selectedOption!.toLowerCase().trim() === current.correctAnswer.toLowerCase().trim();
    }

    if (isCorrect) setScore(s => s + 1);

    const responseData = {
       questionId: current.id,
       isCorrect,
       selected: isTextBased ? textAnswer : selectedOption,
       confidence,
       strategy
    };

    setResponses(prev => [...prev, responseData]);

    if (!isCorrect && featureFlags.adaptiveMastery.errorAnalysis !== 'OFF') {
       setPendingError({ ...responseData, question: current.question });
       setTimeout(() => setErrorModalOpen(true), 1500);
    }

    setIsAnswered(true);
  };

  const handleClassifyError = async (errorType: string) => {
    if (!pendingError || !profile?.uid) return;

    try {
      await progressService.recordError({
        uid: profile.uid,
        question_id: pendingError.questionId,
        concept_id: questions[currentIndex].concept_id,
        chapter_id: chapterId,
        error_type: errorType
      });
    } catch (e) {
      console.error("Failed to record error classification", e);
    } finally {
      setErrorModalOpen(false);
      setPendingError(null);
    }
  };

  const handleExplainError = async () => {
    const current = questions[currentIndex];
    const isTextBased = !current.options || current.options.length === 0;

    try {
      const res = await api.post('/api/adaptive/explain-error', {
        question: current.question,
        student_answer: isTextBased ? textAnswer : selectedOption,
        correct_answer: current.correctAnswer,
        context: pkg?.content?.teacher_explanation
      });
      setDetailedErrorExpl(res.data.explanation);
    } catch (e) {
      console.error(e);
    }
  };
  const handleGetHint = async () => {
    setHintLoading(true);
    try {
      const res = await api.post('/api/adaptive/socratic-hint', {
        question_text: questions[currentIndex].question,
        hint_level: hintLevel,
        context: pkg?.content?.teacher_explanation
      });
      setHint(res.data.hint);
      setHintLevel(res.data.next_level);
    } catch (e) {
      console.error(e);
    } finally {
      setHintLoading(false);
    }
  };

  const handleNext = async () => {
    setHint(null);
    setDetailedErrorExpl(null);
    setHintLevel(1);
    setConfidence(null);
    setStrategy(null);
    setShowMetacognitive(false);

    if (currentIndex < questions.length - 1) {
      const nextQ = questions[currentIndex + 1];
      if (nextQ.difficulty === 'Hard' || nextQ.type === 'hots') {
         setShowMetacognitive(true);
      }
      setCurrentIndex(i => i + 1);
      setSelectedOption(null);
      setTextAnswer('');
      setIsAnswered(false);
    } else {
      const finalScore = score / questions.length;
      const quizResults = questions.map((q, idx) => ({
        question_id: q.id,
        is_correct: responses[idx]?.isCorrect || false
      }));

      await progressService.updateMastery(chapterId, subject, className!, quizResults);

      let rating = 1;
      if (finalScore > 0.9) rating = 4;
      else if (finalScore > 0.7) rating = 3;
      else if (finalScore > 0.5) rating = 2;

      if (profile?.uid) {
        srsService.recordReview(profile.uid, chapterId, 'chapter', rating);
      }

      setShowResults(true);
    }
  };

  if (loading || authLoading) return (
    <div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center">
       <div className="flex flex-col items-center gap-4">
          <RefreshCw className="animate-spin text-slate-400" size={32} />
          <p className="text-slate-600 font-medium">Preparing your session...</p>
       </div>
    </div>
  );

  if (isGenerating) return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center">
       <div className="flex flex-col items-center gap-6 text-white text-center p-6">
          <Sparkles className="animate-pulse text-blue-400" size={64} />
          <div className="space-y-2">
            <h2 className="text-3xl font-bold">Personalizing Challenge</h2>
            <p className="text-slate-400">Our AI is crafting questions based on your progress...</p>
          </div>
       </div>
    </div>
  );

  if (questions.length === 0) return (
    <div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center p-6">
       <div className="bg-white p-12 rounded-3xl shadow-sm border border-slate-200/60 text-center max-w-md">
          <AlertCircle className="mx-auto text-slate-400 mb-6" size={48} />
          <h2 className="text-2xl font-bold text-slate-900 mb-2">Quiz Not Found</h2>
          <p className="text-slate-600 mb-8">The content for this chapter hasn&apos;t been generated yet.</p>
          <button onClick={() => router.back()} className="w-full py-4 bg-slate-900 text-white rounded-xl font-semibold hover:bg-slate-800 transition-colors">Go Back</button>
       </div>
    </div>
  );

  if (showResults) return (
    <div className="min-h-screen bg-[#F8FAFC] flex items-center justify-center p-6">
       <motion.div
         initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
         className="bg-white p-12 rounded-[32px] shadow-sm text-center max-w-lg w-full border border-slate-200/60 relative"
       >
          <div className="relative z-10">
            <div className="w-20 h-20 bg-amber-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <Trophy className="text-amber-500" size={40} />
            </div>
            <h2 className="text-4xl font-bold text-slate-900 mb-2">Quiz Complete!</h2>
            <p className="text-slate-400 font-bold uppercase tracking-widest text-[10px] mb-4">{displayData.name}</p>
            <p className="text-slate-500 font-medium mb-10">You&apos;ve successfully finished this assessment</p>

            <div className="grid grid-cols-2 gap-6 mb-10">
               <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100">
                  <p className="text-slate-500 text-sm font-medium mb-1">Score</p>
                  <p className="text-4xl font-bold text-slate-900">{score}<span className="text-slate-300 text-2xl"> / {questions.length}</span></p>
               </div>
               <div className="bg-slate-50 rounded-2xl p-6 border border-slate-100">
                  <p className="text-slate-500 text-sm font-medium mb-1">Accuracy</p>
                  <p className="text-4xl font-bold text-slate-900">{Math.round((score / questions.length) * 100)}%</p>
               </div>
            </div>

            <div className="p-6 bg-blue-50/50 rounded-2xl border border-blue-100 mb-10">
               <p className="text-blue-900 font-semibold text-lg">
                  {score === questions.length ? "Perfect Score! You've mastered this chapter. 🌟" :
                   score > questions.length / 2 ? "Great job! You have a solid understanding. 👍" :
                   "Good effort! A bit more practice will make you perfect. 💪"}
               </p>
            </div>

            <div className="space-y-4">
               <div className="grid grid-cols-2 gap-4">
                  <button
                    onClick={() => handleMasteryChallenge('Medium')}
                    className="flex flex-col items-center gap-3 p-5 bg-white border border-slate-200 rounded-2xl hover:border-slate-400 hover:bg-slate-50 transition-all"
                  >
                    <Star className="text-blue-500" size={24} />
                    <span className="text-sm font-semibold text-slate-700">Daily Practice</span>
                  </button>
                  <button
                    onClick={() => handleMasteryChallenge('Hard')}
                    className="flex flex-col items-center gap-3 p-5 bg-white border border-slate-200 rounded-2xl hover:border-slate-400 hover:bg-slate-50 transition-all"
                  >
                    <Zap className="text-orange-500" size={24} />
                    <span className="text-sm font-semibold text-slate-700">Elite Challenge</span>
                  </button>
               </div>

               <div className="flex flex-col gap-3 pt-4">
                  <button
                      onClick={() => window.location.reload()}
                      className="w-full py-4 text-slate-600 rounded-xl font-semibold hover:text-slate-900 transition-colors"
                  >
                      Redo Quiz
                  </button>
                  <button
                      onClick={() => router.back()}
                      className="w-full py-4 bg-slate-900 text-white rounded-xl font-semibold shadow-lg shadow-slate-200 hover:bg-slate-800 transition-all"
                  >
                      Return to Chapter
                  </button>
               </div>
            </div>
          </div>
       </motion.div>
    </div>
  );

  const current = questions[currentIndex];
  const options = current.options || (current.type === 'true_false' ? ['True', 'False'] : []);

  return (
    <div className="min-h-screen bg-[#F8FAFC] p-6 md:p-12">
      <div className="max-w-4xl mx-auto space-y-10">
        <div className="flex items-center justify-between">
           <button
              onClick={() => router.back()}
              className="flex items-center gap-3 text-slate-600 hover:text-slate-900 transition-colors group"
           >
              <div className="w-10 h-10 rounded-full border border-slate-200 flex items-center justify-center group-hover:bg-white transition-all">
                <ChevronLeft size={20} />
              </div>
              <div>
                 <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider leading-none mb-1">Chapter Assessment</p>
                 <span className="font-bold text-slate-900">{displayData.fullName}</span>
              </div>
           </button>
           <div className="text-sm font-semibold text-slate-500">
              Question {currentIndex + 1} of {questions.length}
           </div>
        </div>

        <div className="h-1.5 bg-slate-200 rounded-full overflow-hidden">
           <motion.div
              className="h-full bg-slate-900"
              initial={{ width: 0 }}
              animate={{ width: `${((currentIndex + 1) / questions.length) * 100}%` }}
           />
        </div>

        <section className="bg-white border border-slate-200/60 rounded-[32px] p-8 md:p-12 shadow-sm relative">
           <div className="relative z-10">
              <div className="flex items-center justify-between mb-10">
                 <div className="flex items-center gap-3">
                    <span className="px-3 py-1 bg-slate-100 text-slate-600 text-xs font-bold rounded-full border border-slate-200">
                       {current.type?.replace('_', ' ').toUpperCase() || 'QUESTION'}
                    </span>
                    <span className={`px-3 py-1 text-xs font-bold rounded-full border ${
                       current.difficulty === 'Hard' ? 'bg-rose-50 text-rose-600 border-rose-100' :
                       current.difficulty === 'Medium' ? 'bg-amber-50 text-amber-600 border-amber-100' :
                       'bg-emerald-50 text-emerald-600 border-emerald-100'
                    }`}>
                       {current.difficulty?.toUpperCase() || 'NORMAL'}
                    </span>
                 </div>
                 <div className="flex items-center gap-6">
                    {!isAnswered && (
                       <button
                         onClick={handleGetHint}
                         disabled={hintLoading}
                         className="flex items-center gap-2 text-slate-500 hover:text-slate-900 transition-colors font-semibold text-sm"
                       >
                          {hintLoading ? <RefreshCw size={16} className="animate-spin" /> : <Bot size={18} />}
                          <span>Need a Hint?</span>
                       </button>
                    )}
                 </div>
              </div>

              <AnimatePresence>
                {hint && !isAnswered && (
                  <motion.div
                    initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
                    className="mb-8 p-6 bg-slate-50 rounded-2xl border border-slate-200/60 flex gap-4"
                  >
                     <Bot className="text-blue-600 shrink-0 mt-1" size={24} />
                     <div>
                        <p className="text-sm font-bold text-slate-900 mb-1">Study Guide Hint</p>
                        <p className="text-slate-600 leading-relaxed">
                           {hint}
                        </p>
                     </div>
                  </motion.div>
                )}
              </AnimatePresence>

              <h1 className="text-3xl md:text-4xl font-bold text-slate-900 mb-12 leading-[1.3]">
                 {current.question}
              </h1>

              {options.length > 0 ? (
                <div className={`grid gap-4 ${options.length === 2 ? 'grid-cols-2' : 'grid-cols-1'}`}>
                   {options.map((opt: string, i: number) => {
                     const isSelected = selectedOption === opt;
                     const isCorrect = isAnswered && opt.toLowerCase().trim() === current.correctAnswer.toLowerCase().trim();
                     const isWrong = isAnswered && isSelected && !isCorrect;

                     return (
                       <button
                          key={opt}
                          disabled={isAnswered}
                          onClick={() => setSelectedOption(opt)}
                          className={`
                            p-6 rounded-2xl text-left text-lg font-medium transition-all relative flex items-center gap-4 border-2
                            ${isSelected && !isAnswered ? "border-slate-900 bg-slate-50 text-slate-900" : "border-slate-100 bg-white text-slate-600"}
                            ${isCorrect ? "border-emerald-500 bg-emerald-50 text-emerald-900" : ""}
                            ${isWrong ? "border-rose-500 bg-rose-50 text-rose-900" : ""}
                            ${!isAnswered ? "hover:border-slate-300 hover:bg-slate-50/30" : ""}
                          `}
                       >
                          <div className={`
                             w-10 h-10 rounded-xl flex items-center justify-center font-bold text-sm shrink-0
                             ${isSelected && !isAnswered ? "bg-slate-900 text-white" : "bg-slate-100 text-slate-500"}
                             ${isCorrect ? "bg-emerald-500 text-white" : ""}
                             ${isWrong ? "bg-rose-500 text-white" : ""}
                          `}>
                             {String.fromCharCode(65 + i)}
                          </div>
                          <span className="flex-1">{opt}</span>
                          {isCorrect && <CheckCircle2 className="text-emerald-500" size={24} />}
                          {isWrong && <XCircle className="text-rose-500" size={24} />}
                       </button>
                     );
                   })}
                </div>
              ) : (
                <div className="space-y-4">
                  <textarea
                    disabled={isAnswered}
                    value={textAnswer}
                    onChange={(e) => setTextAnswer(e.target.value)}
                    placeholder="Type your answer here..."
                    className="w-full min-h-[180px] p-8 rounded-2xl bg-slate-50 border-2 border-slate-100 focus:border-slate-300 focus:bg-white text-slate-900 text-xl font-medium outline-none transition-all disabled:bg-slate-50/50"
                  />
                </div>
              )}

              {isAnswered && (
                <div className="mt-10 space-y-6">
                   {!responses[currentIndex]?.isCorrect && !detailedErrorExpl && (
                      <button
                        onClick={handleExplainError}
                        className="flex items-center gap-2 text-primary font-bold text-sm hover:underline"
                      >
                         <HelpCircle size={16} /> Why was my answer wrong?
                      </button>
                   )}

                   {detailedErrorExpl && (
                      <motion.div
                        initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
                        className="p-8 bg-rose-50 border border-rose-100 rounded-3xl space-y-4"
                      >
                         <div className="flex items-center gap-3 text-rose-600 font-black uppercase text-[10px] tracking-widest">
                            <AlertCircle size={16} /> Diagnostic Insight
                         </div>
                         <FormattedText content={detailedErrorExpl} className="text-rose-900 leading-relaxed font-medium" />
                      </motion.div>
                   )}

                   <div className="p-8 bg-slate-50 rounded-2xl border border-slate-200/60 flex gap-5">
                      <Info className="text-slate-400 shrink-0 mt-1" size={24} />
                      <div>
                         <p className="text-sm font-bold text-slate-900 mb-2 uppercase tracking-wide">Explanation</p>
                         <p className="text-lg text-slate-700 leading-relaxed font-medium">
                            {current.explanation || "Well done! Move on to the next question."}
                         </p>
                      </div>
                   </div>
                </div>
              )}

              {!isAnswered && (selectedOption || textAnswer.trim()) && (
                <div className="mt-12 p-8 bg-blue-50/30 rounded-[32px] border border-blue-100/50 space-y-6">
                   <p className="text-xs font-black text-blue-600 uppercase tracking-widest text-center">How confident are you in this answer?</p>
                   <div className="flex justify-between gap-4">
                      {[1, 2, 3, 4].map((level) => (
                         <button
                            key={level}
                            onClick={() => setConfidence(level)}
                            className={`flex-1 py-4 rounded-2xl font-bold text-xs transition-all border-2 ${
                               confidence === level
                               ? "bg-blue-600 border-blue-600 text-white shadow-lg shadow-blue-200"
                               : "bg-white border-slate-100 text-slate-400 hover:border-blue-200 hover:text-blue-500"
                            }`}
                         >
                            {level === 1 ? "Guessing" : level === 2 ? "Unsure" : level === 3 ? "Sure" : "Very Sure"}
                         </button>
                      ))}
                   </div>
                </div>
              )}

              <div className="mt-12 flex gap-6">
                 {!isAnswered ? (
                    <button
                      disabled={(!selectedOption && !textAnswer.trim()) || confidence === null}
                      onClick={handleSubmit}
                      className="flex-1 py-5 bg-slate-900 text-white rounded-2xl font-bold text-lg hover:bg-slate-800 transition-all disabled:opacity-20 shadow-lg shadow-slate-100"
                    >
                      {confidence === null ? "Select Confidence" : "Submit Answer"}
                    </button>
                 ) : (
                    <button
                       onClick={handleNext}
                       className="flex-1 py-5 bg-slate-900 text-white rounded-2xl font-bold text-lg hover:bg-slate-800 transition-all shadow-lg shadow-slate-100 flex items-center justify-center gap-3"
                    >
                       <span>{currentIndex === questions.length - 1 ? 'View Final Results' : 'Continue'}</span>
                       <ArrowRight size={20} />
                    </button>
                 )}
              </div>
           </div>
        </section>
      </div>

      <ErrorClassificationModal
        isOpen={errorModalOpen}
        onClose={() => setErrorModalOpen(false)}
        onClassify={handleClassifyError}
        question={pendingError?.question || ""}
      />

      <AnimatePresence>
        {showMetacognitive && (
          <motion.div
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-[100] bg-slate-900/90 backdrop-blur-xl flex items-center justify-center p-6"
          >
             <div className="bg-white rounded-[48px] p-12 max-w-2xl w-full text-center space-y-10 shadow-2xl relative overflow-hidden">
                <div className="space-y-4">
                   <div className="w-20 h-20 bg-indigo-50 text-indigo-600 rounded-3xl flex items-center justify-center mx-auto mb-6">
                      <Brain size={40} />
                   </div>
                   <h3 className="text-4xl font-black text-slate-900 tracking-tight">Pause &amp; Think</h3>
                   <p className="text-slate-500 font-medium text-lg">This is a challenging question. What&apos;s your strategy for solving it?</p>
                </div>

                <div className="grid grid-cols-1 gap-4">
                   {[
                      { id: 'visualize', label: 'Visualize the problem in my head' },
                      { id: 'clues', label: 'Look for keywords and clues first' },
                      { id: 'steps', label: 'Break it down into smaller steps' },
                      { id: 'simplify', label: 'Try to think of a simpler example' }
                   ].map(s => (
                      <button
                         key={s.id}
                         onClick={() => { setStrategy(s.id); setShowMetacognitive(false); }}
                         className="p-6 bg-slate-50 border border-slate-200 rounded-2xl text-left font-bold text-slate-700 hover:bg-indigo-50 hover:border-indigo-200 hover:text-indigo-600 transition-all flex items-center justify-between group"
                      >
                         {s.label}
                         <ChevronRight size={20} className="text-slate-300 group-hover:text-indigo-400" />
                      </button>
                   ))}
                </div>

                <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 rounded-full blur-3xl -mr-32 -mt-32" />
             </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
