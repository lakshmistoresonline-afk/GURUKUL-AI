import React from 'react';
import ChapterClient from './ChapterClient';

export function generateStaticParams() {
  return [
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U01-C01' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U01-C02' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U02-C03' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U02-C04' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U03-C05' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U03-C06' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U04-C07' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U04-C08' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U05-C09' },
    { grade: '5', subject: 'English', chapterId: 'G5-ENG-U05-C10' },
  ];
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
