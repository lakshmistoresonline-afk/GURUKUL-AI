class LearningOutcome {
  final String id;
  final String subject;
  final int classLevel;
  final String chapter;
  final List<String> outcomes;

  const LearningOutcome({
    required this.id,
    required this.subject,
    required this.classLevel,
    required this.chapter,
    required this.outcomes,
  });
}

class LearningOutcomesRepository {
  final Map<String, LearningOutcome> _outcomes = {
    'm5_c1': const LearningOutcome(
      id: 'm5_c1',
      subject: 'Mathematics',
      classLevel: 5,
      chapter: 'The Fish Tale',
      outcomes: [
        'Reads and writes large numbers up to crore.',
        'Uses the four fundamental operations in solving problems related to daily life situations.',
        'Estimates the number of fish caught and their value.',
      ],
    ),
    's6_c1': const LearningOutcome(
      id: 's6_c1',
      subject: 'Science',
      classLevel: 6,
      chapter: 'Components of Food',
      outcomes: [
        'Identifies various nutrients present in food.',
        'Understand the importance of a balanced diet.',
        'Explains deficiency diseases caused by lack of nutrients.',
      ],
    ),
  };

  LearningOutcome? getOutcomesForChapter(String chapterId) {
    return _outcomes[chapterId];
  }
}
