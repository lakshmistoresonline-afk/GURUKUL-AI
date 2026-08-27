'use client';

import React, { useState, useEffect, useCallback, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import { assessmentService } from '@/services/api';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, CheckCircle2, AlertCircle, Award, ArrowRight } from 'lucide-react';
import Link from 'next/link';

function ExamResultContent() {
  const searchParams = useSearchParams();
  const sessionId = searchParams.get('sessionId');

  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  const loadResult = useCallback(async () => {
    try {
      const data = await assessmentService.getResult(sessionId!);
      setResult(data);
    } catch (error) {
      console.error("Failed to load result:", error);
    } finally {
      setLoading(false);
    }
  }, [sessionId]);

  useEffect(() => {
    if (sessionId) loadResult();
  }, [sessionId, loadResult]);

  if (loading) {
    return <div className="flex items-center justify-center min-h-screen"><Loader2 className="animate-spin text-primary" /></div>;
  }

  if (!result) {
    return <div className="text-center p-20">Result not found.</div>;
  }

  return (
    <div className="container mx-auto p-8 max-w-3xl text-center">
      <div className="mb-12">
        <div className="w-24 h-24 bg-primary/10 rounded-full flex items-center justify-center mx-auto mb-6">
          <Award className="w-12 h-12 text-primary" />
        </div>
        <h1 className="text-4xl font-bold mb-2">Exam Completed!</h1>
        <p className="text-muted-foreground text-lg">Here is how you performed on this paper.</p>
      </div>

      <div className="grid grid-cols-2 gap-6 mb-8">
        <Card>
          <CardContent className="pt-6 text-center">
            <p className="text-sm text-muted-foreground mb-1 uppercase font-bold tracking-wider">Score</p>
            <p className="text-4xl font-black text-primary">{result.score}</p>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6 text-center">
            <p className="text-sm text-muted-foreground mb-1 uppercase font-bold tracking-wider">Status</p>
            <p className="text-4xl font-black text-green-600">{result.status}</p>
          </CardContent>
        </Card>
      </div>

      <Card className="text-left mb-8">
        <CardHeader>
          <CardTitle>AI Evaluation & Feedback</CardTitle>
        </CardHeader>
        <CardContent className="space-y-6">
          {result.evaluation_json.map((evalItem: any, idx: number) => (
            <div key={idx} className="p-4 rounded-xl border bg-muted/20">
              <div className="flex justify-between items-start mb-4">
                <span className="font-bold">Question {idx + 1}</span>
                <span className={`px-2 py-1 rounded text-xs font-bold ${evalItem.score > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'}`}>
                  Score: {evalItem.score}
                </span>
              </div>
              <p className="text-sm text-muted-foreground mb-4">Feedback: {evalItem.feedback}</p>
              <div className="text-xs p-3 bg-green-50 text-green-800 rounded-lg">
                <span className="font-bold uppercase mr-2">Model Answer:</span> {evalItem.correct_answer}
              </div>
            </div>
          ))}
        </CardContent>
      </Card>

      <div className="flex gap-4 justify-center">
        <Link href="/assessment/papers">
          <Button variant="outline" size="lg">Back to Center</Button>
        </Link>
        <Link href="/dashboard">
          <Button size="lg" className="gap-2">Go to Dashboard <ArrowRight className="w-4 h-4" /></Button>
        </Link>
      </div>
    </div>
  );
}

export default function ExamResultPage() {
  return (
    <Suspense fallback={<div className="flex items-center justify-center min-h-screen"><Loader2 className="animate-spin" /></div>}>
      <ExamResultContent />
    </Suspense>
  );
}
