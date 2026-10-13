'use client';

import React, { useEffect, useState } from 'react';
import CatchAllChapterClient from '@/components/CatchAllChapterClient';

export default function CurriculumPage() {
  const [segments, setSegments] = useState<string[]>([]);
  const [isLoaded, setIsLoaded] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const grade = params.get('grade') || '';
      const subject = params.get('subject') || '';
      const book = params.get('book') || subject;
      const part = params.get('part') || 'main';
      const unit = params.get('unit') || 'U01';
      const chapterId = params.get('chapter_id') || '';

      setSegments([grade, subject, book, part, unit, chapterId]);
      setIsLoaded(true);
    }
  }, []);

  if (!isLoaded) {
    return (
      <div className="min-h-screen bg-slate-900 flex items-center justify-center text-white">
        <div className="animate-spin w-8 h-8 border-4 border-indigo-500 border-t-transparent rounded-full mr-3" />
        <span className="font-bold">Loading Authoritative Curriculum Workspace...</span>
      </div>
    );
  }

  return <CatchAllChapterClient segments={segments} />;
}
