import React from 'react';
import SubjectExplorerClient from './SubjectExplorerClient';
import { getClassSubjectParams } from '@/utils/staticParams';

export async function generateStaticParams() {
  return getClassSubjectParams();
}

export default function SubjectExplorerPage() {
  return (
    <SubjectExplorerClient />
  );
}
