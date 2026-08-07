import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/learning_journey_screen.dart';
import 'package:project_gurukul_ai/features/gamification/domain/services/certificate_service.dart';

class SubjectDashboardScreen extends StatefulWidget {
  final int classLevel;
  final String subject;

  const SubjectDashboardScreen({
    super.key,
    required this.classLevel,
    required this.subject,
  });

  @override
  State<SubjectDashboardScreen> createState() => _SubjectDashboardScreenState();
}

class _SubjectDashboardScreenState extends State<SubjectDashboardScreen> {
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
          _buildHeroHeader(subjectColor),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 24),
                  _buildContinueLearning(subjectColor),
                  const SizedBox(height: 32),
                  _buildAiRecommendation(subjectColor),
                  const SizedBox(height: 32),
                  _buildQuickLearningActions(subjectColor),
                  const SizedBox(height: 32),
                  const Text('Chapter Navigator', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
                  const SizedBox(height: 16),
                ],
              ),
            ),
          ),
          _buildChapterList(subjectColor),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(20),
              child: Column(
                children: [
                  _buildFunLearningCard(subjectColor),
                  const SizedBox(height: 100),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildHeroHeader(Color color) {
    return SliverAppBar.large(
      expandedHeight: 220,
      backgroundColor: color,
      foregroundColor: Colors.white,
      pinned: true,
      actions: [
        IconButton(
          onPressed: () => sl<CertificateService>().generateAndPreview(
            studentName: 'Gurukul Student',
            courseName: widget.subject,
            completionDate: DateTime.now(),
          ),
          icon: const Icon(Icons.workspace_premium),
          tooltip: 'Get Certificate',
        ),
      ],
      flexibleSpace: FlexibleSpaceBar(
        title: Text(widget.subject, style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.white)),
        background: Stack(
          fit: StackFit.expand,
          children: [
            Positioned(
              right: -20,
              bottom: -20,
              child: Opacity(
                opacity: 0.2,
                child: Icon(_getIconForSubject(widget.subject), size: 200, color: Colors.white),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(24.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.end,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text(
                    'Explore interactive lessons, practice questions, and AI-powered tutoring.',
                    style: TextStyle(color: Colors.white70, fontSize: 13),
                  ),
                  const SizedBox(height: 16),
                  Row(
                    children: [
                      _headerStat('12', 'Chapters'),
                      const SizedBox(width: 24),
                      _headerStat('145', 'Topics'),
                      const SizedBox(width: 24),
                      _headerStat('34h', 'Time'),
                    ],
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _headerStat(String value, String label) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(value, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 18)),
        Text(label, style: const TextStyle(color: Colors.white60, fontSize: 10)),
      ],
    );
  }

  Widget _buildContinueLearning(Color color) {
    return Card(
      elevation: 0,
      color: color.withOpacity(0.12),
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(24), side: BorderSide(color: color.withOpacity(0.1))),
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(Icons.play_circle_fill, color: color, size: 32),
                const SizedBox(width: 12),
                const Text('RESUME LAST LESSON', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, letterSpacing: 1.1)),
              ],
            ),
            const SizedBox(height: 20),
            const Text('The Fish Tale', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
            const Text('Topic: Large Numbers', style: TextStyle(color: Colors.grey)),
            const SizedBox(height: 20),
            ClipRRect(
              borderRadius: BorderRadius.circular(10),
              child: LinearProgressIndicator(value: 0.65, backgroundColor: Colors.white, valueColor: AlwaysStoppedAnimation(color), minHeight: 8),
            ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('15 mins remaining', style: TextStyle(fontSize: 12, fontWeight: FontWeight.w500)),
                FilledButton(onPressed: () {}, style: FilledButton.styleFrom(backgroundColor: color), child: const Text('Continue')),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAiRecommendation(Color color) {
    return Container(
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: Colors.grey.shade200),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.auto_awesome, color: Colors.purple, size: 20),
              SizedBox(width: 8),
              Text('AI TEACHER RECOMMENDS', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 12, color: Colors.purple)),
            ],
          ),
          const SizedBox(height: 16),
          const Text('You are doing great in Numbers! Shall we try a "Quick Quiz" to lock in your mastery?', style: TextStyle(fontSize: 15, height: 1.4)),
          const SizedBox(height: 20),
          Row(
            children: [
              _recBadge(Icons.timer_outlined, '5 Mins'),
              const SizedBox(width: 12),
              _recBadge(Icons.stars_outlined, '50 XP'),
              const Spacer(),
              TextButton(onPressed: () {}, child: const Text('Start Now →', style: TextStyle(fontWeight: FontWeight.bold))),
            ],
          ),
        ],
      ),
    );
  }

  Widget _recBadge(IconData icon, String label) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(10)),
      child: Row(
        children: [
          Icon(icon, size: 14, color: Colors.grey),
          const SizedBox(width: 4),
          Text(label, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold, color: Colors.grey)),
        ],
      ),
    );
  }

  Widget _buildQuickLearningActions(Color color) {
    final actions = [
      {'icon': Icons.menu_book, 'label': 'Learn'},
      {'icon': Icons.movie_filter, 'label': 'Animated'},
      {'icon': Icons.videogame_asset, 'label': 'Activity'},
      {'icon': Icons.edit_note, 'label': 'Practice'},
      {'icon': Icons.quiz, 'label': 'Quiz'},
      {'icon': Icons.style, 'label': 'Flashcards'},
      {'icon': Icons.psychology, 'label': 'Revision'},
      {'icon': Icons.smart_toy, 'label': 'AI Tutor'},
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 4, crossAxisSpacing: 12, mainAxisSpacing: 16, childAspectRatio: 0.8),
      itemCount: actions.length,
      itemBuilder: (context, index) {
        final a = actions[index];
        return Column(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(color: color.withOpacity(0.12), borderRadius: BorderRadius.circular(16)),
              child: Icon(a['icon'] as IconData, color: color),
            ),
            const SizedBox(height: 8),
            Text(a['label'] as String, style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold), textAlign: TextAlign.center),
          ],
        );
      },
    );
  }

  Widget _buildChapterList(Color color) {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: _chaptersFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const SliverFillRemaining(child: Center(child: CircularProgressIndicator()));
        }
        final chapters = snapshot.data ?? [];
        return SliverPadding(
          padding: const EdgeInsets.symmetric(horizontal: 20),
          sliver: SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, index) => _buildChapterCard(chapters[index], index, color),
              childCount: chapters.length,
            ),
          ),
        );
      },
    );
  }

  Widget _buildChapterCard(Map<String, dynamic> chapter, int index, Color color) {
    return Card(
      margin: const EdgeInsets.only(bottom: 20),
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: () async {
          final concept = await sl<FrameworkRepository>().getConceptNode(chapter['id']);
          if (concept != null && mounted) {
            Navigator.push(context, MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: concept)));
          }
        },
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Text('CHAPTER ${index + 1}', style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 11, letterSpacing: 1.1)),
                  const Spacer(),
                  const Icon(Icons.check_circle, color: Colors.green, size: 20),
                ],
              ),
              const SizedBox(height: 12),
              Text(chapter['title'], style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 20),
              Row(
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Mastery Progress', style: TextStyle(fontSize: 12, color: Colors.grey)),
                        const SizedBox(height: 8),
                        ClipRRect(
                          borderRadius: BorderRadius.circular(10),
                          child: LinearProgressIndicator(value: 0.4, backgroundColor: Colors.grey.shade100, valueColor: AlwaysStoppedAnimation(color), minHeight: 6),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(width: 24),
                  FilledButton.tonal(
                    onPressed: () {},
                    style: FilledButton.styleFrom(backgroundColor: color.withOpacity(0.12), foregroundColor: color),
                    child: const Text('Start'),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFunLearningCard(Color color) {
    return Container(
      padding: const EdgeInsets.all(24),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [color.withOpacity(0.8), color]),
        borderRadius: BorderRadius.circular(24),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.emoji_objects, color: Colors.white, size: 40),
          const SizedBox(height: 16),
          const Text('MATH TRICK OF THE DAY', style: TextStyle(color: Colors.white70, fontWeight: FontWeight.bold, fontSize: 12)),
          const SizedBox(height: 8),
          const Text('Multiplying by 5 is the same as multiplying by 10 and then dividing by 2!', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
          const SizedBox(height: 20),
          OutlinedButton(onPressed: () {}, style: OutlinedButton.styleFrom(foregroundColor: Colors.white, side: const BorderSide(color: Colors.white)), child: const Text('Try it Out')),
        ],
      ),
    );
  }

  IconData _getIconForSubject(String subject) {
    switch (subject) {
      case 'Mathematics': return Icons.calculate;
      case 'EVS': return Icons.nature_people;
      case 'English': return Icons.book;
      case 'Hindi': return Icons.translate;
      case 'Science': return Icons.science;
      case 'Social Science': return Icons.public;
      default: return Icons.school;
    }
  }
}
