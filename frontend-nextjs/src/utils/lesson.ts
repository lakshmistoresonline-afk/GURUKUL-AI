/**
 * Student Lesson Normalization for Class 5 & 6
 */

export interface NormalizedConcept {
  id: string;
  name: string;
  explanation?: string;
  example?: string;
  masteryCriteria?: string[];
}

export interface NormalizedActivity {
  title: string;
  description: string;
  concept?: string;
}

export interface NormalizedLesson {
  title: string;
  subject: string;
  classNumber: string;
  chapterId: string;
  introduction: string;
  learningGoals: string[];
  concepts: NormalizedConcept[];
  teacherExplanation: string;
  story: string;
  activities: NormalizedActivity[];
  flashcards: { front: string; back: string }[];
  retrievalPractice: string[];
  quiz: any[];
  hasAnimation: boolean;
  hasMindMap: boolean;
  animationFallback: string;
  mindMap?: any;
  subjectKnowledge?: { category: string, content: string }[];
}

/**
 * Normalizes raw package data from Class 5 or Class 6 into a canonical Student Lesson Model.
 * Supports V3 component-based structure and legacy content structure.
 */
export function normalizeLesson(pkg: any): NormalizedLesson {
  if (!pkg) return {
    title: 'Loading...',
    subject: 'general',
    classNumber: '5',
    chapterId: 'unknown',
    introduction: '',
    learningGoals: [],
    concepts: [],
    teacherExplanation: '',
    story: '',
    activities: [],
    flashcards: [],
    retrievalPractice: [],
    quiz: [],
    hasAnimation: false,
    hasMindMap: false,
    animationFallback: '',
    subjectKnowledge: []
  };

  const content = pkg?.content || {};
  const metadata = pkg?.metadata || {};
  const original = pkg?.original_data || {};
  const aiEnrichment = original?.aiEnrichment || {};
  const components = pkg?.components || {};
  const rootChapter = pkg?.chapter || {};

  // Helper to extract content from V3 components
  const getComp = (id: string) => components[id]?.content;

  // 1. Learning Goals
  let learningGoals: string[] = [];
  const goalsData = getComp('learning_objectives');
  if (Array.isArray(goalsData?.objectives)) {
    learningGoals = goalsData.objectives;
  } else if (Array.isArray(aiEnrichment.learningObjectives)) {
    learningGoals = aiEnrichment.learningObjectives;
  } else if (Array.isArray(content.learning_goals)) {
    learningGoals = content.learning_goals;
  } else if (Array.isArray(content.objectives)) {
    learningGoals = content.objectives;
  }

  // 2. Concepts
  let concepts: NormalizedConcept[] = [];
  const conceptsData = getComp('concepts');
  const conceptsPool = conceptsData?.concepts || aiEnrichment.concepts || content.concepts || [];

  if (Array.isArray(conceptsPool)) {
    concepts = conceptsPool.map((c: any) => ({
      id: c.id || c.conceptId || c.name,
      name: c.name || c.topic || 'Concept',
      explanation: c.definition || c.explanation || c.studentExplanation || c.explanation,
      example: c.example || c.source_evidence || c.evidence,
      masteryCriteria: c.mastery_criteria || c.masteryCriteria
    }));
  }

  // 3. Story Mode
  const storyData = getComp('story_mode');
  let story = storyData?.opening || storyData?.narration || content.story_explanation || content.storyExplanation || content.introduction || '';
  if (Array.isArray(storyData?.scenes)) {
     story = storyData.scenes.map((s: any) => s.narration).filter(Boolean).join('\n\n');
  }
  if ((!story || story.length < 50) && storyData?.ending_reflection) {
      story = storyData.ending_reflection;
  }
  if (!story || story.length < 50) {
      story = content.introduction || rootChapter.source_key_points?.[0] || '';
  }

  // 4. Teacher Explanation
  const teacherData = getComp('teacher_explanation');
  let teacherExplanation = '';
  if (Array.isArray(teacherData?.explanation_sections)) {
    teacherExplanation = teacherData.explanation_sections.map((s: any) => {
        let text = `### ${s.title}\n${s.explanation}`;
        if (s.source_evidence && s.source_evidence.length > 0) {
            text += `\n\n**Evidence from chapter:**\n${Array.isArray(s.source_evidence) ? s.source_evidence.join('\n') : s.source_evidence}`;
        }
        return text;
    }).join('\n\n');
  } else {
    teacherExplanation = teacherData?.explanation || teacherData?.learning_goal || content.teacher_explanation || content.detailedLesson?.overview || '';
  }

  // 5. Activities
  let activities: NormalizedActivity[] = [];
  const labsData = getComp('interactive_lab');
  const activityBankData = getComp('activities');
  const scenariosData = getComp('interactive_scenarios');

  const rawActivities = [
      ...(labsData?.activities || []),
      ...(activityBankData?.items || activityBankData?.activities || []),
      ...(scenariosData?.scenarios || []),
      ...(Array.isArray(content.activities) ? content.activities : [])
  ];

  if (rawActivities.length > 0) {
    activities = rawActivities.map((a: any) => ({
      title: a.title || a.label || a.situation || 'Mastery Activity',
      description: a.objective || a.description || (Array.isArray(a.instructions) ? a.instructions.join('\n') : a.instructions) || a.prompt || (a.choices ? 'Scenario choices available.' : ''),
      concept: a.concept || a.concept_id
    }));
  }

  // 6. Visual assets
  const mindMap = getComp('concept_graph') || content.mind_map || aiEnrichment.mindMap;
  const hasMindMap = !!mindMap;
  const multimedia = getComp('multimedia');
  const hasAnimation = !!(multimedia?.animation_url || content.animation_url);
  const animationFallback = story || content.summary || content.introduction || '';

  // 7. Flashcards
  const flashData = getComp('flashcards');
  const flashcards = flashData?.cards || content.flashcards || aiEnrichment.flashcards || [];

  // 8. Retrieval Practice
  const rpData = getComp('spaced_retrieval');
  const retrievalPractice = rpData?.prompts || aiEnrichment?.retrieval_prompts || content.retrieval_prompts || [];

  // 9. Quiz
  const practiceBank = getComp('practice_bank');
  const assessBank = getComp('assessment_bank');
  const fullQuiz = [...(practiceBank?.items || []), ...(assessBank?.items || []), ...(Array.isArray(content.quiz) ? content.quiz : [])];

  return {
    title: rootChapter.chapter_title || original?.curriculum?.displayName || metadata.chapterTitle || content.topic || 'Untitled Lesson',
    subject: rootChapter.subject || metadata.subject || 'general',
    classNumber: (rootChapter.class || metadata.class_name || '5').toString().split('_').pop() || '5',
    chapterId: rootChapter.chapter_id || metadata.chapterId || pkg.id || 'unknown',
    introduction: getComp('chapter_content')?.overview || content.introduction || rootChapter.source_key_points?.[0] || '',
    learningGoals,
    concepts,
    teacherExplanation,
    story,
    activities,
    flashcards,
    retrievalPractice,
    quiz: fullQuiz,
    hasAnimation,
    hasMindMap,
    animationFallback,
    mindMap,
    subjectKnowledge: content.subject_knowledge || []
  };
}
