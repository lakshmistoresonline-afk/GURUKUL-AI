import React, { Suspense } from 'react';
import FlashcardsClient from './FlashcardsClient';
import { getChapterIds } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getChapterIds();
}

export default function FlashcardsPage() {
  return (
    <Suspense fallback={<div>Loading Flashcards...</div>}>
      <FlashcardsClient />
    </Suspense>
  );
}
