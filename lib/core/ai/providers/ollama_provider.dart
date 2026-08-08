import 'dart:convert';
import 'package:http/http.dart' as http;
import '../ai_provider.dart';
import '../../../features/curriculum/domain/models/concept_node.dart';
import '../../../features/curriculum/domain/models/interactive_activity.dart';

class OllamaProvider implements AIProvider {
  final String baseUrl;
  final String model;
  final String embeddingModel;

  OllamaProvider({
    this.baseUrl = 'http://localhost:11434',
    this.model = 'phi3:latest',
    this.embeddingModel = 'mxbai-embed-large',
  });

  @override
  Future<String> generate(String prompt) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/generate'),
        body: jsonEncode({
          'model': model,
          'prompt': prompt,
          'stream': false,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['response'] ?? '';
      }
      return 'Error: Ollama returned ${response.statusCode}';
    } catch (e) {
      return 'Error connecting to Ollama: $e';
    }
  }

  @override
  Future<String> generateSummary(String topic) async {
    return generate('Generate a concise educational summary for the topic "$topic" suitable for Class 5-6 students. Focus on clarity and simplicity.');
  }

  @override
  Future<List<Flashcard>> generateFlashcards(String topic) async {
    final prompt = 'Generate 5 flashcards (front and back) for "$topic". Return ONLY a JSON list of objects with "front" and "back" keys. No conversational text.';
    final response = await generate(prompt);
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
    final prompt = 'Generate 5 multiple-choice questions for "$topic". Return ONLY a JSON list of objects with "question", "options" (list of 4), "correctAnswer", "hint", and "explanation" keys. No conversational text.';
    final response = await generate(prompt);
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
    return generate('Generate bulleted revision notes for "$topic" focused on NCERT exam preparation for Class 5-6.');
  }

  @override
  Future<List<String>> generateLearningOutcomes(String topic) async {
    final response = await generate('List 5 clear, actionable learning outcomes for "$topic". Start each with a bullet point.');
    return response.split('\n').where((s) => s.trim().isNotEmpty && s.contains('•')).map((s) => s.replaceAll('•', '').trim()).toList();
  }

  @override
  Future<Map<String, String>> generateGlossary(String topic) async {
    final prompt = 'Provide a glossary of 5 key terms for "$topic". Return ONLY a JSON object where keys are terms and values are definitions. No conversational text.';
    final response = await generate(prompt);
    try {
      return Map<String, String>.from(jsonDecode(_extractJson(response)));
    } catch (_) {
      return {};
    }
  }

  @override
  Future<List<InteractiveActivity>> generateActivities(String topic) async {
    final prompt = 'Design 2 interactive activities for "$topic". Return ONLY a JSON list matching this model: [{"id": "unique_id", "type": "matching", "title": "Activity Title", "instruction": "Step by step", "data": {"pairs": {"key": "value"}}}]. Valid types: matching, tapReveal. No conversational text.';
    final response = await generate(prompt);
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
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/embeddings'),
        body: jsonEncode({
          'model': embeddingModel,
          'prompt': text,
        }),
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return List<double>.from(data['embedding'] ?? []);
      }
      return [];
    } catch (e) {
      return [];
    }
  }

  String _extractJson(String text) {
    if (text.contains('```json')) {
      return text.split('```json')[1].split('```').first.trim();
    } else if (text.contains('[')) {
       // Try to find the first array
       final start = text.indexOf('[');
       final end = text.lastIndexOf(']') + 1;
       return text.substring(start, end);
    } else if (text.contains('{')) {
       // Try to find the first object
       final start = text.indexOf('{');
       final end = text.lastIndexOf('}') + 1;
       return text.substring(start, end);
    }
    return text.trim();
  }
}
