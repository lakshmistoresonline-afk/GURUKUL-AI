import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../data/question_repository.dart';
import '../../domain/models/question_paper.dart';
import 'exam_generator_screen.dart';

class QuestionCenterScreen extends StatefulWidget {
  final int classLevel;
  final String subject;

  const QuestionCenterScreen({super.key, required this.classLevel, required this.subject});

  @override
  State<QuestionCenterScreen> createState() => _QuestionCenterScreenState();
}

class _QuestionCenterScreenState extends State<QuestionCenterScreen> {
  late Future<List<QuestionPaper>> _papersFuture;

  @override
  void initState() {
    super.initState();
    _papersFuture = sl<QuestionRepository>().getPapers(widget.classLevel, widget.subject);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Question Center'),
        actions: [
          IconButton(onPressed: () {}, icon: const Icon(Icons.search)),
          IconButton(onPressed: () {}, icon: const Icon(Icons.bookmark_border)),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildAiGeneratorBanner(context),
            const SizedBox(height: 32),
            const Text('Exam Papers', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildPapersList(),
            const SizedBox(height: 32),
            const Text('Practice by Category', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildCategoryGrid(),
          ],
        ),
      ),
    );
  }

  Widget _buildAiGeneratorBanner(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [Colors.blue.shade700, Colors.blue.shade400]),
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        children: [
          const Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('AI Practice Paper', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 20)),
                SizedBox(height: 4),
                Text('Generate a custom test paper with AI', style: TextStyle(color: Colors.white70)),
              ],
            ),
          ),
          ElevatedButton(
            onPressed: () => Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => ExamGeneratorScreen(classLevel: widget.classLevel, subject: widget.subject))
            ),
            child: const Text('Generate'),
          ),
        ],
      ),
    );
  }

  Widget _buildPapersList() {
    return FutureBuilder<List<QuestionPaper>>(
      future: _papersFuture,
      builder: (context, snapshot) {
        // Return dummy data if empty for demonstration
        final papers = [
          {'title': 'Annual Exam 2024', 'type': 'Previous Year', 'marks': '80'},
          {'title': 'Mid-Term 2023', 'type': 'Previous Year', 'marks': '40'},
          {'title': 'Unit Test - Numbers', 'type': 'Sample', 'marks': '20'},
        ];

        return Column(
          children: papers.map((p) => Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: ListTile(
              leading: const Icon(Icons.description, color: Colors.blue),
              title: Text(p['title']!, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text('${p['type']} • ${p['marks']} Marks'),
              trailing: const Icon(Icons.download, size: 18),
              onTap: () {},
            ),
          )).toList(),
        );
      },
    );
  }

  Widget _buildCategoryGrid() {
    final categories = [
      {'name': 'HOTS', 'icon': Icons.flash_on, 'color': Colors.red},
      {'name': 'Important', 'icon': Icons.star, 'color': Colors.amber},
      {'name': 'Revision', 'icon': Icons.history, 'color': Colors.green},
      {'name': 'Question Bank', 'icon': Icons.account_balance, 'color': Colors.purple},
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 16,
        mainAxisSpacing: 16,
        childAspectRatio: 2.5,
      ),
      itemCount: categories.length,
      itemBuilder: (context, index) {
        final c = categories[index];
        return Container(
          decoration: BoxDecoration(
            color: (c['color'] as Color).withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
            border: Border.all(color: (c['color'] as Color).withOpacity(0.2)),
          ),
          child: Center(
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                Icon(c['icon'] as IconData, color: c['color'] as Color, size: 20),
                const SizedBox(width: 8),
                Text(c['name'] as String, style: TextStyle(fontWeight: FontWeight.bold, color: c['color'] as Color)),
              ],
            ),
          ),
        );
      },
    );
  }
}
