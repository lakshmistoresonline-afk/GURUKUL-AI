import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../data/question_repository.dart';
import '../../domain/models/question_paper.dart';

class ExamGeneratorScreen extends StatefulWidget {
  final int classLevel;
  final String subject;

  const ExamGeneratorScreen({super.key, required this.classLevel, required this.subject});

  @override
  State<ExamGeneratorScreen> createState() => _ExamGeneratorScreenState();
}

class _ExamGeneratorScreenState extends State<ExamGeneratorScreen> {
  String _difficulty = 'Medium';
  int _totalMarks = 50;
  bool _isGenerating = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Exam Generator')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Generate Practice Paper for ${widget.subject}', style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const SizedBox(height: 24),
            const Text('Select Difficulty'),
            const SizedBox(height: 8),
            SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'Easy', label: Text('Easy')),
                ButtonSegment(value: 'Medium', label: Text('Medium')),
                ButtonSegment(value: 'Hard', label: Text('Hard')),
              ],
              selected: {_difficulty},
              onSelectionChanged: (v) => setState(() => _difficulty = v.first),
            ),
            const SizedBox(height: 32),
            const Text('Total Marks'),
            Slider(
              value: _totalMarks.toDouble(),
              min: 10,
              max: 100,
              divisions: 9,
              label: '$_totalMarks Marks',
              onChanged: (v) => setState(() => _totalMarks = v.round()),
            ),
            const SizedBox(height: 48),
            SizedBox(
              width: double.infinity,
              height: 56,
              child: FilledButton.icon(
                onPressed: _isGenerating ? null : _generatePaper,
                icon: const Icon(Icons.auto_awesome),
                label: Text(_isGenerating ? 'Generating...' : 'Generate Practice Paper'),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Future<void> _generatePaper() async {
    setState(() => _isGenerating = true);

    // Simulate generation
    await Future.delayed(const Duration(seconds: 2));

    if (mounted) {
      setState(() => _isGenerating = false);
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Paper generated successfully! Check Question Center.')),
      );
      Navigator.pop(context);
    }
  }
}
