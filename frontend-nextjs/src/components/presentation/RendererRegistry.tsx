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
import Class7UniversalNotesComponent from './Class7/Class7UniversalNotesComponent';
import Class7UniversalMasterComponent from './Class7/Class7UniversalMasterComponent';

export interface RendererResolutionParams {
  grade: string;
  subject: string;
  book: string;
  part: string;
  contentType: string;
  data: any;
}

export interface UnsupportedRendererProps {
  grade: string;
  subject: string;
  book: string;
  part: string;
  contentType: string;
}

export function UnsupportedRendererState({ grade, subject, book, part, contentType }: UnsupportedRendererProps) {
  console.warn(`[RendererRegistry] Unsupported renderer requested for exact identity -> Grade: ${grade}, Subject: ${subject}, Book: ${book}, Part: ${part}, ContentType: ${contentType}`);
  return (
    <div className="p-12 text-center bg-rose-50 border border-rose-200 rounded-3xl space-y-3 shadow-sm">
      <h3 className="text-lg font-black text-rose-900">Unsupported Renderer State</h3>
      <p className="text-xs text-rose-700 font-mono">
        No exact renderer registered for identity: {grade}:{subject}:{book}:{part}:{contentType}
      </p>
    </div>
  );
}

class RendererRegistry {
  private static registry: Map<string, React.ComponentType<any>> = new Map();

  static register(key: string, component: React.ComponentType<any>) {
    this.registry.set(key.toLowerCase(), component);
  }

  static get(key: string): React.ComponentType<any> | undefined {
    return this.registry.get(key.toLowerCase());
  }

  static resolve(params: RendererResolutionParams): React.ReactNode {
    const grade = (params.grade || '').trim().toLowerCase();
    const subject = (params.subject || '').trim().toLowerCase();
    const book = (params.book || 'main').trim().toLowerCase();
    const part = (params.part || 'none').trim().toLowerCase();
    const ct = (params.contentType || '').trim().toLowerCase();

    // Exact key formation: grade:subject:book:part:contentType
    const exactKey = `${grade}:${subject}:${book}:${part}:${ct}`;

    // Fallback key ignoring part if part is 'none' or 'main'
    const fallbackKey1 = `${grade}:${subject}:${book}:none:${ct}`;
    const fallbackKey2 = `${grade}:${subject}:main:none:${ct}`;

    const Component = this.get(exactKey) || this.get(fallbackKey1) || this.get(fallbackKey2);

    if (!Component) {
      return (
        <UnsupportedRendererState
          grade={params.grade}
          subject={params.subject}
          book={params.book}
          part={params.part}
          contentType={params.contentType}
        />
      );
    }

    return <Component data={params.data} subject={params.subject} />;
  }
}

// ==========================================
// EXACT AUTHORITATIVE REGISTRATION MAPPINGS
// ==========================================

// Class 5 Registrations
RendererRegistry.register('5:english:main:none:overview', OverviewComponent);
RendererRegistry.register('5:english:main:none:notes', NotesComponent);
RendererRegistry.register('5:english:main:none:master', MasterComponent);
RendererRegistry.register('5:english:main:none:foundational', FoundationalComponent);
RendererRegistry.register('5:english:main:none:flashcards', FlashcardsComponent);
RendererRegistry.register('5:english:main:none:mindmaps', MindmapComponent);
RendererRegistry.register('5:english:main:none:quiz', QuizComponent);
RendererRegistry.register('5:english:main:none:question_papers', QuestionPapersComponent);

RendererRegistry.register('5:hindi:main:none:overview', OverviewComponent);
RendererRegistry.register('5:hindi:main:none:notes', HindiNotesComponent);
RendererRegistry.register('5:hindi:main:none:master', MasterComponent);
RendererRegistry.register('5:hindi:main:none:foundational', FoundationalComponent);
RendererRegistry.register('5:hindi:main:none:flashcards', FlashcardsComponent);
RendererRegistry.register('5:hindi:main:none:mindmaps', MindmapComponent);
RendererRegistry.register('5:hindi:main:none:quiz', QuizComponent);
RendererRegistry.register('5:hindi:main:none:question_papers', QuestionPapersComponent);

RendererRegistry.register('5:mathematics:main:none:overview', OverviewComponent);
RendererRegistry.register('5:mathematics:main:none:notes', MathsNotesComponent);
RendererRegistry.register('5:mathematics:main:none:master', MasterComponent);
RendererRegistry.register('5:mathematics:main:none:foundational', FoundationalComponent);
RendererRegistry.register('5:mathematics:main:none:flashcards', FlashcardsComponent);
RendererRegistry.register('5:mathematics:main:none:mindmaps', MindmapComponent);
RendererRegistry.register('5:mathematics:main:none:quiz', QuizComponent);
RendererRegistry.register('5:mathematics:main:none:question_papers', QuestionPapersComponent);

RendererRegistry.register('5:science:main:none:overview', OverviewComponent);
RendererRegistry.register('5:science:main:none:notes', NotesComponent);
RendererRegistry.register('5:science:main:none:master', MasterComponent);
RendererRegistry.register('5:science:main:none:foundational', FoundationalComponent);
RendererRegistry.register('5:science:main:none:flashcards', FlashcardsComponent);
RendererRegistry.register('5:science:main:none:mindmaps', MindmapComponent);
RendererRegistry.register('5:science:main:none:quiz', QuizComponent);
RendererRegistry.register('5:science:main:none:question_papers', QuestionPapersComponent);

// Class 6 Registrations
RendererRegistry.register('6:english:main:none:overview', OverviewComponent);
RendererRegistry.register('6:english:main:none:notes', NotesComponent);
RendererRegistry.register('6:english:main:none:master', MasterComponent);
RendererRegistry.register('6:english:main:none:foundational', FoundationalComponent);
RendererRegistry.register('6:english:main:none:flashcards', FlashcardsComponent);
RendererRegistry.register('6:english:main:none:mindmaps', MindmapComponent);
RendererRegistry.register('6:english:main:none:quiz', QuizComponent);
RendererRegistry.register('6:english:main:none:question_papers', QuestionPapersComponent);

RendererRegistry.register('6:mathematics:main:none:overview', OverviewComponent);
RendererRegistry.register('6:mathematics:main:none:notes', MathsNotesComponent);
RendererRegistry.register('6:mathematics:main:none:master', Class6MathsMasterComponent);
RendererRegistry.register('6:mathematics:main:none:foundational', FoundationalComponent);
RendererRegistry.register('6:mathematics:main:none:flashcards', FlashcardsComponent);
RendererRegistry.register('6:mathematics:main:none:mindmaps', Class6MathsMindmapComponent);
RendererRegistry.register('6:mathematics:main:none:quiz', QuizComponent);
RendererRegistry.register('6:mathematics:main:none:question_papers', QuestionPapersComponent);

// Class 7 Split Books / Parts Registrations
RendererRegistry.register('7:mathematics:maths_i:part1:overview', OverviewComponent);
RendererRegistry.register('7:mathematics:maths_i:part1:notes', Class7UniversalNotesComponent);
RendererRegistry.register('7:mathematics:maths_i:part1:master', Class7UniversalMasterComponent);
RendererRegistry.register('7:mathematics:maths_i:part1:foundational', FoundationalComponent);
RendererRegistry.register('7:mathematics:maths_i:part1:flashcards', FlashcardsComponent);
RendererRegistry.register('7:mathematics:maths_i:part1:mindmaps', MindmapComponent);
RendererRegistry.register('7:mathematics:maths_i:part1:quiz', QuizComponent);
RendererRegistry.register('7:mathematics:maths_i:part1:question_papers', QuestionPapersComponent);

RendererRegistry.register('7:mathematics:maths_ii:part2:overview', OverviewComponent);
RendererRegistry.register('7:mathematics:maths_ii:part2:notes', Class7UniversalNotesComponent);
RendererRegistry.register('7:mathematics:maths_ii:part2:master', Class7UniversalMasterComponent);
RendererRegistry.register('7:mathematics:maths_ii:part2:foundational', FoundationalComponent);
RendererRegistry.register('7:mathematics:maths_ii:part2:flashcards', FlashcardsComponent);
RendererRegistry.register('7:mathematics:maths_ii:part2:mindmaps', MindmapComponent);
RendererRegistry.register('7:mathematics:maths_ii:part2:quiz', QuizComponent);
RendererRegistry.register('7:mathematics:maths_ii:part2:question_papers', QuestionPapersComponent);

RendererRegistry.register('7:social_science:social_i:part1:overview', OverviewComponent);
RendererRegistry.register('7:social_science:social_i:part1:notes', Class7UniversalNotesComponent);
RendererRegistry.register('7:social_science:social_i:part1:master', Class7UniversalMasterComponent);
RendererRegistry.register('7:social_science:social_i:part1:foundational', FoundationalComponent);
RendererRegistry.register('7:social_science:social_i:part1:flashcards', FlashcardsComponent);
RendererRegistry.register('7:social_science:social_i:part1:mindmaps', MindmapComponent);
RendererRegistry.register('7:social_science:social_i:part1:quiz', QuizComponent);
RendererRegistry.register('7:social_science:social_i:part1:question_papers', QuestionPapersComponent);

RendererRegistry.register('7:social_science:social_ii:part2:overview', OverviewComponent);
RendererRegistry.register('7:social_science:social_i:part2:notes', Class7UniversalNotesComponent);
RendererRegistry.register('7:social_science:social_ii:part2:master', Class7UniversalMasterComponent);
RendererRegistry.register('7:social_science:social_ii:part2:foundational', FoundationalComponent);
RendererRegistry.register('7:social_science:social_ii:part2:flashcards', FlashcardsComponent);
RendererRegistry.register('7:social_science:social_ii:part2:mindmaps', MindmapComponent);
RendererRegistry.register('7:social_science:social_ii:part2:quiz', QuizComponent);
RendererRegistry.register('7:social_science:social_ii:part2:question_papers', QuestionPapersComponent);

export default RendererRegistry;
