import React from 'react';
import OverviewComponent from './OverviewComponent';
import NotesComponent from './NotesComponent';
import MasterComponent from './MasterComponent';
import FoundationalComponent from './FoundationalComponent';
import FlashcardsComponent from './FlashcardsComponent';
import MindmapComponent from './MindmapComponent';
import QuizComponent from './QuizComponent';
import QuestionPapersComponent from './QuestionPapersComponent';

import HindiNotesComponent from './HindiNotesComponent';
import MathsNotesComponent from './MathsNotesComponent';
import Class6MathsMasterComponent from './Class6/Class6MathsMasterComponent';
import Class6MathsMindmapComponent from './Class6/Class6MathsMindmapComponent';

export interface RendererResolutionParams {
  grade: string;
  subject: string;
  book: string;
  contentType: string;
  data: any;
}

class RendererRegistry {
  private static registry: Map<string, React.ComponentType<any>> = new Map();

  static register(key: string, component: React.ComponentType<any>) {
    this.registry.set(key, component);
  }

  static resolve(params: RendererResolutionParams): React.ReactNode {
    const canonicalSubj = params.subject.toLowerCase();
    const ct = params.contentType.toLowerCase();

    if (ct === 'overview') return <OverviewComponent data={params.data} />;
    if (ct === 'notes') {
      if (canonicalSubj.includes('hindi')) return <HindiNotesComponent data={params.data} />;
      if (canonicalSubj.includes('maths') || canonicalSubj.includes('mathematics')) return <MathsNotesComponent data={params.data} />;
      return <NotesComponent data={params.data} subject={params.subject} />;
    }
    if (ct === 'master') {
      if (canonicalSubj.includes('maths') || canonicalSubj.includes('mathematics')) return <Class6MathsMasterComponent data={params.data} />;
      return <MasterComponent data={params.data} subject={params.subject} />;
    }
    if (ct === 'foundational') return <FoundationalComponent data={params.data} />;
    if (ct === 'flashcards') return <FlashcardsComponent flashcards={params.data} />;
    if (ct === 'mindmaps') {
      if (canonicalSubj.includes('maths') || canonicalSubj.includes('mathematics')) return <Class6MathsMindmapComponent data={params.data} />;
      return <MindmapComponent data={params.data} />;
    }
    if (ct === 'quiz') return <QuizComponent quiz={params.data} />;
    if (ct === 'question_papers') return <QuestionPapersComponent data={params.data} />;

    return (
      <div className="p-8 text-center text-slate-500 bg-white rounded-3xl border border-slate-200">
        <h4 className="text-base font-bold text-slate-800">Content Type: {ct}</h4>
        <pre className="text-xs text-left mt-4 overflow-x-auto bg-slate-50 p-4 rounded-2xl">{JSON.stringify(params.data, null, 2)}</pre>
      </div>
    );
  }
}

export default RendererRegistry;
