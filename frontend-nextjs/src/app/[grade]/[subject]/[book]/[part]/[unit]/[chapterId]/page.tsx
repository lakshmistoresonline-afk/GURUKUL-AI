import AuthoritativeChapterClient from './AuthoritativeChapterClient';

interface PageProps {
  params: {
    grade: string;
    subject: string;
    book: string;
    part: string;
    unit: string;
    chapterId: string;
  };
}

export default function AuthoritativeChapterPage({ params }: PageProps) {
  const { grade, subject, book, part, unit, chapterId } = params;
  return (
    <AuthoritativeChapterClient
      grade={grade}
      subject={subject}
      book={book}
      part={part}
      unit={unit}
      chapterId={chapterId}
    />
  );
}
