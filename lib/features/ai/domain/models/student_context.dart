class StudentContext {
  final String studentId;
  final List<String> strongConcepts;
  final List<String> weakConcepts;
  final String preferredLearningStyle; // visual, auditory, reading, kinesthetic
  final List<String> previousMistakes;
  final double learningSpeed; // 1.0 is normal
  final int currentConfidence; // 1-10

  StudentContext({
    required this.studentId,
    this.strongConcepts = const [],
    this.weakConcepts = const [],
    this.preferredLearningStyle = 'visual',
    this.previousMistakes = const [],
    this.learningSpeed = 1.0,
    this.currentConfidence = 5,
  });

  Map<String, dynamic> toMap() {
    return {
      'studentId': studentId,
      'strongConcepts': strongConcepts,
      'weakConcepts': weakConcepts,
      'preferredLearningStyle': preferredLearningStyle,
      'previousMistakes': previousMistakes,
      'learningSpeed': learningSpeed,
      'currentConfidence': currentConfidence,
    };
  }
}
