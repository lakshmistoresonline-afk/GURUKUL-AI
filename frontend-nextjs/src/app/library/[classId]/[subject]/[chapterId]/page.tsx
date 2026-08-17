import React, { Suspense } from 'react';
import ChapterDashboardClient from './ChapterDashboardClient';
import { getClassSubjectChapterParams } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getClassSubjectChapterParams();
}

export default function ChapterDashboardPage() {
  return (
    <Suspense fallback={<div>Loading Chapter...</div>}>
      <ChapterDashboardClient />
    </Suspense>
  );
}
