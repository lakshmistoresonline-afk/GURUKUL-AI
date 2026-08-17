import React, { Suspense } from 'react';
import CategoryClient from './CategoryClient';
import { getGeneralLearningCategories } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getGeneralLearningCategories();
}

export default function CategoryPage() {
  return (
    <Suspense fallback={<div>Loading Category...</div>}>
      <CategoryClient />
    </Suspense>
  );
}
