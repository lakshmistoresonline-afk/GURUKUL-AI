import React, { Suspense } from 'react';
import LearnClient from './LearnClient';
import { getGeneralLearningIds } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getGeneralLearningIds();
}

export default function LearnItemPage() {
  return (
    <Suspense fallback={<div>Loading Module...</div>}>
      <LearnClient />
    </Suspense>
  );
}
