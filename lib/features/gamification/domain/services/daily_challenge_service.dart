import 'dart:math';

class DailyChallenge {
  final String title;
  final String description;
  final String type;
  final int rewardXp;

  DailyChallenge({required this.title, required this.description, required this.type, required this.rewardXp});
}

class DailyChallengeService {
  final List<DailyChallenge> _pool = [
    DailyChallenge(title: 'Mental Math', description: 'Solve 5 multiplication problems in 60 seconds.', type: 'math', rewardXp: 50),
    DailyChallenge(title: 'Vocabulary Master', description: 'Learn 3 new words and their meanings.', type: 'english', rewardXp: 30),
    DailyChallenge(title: 'Science Observer', description: 'Identify 3 different leaves in your garden.', type: 'science', rewardXp: 40),
    DailyChallenge(title: 'Speed Reader', description: 'Read a short story in less than 2 minutes.', type: 'hindi', rewardXp: 30),
  ];

  DailyChallenge getTodaysChallenge() {
    // Consistent challenge based on day of year
    final dayOfYear = DateTime.now().difference(DateTime(DateTime.now().year, 1, 1)).inDays;
    return _pool[dayOfYear % _pool.length];
  }
}
