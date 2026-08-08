import 'dart:convert';
import 'package:google_generative_ai/google_generative_ai.dart';
import '../ai_provider.dart';
import '../../../features/curriculum/domain/models/concept_node.dart';
import '../../../features/curriculum/domain/models/interactive_activity.dart';

class GeminiProvider implements AIProvider {
  final GenerativeModel _model;
  final GenerativeModel _embeddingModel;

  GeminiProvider(String apiKey)
      : _model = GenerativeModel(model: 'gemini-1.5-flash', apiKey: apiKey),
        _embeddingModel = GenerativeModel(model: 'text-embedding-004', apiKey: apiKey);

  @override
  Future<String> generate(String prompt) async {
    final response = await _model.generateContent([Content.text(prompt)]);
    return response.text ?? '';
  }

  @override
  Future<String> generateSummary(String topic) async {
    return generate('Generate a concise educational summary for the topic "$topic" suitable for Class 5-6 students.');
  }

  @override
  Future<List<Flashcard>> generateFlashcards(String topic) async {
    final response = await generate('Generate 5 flashcards (front and back) for "$topic". Format as JSON: [{"front": "", "back": ""}]');
    try {
      final decoded = jsonDecode(_extractJson(response));
      final data = decoded is List ? decoded : [];
      return data.map((f) => Flashcard.fromMap(Map<String, dynamic>.from(f))).toList();
    } catch (_) {
      return [];
    }
  }

  @override
  Future<List<PracticeExercise>> generateQuizzes(String topic) async {
    final response = await generate('Generate 5 multiple-choice questions for "$topic". Include hint and explanation. Format as JSON: [{"question": "", "options": [], "correctAnswer": "", "hint": "", "explanation": ""}]');
    try {
      final decoded = jsonDecode(_extractJson(response));
      final data = decoded is List ? decoded : [];
      return data.map((e) => PracticeExercise.fromMap(Map<String, dynamic>.from(e))).toList();
    } catch (_) {
      return [];
    }
  }

  @override
  Future<String> generateRevisionNotes(String topic) async {
    return generate('Generate bulleted revision notes for "$topic" focused on exam preparation for Class 5-6.');
  }

  @override
  Future<List<String>> generateLearningOutcomes(String topic) async {
    final response = await generate('List 5 clear learning outcomes for "$topic".');
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  @override
  Future<Map<String, String>> generateGlossary(String topic) async {
    final response = await generate('Provide a glossary of 5 key terms for "$topic". Format as JSON: {"term": "definition"}');
    try {
      return Map<String, String>.from(jsonDecode(_extractJson(response)));
    } catch (_) {
      return {};
    }
  }

  @override
  Future<List<InteractiveActivity>> generateActivities(String topic) async {
    final response = await generate('Design 2 interactive activities for "$topic". Format as JSON matching InteractiveActivity model: [{"id": "", "type": "matching/sorting/etc", "title": "", "instruction": "", "data": {}}]');
    try {
      final decoded = jsonDecode(_extractJson(response));
      final data = decoded is List ? decoded : [];
      return data.map((a) => InteractiveActivity.fromMap(Map<String, dynamic>.from(a))).toList();
    } catch (_) {
      return [];
    }
  }

  @override
  Future<List<double>> generateEmbeddings(String text) async {
    final content = Content.text(text);
    final result = await _embeddingModel.embedContent(content);
    return result.embedding.values.toList();
  }

  String _extractJson(String text) {
    if (text.contains('```json')) {
      return text.split('```json')[1].split('```').first.trim();
    }
    return text.trim();
  }
}
