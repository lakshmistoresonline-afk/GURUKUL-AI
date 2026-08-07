import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:google_generative_ai/google_generative_ai.dart';
import '../../curriculum/domain/models/concept_node.dart';
import '../../curriculum/domain/models/interactive_activity.dart';

class AiContentFactory {
  final GenerativeModel _model;

  AiContentFactory(String apiKey)
      : _model = GenerativeModel(model: 'gemini-1.5-flash', apiKey: apiKey);

  Future<ConceptNode?> createLessonFromText({
    required String text,
    required String subject,
    required int classLevel,
    required String chapterTitle,
  }) async {
    final prompt = '''
Analyze the following text from an NCERT textbook chapter: "$chapterTitle" for Class $classLevel $subject.
Extract the core concept and create a structured learning journey.

### TEXT
${text.substring(0, text.length > 8000 ? 8000 : text.length)}

### INSTRUCTIONS
Generate a JSON object for a "ConceptNode" model.
Strictly follow this structure:
{
  "id": "string (unique)",
  "topic": "string",
  "introduction": "string (engaging)",
  "realLifeConnection": "string",
  "storyBasedExplanation": "string",
  "childFriendlyExplanation": "string",
  "teacherExplanation": "string",
  "learningObjectives": ["string"],
  "examples": ["string"],
  "misconceptions": ["string"],
  "vocabulary": {"word": "meaning"},
  "activities": [
    {
      "id": "string",
      "type": "matching",
      "data": {"pairs": {"key": "value"}}
    }
  ],
  "practiceExercises": [
    {
      "question": "string",
      "hint": "string",
      "options": ["string"],
      "correctAnswer": "string",
      "explanation": "string"
    }
  ],
  "flashcards": [
    {"front": "string", "back": "string"}
  ],
  "revisionNotes": "string (markdown)",
  "estStudyTime": 30
}

Return ONLY the JSON. No other text.
''';

    try {
      final content = [Content.text(prompt)];
      final response = await _model.generateContent(content);
      final jsonStr = response.text?.replaceAll('```json', '').replaceAll('```', '').trim();

      if (jsonStr == null) return null;

      final Map<String, dynamic> data = jsonDecode(jsonStr);

      return ConceptNode(
        id: data['id'] ?? DateTime.now().millisecondsSinceEpoch.toString(),
        subject: subject,
        classLevel: classLevel,
        chapter: chapterTitle,
        topic: data['topic'] ?? chapterTitle,
        subtopic: '',
        difficulty: Difficulty.intermediate,
        bloomLevel: BloomLevel.understand,
        examWeightage: 5,
        estStudyTime: Duration(minutes: data['estStudyTime'] ?? 20),
        prerequisites: const [],
        dependencies: const [],
        relatedConcepts: const [],
        learningObjectives: List<String>.from(data['learningObjectives'] ?? []),
        examples: List<String>.from(data['examples'] ?? []),
        misconceptions: List<String>.from(data['misconceptions'] ?? []),
        practiceExercises: (data['practiceExercises'] as List? ?? []).map((e) => PracticeExercise(
          question: e['question'] ?? '',
          hint: e['hint'] ?? '',
          options: List<String>.from(e['options'] ?? []),
          correctAnswer: e['correctAnswer'] ?? '',
          explanation: e['explanation'] ?? '',
          isHots: false,
        )).toList(),
        flashcards: (data['flashcards'] as List? ?? []).map((f) => Flashcard(
          front: f['front'] ?? '',
          back: f['back'] ?? '',
        )).toList(),
        revisionNotes: data['revisionNotes'] ?? '',
        mindMapUrl: '',
        commonMistakes: const [],
        vocabulary: Map<String, String>.from(data['vocabulary'] ?? {}),
        interactiveActivities: const [],
        masteryCheckpoints: const [],
        introduction: data['introduction'] ?? '',
        realLifeConnection: data['realLifeConnection'] ?? '',
        storyBasedExplanation: data['storyBasedExplanation'] ?? '',
        childFriendlyExplanation: data['childFriendlyExplanation'] ?? '',
        teacherExplanation: data['teacherExplanation'] ?? '',
        animatedLessonAsset: '',
        videoUrl: 'https://flutter.github.io/assets-for-api-docs/assets/videos/bee.mp4',
        activities: (data['activities'] as List? ?? []).map((a) => InteractiveActivity(
          id: a['id'] ?? '',
          type: ActivityType.values.firstWhere((t) => t.name == a['type'], orElse: () => ActivityType.matching),
          data: a['data'] ?? {},
        )).toList(),
        handsOnActivities: const [],
      );
    } catch (e) {
      debugPrint('Error creating AI lesson: $e');
      return null;
    }
  }
}
