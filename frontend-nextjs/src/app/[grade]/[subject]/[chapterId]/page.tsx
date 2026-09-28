import React from 'react';
import ChapterClient from './ChapterClient';
import fs from 'fs';
import path from 'path';

export function generateStaticParams() {
  const params: { grade: string; subject: string; chapterId: string }[] = [];
  const processedRoot = path.join(process.cwd(), '..', 'ProcessedContent');

  if (fs.existsSync(processedRoot)) {
    const classes = fs.readdirSync(processedRoot);
    for (const clsFolder of classes) {
      if (clsFolder.toLowerCase().startsWith('class')) {
        const grade = clsFolder.replace('Class', '');
        const gradeDir = path.join(processedRoot, clsFolder);
        if (fs.statSync(gradeDir).isDirectory()) {
          const subjects = fs.readdirSync(gradeDir);
          for (const subject of subjects) {
            const subjDir = path.join(gradeDir, subject);
            if (fs.statSync(subjDir).isDirectory()) {
              const chapters = fs.readdirSync(subjDir);
              for (const chapterId of chapters) {
                params.push({
                  grade,
                  subject,
                  chapterId
                });
              }
            }
          }
        }
      }
    }
  }

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
