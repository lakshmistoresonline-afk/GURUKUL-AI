import 'dart:io';
import 'dart:convert';
import 'package:http/http.dart' as http;

class OllamaClient {
  final String baseUrl = 'http://localhost:11434';
  final String model = 'phi3'; // Using phi3 for better quality

  Future<String> generate(String prompt) async {
    try {
      final response = await http.post(
        Uri.parse('$baseUrl/api/generate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'model': model,
          'prompt': prompt,
          'stream': false,
          'options': {
            'temperature': 0.3,
          }
        }),
      );
      if (response.statusCode == 200) {
        return jsonDecode(response.body)['response'] ?? '';
      }
      return '';
    } catch (e) {
      return '';
    }
  }

  String _extractJson(String text) {
    if (text.contains('```json')) {
      return text.split('```json')[1].split('```').first.trim();
    } else if (text.contains('[')) {
       final start = text.indexOf('[');
       final end = text.lastIndexOf(']') + 1;
       return text.substring(start, end);
    }
    return text.trim();
  }
}

void main() async {
  final client = OllamaClient();
  final chaptersDir = Directory('datasets/processed/chapters');
  int count = 0;

  final classes = ['class_05', 'class_06'];

  for (var className in classes) {
    final classPath = Directory('${chaptersDir.path}/$className');
    if (!classPath.existsSync()) {
      print('Class directory not found: ${classPath.path}');
      continue;
    }

    print('Scanning $className...');
    final entities = classPath.listSync(recursive: true);
    for (var entity in entities) {
      if (count >= 1) break; // LIMIT TO 1 FOR TESTING
      if (entity is Directory && entity.path.contains('chapter_')) {
        final lessonFile = File('${entity.path}/lesson.json');
        if (!lessonFile.existsSync()) continue;

        Map<String, dynamic> lesson;
        try {
          lesson = jsonDecode(await lessonFile.readAsString());
        } catch (e) {
          print('Error reading ${lessonFile.path}: $e');
          continue;
        }

        // Check if enrichment is needed
        bool needsEnrichment = lesson['status'] != 'Processed' ||
            (lesson['learningOutcomes'] ?? '').toString().isEmpty ||
            (lesson['storyBasedExplanation'] ?? '').toString().contains('Quest for Knowledge') ||
            (lesson['storyBasedExplanation'] ?? '').toString().contains('Wonderful Waste!') || // Fix for tinyllama hallucination
            (lesson['practiceExercises'] as List).length < 5 ||
            (lesson['flashcards'] as List).length < 5;

        if (needsEnrichment) {
          print('Enriching ${lesson['id']} - ${lesson['chapter']}...');
          final topic = "${lesson['chapter']} for ${lesson['subject']} Class ${lesson['classLevel']}";

          // 1. Learning Outcomes
          final outcomesPrompt = 'Generate 5 clear learning outcomes for "$topic". Return as a plain string of bullet points. No other text.';
          final outcomes = await client.generate(outcomesPrompt);
          if (outcomes.isNotEmpty) lesson['learningOutcomes'] = outcomes;

          // 2. Story
          final storyPrompt = 'Write a short educational story (max 250 words) about "$topic" to explain the concepts to a Class ${lesson['classLevel']} student. Use a child-friendly tone. No conversational text.';
          final story = await client.generate(storyPrompt);
          if (story.isNotEmpty) lesson['storyBasedExplanation'] = story;

          // 3. Teacher Explanation
          final teacherPrompt = 'Provide a professional teacher explanation for "$topic" following NCERT guidelines and pedagogical best practices for Class ${lesson['classLevel']}. No conversational text.';
          final teacher = await client.generate(teacherPrompt);
          if (teacher.isNotEmpty) lesson['teacherExplanation'] = teacher;

          // 4. Quizzes
          final quizPrompt = 'Generate 5 MCQs for "$topic". Return ONLY a JSON array of objects with keys: question, options (list of 4), correctAnswer, hint, explanation. No other text.';
          final quizResponse = await client.generate(quizPrompt);
          bool hasQuizzes = false;
          if (quizResponse.isNotEmpty) {
            try {
              final jsonStr = client._extractJson(quizResponse);
              final quizzes = jsonDecode(jsonStr) as List;
              if (quizzes.length >= 3) { // At least 3 for progress
                lesson['practiceExercises'] = quizzes;
                await File('${entity.path}/quiz.json').writeAsString(JsonEncoder.withIndent('  ').convert(quizzes));
                hasQuizzes = true;
              }
            } catch (e) {}
          }

          // 5. Flashcards
          final flashPrompt = 'Generate 5 flashcards for "$topic". Return ONLY a JSON array of objects with "front" and "back" keys. No other text.';
          final flashResponse = await client.generate(flashPrompt);
          bool hasFlashcards = false;
          if (flashResponse.isNotEmpty) {
            try {
              final jsonStr = client._extractJson(flashResponse);
              final flashcards = jsonDecode(jsonStr) as List;
              if (flashcards.length >= 3) {
                lesson['flashcards'] = flashcards;
                await File('${entity.path}/flashcards.json').writeAsString(JsonEncoder.withIndent('  ').convert(flashcards));
                hasFlashcards = true;
              }
            } catch (e) {}
          }

          // Update Status only if we made significant progress
          if (outcomes.isNotEmpty && (hasQuizzes || hasFlashcards)) {
            lesson['status'] = 'Processed';
            lesson['generationMetadata'] = {
              'last_processed': DateTime.now().toIso8601String(),
              'method': 'Phi3 Enrichment'
            };

            await lessonFile.writeAsString(JsonEncoder.withIndent('  ').convert(lesson));
            count++;
            print('Successfully enriched ${lesson['id']}');
          } else {
            print('Incomplete enrichment for ${lesson['id']}, not marking as processed.');
          }
        }
      }
    }
  }

  print('TOTAL_ENRICHED: $count');
}
