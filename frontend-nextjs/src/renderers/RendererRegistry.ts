import React from 'react';
import { OverviewRenderer } from './OverviewRenderer';
import { SectionRenderer } from './SectionRenderer';
import { TerminologyRenderer } from './TerminologyRenderer';
import { VocabularyRenderer } from './VocabularyRenderer';
import { FillInTheBlanksRenderer } from './FillInTheBlanksRenderer';
import { GrammarRenderer } from './GrammarRenderer';
import { PhoneticsRenderer } from './PhoneticsRenderer';
import { QuestionRenderer } from './QuestionRenderer';
import { StudyQuestionsRenderer } from './StudyQuestionsRenderer';
import { QuizRenderer } from './QuizRenderer';
import { FlashcardDeck } from './FlashcardDeck';
import { MindMapRenderer } from './MindMapRenderer';
import { GenericStructuredRenderer } from './GenericStructuredRenderer';

export class RendererRegistry {
  private static registry: Record<string, React.FC<any>> = {
    overview: OverviewRenderer,
    'text-section': SectionRenderer,
    text_section: SectionRenderer,
    detailedBreakdown: SectionRenderer,
    importantTakeaways: SectionRenderer,
    keyTerminology: TerminologyRenderer,
    terminology: TerminologyRenderer,
    vocabulary: VocabularyRenderer,
    fill_in_the_blanks: FillInTheBlanksRenderer,
    grammar: GrammarRenderer,
    phonetics: PhoneticsRenderer,
    studyQuestions: StudyQuestionsRenderer,
    'study-questions': StudyQuestionsRenderer,
    master_testbank: StudyQuestionsRenderer,
    model_question_bank: StudyQuestionsRenderer,
    quiz: QuizRenderer,
    question: QuestionRenderer,
    'flashcard-deck': FlashcardDeck,
    flashcards: FlashcardDeck,
    flashcard: FlashcardDeck,
    mindmap: MindMapRenderer,
    'generic-structured': GenericStructuredRenderer,
  };

  /**
   * Registers a new content block type renderer at runtime.
   */
  static registerRenderer(type: string, component: React.FC<any>) {
    this.registry[type] = component;
  }

  /**
   * Returns renderer component for type, or GenericStructuredRenderer as safe fallback.
   * UNKNOWN CONTENT TYPES DO NOT CRASH THE APP.
   */
  static getRenderer(type: string): React.FC<any> {
    return this.registry[type] || GenericStructuredRenderer;
  }
}
