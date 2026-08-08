import 'dart:convert';
import '../../curriculum/domain/models/concept_node.dart';
import '../../curriculum/domain/models/interactive_activity.dart';
import '../../../core/ai/ai_provider.dart';
import '../../../core/ai/prompt_manager.dart';

class ModularLessonGenerator {
  final AIProvider _ai;
  final PromptManager _promptManager;

  ModularLessonGenerator(this._ai, this._promptManager);

  Future<String> generateStory({required String topic, required List<String> outcomes}) async {
    final promptTemplate = await _promptManager.getPrompt('story_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic).replaceAll('{{outcomes}}', outcomes.join(", "))
      : 'Generate an engaging story for Class 5-6 students to explain "$topic". Incorporate these learning outcomes: ${outcomes.join(", ")}. Keep it culturally relevant to India.';
    return _ai.generate(prompt);
  }

  Future<String> generateTeacherExplanation({required String topic, required List<String> outcomes}) async {
    final promptTemplate = await _promptManager.getPrompt('teacher_explanation_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic).replaceAll('{{outcomes}}', outcomes.join(", "))
      : 'Generate a formal teacher explanation for "$topic" suitable for an NCERT classroom. Focus on clarity and mapping to outcomes: ${outcomes.join(", ")}.';
    return _ai.generate(prompt);
  }

  Future<String> generateChildExplanation({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('child_explanation_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Explain "$topic" to a 10-year-old child using very simple words and fun analogies.';
    return _ai.generate(prompt);
  }

  Future<List<String>> generateExamples({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('examples_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Provide 5 real-life examples of "$topic" that a student in India would encounter.';
    final response = await _ai.generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<String> generateAnimationScript({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('animation_script_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Write a 2-minute animation script to visualize the concept of "$topic". Include scene descriptions and narration.';
    return _ai.generate(prompt);
  }

  Future<String> generateVideoScript({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('video_script_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Write a script for a teacher-led educational video on "$topic". Include key talking points and overlay text suggestions.';
    return _ai.generate(prompt);
  }

  Future<String> generateParentNotes({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('parent_notes_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Generate a brief note for parents on how to help their child learn "$topic" at home with a simple activity.';
    return _ai.generate(prompt);
  }

  Future<String> generateTeacherNotes({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('teacher_notes_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Generate teaching tips and a lesson plan outline for a teacher covering "$topic".';
    return _ai.generate(prompt);
  }

  Future<String> generateMindMapMarkdown({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('mind_map_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Generate a structured markdown representation of a mind map for "$topic".';
    return _ai.generate(prompt);
  }

  Future<List<Flashcard>> generateFlashcards({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('flashcard_prompt');
    if (promptTemplate.isNotEmpty) {
      final prompt = promptTemplate.replaceAll('{{topic}}', topic);
      final response = await _ai.generate(prompt);
      try {
        final decoded = jsonDecode(_extractJson(response));
        final data = decoded is List ? decoded : [];
        return data.map((f) => Flashcard.fromMap(Map<String, dynamic>.from(f))).toList();
      } catch (_) {
        return [];
      }
    }
    return _ai.generateFlashcards(topic);
  }

  Future<List<PracticeExercise>> generateQuizzes({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('quiz_prompt');
    if (promptTemplate.isNotEmpty) {
      final prompt = promptTemplate.replaceAll('{{topic}}', topic);
      final response = await _ai.generate(prompt);
      try {
        final decoded = jsonDecode(_extractJson(response));
        final data = decoded is List ? decoded : [];
        return data.map((e) => PracticeExercise.fromMap(Map<String, dynamic>.from(e))).toList();
      } catch (_) {
        return [];
      }
    }
    return _ai.generateQuizzes(topic);
  }

  Future<List<String>> generatePrerequisites({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('prerequisites_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Identify 3 conceptual prerequisites a student must know before learning "$topic".';
    final response = await _ai.generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<String> generateImportantNotes({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('important_notes_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Generate important exam-oriented notes and "points to remember" for "$topic".';
    return _ai.generate(prompt);
  }

  Future<List<String>> generateKeyTakeaways({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('learning_outcomes_prompt');
    if (promptTemplate.isNotEmpty) {
       final prompt = promptTemplate.replaceAll('{{topic}}', topic);
       final response = await _ai.generate(prompt);
       return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
    }
    return _ai.generateLearningOutcomes(topic);
  }

  Future<List<String>> generateCommonMistakes({required String topic}) async {
    final prompt = 'Identify 3 common mistakes or misconceptions students have about "$topic".';
    final response = await _ai.generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<Map<String, String>> generateFAQs({required String topic}) async {
    final prompt = 'Generate 3 Frequently Asked Questions and their answers for "$topic". Format as JSON: {"Q1": "A1", ...}';
    final response = await _ai.generate(prompt);
    try {
      final jsonStr = _extractJson(response);
      return Map<String, String>.from(jsonDecode(jsonStr));
    } catch (e) {
      return {};
    }
  }

  Future<List<InteractiveActivity>> generateActivities({required String topic}) async {
    return _ai.generateActivities(topic);
  }

  Future<List<String>> generateSocraticPrompts({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('socratic_prompts_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Provide 3 Socratic questions that an AI tutor could ask to help a student discover the concept of "$topic" themselves.';
    final response = await _ai.generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  Future<List<String>> generateIllustrationPrompts({required String topic}) async {
    final promptTemplate = await _promptManager.getPrompt('illustration_prompts_prompt');
    final prompt = promptTemplate.isNotEmpty
      ? promptTemplate.replaceAll('{{topic}}', topic)
      : 'Provide 3 detailed prompts for an AI image generator to create educational illustrations for "$topic".';
    final response = await _ai.generate(prompt);
    return response.split('\n').where((s) => s.trim().isNotEmpty).toList();
  }

  String _extractJson(String text) {
    if (text.contains('```json')) {
      return text.split('```json')[1].split('```').first.trim();
    } else if (text.contains('{')) {
      final start = text.indexOf('{');
      final end = text.lastIndexOf('}') + 1;
      return text.substring(start, end);
    }
    return text.trim();
  }
}
