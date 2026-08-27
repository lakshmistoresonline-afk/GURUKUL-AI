'use client';

import React, { useState } from 'react';
import { assessmentService } from '@/services/api';
import { useAuth } from '@/context/AuthContext';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, Sparkles, Wand2 } from 'lucide-react';
import { useRouter } from 'next/navigation';

export default function ExamGeneratorPage() {
  const { profile } = useAuth();
  const router = useRouter();
  const [subject, setSubject] = useState('Mathematics');
  const [paperType, setPaperType] = useState('MODEL');
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async () => {
    if (!profile?.className) return;

    setIsGenerating(true);
    try {
      const classLevel = parseInt(profile.className.split('_')[1]);
      const paper = await assessmentService.generatePaper(classLevel, subject, paperType);
      router.push('/assessment/papers');
    } catch (error) {
      console.error("Generation failed:", error);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="container mx-auto p-8 max-w-2xl text-center">
      <Sparkles className="w-12 h-12 text-primary mx-auto mb-6" />
      <h1 className="text-3xl font-bold mb-2">AI Exam Generator</h1>
      <p className="text-muted-foreground mb-12">Create a custom practice paper tailored to your curriculum.</p>

      <Card className="text-left">
        <CardContent className="pt-6 space-y-6">
          <div>
            <label className="text-sm font-medium mb-2 block">Select Subject</label>
            <div className="grid grid-cols-2 gap-3">
              {['Mathematics', 'Science', 'EVS', 'English', 'Hindi', 'Social Science'].map((s) => (
                <Button
                  key={s}
                  variant={subject === s ? 'default' : 'outline'}
                  onClick={() => setSubject(s)}
                  className="justify-start"
                >
                  {s}
                </Button>
              ))}
            </div>
          </div>

          <div>
            <label className="text-sm font-medium mb-2 block">Test Type</label>
            <div className="grid grid-cols-2 gap-3">
              {[
                { id: 'UNIT_TEST', label: 'Unit Test' },
                { id: 'MID_TERM', label: 'Mid-Term' },
                { id: 'MODEL', label: 'Model Paper' },
                { id: 'ANNUAL', label: 'Annual Practice' }
              ].map((t) => (
                <Button
                  key={t.id}
                  variant={paperType === t.id ? 'default' : 'outline'}
                  onClick={() => setPaperType(t.id)}
                  className="justify-start"
                >
                  {t.label}
                </Button>
              ))}
            </div>
          </div>

          <Button
            className="w-full h-12 text-lg gap-2"
            size="lg"
            onClick={handleGenerate}
            disabled={isGenerating}
          >
            {isGenerating ? <Loader2 className="w-5 h-5 animate-spin" /> : <Wand2 className="w-5 h-5" />}
            {isGenerating ? 'Generating Your Paper...' : 'Generate Paper'}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
