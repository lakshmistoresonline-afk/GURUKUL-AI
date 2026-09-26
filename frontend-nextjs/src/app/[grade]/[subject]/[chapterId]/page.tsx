import React from 'react';
import ChapterClient from './ChapterClient';
import fs from 'fs';
import path from 'path';

export function generateStaticParams() {
  const params: { grade: string; subject: string; chapterId: string }[] = [];
  const processedRoot = path.join(process.cwd(), '..', 'ProcessedContent', 'Class5');

  if (fs.existsSync(processedRoot)) {
    const subjects = fs.readdirSync(processedRoot);
    for (const subject of subjects) {
      const subjDir = path.join(processedRoot, subject);
      if (fs.statSync(subjDir).isDirectory()) {
        const chapters = fs.readdirSync(subjDir);
        for (const chapterId of chapters) {
          params.push({
            grade: '5',
            subject,
            chapterId
          });
        }
      }
    }
  }

  // Fallback if processedRoot is not found at build time
  if (params.length === 0) {
    params.push({ grade: '5', subject: 'English', chapterId: 'G5-ENG-U01-C01' });
  }

  return params;
}

export default function DynamicChapterPage({
  params,
}: {
  params: { grade: string; subject: string; chapterId: string };
}) {
  return (
    <ChapterClient
      grade={params.grade || '5'}
      subject={params.subject || 'English'}
      chapterId={params.chapterId || 'G5-ENG-U01-C01'}
    />
  );
}
