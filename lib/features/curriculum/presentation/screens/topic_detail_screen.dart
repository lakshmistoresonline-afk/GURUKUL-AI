import 'package:flutter/material.dart';
import '../../../curriculum/domain/models/concept_node.dart';
import '../../../../core/di/injection.dart';
import '../../../curriculum/data/framework_repository.dart';

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

    return Scaffold(
      appBar: AppBar(
        title: Text(_concept!.chapter),
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Learn', icon: Icon(Icons.menu_book)),
            Tab(text: 'Practice', icon: Icon(Icons.quiz)),
            Tab(text: 'Review', icon: Icon(Icons.psychology)),
          ],
        ),
      ),
      body: TabBarView(
        controller: _tabController,
        children: [
          _buildLearnTab(),
          _buildPracticeTab(),
          _buildReviewTab(),
        ],
      ),
    );
  }

  Widget _buildLearnTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('Learning Objectives', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        ..._concept!.learningObjectives.map((o) => ListTile(
              leading: const Icon(Icons.check_circle_outline, color: Colors.green),
              title: Text(o),
            )),
        const Divider(height: 32),
        Text('Revision Notes', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        Card(
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Text(_concept!.revisionNotes),
          ),
        ),
        const SizedBox(height: 16),
        Text('Interactive Activities', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        ..._concept!.interactiveActivities.map((a) => Card(
              color: Colors.orange.withOpacity(0.1),
              child: ListTile(
                leading: const Icon(Icons.explore, color: Colors.orange),
                title: Text(a),
              ),
            )),
      ],
    );
  }

  Widget _buildPracticeTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('Practice Exercises', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 16),
        ..._concept!.practiceExercises.map((e) => Card(
              margin: const EdgeInsets.only(bottom: 12),
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (e.isHots)
                      const Chip(
                        label: Text('HOTS', style: TextStyle(color: Colors.white, fontSize: 10)),
                        backgroundColor: Colors.redAccent,
                      ),
                    Text(e.question, style: const TextStyle(fontWeight: FontWeight.bold)),
                    const SizedBox(height: 8),
                    ...e.options.map((opt) => RadioListTile(
                          value: opt,
                          groupValue: null,
                          onChanged: (_) {},
                          title: Text(opt),
                        )),
                    TextButton(
                      onPressed: () {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(content: Text('Hint: ${e.hint}')),
                        );
                      },
                      child: const Text('Need a Hint?'),
                    ),
                  ],
                ),
              ),
            )),
      ],
    );
  }

  Widget _buildReviewTab() {
    return ListView(
      padding: const EdgeInsets.all(16),
      children: [
        Text('Vocabulary', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        ..._concept!.vocabulary.entries.map((v) => ListTile(
              title: Text(v.key, style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: Text(v.value),
            )),
        const Divider(height: 32),
        Text('Flashcards', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 8),
        SizedBox(
          height: 150,
          child: ListView.builder(
            scrollDirection: Axis.horizontal,
            itemCount: _concept!.flashcards.length,
            itemBuilder: (context, index) {
              final f = _concept!.flashcards[index];
              return Card(
                width: 250,
                color: Colors.blue.withOpacity(0.1),
                child: Center(
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Text('Front', style: Theme.of(context).textTheme.bodySmall),
                        const SizedBox(height: 8),
                        Text(f.front, textAlign: TextAlign.center, style: const TextStyle(fontSize: 18)),
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
