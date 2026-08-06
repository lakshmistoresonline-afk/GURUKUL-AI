import 'package:cloud_firestore/cloud_firestore.dart';
import '../domain/models/achievement.dart';

class GamificationRepository {
  final FirebaseFirestore _firestore;

  GamificationRepository({FirebaseFirestore? firestore})
      : _firestore = firestore ?? FirebaseFirestore.instance;

  Stream<UserGamification> watchUserStats(String userId) {
    return _firestore
        .collection('gamification')
        .doc(userId)
        .snapshots()
        .map((doc) {
      if (doc.exists) {
        return UserGamification(
          userId: userId,
          currentXp: doc['currentXp'] ?? 0,
          currentStreak: doc['currentStreak'] ?? 0,
          lastActivityDate: DateTime.parse(doc['lastActivityDate'] ?? DateTime.now().toIso8601String()),
          unlockedAchievementIds: List<String>.from(doc['unlockedAchievementIds'] ?? []),
        );
      }
      return UserGamification(userId: userId, lastActivityDate: DateTime.now());
    });
  }

  Future<UserGamification> getUserStats(String userId) async {
    final doc = await _firestore.collection('gamification').doc(userId).get();
    if (doc.exists) {
      return UserGamification(
        userId: userId,
        currentXp: doc['currentXp'] ?? 0,
        currentStreak: doc['currentStreak'] ?? 0,
        lastActivityDate: DateTime.parse(doc['lastActivityDate']),
        unlockedAchievementIds: List<String>.from(doc['unlockedAchievementIds'] ?? []),
      );
    }
    return UserGamification(userId: userId, lastActivityDate: DateTime.now());
  }

  Future<void> addXp(String userId, int amount) async {
    final stats = await getUserStats(userId);
    final updatedXp = stats.currentXp + amount;

    await _firestore.collection('gamification').doc(userId).set({
      'currentXp': updatedXp,
      'lastActivityDate': DateTime.now().toIso8601String(),
    }, SetOptions(merge: true));
  }

  Future<void> updateStreak(String userId) async {
    final stats = await getUserStats(userId);
    final now = DateTime.now();
    final lastActivity = stats.lastActivityDate;

    int newStreak = stats.currentStreak;
    if (now.difference(lastActivity).inDays == 1) {
      newStreak++;
    } else if (now.difference(lastActivity).inDays > 1) {
      newStreak = 1;
    }

    await _firestore.collection('gamification').doc(userId).set({
      'currentStreak': newStreak,
      'lastActivityDate': now.toIso8601String(),
    }, SetOptions(merge: true));
  }

  Future<List<UserGamification>> getLeaderboard(String classId) async {
    final snapshot = await _firestore
        .collection('gamification')
        .where('classId', isEqualTo: classId)
        .orderBy('currentXp', descending: true)
        .limit(20)
        .get();

    return snapshot.docs.map((doc) => UserGamification(
      userId: doc.id,
      currentXp: doc['currentXp'] ?? 0,
      currentStreak: doc['currentStreak'] ?? 0,
      lastActivityDate: DateTime.parse(doc['lastActivityDate'] ?? DateTime.now().toIso8601String()),
      unlockedAchievementIds: List<String>.from(doc['unlockedAchievementIds'] ?? []),
    )).toList();
  }

  List<Achievement> getAvailableAchievements() {
    return [
      Achievement(id: 'first_login', title: 'Welcome!', description: 'Log in for the first time', iconUrl: 'icon_welcome', xpReward: 100),
      Achievement(id: 'first_mastery', title: 'First Mastery', description: 'Master your first concept', iconUrl: 'icon_first', xpReward: 200),
      Achievement(id: 'concept_master', title: 'Concept Master', description: 'Master 10 concepts', iconUrl: 'icon_master', xpReward: 500),
      Achievement(id: 'streak_7', title: 'Weekly Warrior', description: 'Maintain a 7-day streak', iconUrl: 'icon_streak', xpReward: 1000),
      Achievement(id: 'xp_1000', title: 'Thousandaire', description: 'Earn 1,000 total XP', iconUrl: 'icon_1000', xpReward: 500),
    ];
  }
}
