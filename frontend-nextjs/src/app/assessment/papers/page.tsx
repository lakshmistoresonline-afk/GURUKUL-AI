'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { assessmentService } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, FileText, Download, Play, Plus } from 'lucide-react';
import Link from 'next/link';

export default function QuestionCenterPage() {
  const { profile } = useAuth();
  const [papers, setPapers] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const loadPapers = useCallback(async (classLevel: number) => {
    try {
      const data = await assessmentService.getPapers(classLevel);
      setPapers(data);
    } catch (error) {
      console.error("Failed to load papers:", error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (profile?.className) {
      const classLevel = parseInt(profile.className.split('_')[1]);
      loadPapers(classLevel);
    }
  }, [profile, loadPapers]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader2 className="w-8 h-8 animate-spin text-primary" />
      </div>
    );
  }

  return (
    <div className="container mx-auto p-8 max-w-6xl">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Question Center</h1>
          <p className="text-muted-foreground">Previous year questions, model papers, and sample tests.</p>
        </div>
        <Link href="/assessment/generator">
          <Button className="gap-2">
            <Plus className="w-4 h-4" />
            Generate New Paper
          </Button>
        </Link>
      </div>

      {papers.length === 0 ? (
        <div className="text-center py-20 bg-muted/30 rounded-2xl border-2 border-dashed">
          <FileText className="w-16 h-12 mx-auto mb-4 opacity-20" />
          <h3 className="text-xl font-semibold">No Papers Available</h3>
          <p className="text-muted-foreground mb-6">Start by generating an AI-powered practice paper.</p>
          <Link href="/assessment/generator">
            <Button variant="secondary">Go to Exam Generator</Button>
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {papers.map((paper) => (
            <Card key={paper.id} className="hover:shadow-lg transition-shadow">
              <CardHeader>
                <div className="flex justify-between items-start">
                  <span className="px-2 py-1 bg-primary/10 text-primary rounded text-xs font-bold uppercase">
                    {paper.paper_type}
                  </span>
                  {paper.year && <span className="text-xs text-muted-foreground">{paper.year}</span>}
                </div>
                <CardTitle className="mt-4">{paper.title}</CardTitle>
                <p className="text-sm text-muted-foreground">{paper.subject} • Class {paper.class_level}</p>
              </CardHeader>
              <CardContent>
                <div className="flex gap-4 text-sm">
                  <div>
                    <p className="font-semibold">{paper.total_marks}</p>
                    <p className="text-xs text-muted-foreground">Marks</p>
                  </div>
                  <div>
                    <p className="font-semibold">{paper.duration_minutes}m</p>
                    <p className="text-xs text-muted-foreground">Time</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter className="gap-2">
                <Link href={`/assessment/session?paperId=${paper.id}`} className="flex-1">
                  <Button className="w-full gap-2">
                    <Play className="w-4 h-4" /> Take Exam
                  </Button>
                </Link>
                <Button variant="outline" size="icon">
                  <Download className="w-4 h-4" />
                </Button>
              </CardFooter>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
