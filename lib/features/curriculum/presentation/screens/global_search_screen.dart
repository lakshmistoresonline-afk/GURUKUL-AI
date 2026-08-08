import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../data/framework_repository.dart';
import 'learning_journey_screen.dart';
import '../../../../features/content_acquisition/services/search_engine_service.dart';

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

    try {
      final results = await sl<SearchEngineService>().search(
        query,
        classLevel: widget.classLevel,
      );

      if (mounted) {
        setState(() {
          _results = results;
          _isSearching = false;
        });
      }
    } catch (e) {
      if (mounted) {
        setState(() => _isSearching = false);
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Search failed: $e')));
      }
    }
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
                leading: Container(
                  padding: const EdgeInsets.all(8),
                  decoration: BoxDecoration(color: Colors.blue.shade50, borderRadius: BorderRadius.circular(8)),
                  child: const Icon(Icons.search, color: Colors.blue),
                ),
                title: Text(res['title'] ?? 'Untitled'),
                subtitle: Text('${res['subject']} • Class ${res['class_level']}'),
                trailing: Text((res['score'] as num?)?.toStringAsFixed(2) ?? '', style: const TextStyle(fontSize: 10, color: Colors.grey)),
                onTap: () async {
                   final concept = await sl<FrameworkRepository>().getConceptNode(res['node_id'] ?? res['id']);
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
