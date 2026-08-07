import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/concept_node.dart';
import 'package:project_gurukul_ai/features/content/data/modular_lesson_generator.dart';
import 'package:project_gurukul_ai/features/content/data/learning_outcomes_repository.dart';

class LessonEditorScreen extends StatefulWidget {
  final ConceptNode? existingLesson;
  final String chapterId;

  const LessonEditorScreen({super.key, this.existingLesson, required this.chapterId});

  @override
  State<LessonEditorScreen> createState() => _LessonEditorScreenState();
}

class _LessonEditorScreenState extends State<LessonEditorScreen> {
  late ConceptNode _lesson;
  bool _isGenerating = false;

  @override
  void initState() {
    super.initState();
    _lesson = widget.existingLesson ?? _createEmptyLesson();
  }

  ConceptNode _createEmptyLesson() {
    return ConceptNode(
      id: widget.chapterId,
      subject: 'Science',
      classLevel: 6,
      chapter: 'Chapter',
      topic: 'Topic',
      subtopic: '',
      difficulty: Difficulty.beginner,
      bloomLevel: BloomLevel.remember,
      examWeightage: 1,
      estStudyTime: const Duration(minutes: 30),
      prerequisites: const [],
      dependencies: const [],
      relatedConcepts: const [],
      learningObjectives: const [],
      examples: const [],
      misconceptions: const [],
    );
  }

  Future<void> _generatePart(String type) async {
    setState(() => _isGenerating = true);
    final gen = sl<ModularLessonGenerator>();
    final outcomesRepo = sl<LearningOutcomesRepository>();
    final outcomes = outcomesRepo.getOutcomesForChapter(widget.chapterId)?.outcomes ?? [];

    try {
      ConceptNode updatedLesson = _lesson;
      switch (type) {
        case 'Story':
          final story = await gen.generateStory(topic: _lesson.topic, outcomes: outcomes);
          updatedLesson = _updateLessonField(updatedLesson, 'storyBasedExplanation', story);
          break;
        case 'Teacher Explanation':
          final exp = await gen.generateTeacherExplanation(topic: _lesson.topic, outcomes: outcomes);
          updatedLesson = _updateLessonField(updatedLesson, 'teacherExplanation', exp);
          break;
        case 'Quizzes':
          final quizzes = await gen.generateQuizzes(topic: _lesson.topic);
          updatedLesson = _updateLessonField(updatedLesson, 'practiceExercises', quizzes);
          break;
        case 'Flashcards':
          final cards = await gen.generateFlashcards(topic: _lesson.topic);
          updatedLesson = _updateLessonField(updatedLesson, 'flashcards', cards);
          break;
      }
      setState(() {
        _lesson = updatedLesson;
        _isGenerating = false;
      });
    } catch (e) {
      setState(() => _isGenerating = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Generation failed: $e')));
    }
  }

  ConceptNode _updateLessonField(ConceptNode lesson, String field, dynamic value) {
    final map = lesson.toMap();
    map[field] = value;
    return ConceptNode.fromMap(map);
  }

  Future<void> _saveLesson() async {
    setState(() => _isGenerating = true);
    try {
      await sl<FrameworkRepository>().saveConceptNode(_lesson);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(content: Text('Lesson saved to Content Repository')));
        Navigator.pop(context);
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Save failed: $e')));
      }
    } finally {
      setState(() => _isGenerating = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Editing: ${_lesson.topic}')),
      body: _isGenerating
        ? const Center(child: CircularProgressIndicator())
        : ListView(
            padding: const EdgeInsets.all(16),
            children: [
              _buildSectionHeader('Basic Info'),
              TextFormField(
                initialValue: _lesson.topic,
                decoration: const InputDecoration(labelText: 'Topic Title'),
                onChanged: (v) => _lesson = _updateLessonField(_lesson, 'topic', v),
              ),
              const SizedBox(height: 24),
              _buildGeneratorRow(),
              const SizedBox(height: 24),
              _buildField('Story', _lesson.storyBasedExplanation),
              _buildField('Teacher Explanation', _lesson.teacherExplanation),
              _buildListField('Quizzes', _lesson.practiceExercises.map((e) => e.question).toList()),
              _buildListField('Flashcards', _lesson.flashcards.map((f) => f.front).toList()),
            ],
          ),
      floatingActionButton: FloatingActionButton(
        onPressed: _saveLesson,
        child: const Icon(Icons.save),
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8),
      child: Text(title, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
    );
  }

  Widget _buildGeneratorRow() {
    return Wrap(
      spacing: 8,
      children: ['Story', 'Teacher Explanation', 'Quizzes', 'Flashcards'].map((type) => ActionChip(
        avatar: const Icon(Icons.auto_awesome, size: 16),
        label: Text('Generate $type'),
        onPressed: () => _generatePart(type),
      )).toList(),
    );
  }

  Widget _buildField(String label, String value) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSectionHeader(label),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(8)),
          child: Text(value.isEmpty ? 'Not generated yet.' : value, maxLines: 5, overflow: TextOverflow.ellipsis),
        ),
      ],
    );
  }

  Widget _buildListField(String label, List<String> items) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        _buildSectionHeader(label),
        if (items.isEmpty)
          const Text('No items yet.')
        else
          ...items.map((i) => ListTile(title: Text(i), dense: true)),
      ],
    );
  }
}
