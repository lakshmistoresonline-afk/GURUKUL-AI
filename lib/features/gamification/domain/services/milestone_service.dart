import '../models/achievement.dart';
import '../../../curriculum/domain/models/mastery.dart';
import '../../../curriculum/domain/models/concept_node.dart';

class MilestoneService {
  /// Checks for new milestones based on current stats.
  /// Returns a list of newly unlocked achievement IDs.
  List<String> checkMilestones({
    required UserGamification stats,
    required List<Mastery> studentMastery,
  }) {
    List<String> newlyUnlocked = [];

    // 1. Mastery Milestones
    final masteredCount = studentMastery.where((m) => m.status == LearningStatus.mastered).length;
    if (masteredCount >= 1 && !stats.unlockedAchievementIds.contains('first_mastery')) {
      newlyUnlocked.add('first_mastery');
    }
    if (masteredCount >= 10 && !stats.unlockedAchievementIds.contains('concept_master')) {
      newlyUnlocked.add('concept_master');
    }

    // 2. Streak Milestones
    if (stats.currentStreak >= 7 && !stats.unlockedAchievementIds.contains('streak_7')) {
      newlyUnlocked.add('streak_7');
    }

    // 3. XP Milestones
    if (stats.currentXp >= 1000 && !stats.unlockedAchievementIds.contains('xp_1000')) {
      newlyUnlocked.add('xp_1000');
    }

    return newlyUnlocked;
  }
}
