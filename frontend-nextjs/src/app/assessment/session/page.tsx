'use client';

import React, { useState, useEffect, useCallback, Suspense } from 'react';
import { useSearchParams, useRouter } from 'next/navigation';
import { assessmentService } from '@/services/api';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, Timer, Send, ArrowRight, ArrowLeft } from 'lucide-react';

function ExamSessionContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const paperId = searchParams.get('paperId');

  const [paper, setPaper] = useState<any>(null);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [currentQuestionIdx, setCurrentQuestionIdx] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [timeLeft, setTimeLeft] = useState(0);

  const startSession = useCallback(async () => {
    try {
      const session = await assessmentService.startSession(paperId!);
      // In a real app, the session object would include the paper content
      // For now, we'll assume the session has paper details or fetch them
      const papers = await assessmentService.getPapers(6); // Mock class level
      const selectedPaper = papers.find((p: any) => p.id === paperId);

      setPaper(selectedPaper);
      setSessionId(session.id);
      setTimeLeft(selectedPaper.duration_minutes * 60);
    } catch (error) {
      console.error("Failed to start session:", error);
    }
  }, [paperId]);

  useEffect(() => {
    if (paperId) startSession();
  }, [paperId, startSession]);

  const handleNext = () => {
    if (currentQuestionIdx < paper.questions_json.length - 1) {
      setCurrentQuestionIdx(currentQuestionIdx + 1);
    }
  };

  const handlePrev = () => {
    if (currentQuestionIdx > 0) {
      setCurrentQuestionIdx(currentQuestionIdx - 1);
    }
  };

  const handleSubmit = async () => {
    if (!sessionId) return;
    setIsSubmitting(true);
    try {
      const responses = Object.entries(answers).map(([qId, ans]) => ({
        question_id: qId,
        answer: ans
      }));
      await assessmentService.submitExam(sessionId, responses);
      router.push(`/assessment/session/result?sessionId=${sessionId}`);
    } catch (error) {
      console.error("Submission failed:", error);
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!paper) {
    return <div className="flex items-center justify-center min-h-screen"><Loader2 className="animate-spin" /></div>;
  }

  const currentQuestion = paper.questions_json[currentQuestionIdx];

  return (
    <div className="min-h-screen bg-muted/30 p-8">
      <div className="container mx-auto max-w-4xl">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-2xl font-bold">{paper.title}</h1>
            <p className="text-muted-foreground">Question {currentQuestionIdx + 1} of {paper.questions_json.length}</p>
          </div>
          <div className="flex items-center gap-2 bg-white px-4 py-2 rounded-lg border shadow-sm">
            <Timer className="w-5 h-5 text-primary" />
            <span className="font-mono text-lg font-bold">
              {Math.floor(timeLeft / 60)}:{String(timeLeft % 60).padStart(2, '0')}
            </span>
          </div>
        </div>

        <Card className="min-h-[400px] flex flex-col">
          <CardHeader>
            <CardTitle className="text-xl leading-relaxed">
              {currentQuestion.question}
            </CardTitle>
          </CardHeader>
          <CardContent className="flex-1 space-y-4 pt-4">
            {currentQuestion.options && currentQuestion.options.length > 0 ? (
              <div className="grid grid-cols-1 gap-3">
                {currentQuestion.options.map((opt: string) => (
                  <Button
                    key={opt}
                    variant={answers[currentQuestion.id] === opt ? 'default' : 'outline'}
                    className="justify-start h-auto py-4 px-6 text-left whitespace-normal"
                    onClick={() => setAnswers({...answers, [currentQuestion.id]: opt})}
                  >
                    {opt}
                  </Button>
                ))}
              </div>
            ) : (
              <textarea
                className="w-full h-40 p-4 rounded-xl border bg-muted/20 focus:outline-none focus:ring-2 focus:ring-primary"
                placeholder="Write your answer here or upload a photo..."
                value={answers[currentQuestion.id] || ''}
                onChange={(e) => setAnswers({...answers, [currentQuestion.id]: e.target.value})}
              />
            )}
          </CardContent>
          <div className="p-6 border-t flex justify-between">
            <Button variant="outline" onClick={handlePrev} disabled={currentQuestionIdx === 0}>
              <ArrowLeft className="w-4 h-4 mr-2" /> Previous
            </Button>

            {currentQuestionIdx === paper.questions_json.length - 1 ? (
              <Button onClick={handleSubmit} disabled={isSubmitting} className="bg-green-600 hover:bg-green-700">
                {isSubmitting ? <Loader2 className="animate-spin mr-2" /> : <Send className="w-4 h-4 mr-2" />}
                Submit Exam
              </Button>
            ) : (
              <Button onClick={handleNext}>
                Next <ArrowRight className="w-4 h-4 ml-2" />
              </Button>
            )}
          </div>
        </Card>
      </div>
    </div>
  );
}

export default function ExamSessionPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><Loader2 className="animate-spin" /></div>}>
      <ExamSessionContent />
    </Suspense>
  );
}
