import { progressService, MasteryRecord } from './progress';
import { chapterService } from './api';
import { getChapterDisplayData } from '@/utils/chapter';

export interface Recommendation {
  type: 'continue' | 'review' | 'quiz' | 'next';
  title: string;
  description: string;
  action: string;
  href: string;
  priority: 'high' | 'normal' | 'low';
}

export const recommendationService = {
  async getRecommendations(): Promise<Recommendation[]> {
    const mastery = await progressService.getStudentMastery();
    const recommendations: Recommendation[] = [];

    // 1. Weak Topics (Score < 0.6)
    const weak = mastery.filter(m => m.score < 0.6 && m.status !== 'NOT_STARTED');
    for (const record of weak.slice(0, 2)) {
      const display = getChapterDisplayData(record.chapterId);
      recommendations.push({
        type: 'review',
        title: `Review ${display.name}`,
        description: `Your score is ${Math.round(record.score * 100)}%. Try the story mode or AI Tutor.`,
        action: 'RE-LEARN',
        href: `/library/${record.className}/${record.subject}/${record.chapterId}`,
        priority: 'high'
      });
    }

    // 2. Continue Learning (Most recent started but not mastered)
    const recent = mastery.sort((a, b) => b.lastAccessed?.seconds - a.lastAccessed?.seconds)
                          .find(m => m.status !== 'MASTERED' && m.status !== 'NOT_STARTED');
    if (recent) {
       const display = getChapterDisplayData(recent.chapterId);
       recommendations.push({
         type: 'continue',
         title: `Keep Going: ${display.name}`,
         description: `You're doing great! Continue where you left off.`,
         action: 'RESUME',
         href: `/library/${recent.className}/${recent.subject}/${recent.chapterId}`,
         priority: 'normal'
       });
    }

    // 3. Fallback: Suggest first chapter if nothing started
    if (recommendations.length === 0) {
      recommendations.push({
        type: 'next',
        title: 'Start Your Journey',
        description: 'Discover your first AI-powered chapter in the library.',
        action: 'EXPLORE',
        href: '/library',
        priority: 'low'
      });
    }

    return recommendations;
  }
};
