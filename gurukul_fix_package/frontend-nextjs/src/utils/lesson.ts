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
}

/**
 * Normalizes raw package data from Class 5 or Class 6 into a canonical Student Lesson Model.
 */
export function normalizeLesson(pkg: any): NormalizedLesson {
  const content = pkg?.content || {};
  const metadata = pkg?.metadata || {};
  const original = pkg?.original_data || {};
  const aiEnrichment = original?.aiEnrichment || {};

  // 1. Learning Goals
  let learningGoals: string[] = [];
  if (Array.isArray(aiEnrichment.learningObjectives) && aiEnrichment.learningObjectives.length > 0) {
    learningGoals = aiEnrichment.learningObjectives;
  } else if (Array.isArray(content.learning_goals) && content.learning_goals.length > 0) {
    learningGoals = content.learning_goals;
  } else if (content.summary) {
    // If it's a string, we keep it as a single goal if it's meaningful
    const summary = content.summary.trim();
    if (summary && !summary.toLowerCase().startsWith('recall the chapter title')) {
      learningGoals = [summary];
    }
  }

  // 2. Concepts
  let concepts: NormalizedConcept[] = [];
  if (Array.isArray(aiEnrichment.concepts) && aiEnrichment.concepts.length > 0) {
    concepts = aiEnrichment.concepts.map((c: any) => ({
      id: c.conceptId || c.id || c.name,
      name: c.name || c.id || 'Concept',
      explanation: c.studentExplanation || c.explanation,
      example: c.example,
      masteryCriteria: c.masteryCriteria
    }));
  } else if (Array.isArray(aiEnrichment.topicGuides) && aiEnrichment.topicGuides.length > 0) {
    concepts = aiEnrichment.topicGuides.map((t: any) => ({
      id: t.topicId || t.topic,
      name: t.topic || 'Topic',
      explanation: t.studentFriendlySummary || t.sourceGroundedExplanation,
      example: t.sourceEvidence?.[0]?.evidence
    }));
  } else if (content.concepts) {
    concepts = content.concepts.split('\n')
      .filter((l: string) => l.trim())
      .map((c: string) => ({
        name: c.replace(/^[0-9\.\-\*\s]+/, '').trim()
      }));
  }

  // 3. Story Mode
  let story = content.story_explanation || content.storyExplanation || content.studentExplanation || '';

  // Fallback for Class 6 & 7: join lesson sequence sections if no direct story exists
  if (!story && (Array.isArray(content.studentLesson) || Array.isArray(content.studentLearningSequence))) {
    const sequence = content.studentLesson || content.studentLearningSequence;
    story = sequence
      .map((s: any) => s.explanation || s.content || s.instruction)
      .filter(Boolean)
      .join('\n\n');
  }

  // Final fallback to introduction/overview if still empty
  if (!story || story.length < 50) {
     const fallback = content.detailedLesson?.overview || content.introduction || content.summary || '';
     if (fallback.length > story.length) story = fallback;
  }

  // Sanitize bad fallbacks
  if (story.includes('Retell the chapter concepts as a short age-appropriate story')) {
    story = content.introduction || ''; // It's just an instruction placeholder
  }
  if (story.toLowerCase().includes('read the story in your original textbook')) {
    story = content.introduction || '';
  }

  // 4. Activities
  let activities: NormalizedActivity[] = [];
  const rawActivities = aiEnrichment.masteryLab?.activities || aiEnrichment.activity_bank || content.activities || [];
  if (Array.isArray(rawActivities)) {
    activities = rawActivities.map((a: any) => ({
      title: a.label || a.title || 'Mastery Activity',
      description: a.teachBackPrompt || a.transferPrompt || a.errorPrompt || a.misconceptionCheck || a.instructions || a.description || '',
      concept: a.concept
    }));
  }
  // Fallback to objectives if no activities in masteryLab
  if (activities.length === 0 && content.objectives) {
    const objectivesList = typeof content.objectives === 'string'
      ? content.objectives.split('\n').filter((l: string) => l.trim() && !l.includes('Perform the following operation'))
      : Array.isArray(content.objectives) ? content.objectives : [];

    if (objectivesList.length > 0) {
      activities = objectivesList.map((obj: any) => ({
        title: 'Interactive Task',
        description: typeof obj === 'string' ? obj.replace(/^[0-9\.\-\*\s]+/, '').trim() : (obj.description || obj.goal || '')
      }));
    }
  }

  // 5. Visual assets
  const mindMap = content.mind_map || content.mindMap || aiEnrichment.mindMap || aiEnrichment.mind_map;
  const hasMindMap = !!mindMap;
  const hasAnimation = !!(content.animation_url || content.lottie_url);
  const animationFallback = story || content.summary || content.introduction || '';

  // 6. Retrieval Practice
  let retrievalPractice: string[] = [];
  const rawRP = original?.mastery?.retrievalPracticeSet || aiEnrichment?.revision?.expandedRevisionPlan?.retrievalPractice || aiEnrichment?.retrieval_prompts || content.retrieval_prompts || [];
  if (Array.isArray(rawRP)) {
    retrievalPractice = rawRP.map((r: any) => typeof r === 'string' ? r : (r.prompt || r.question || ''));
  }

  // 7. Quiz (Merge Foundation and Expanded)
  const baseQuiz = Array.isArray(content.quiz) ? content.quiz : (content.quiz?.questions || []);
  const expandedQuiz = Array.isArray(original?.assessment?.expandedQuestionBank)
    ? original.assessment.expandedQuestionBank.map((q: any) => ({
        ...q,
        difficulty: q.level || q.difficulty // Map 'level' to 'difficulty' for UI
      }))
    : [];

  const fullQuiz = [...baseQuiz, ...expandedQuiz];

  return {
    title: original?.curriculum?.displayName || metadata.chapterTitle || metadata.chapter_name || content.topic || content.title || 'Untitled Lesson',
    subject: metadata.subject || 'general',
    classNumber: (metadata.class_name || metadata.className || '5').toString().split('_').pop() || '5',
    chapterId: metadata.chapterId || metadata.chapter_id || metadata.code || 'unknown',
    introduction: String(content.introduction || content.detailedLesson?.overview || ''),
    learningGoals,
    concepts,
    teacherExplanation: String(content.teacher_explanation || content.teacherExplanation || content.detailedLesson?.overview || ''),
    story: String(story || ''),
    activities,
    flashcards: content.flashcards || aiEnrichment.flashcards || [],
    retrievalPractice,
    quiz: fullQuiz,
    hasAnimation,
    hasMindMap,
    animationFallback: String(animationFallback || ''),
    mindMap
  };
}
