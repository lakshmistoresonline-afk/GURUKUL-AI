import React from 'react';
import ChapterClient from './ChapterClient';

export function generateStaticParams() {
  const params: { grade: string; subject: string; chapterId: string }[] = [];

  const subjects = ['English', 'Hindi', 'Maths', 'Science'];
  const counts = { 'English': 10, 'Hindi': 12, 'Maths': 15, 'Science': 10 };
  const prefixes = { 'English': 'ENG', 'Hindi': 'HIN', 'Maths': 'MAT', 'Science': 'SCI' };

  for (const subject of subjects) {
    const total = counts[subject as keyof typeof counts];
    const prefix = prefixes[subject as keyof typeof prefixes];
    for (let i = 1; i <= total; i++) {
      const uNum = Math.floor((i - 1) / 3) + 1;
      const chId = `G5-${prefix}-U0${uNum}-C${i < 10 ? '0' + i : i}`;
      params.push({
        grade: '5',
        subject,
        chapterId: chId
      });
    }
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
