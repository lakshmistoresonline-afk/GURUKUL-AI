import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as p;

void main() async {
  print('--- GURUKUL AI: Batch Enrichment (Multi-Pass Local Ollama) ---');

  final baseDir = Directory('D:/GURUKUL-AI/datasets/processed/chapters');
  if (!baseDir.existsSync()) {
    print('Error: Directory not found: ${baseDir.path}');
    return;
  }

  // Phi-3 is better for JSON, but we will split the work to prevent timeouts
  final model = 'phi3:latest';
  print('Using Model: $model');

  final chapters = baseDir.listSync(recursive: true)
      .whereType<Directory>()
      .where((d) => p.basename(d.path).startsWith('chapter_'))
      .toList();

  print('Found ${chapters.length} total chapters.');

  int enriched = 0;
  int skipped = 0;
  int failed = 0;

  for (var dir in chapters) {
    final lessonFile = File(p.join(dir.path, 'lesson.json'));
    if (!lessonFile.existsSync()) continue;

    final content = await lessonFile.readAsString();
    final Map<String, dynamic> data = jsonDecode(content);

    // Skip if already fully enriched
    final List quizzes = data['practiceExercises'] ?? [];
    if (data['status'] == 'Processed' && quizzes.length >= 5 && (data['storyBasedExplanation'] ?? '').toString().length > 100) {
      skipped++;
      continue;
    }

    final topic = data['topic'] ?? data['chapter'] ?? 'Unknown Topic';
    final subject = data['subject'] ?? 'General';
    final classLevel = data['classLevel'] ?? 5;

    print('\n[$enriched] Processing: $topic ($subject Class $classLevel)...');

    try {
      // PASS 1: Learning Outcomes & Explanations
      print('  Pass 1: Generating Stories & Explanations...');
      final pass1 = await _callOllama(topic, level: classLevel, subject: subject, model: model, type: 'content');

      // PASS 2: Quizzes & Flashcards
      print('  Pass 2: Generating Assessments...');
      final pass2 = await _callOllama(topic, level: classLevel, subject: subject, model: model, type: 'assessment');

      if (pass1 != null && pass2 != null) {
        // Merge data
        data['learningObjectives'] = pass1['outcomes'] ?? data['learningObjectives'] ?? [];
        data['storyBasedExplanation'] = pass1['story'] ?? '';
        data['teacherExplanation'] = pass1['explanation'] ?? '';
        data['vocabulary'] = pass1['vocabulary'] ?? {};

        data['practiceExercises'] = pass2['quizzes'] ?? [];
        data['flashcards'] = pass2['flashcards'] ?? [];

        data['status'] = 'Processed';
        data['generationMetadata'] = {
          'last_processed': DateTime.now().toIso8601String(),
          'method': 'Ollama ($model) Multi-Pass Enrichment'
        };

        await lessonFile.writeAsString(const JsonEncoder.withIndent('  ').convert(data));

        // Save separate files for dashboard compatibility
        if (data['practiceExercises'] != null) {
          await File(p.join(dir.path, 'quiz.json')).writeAsString(const JsonEncoder.withIndent('  ').convert(data['practiceExercises']));
        }
        if (data['flashcards'] != null) {
          await File(p.join(dir.path, 'flashcards.json')).writeAsString(const JsonEncoder.withIndent('  ').convert(data['flashcards']));
        }

        enriched++;
        print('  Done!');
      } else {
        failed++;
        print('  Failed: One or more passes returned null.');
      }
    } catch (e) {
      failed++;
      print('  Error: $e');
    }

    // Limit batch size per run to avoid long-running process timeouts
    if (enriched >= 15) {
       print('\nBatch limit reached (15). Run the script again to process more.');
       break;
    }
  }

  print('\n--- SUMMARY ---');
  print('Total Chapters: ${chapters.length}');
  print('Skipped:        $skipped');
  print('Enriched:       $enriched');
  print('Failed:         $failed');
}

Future<Map<String, dynamic>?> _callOllama(String topic, {required dynamic level, required String subject, required String model, required String type}) async {
  String prompt = '';
  if (type == 'content') {
    prompt = '''
Topic: "$topic" ($subject, Class $level).
You are an expert NCERT teacher. Generate educational content.
Return ONLY JSON:
{
  "outcomes": ["3 specific objectives"],
  "story": "2-paragraph engaging story for a 10yo",
  "explanation": "2-paragraph formal teacher explanation",
  "vocabulary": {"word": "def", "word2": "def"}
}
''';
  } else {
    prompt = '''
Topic: "$topic" ($subject, Class $level).
Generate assessment data.
Return ONLY JSON:
{
  "quizzes": [
    {"question": "string", "options": ["a", "b", "c", "d"], "correctAnswer": "string", "hint": "string", "explanation": "string"}
  ],
  "flashcards": [{"front": "string", "back": "string"}]
}
Count: 5 quizzes, 5 flashcards.
''';
  }

  try {
    final client = HttpClient();
    final request = await client.postUrl(Uri.parse('http://localhost:11434/api/generate'));
    request.write(jsonEncode({
      'model': model,
      'prompt': prompt,
      'stream': false,
      'format': 'json',
      'options': {'temperature': 0.2}
    }));

    final response = await request.close().timeout(const Duration(minutes: 4));
    if (response.statusCode != 200) return null;

    final body = await response.transform(utf8.decoder).join();
    final decoded = jsonDecode(body);
    final responseText = decoded['response'] as String;
    client.close();

    final jsonStr = _extractJson(responseText);
    return jsonDecode(jsonStr) as Map<String, dynamic>;
  } catch (e) {
    print('    API Error ($type): $e');
    return null;
  }
}

String _extractJson(String text) {
  if (text.contains('```json')) {
    return text.split('```json')[1].split('```').first.trim();
  } else if (text.contains('{')) {
    final start = text.indexOf('{');
    final end = text.lastIndexOf('}') + 1;
    if (start != -1 && end > start) {
      return text.substring(start, end);
    }
  }
  return text.trim();
}
