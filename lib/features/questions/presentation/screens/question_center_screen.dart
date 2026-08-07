import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/features/questions/presentation/screens/exam_generator_screen.dart';

class QuestionCenterScreen extends StatefulWidget {
  final int classLevel;
  final String subject;

  const QuestionCenterScreen({super.key, required this.classLevel, required this.subject});

  @override
  State<QuestionCenterScreen> createState() => _QuestionCenterScreenState();
}

class _QuestionCenterScreenState extends State<QuestionCenterScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: const Text('Question Centre'),
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          labelColor: DesignSystem.primary,
          unselectedLabelColor: DesignSystem.textSecondary,
          indicatorColor: DesignSystem.primary,
          tabs: const [
            Tab(text: 'Chapter-wise'),
            Tab(text: 'Papers'),
            Tab(text: 'Revision'),
            Tab(text: 'AI Generator'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildChapterWiseList(),
          _buildPapersList(),
          _buildRevisionList(),
          _buildAiGeneratorTab(),
        ],
      ),
    );
  }

  Widget _buildChapterWiseList() {
    return ListView.builder(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      itemCount: 10,
      itemBuilder: (context, index) {
        return Card(
          margin: const EdgeInsets.only(bottom: DesignSystem.spacingMd),
          child: ExpansionTile(
            title: Text('Chapter ${index + 1}: Living Organisms', style: const TextStyle(fontWeight: FontWeight.bold)),
            children: [
              ListTile(
                leading: const Icon(Icons.quiz, color: Colors.blue),
                title: const Text('Concept Check Questions'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {},
              ),
              ListTile(
                leading: const Icon(Icons.flash_on, color: Colors.orange),
                title: const Text('HOTS Questions'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {},
              ),
              ListTile(
                leading: const Icon(Icons.history, color: Colors.purple),
                title: const Text('Previous Year Questions'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {},
              ),
            ],
          ),
        );
      },
    );
  }

  Widget _buildPapersList() {
    final papers = [
      {'title': 'Annual Exam 2024', 'marks': '80', 'time': '3h'},
      {'title': 'Mid-Term 2023', 'marks': '40', 'time': '1.5h'},
      {'title': 'Unit Test 1', 'marks': '20', 'time': '45m'},
    ];
    return ListView.builder(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      itemCount: papers.length,
      itemBuilder: (context, index) {
        final p = papers[index];
        return Card(
          child: ListTile(
            leading: const Icon(Icons.description, color: Colors.blue),
            title: Text(p['title']!, style: const TextStyle(fontWeight: FontWeight.bold)),
            subtitle: Text('Marks: ${p['marks']} • Duration: ${p['time']}'),
            trailing: const Icon(Icons.download),
            onTap: () {},
          ),
        );
      },
    );
  }

  Widget _buildRevisionList() {
    return ListView(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      children: [
        _buildRevisionCard('Wrongly Answered', '15 Questions', Icons.error_outline, Colors.red),
        _buildRevisionCard('Bookmarked', '8 Questions', Icons.bookmark_border, Colors.blue),
        _buildRevisionCard('Frequently Missed', 'Concepts you struggle with', Icons.psychology, Colors.orange),
      ],
    );
  }

  Widget _buildRevisionCard(String title, String subtitle, IconData icon, Color color) {
    return Card(
      child: ListTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: color.withOpacity(0.1), shape: BoxShape.circle),
          child: Icon(icon, color: color),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle),
        trailing: const Icon(Icons.chevron_right),
        onTap: () {},
      ),
    );
  }

  Widget _buildAiGeneratorTab() {
    return Padding(
      padding: const EdgeInsets.all(DesignSystem.spacingLg),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.auto_awesome, size: 80, color: Colors.purple),
          const SizedBox(height: 24),
          const Text(
            'Personalized Exam Generator',
            style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 12),
          const Text(
            'Gurukul AI can create a custom practice paper based on your weak areas and latest NCERT patterns.',
            textAlign: TextAlign.center,
            style: TextStyle(color: Colors.grey),
          ),
          const SizedBox(height: 48),
          FilledButton.icon(
            onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ExamGeneratorScreen(classLevel: widget.classLevel, subject: widget.subject))),
            icon: const Icon(Icons.bolt),
            label: const Text('Generate Now'),
            style: FilledButton.styleFrom(
              padding: const EdgeInsets.symmetric(horizontal: 40, vertical: 16),
              backgroundColor: Colors.purple,
            ),
          ),
        ],
      ),
    );
  }
}
