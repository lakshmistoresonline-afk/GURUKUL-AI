import '../../features/curriculum/domain/models/concept_node.dart';
import '../../features/curriculum/domain/models/interactive_activity.dart';

/// Abstract interface for AI providers to ensure modularity and avoid vendor lock-in.
abstract class AIProvider {
  /// Generates a structured response based on a prompt.
  Future<String> generate(String prompt);

  /// Specialized methods for curriculum enrichment.
  Future<String> generateSummary(String topic);
  Future<List<Flashcard>> generateFlashcards(String topic);
  Future<List<PracticeExercise>> generateQuizzes(String topic);
  Future<String> generateRevisionNotes(String topic);
  Future<List<String>> generateLearningOutcomes(String topic);
  Future<Map<String, String>> generateGlossary(String topic);
  Future<List<InteractiveActivity>> generateActivities(String topic);

  /// Generates embeddings for semantic search.
  Future<List<double>> generateEmbeddings(String text);
}
