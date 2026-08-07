import 'dart:convert';
import 'package:google_generative_ai/google_generative_ai.dart';
import '../../curriculum/domain/models/concept_node.dart';
import '../../curriculum/domain/models/interactive_activity.dart';

class ModularLessonGenerator {
  final GenerativeModel _model;

  ModularLessonGenerator(String apiKey)
      : _model = GenerativeModel(model: 'gemini-1.5-flash', apiKey: apiKey);

  Future<String> generateStory({required String topic, required List<String> outcomes}) async {
    final prompt = 'Generate an engaging story for Class 5-6 students to explain "$topic". Incorporate these learning outcomes: ${outcomes.join(", ")}. Keep it culturally relevant to India.';
    return _generate(prompt);
  }

  Future<String> generateTeacherExplanation({required String topic, required List<String> outcomes}) async {
    final prompt = 'Generate a formal teacher explanation for "$topic" suitable for an NCERT classroom. Focus on clarity and mapping to outcomes: ${outcomes.join(", ")}.';
    return _generate(prompt);
  }

  Future<String> generateChildExplanation({required String topic}) async {
    final prompt = 'Explain "$topic" to a 10-year-old child using very simple words and fun analogies.';
    return _generate(prompt);
  }

  Future<List<String>> generateExamples({required String topic}) async {
    final prompt = 'Provide 5 real-life examples of "$topic" that a student in India would encounter.';
    final response = await _generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<String> generateAnimationScript({required String topic}) async {
    final prompt = 'Write a 2-minute animation script to visualize the concept of "$topic". Include scene descriptions and narration.';
    return _generate(prompt);
  }

  Future<String> generateVideoScript({required String topic}) async {
    final prompt = 'Write a script for a teacher-led educational video on "$topic". Include key talking points and overlay text suggestions.';
    return _generate(prompt);
  }

  Future<String> generateParentNotes({required String topic}) async {
    final prompt = 'Generate a brief note for parents on how to help their child learn "$topic" at home with a simple activity.';
    return _generate(prompt);
  }

  Future<String> generateTeacherNotes({required String topic}) async {
    final prompt = 'Generate teaching tips and a lesson plan outline for a teacher covering "$topic".';
    return _generate(prompt);
  }

  Future<String> generateMindMapMarkdown({required String topic}) async {
    final prompt = 'Generate a structured markdown representation of a mind map for "$topic".';
    return _generate(prompt);
  }

  Future<List<Flashcard>> generateFlashcards({required String topic}) async {
    final prompt = 'Generate 5 flashcards (front and back) for "$topic". Format as JSON: [{"front": "", "back": ""}]';
    final response = await _generate(prompt);
    try {
      final jsonStr = _extractJson(response);
      final List data = jsonDecode(jsonStr);
      return data.map((f) => Flashcard(front: f['front'], back: f['back'])).toList();
    } catch (e) {
      return [];
    }
  }

  Future<List<PracticeExercise>> generateQuizzes({required String topic}) async {
    final prompt = 'Generate 5 multiple-choice questions for "$topic". Include a hint and explanation for each. Format as JSON: [{"question": "", "options": [], "correctAnswer": "", "hint": "", "explanation": ""}]';
    final response = await _generate(prompt);
    try {
      final jsonStr = _extractJson(response);
      final List data = jsonDecode(jsonStr);
      return data.map((e) => PracticeExercise(
        question: e['question'],
        options: List<String>.from(e['options']),
        correctAnswer: e['correctAnswer'],
        hint: e['hint'],
        explanation: e['explanation'],
      )).toList();
    } catch (e) {
      return [];
    }
  }

  // Phase 56 Additions
  Future<List<String>> generatePrerequisites({required String topic}) async {
    final prompt = 'Identify 3 conceptual prerequisites a student must know before learning "$topic".';
    final response = await _generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<String> generateImportantNotes({required String topic}) async {
    final prompt = 'Generate important exam-oriented notes and "points to remember" for "$topic".';
    return _generate(prompt);
  }

  Future<List<String>> generateKeyTakeaways({required String topic}) async {
    final prompt = 'Provide a list of 5 key takeaways or learning outcomes for the topic "$topic".';
    final response = await _generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<List<String>> generateCommonMistakes({required String topic}) async {
    final prompt = 'Identify 3 common mistakes or misconceptions students have about "$topic".';
    final response = await _generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<Map<String, String>> generateFAQs({required String topic}) async {
    final prompt = 'Generate 3 Frequently Asked Questions and their answers for "$topic". Format as JSON: {"Q1": "A1", ...}';
    final response = await _generate(prompt);
    try {
      final jsonStr = _extractJson(response);
      return Map<String, String>.from(jsonDecode(jsonStr));
    } catch (e) {
      return {};
    }
  }

  Future<List<InteractiveActivity>> generateActivities({required String topic}) async {
    final prompt = 'Design 2 interactive learning activities for "$topic" (e.g. matching, sorting). Format as JSON matching the InteractiveActivity model: [{"id": "", "type": "matching/sorting/etc", "title": "", "instruction": "", "data": {}}]';
    final response = await _generate(prompt);
    try {
      final jsonStr = _extractJson(response);
      final List data = jsonDecode(jsonStr);
      return data.map((a) => InteractiveActivity.fromMap(a)).toList();
    } catch (e) {
      return [];
    }
  }

  Future<List<String>> generateSocraticPrompts({required String topic}) async {
    final prompt = 'Provide 3 Socratic questions that an AI tutor could ask to help a student discover the concept of "$topic" themselves.';
    final response = await _generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<List<String>> generateIllustrationPrompts({required String topic}) async {
    final prompt = 'Provide 3 detailed prompts for an AI image generator to create educational illustrations for "$topic".';
    final response = await _generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  String _extractJson(String text) {
    return text.replaceAll('```json', '').replaceAll('```', '').trim();
  }

  Future<String> _generate(String prompt) async {
    final content = [Content.text(prompt)];
    final response = await _model.generateContent(content);
    return response.text ?? "Generation failed.";
  }
}
