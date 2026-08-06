import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../../curriculum/data/framework_repository.dart';
import '../../../curriculum/presentation/screens/topic_detail_screen.dart';

class ChapterListScreen extends StatefulWidget {
  final int classLevel;
  final String subject;

  const ChapterListScreen({
    super.key,
    required this.classLevel,
    required this.subject,
  });

  @override
  State<ChapterListScreen> createState() => _ChapterListScreenState();
}

class _ChapterListScreenState extends State<ChapterListScreen> {
  late Future<List<Map<String, dynamic>>> _chaptersFuture;

  @override
  void initState() {
    super.initState();
    _chaptersFuture = sl<FrameworkRepository>().getChapters(widget.classLevel, widget.subject);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('${widget.subject} - Class ${widget.classLevel}'),
      ),
      body: FutureBuilder<List<Map<String, dynamic>>>(
        future: _chaptersFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final chapters = snapshot.data ?? [];
          return ListView.separated(
            padding: const EdgeInsets.all(16),
            itemCount: chapters.length,
            separatorBuilder: (_, __) => const SizedBox(height: 12),
            itemBuilder: (context, index) {
              final chapter = chapters[index];
              return ListTile(
                title: Text(chapter['title']),
                subtitle: Text('Topics: ${(chapter['topics'] as List).join(', ')}'),
                leading: CircleAvatar(child: Text('${index + 1}')),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(
                      builder: (_) => TopicDetailScreen(conceptId: chapter['id']),
                    ),
                  );
                },
              );
            },
          );
        },
      ),
    );
  }
}
