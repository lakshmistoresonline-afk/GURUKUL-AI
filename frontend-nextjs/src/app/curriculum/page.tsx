'use client';

import React, { Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import CatchAllChapterClient from '@/components/CatchAllChapterClient';

export const dynamic = 'force-dynamic';

function CurriculumSearchContent() {
  const searchParams = useSearchParams();
  const grade = searchParams.get('grade') || '';
  const subject = searchParams.get('subject') || '';
  const book = searchParams.get('book') || subject;
  const part = searchParams.get('part') || 'main';
  const unit = searchParams.get('unit') || 'U01';
  const chapterId = searchParams.get('chapter_id') || '';

  const segments = [grade, subject, book, part, unit, chapterId];

  return <CatchAllChapterClient segments={segments} />;
}

export default function CurriculumPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen bg-slate-900 flex items-center justify-center text-white">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full mr-3" />
        <span className="font-bold">Loading Authoritative Curriculum Workspace...</span>
      </div>
    }>
      <CurriculumSearchContent />
    </Suspense>
  );
}
