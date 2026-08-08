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
    DailyChallenge(title: 'Number Cruncher', description: 'Solve 5 word problems from "The Fish Tale".', type: 'math', rewardXp: 50),
    DailyChallenge(title: 'Vocabulary Master', description: 'Learn 3 new words from the "Ice-cream Man" poem.', type: 'english', rewardXp: 30),
    DailyChallenge(title: 'Nature Scout', description: 'Find 3 objects with different textures like in "Super Senses".', type: 'evs', rewardXp: 40),
    DailyChallenge(title: 'Hindi Scholar', description: 'Read "Raakh ki Rassi" and find 2 new adjectives.', type: 'hindi', rewardXp: 30),
  ];

  DailyChallenge getTodaysChallenge() {
    // Consistent challenge based on day of year
    final dayOfYear = DateTime.now().difference(DateTime(DateTime.now().year, 1, 1)).inDays;
    return _pool[dayOfYear % _pool.length];
  }
}
