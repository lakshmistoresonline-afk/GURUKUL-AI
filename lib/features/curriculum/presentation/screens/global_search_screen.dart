import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../data/framework_repository.dart';
import 'learning_journey_screen.dart';

class GlobalSearchScreen extends StatefulWidget {
  final int classLevel;
  const GlobalSearchScreen({super.key, required this.classLevel});

  @override
  State<GlobalSearchScreen> createState() => _GlobalSearchScreenState();
}

class _GlobalSearchScreenState extends State<GlobalSearchScreen> {
  final TextEditingController _searchController = TextEditingController();
  List<Map<String, dynamic>> _results = [];
  bool _isSearching = false;

  void _handleSearch(String query) async {
    if (query.length < 3) {
      setState(() => _results = []);
      return;
    }

    setState(() => _isSearching = true);

    // In real app, this would be a more efficient search in Hive or Firestore
    final allChapters = await sl<FrameworkRepository>().getAllChapters(widget.classLevel);
    final results = allChapters.where((c) =>
      c['title'].toString().toLowerCase().contains(query.toLowerCase()) ||
      (c['topics'] as List).any((t) => t.toString().toLowerCase().contains(query.toLowerCase()))
    ).toList();

    setState(() {
      _results = results;
      _isSearching = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: TextField(
          controller: _searchController,
          autofocus: true,
          decoration: const InputDecoration(
            hintText: 'Search chapters, topics, concepts...',
            border: InputBorder.none,
          ),
          onChanged: _handleSearch,
        ),
      ),
      body: _isSearching
        ? const Center(child: CircularProgressIndicator())
        : ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: _results.length,
            itemBuilder: (context, index) {
              final res = _results[index];
              return ListTile(
                leading: const Icon(Icons.menu_book),
                title: Text(res['title']),
                subtitle: Text(res['subject'] ?? 'Subject'),
                trailing: const Icon(Icons.arrow_forward_ios, size: 14),
                onTap: () async {
                   final concept = await sl<FrameworkRepository>().getConceptNode(res['id']);
                   if (concept != null && mounted) {
                     Navigator.push(context, MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: concept)));
                   }
                },
              );
            },
          ),
    );
  }
}
