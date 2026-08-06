import 'package:google_generative_ai/google_generative_ai.dart';
import '../../curriculum/domain/models/concept_node.dart';
import '../../curriculum/domain/models/mastery.dart';
import '../../../core/utils/input_validation_util.dart';

class AiTutorService {
  final GenerativeModel _model;

  AiTutorService(String apiKey)
      : _model = GenerativeModel(model: 'gemini-1.5-flash', apiKey: apiKey);

  Future<String> getTeacherExplanation(ConceptNode concept) async {
    final prompt = '''
You are a formal and structured NCERT teacher. Explain the following concept:
Subject: ${concept.subject}
Chapter: ${concept.chapter}
Topic: ${concept.topic}
Learning Objectives: ${concept.learningObjectives.join(', ')}

Instructions:
1. Provide a formal definition.
2. Link it to the NCERT curriculum standards.
3. Use a structured, classroom-like tone.
''';
    return _generate(prompt);
  }

  Future<String> getChildFriendlyExplanation(ConceptNode concept) async {
    final prompt = '''
You are a friendly and fun older sibling. Explain this to a ${concept.classLevel}-year-old:
Topic: ${concept.topic} - ${concept.subtopic}
Examples to use: ${concept.examples.join(', ')}

Instructions:
1. Use very simple words.
2. Use the provided examples to make it relatable.
3. Be very encouraging.
4. Address this common mistake if possible: ${concept.commonMistakes.join(', ')}
''';
    return _generate(prompt);
  }

  Future<String> getStepByStepExplanation(ConceptNode concept) async {
    final prompt = '''
Provide a clear, numbered step-by-step guide for:
Concept: ${concept.topic}
Context: ${concept.revisionNotes}

Instructions:
1. Break it down into 3-5 logical steps.
2. Each step should be actionable.
3. Perfect for a student who is seeing this for the first time.
''';
    return _generate(prompt);
  }

  Future<String> getExamPrepMode(ConceptNode concept) async {
    final prompt = '''
You are an Exam Coach. Prepare the student for an upcoming test on:
Topic: ${concept.topic}
Weightage: ${concept.examWeightage}/10

Instructions:
1. List 3 "Must-Know" points based on learning objectives: ${concept.learningObjectives.join(', ')}
2. Warn about these common mistakes: ${concept.commonMistakes.join(', ')}
3. Provide one "HOTS" (Higher Order Thinking Skills) challenge question.
''';
    return _generate(prompt);
  }

  Future<String> getHomeworkHelpMode(String question, ConceptNode concept) async {
    final prompt = '''
A student needs help with this homework question: "$question"
Related Topic: ${concept.topic}

Instructions:
1. Do NOT give the direct answer.
2. Explain the logic or formula needed.
3. Ask a guiding question to help them solve the first step.
4. Use the Socratic method.
''';
    return _generate(prompt);
  }

  Future<String> getRevisionSummary(ConceptNode concept) async {
    final prompt = '''
Create a "Fast Revision" summary for:
Topic: ${concept.topic} - ${concept.subtopic}

Instructions:
1. Use bullet points.
2. Include the 5 most important keywords/vocabulary words and their meanings.
3. Summarize the core concept in 2 sentences.
''';
    return _generate(prompt);
  }

  Future<String> getParentExplanation(ConceptNode concept) async {
    final prompt = '''
You are an educational consultant talking to a parent.
The student is learning: ${concept.topic}

Instructions:
1. Explain why this concept is important for their child's development.
2. Suggest one simple activity they can do at home to reinforce this.
3. Keep the tone professional but empathetic.
''';
    return _generate(prompt);
  }

  Future<String> getAssessmentHint({
    required String questionText,
    required String? previousAttempt,
    required ConceptNode concept,
  }) async {
    final prompt = '''
You are Gurukul AI, a helpful Socratic tutor. A Class ${concept.classLevel} student is stuck on this question:
"$questionText"

${previousAttempt != null ? 'Their previous incorrect attempt was: "$previousAttempt"' : ''}

### INSTRUCTIONS
Give a small hint that helps them think about the right answer without giving it away.
Relate it to the concept: ${concept.topic} - ${concept.subtopic}.
Use the Socratic method.
''';
    return _generate(prompt);
  }

  Future<String> getHelp({
    required String userQuery,
    required ConceptNode concept,
    required Mastery mastery,
    List<Mastery>? prerequisiteMastery,
    String language = 'en',
  }) async {
    final sanitizedQuery = InputValidationUtil.sanitizeText(userQuery);
    if (sanitizedQuery.isEmpty) return "Please ask a question so I can help you!";

    final prereqsStatus = prerequisiteMastery != null
        ? prerequisiteMastery.map((m) => '${m.conceptId}: ${(m.masteryScore * 100).toStringAsFixed(0)}%').join(', ')
        : 'Unknown';

    final languageInstruction = language == 'hi'
        ? 'Please respond primarily in Hindi, but use English technical terms from the NCERT textbook.'
        : 'Respond in English, keeping the language simple for a ${concept.classLevel}-year-old.';

    final prompt = '''
You are Gurukul AI, a highly intelligent and empathetic Socratic tutor for NCERT Class ${concept.classLevel} students.

### LANGUAGE
$languageInstruction

### GOAL
Guide the student to understand "${concept.topic}" without directly giving away the final answer. Use the Socratic method: ask guiding questions, provide hints, and relate to things they already know.

### STUDENT CONTEXT
- Subject: ${concept.subject}
- Target Concept: ${concept.topic} - ${concept.subtopic}
- Current Mastery of this Concept: ${(mastery.masteryScore * 100).toStringAsFixed(0)}%
- Mastery of Prerequisites: $prereqsStatus

### NCERT BOUNDARIES
- Stay within the learning objectives: ${concept.learningObjectives.join(', ')}
- Use simple, encouraging language for a ${concept.classLevel}-year-old.
- Address these common misconceptions if the student seems stuck: ${concept.misconceptions.join(', ')}

### INSTRUCTIONS
1. Analyze the student's question: "$sanitizedQuery"
2. If the mastery of prerequisites is low, gently remind them of a foundational concept.
3. Use examples from the NCERT textbook context if possible: ${concept.examples.join(', ')}
4. Use the Socratic Method:
   - Example 1: If stuck on "Lakhs", don't say "it's 5 zeros". Ask: "How many zeros are in 10,000? And what comes after ten thousand?"
   - Example 2: If stuck on "Fractions", ask: "If you cut a pizza into 4 equal parts and eat one, how many are left?"
5. Keep responses concise and focused on one small step at a time.
''';
    return _generate(prompt);
  }

  Future<String> _generate(String prompt) async {
    final content = [Content.text(prompt)];
    final response = await _model.generateContent(content);
    return response.text ?? "I'm sorry, I'm having trouble thinking right now. Please try again later.";
  }
}
