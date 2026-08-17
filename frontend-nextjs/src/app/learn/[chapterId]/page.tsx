import React, { Suspense } from 'react';
import LearnClient from './LearnClient';
import { getChapterIds } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getChapterIds();
}

export default function LearnPage() {
  return (
    <Suspense fallback={<div>Loading Lesson...</div>}>
      <LearnClient />
    </Suspense>
  );
}
