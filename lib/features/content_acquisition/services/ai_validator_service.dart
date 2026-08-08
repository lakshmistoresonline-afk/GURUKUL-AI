import '../../curriculum/domain/models/concept_node.dart';

/// Production-grade validation for AI-enriched curriculum content.
class AIValidatorService {

  /// Performs a multi-point validation of the [ConceptNode].
  bool validate(ConceptNode node) {
    // 1. Mandatory Metadata
    if (node.id.isEmpty) return false;
    if (node.topic.isEmpty) return false;
    if (node.subject.isEmpty) return false;

    // 2. Content Density
    if (node.introduction.length < 50) return false;
    if (node.teacherExplanation.length < 100) return false;
    if (node.storyBasedExplanation.length < 100) return false;

    // 3. Assessment Integrity
    if (node.practiceExercises.length < 3) return false; // Minimum 3 quizzes
    if (node.flashcards.length < 3) return false;      // Minimum 3 flashcards

    // Check for duplicate questions (strict)
    final questions = node.practiceExercises.map((e) => e.question.toLowerCase().trim()).toSet();
    if (questions.length < node.practiceExercises.length) return false;

    // Validate individual exercises
    for (final exercise in node.practiceExercises) {
      if (exercise.question.isEmpty) return false;
      if (exercise.options.length < 2) return false;
      if (exercise.options.any((o) => o.isEmpty)) return false;
      if (exercise.correctAnswer.isEmpty) return false;

      // Ensure correct answer is actually in the options
      if (!exercise.options.contains(exercise.correctAnswer)) return false;
    }

    // 4. Learning Objectives
    if (node.learningObjectives.isEmpty) return false;
    if (node.learningObjectives.any((o) => o.length < 10)) return false;

    // 5. Vocabulary
    if (node.vocabulary.isEmpty) return false;

    return true;
  }

  /// Calculates a quality score (0.0 to 1.0) for the generated node.
  double calculateQualityScore(ConceptNode node) {
    double score = 0.0;

    if (node.introduction.length > 200) score += 0.2;
    if (node.practiceExercises.length >= 5) score += 0.2;
    if (node.flashcards.length >= 5) score += 0.2;
    if (node.vocabulary.length >= 5) score += 0.2;
    if (node.learningObjectives.length >= 3) score += 0.2;

    return score;
  }
}
