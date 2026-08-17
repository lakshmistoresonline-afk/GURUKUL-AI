import manifest from '@/data/manifest.json';
import generalLearningManifest from '@/data/generalLearningManifest.json';

export function getManifest() {
  return manifest;
}

export function getChapterIds() {
  const manifest = getManifest();
  return manifest.map((c: any) => ({
    chapterId: c.id,
  }));
}

export function getClassSubjectParams() {
  const manifest = getManifest();
  const unique = new Set();
  manifest.forEach((c: any) => {
    unique.add(`class_${c.class}|${c.subject.toLowerCase()}`);
  });
  return Array.from(unique).map((u: any) => {
    const [classId, subject] = u.split('|');
    return { classId, subject };
  });
}

export function getClassSubjectChapterParams() {
  const manifest = getManifest();
  return manifest.map((c: any) => ({
    classId: `class_${c.class}`,
    subject: c.subject.toLowerCase(),
    chapterId: c.id,
  }));
}

export function getGeneralLearningCategories() {
  return [
    { category: 'english_vocabulary' },
    { category: 'general_knowledge' },
    { category: 'science_facts' },
    { category: 'maths_quick_practice' },
    { category: 'india_and_world' },
    { category: 'life_skills' },
    { category: 'logic_and_reasoning' }
  ];
}

export function getGeneralLearningIds() {
  return generalLearningManifest.map((id: string) => ({ id }));
}
