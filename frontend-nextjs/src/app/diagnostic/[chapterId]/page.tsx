import React, { Suspense } from 'react';
import DiagnosticClient from './DiagnosticClient';
import { getChapterIds } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getChapterIds();
}

export default function DiagnosticPage() {
  return (
    <Suspense fallback={<div className="min-h-screen bg-slate-900 flex items-center justify-center text-white font-black uppercase tracking-[0.4em] text-[10px]">Initializing Neural Probe...</div>}>
      <DiagnosticClient />
    </Suspense>
  );
}
