export interface ContentManifestItem {
  type: string;
  sourceType?: string;
  count: number;
  renderer: string;
}

export interface ContentManifest {
  chapterId: string;
  contentTypes: ContentManifestItem[];
}

export interface NavigationTab {
  id: string;
  label: string;
  order: number;
  contentTypes: string[];
}

export class NavigationBuilder {
  /**
   * Returns the exact 7 fixed dashboard sections:
   * 1. Overview
   * 2. Notes
   * 3. Master
   * 4. Flashcards
   * 5. Mindmaps
   * 6. Quiz
   * 7. Question Papers
   * (Overview and Question Papers show professional empty states when source data is absent).
   */
  static buildNavigation(subject: string, manifest: ContentManifest): NavigationTab[] {
    const presentTypes = new Set<string>();
    for (const item of manifest.contentTypes) {
      presentTypes.add(item.type);
      if (item.sourceType) {
        presentTypes.add(item.sourceType);
      }
    }

    return [
      { id: 'overview', label: 'Overview', order: 10, contentTypes: ['overview'] },
      { id: 'notes', label: 'Notes', order: 20, contentTypes: ['notes', 'detailedBreakdown', 'importantTakeaways', 'keyTerminology'] },
      { id: 'master', label: 'Master', order: 30, contentTypes: ['master', 'studyQuestions', 'model_question_bank', 'fill_in_the_blanks'] },
      { id: 'flashcards', label: 'Flashcards', order: 40, contentTypes: ['flashcards', 'flashcard'] },
      { id: 'mindmaps', label: 'Mindmaps', order: 50, contentTypes: ['mindmap', 'mindmaps'] },
      { id: 'quiz', label: 'Quiz', order: 60, contentTypes: ['quiz', 'master_quiz'] },
      { id: 'question_papers', label: 'Question Papers', order: 70, contentTypes: ['question_papers', 'sampleModelPaper'] },
    ];
  }
}
