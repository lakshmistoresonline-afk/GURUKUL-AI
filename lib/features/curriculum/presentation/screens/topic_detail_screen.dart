import 'package:flutter/material.dart';
import '../../../curriculum/domain/models/concept_node.dart';
import '../../../../core/di/injection.dart';
import '../../../curriculum/data/framework_repository.dart';

import '../../../../core/theme/theme_service.dart';
import '../../../ai/presentation/screens/ai_tutor_chat_screen.dart';

class TopicDetailScreen extends StatefulWidget {
  final String conceptId;

  const TopicDetailScreen({super.key, required this.conceptId});

  @override
  State<TopicDetailScreen> createState() => _TopicDetailScreenState();
}

class _TopicDetailScreenState extends State<TopicDetailScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  ConceptNode? _concept;
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 3, vsync: this);
    _loadConcept();
  }

  Future<void> _loadConcept() async {
    final concept = await sl<FrameworkRepository>().getConceptNode(widget.conceptId);
    setState(() {
      _concept = concept;
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return const Scaffold(body: Center(child: CircularProgressIndicator()));
    }

    if (_concept == null) {
      return const Scaffold(body: Center(child: Text('Concept not found')));
    }

    final themeService = sl<ThemeService>();
    final subjectColor = themeService.getSubjectColor(_concept!.subject);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: Text(_concept!.topic, style: const TextStyle(fontWeight: FontWeight.bold)),
        backgroundColor: Colors.white,
        foregroundColor: Colors.black87,
        elevation: 0,
        bottom: TabBar(
          controller: _tabController,
          labelColor: subjectColor,
          unselectedLabelColor: Colors.grey,
          indicatorColor: subjectColor,
          indicatorWeight: 3,
          tabs: const [
            Tab(text: 'Learn'),
            Tab(text: 'Practice'),
            Tab(text: 'Review'),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildLearnTab(subjectColor),
          _buildPracticeTab(subjectColor),
          _buildReviewTab(subjectColor),
        ],
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => AiTutorChatScreen(concept: _concept!)),
        ),
        backgroundColor: subjectColor,
        icon: const Icon(Icons.smart_toy, color: Colors.white),
        label: const Text('Ask AI Tutor', style: TextStyle(color: Colors.white)),
      ),
    );
  }

  Widget _buildLearnTab(Color subjectColor) {
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        _buildSectionHeader('Learning Objectives', subjectColor),
        const SizedBox(height: 12),
        ..._concept!.learningObjectives.map((o) => Padding(
          padding: const EdgeInsets.only(bottom: 8),
          child: Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(Icons.check_circle, color: subjectColor, size: 20),
              const SizedBox(width: 12),
              Expanded(child: Text(o, style: const TextStyle(fontSize: 15, height: 1.4))),
            ],
          ),
        )),
        const SizedBox(height: 32),
        _buildSectionHeader('Concept Notes', subjectColor),
        const SizedBox(height: 12),
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(20),
            border: Border.all(color: Colors.grey.shade200),
          ),
          child: Text(
            _concept!.revisionNotes,
            style: const TextStyle(fontSize: 16, height: 1.6, color: Colors.black87),
          ),
        ),
        const SizedBox(height: 32),
        _buildSectionHeader('Interactive Activities', subjectColor),
        const SizedBox(height: 12),
        ..._concept!.interactiveActivities.map((a) => Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.amber.shade50,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.amber.shade100),
          ),
          child: Row(
            children: [
              const Icon(Icons.explore, color: Colors.orange),
              const SizedBox(width: 16),
              Expanded(child: Text(a, style: const TextStyle(fontWeight: FontWeight.w500))),
            ],
          ),
        )),
      ],
    );
  }

  Widget _buildSectionHeader(String title, Color color) {
    return Text(
      title.toUpperCase(),
      style: TextStyle(
        fontSize: 13,
        fontWeight: FontWeight.bold,
        color: color,
        letterSpacing: 1.2,
      ),
    );
  }

  Widget _buildPracticeTab(Color subjectColor) {
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        _buildSectionHeader('Quick Assessment', subjectColor),
        const SizedBox(height: 16),
        ..._concept!.practiceExercises.map((e) => Card(
          margin: const EdgeInsets.only(bottom: 20),
          child: Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (e.isHots)
                  Container(
                    margin: const EdgeInsets.only(bottom: 12),
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: Colors.red.shade50, borderRadius: BorderRadius.circular(8)),
                    child: const Text('CHALLENGE', style: TextStyle(color: Colors.red, fontSize: 10, fontWeight: FontWeight.bold)),
                  ),
                Text(e.question, style: const TextStyle(fontSize: 17, fontWeight: FontWeight.bold, height: 1.4)),
                const SizedBox(height: 16),
                ...e.options.map((opt) => Container(
                  margin: const EdgeInsets.only(bottom: 8),
                  decoration: BoxDecoration(
                    color: Colors.grey.shade50,
                    borderRadius: BorderRadius.circular(12),
                    border: Border.all(color: Colors.grey.shade200),
                  ),
                  child: RadioListTile(
                    value: opt,
                    groupValue: null,
                    onChanged: (_) {},
                    title: Text(opt),
                    activeColor: subjectColor,
                  ),
                )),
                const SizedBox(height: 12),
                TextButton.icon(
                  onPressed: () {
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        backgroundColor: subjectColor,
                        content: Text('Hint: ${e.hint}'),
                        behavior: SnackBarBehavior.floating,
                      ),
                    );
                  },
                  icon: const Icon(Icons.lightbulb_outline, size: 18),
                  label: const Text('Get a Hint'),
                  style: TextButton.styleFrom(foregroundColor: subjectColor),
                ),
              ],
            ),
          ),
        )),
      ],
    );
  }

  Widget _buildReviewTab(Color subjectColor) {
    return ListView(
      padding: const EdgeInsets.all(20),
      children: [
        _buildSectionHeader('Key Vocabulary', subjectColor),
        const SizedBox(height: 12),
        ..._concept!.vocabulary.entries.map((v) => Container(
          margin: const EdgeInsets.only(bottom: 12),
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.grey.shade200),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(v.key, style: TextStyle(fontWeight: FontWeight.bold, color: subjectColor, fontSize: 16)),
              const SizedBox(height: 4),
              Text(v.value, style: TextStyle(color: Colors.grey.shade700, height: 1.4)),
            ],
          ),
        )),
        const SizedBox(height: 32),
        _buildSectionHeader('Flashcards', subjectColor),
        const SizedBox(height: 16),
        SizedBox(
          height: 180,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: _concept!.flashcards.length,
            itemBuilder: (context, index) {
              final f = _concept!.flashcards[index];
              return Container(
                width: 280,
                margin: const EdgeInsets.only(right: 16),
                child: Card(
                  color: subjectColor.withOpacity(0.05),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(24),
                    side: BorderSide(color: subjectColor.withOpacity(0.2)),
                  ),
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.style, color: Colors.grey, size: 24),
                        const SizedBox(height: 16),
                        Text(
                          f.front,
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        const Text('Tap to reveal', style: TextStyle(fontSize: 12, color: Colors.grey)),
                      ],
                    ),
                  ),
                ),
              );
            },
          ),
        ),
      ],
    );
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }
}
