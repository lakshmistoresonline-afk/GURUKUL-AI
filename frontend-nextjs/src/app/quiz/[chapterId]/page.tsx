import React, { Suspense } from 'react';
import QuizClient from './QuizClient';
import { getChapterIds } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getChapterIds();
}

export default function QuizPage() {
  return (
    <Suspense fallback={<div>Loading Quiz...</div>}>
      <QuizClient />
    </Suspense>
  );
}
