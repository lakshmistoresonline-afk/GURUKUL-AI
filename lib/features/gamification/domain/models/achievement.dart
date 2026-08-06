class Achievement {
  final String id;
  final String title;
  final String description;
  final String iconUrl;
  final int xpReward;

  Achievement({
    required this.id,
    required this.title,
    required this.description,
    required this.iconUrl,
    required this.xpReward,
  });
}

class UserGamification {
  final String userId;
  final int currentXp;
  final int currentStreak;
  final DateTime lastActivityDate;
  final List<String> unlockedAchievementIds;

  UserGamification({
    required this.userId,
    this.currentXp = 0,
    this.currentStreak = 0,
    required this.lastActivityDate,
    this.unlockedAchievementIds = const [],
  });

  int get level => (currentXp / 1000).floor() + 1;
}
