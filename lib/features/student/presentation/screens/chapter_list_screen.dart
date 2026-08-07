import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../../curriculum/data/framework_repository.dart';
import '../../../../core/theme/theme_service.dart';
import '../../../curriculum/presentation/screens/learning_journey_screen.dart';

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
    final themeService = sl<ThemeService>();
    final subjectColor = themeService.getSubjectColor(widget.subject);

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      body: CustomScrollView(
        slivers: [
          SliverAppBar.large(
            title: Text(widget.subject),
            backgroundColor: subjectColor,
            foregroundColor: Colors.white,
            expandedHeight: 120,
          ),
          FutureBuilder<List<Map<String, dynamic>>>(
            future: _chaptersFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const SliverFillRemaining(child: Center(child: CircularProgressIndicator()));
              }
              final chapters = snapshot.data ?? [];
              return SliverPadding(
                padding: const EdgeInsets.all(20),
                sliver: SliverList(
                  delegate: SliverChildBuilderDelegate(
                    (context, index) {
                      final chapter = chapters[index];
                      return _buildChapterCard(chapter, index, subjectColor);
                    },
                    childCount: chapters.length,
                  ),
                ),
              );
            },
          ),
        ],
      ),
    );
  }

  Widget _buildChapterCard(Map<String, dynamic> chapter, int index, Color subjectColor) {
    return Card(
      margin: const EdgeInsets.only(bottom: 20),
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: () async {
          final concept = await sl<FrameworkRepository>().getConceptNode(chapter['id']);
          if (concept != null) {
            if (mounted) {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: concept)),
              );
            }
          } else {
             if (mounted) {
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(content: Text('Working on this lesson! Please check back soon.')),
              );
            }
          }
        },
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
                    decoration: BoxDecoration(
                      color: subjectColor.withOpacity(0.12),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Text(
                      'Chapter ${index + 1}',
                      style: TextStyle(color: subjectColor, fontWeight: FontWeight.bold, fontSize: 12),
                    ),
                  ),
                  const Spacer(),
                  const Icon(Icons.star_border, color: Colors.amber),
                ],
              ),
              const SizedBox(height: 12),
              Text(
                chapter['title'],
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 8),
              Text(
                'Topics: ${(chapter['topics'] as List).take(3).join(', ')}...',
                style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
              ),
              const SizedBox(height: 20),
              Row(
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(10),
                      child: LinearProgressIndicator(
                        value: (index % 3 + 1) * 0.3,
                        backgroundColor: Colors.grey.shade100,
                        valueColor: AlwaysStoppedAnimation(subjectColor),
                        minHeight: 8,
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  const Text('45%', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
                ],
              ),
              const SizedBox(height: 20),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Row(
                    children: [
                      _buildQuickAction(Icons.flash_on, subjectColor),
                      const SizedBox(width: 8),
                      _buildQuickAction(Icons.quiz_outlined, subjectColor),
                    ],
                  ),
                  FilledButton.tonal(
                    onPressed: () {},
                    style: FilledButton.styleFrom(
                      backgroundColor: subjectColor.withOpacity(0.12),
                      foregroundColor: subjectColor,
                    ),
                    child: const Text('Start Learning'),
                  ),
                ],
              )
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildQuickAction(IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: BoxDecoration(
        color: Colors.grey.shade50,
        border: Border.all(color: Colors.grey.shade200),
        borderRadius: BorderRadius.circular(10),
      ),
      child: Icon(icon, size: 18, color: color),
    );
  }
}
