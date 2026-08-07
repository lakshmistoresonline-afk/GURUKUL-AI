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
    _tabController = TabController(length: 5, vsync: this);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: Text('${widget.subject} Question Centre'),
        bottom: TabBar(
          controller: _tabController,
          isScrollable: true,
          labelColor: DesignSystem.primary,
          unselectedLabelColor: DesignSystem.textSecondary,
          indicatorColor: DesignSystem.primary,
          tabs: const [
            Tab(text: 'Hub'),
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
          _buildHubTab(),
          _buildChapterWiseList(),
          _buildPapersList(),
          _buildRevisionList(),
          _buildAiGeneratorTab(),
        ],
      ),
    );
  }

  Widget _buildHubTab() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHighFidelityHeader(),
          const SizedBox(height: DesignSystem.spacingLg),
          Text('ACTIVE QUESTION BANKS', style: DesignSystem.label),
          const SizedBox(height: DesignSystem.spacingMd),
          _buildQuestionBankItem('Previous Year Questions (PYQ)', '125 Questions', Icons.history_edu, Colors.blue),
          _buildQuestionBankItem('Exemplar Problems', '85 Questions', Icons.star_outline, Colors.orange),
          _buildQuestionBankItem('HOTS (High Order Thinking Skills)', '40 Questions', Icons.psychology, Colors.purple),
          _buildQuestionBankItem('Diagnostic Quiz', '20 Questions', Icons.fact_check_outlined, Colors.green),
          const SizedBox(height: DesignSystem.spacingXl),
          _buildComingSoonSection(),
        ],
      ),
    );
  }

  Widget _buildHighFidelityHeader() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingLg),
      decoration: BoxDecoration(
        gradient: const LinearGradient(colors: [Colors.indigo, Colors.blue]),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
        boxShadow: DesignSystem.shadowMd,
      ),
      child: Row(
        children: [
          const Icon(Icons.help_center_rounded, color: Colors.white, size: 48),
          const SizedBox(width: DesignSystem.spacingMd),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Practice makes perfect!', style: DesignSystem.h2.copyWith(color: Colors.white, fontSize: 18)),
                const SizedBox(height: 4),
                Text('Access thousands of NCERT-aligned questions with AI-powered step-by-step solutions.',
                  style: DesignSystem.bodySmall.copyWith(color: Colors.white.withOpacity(0.9))),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildQuestionBankItem(String title, String count, IconData icon, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: ListTile(
        leading: Container(
          padding: const EdgeInsets.all(8),
          decoration: BoxDecoration(color: color.withOpacity(0.1), borderRadius: BorderRadius.circular(8)),
          child: Icon(icon, color: color),
        ),
        title: Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
        subtitle: Text(count),
        trailing: const Icon(Icons.chevron_right),
        onTap: () {},
      ),
    );
  }

  Widget _buildComingSoonSection() {
    return Center(
      child: Column(
        children: [
          const Icon(Icons.construction_rounded, size: 48, color: DesignSystem.textTertiary),
          const SizedBox(height: 8),
          Text('AI Adaptive Practice', style: DesignSystem.title),
          const SizedBox(height: 4),
          const Text('Coming Soon: Real-time difficulty adjustment based on your performance.',
            textAlign: TextAlign.center,
            style: TextStyle(color: DesignSystem.textTertiary, fontSize: 12)),
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
