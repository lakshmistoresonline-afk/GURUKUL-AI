import CatchAllChapterClient from './CatchAllChapterClient';

interface PageProps {
  params: {
    identity: string[];
  };
}

export default function CurriculumCatchAllPage({ params }: PageProps) {
  const { identity } = params;
  return <CatchAllChapterClient segments={identity} />;
}
