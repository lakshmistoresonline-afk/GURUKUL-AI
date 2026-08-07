import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/concept_node.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/learning_journey_screen.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/chapter_dashboard_screen.dart';

import 'package:project_gurukul_ai/features/questions/presentation/screens/question_center_screen.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/flashcards_screen.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/mind_map_screen.dart';

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
    final color = sl<ThemeService>().getSubjectColor(widget.subject);

    return Scaffold(
      backgroundColor: DesignSystem.background,
      body: CustomScrollView(
        physics: const BouncingScrollPhysics(),
        slivers: [
          _SubjectAppBar(subject: widget.subject, color: color),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(DesignSystem.spacingMd),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _AnalyticsSection(color: color),
                  const SizedBox(height: DesignSystem.spacingLg),
                  _LearningJourneyMap(color: color, subject: widget.subject, classLevel: widget.classLevel),
                  const SizedBox(height: DesignSystem.spacingLg),
                  Text('COMMAND CENTRE', style: DesignSystem.label),
                  const SizedBox(height: DesignSystem.spacingMd),
                  _CommandCenter(color: color, subject: widget.subject, classLevel: widget.classLevel),
                  const SizedBox(height: DesignSystem.spacingLg),
                  Text('CHAPTERS', style: DesignSystem.label),
                  const SizedBox(height: DesignSystem.spacingMd),
                ],
              ),
            ),
          ),
          _ChapterList(chaptersFuture: _chaptersFuture, subject: widget.subject, color: color),
          const SliverToBoxAdapter(child: SizedBox(height: 100)),
        ],
      ),
    );
  }
}

class _SubjectAppBar extends StatelessWidget {
  final String subject;
  final Color color;
  const _SubjectAppBar({required this.subject, required this.color});

  @override
  Widget build(BuildContext context) {
    return SliverAppBar.large(
      pinned: true,
      backgroundColor: color,
      foregroundColor: Colors.white,
      expandedHeight: 220,
      flexibleSpace: FlexibleSpaceBar(
        titlePadding: const EdgeInsets.only(left: 16, bottom: 16),
        title: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(subject, style: DesignSystem.h2.copyWith(color: Colors.white)),
            const SizedBox(height: 4),
            Row(
              children: [
                const Icon(Icons.stars, color: Colors.amber, size: 12),
                const SizedBox(width: 4),
                Text('45% Mastered', style: DesignSystem.bodySmall.copyWith(color: Colors.white.withValues(alpha: 0.9), fontSize: 10)),
              ],
            ),
          ],
        ),
        background: Stack(
          fit: StackFit.expand,
          children: [
            Positioned(
              right: -40,
              top: 20,
              child: Opacity(
                opacity: 0.2,
                child: Icon(_getIcon(subject), size: 240, color: Colors.white),
              ),
            ),
            Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  colors: [color, color.withValues(alpha: 0.6), Colors.transparent],
                  begin: Alignment.bottomLeft,
                  end: Alignment.topRight,
                ),
              ),
            ),
            Positioned(
              bottom: 60,
              left: 16,
              right: 16,
              child: ClipRRect(
                borderRadius: BorderRadius.circular(2),
                child: LinearProgressIndicator(
                  value: 0.45,
                  backgroundColor: Colors.white.withValues(alpha: 0.2),
                  valueColor: const AlwaysStoppedAnimation(Colors.white),
                  minHeight: 4,
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  IconData _getIcon(String subject) {
    switch (subject.toLowerCase()) {
      case 'mathematics': return Icons.calculate_rounded;
      case 'science': return Icons.science_rounded;
      case 'english': return Icons.translate_rounded;
      case 'social science': return Icons.public_rounded;
      case 'hindi': return Icons.menu_book_rounded;
      default: return Icons.auto_stories_rounded;
    }
  }
}

class _AnalyticsSection extends StatelessWidget {
  final Color color;
  const _AnalyticsSection({required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _StatItem(label: 'Total Study', value: '14.5h', icon: Icons.timer_outlined, color: color),
              _StatItem(label: 'Mastery', value: '45%', icon: Icons.insights_outlined, color: color),
              _StatItem(label: 'Flashcards', value: '82/150', icon: Icons.style_outlined, color: color),
            ],
          ),
          const Divider(height: DesignSystem.spacingLg),
          Row(
            children: [
              const Icon(Icons.emoji_events_outlined, size: 16, color: Colors.orange),
              const SizedBox(width: 8),
              Text('Next Milestone: Chapter 5 Master', style: DesignSystem.bodySmall),
              const Spacer(),
              Text('2/5', style: DesignSystem.label.copyWith(color: color)),
            ],
          ),
        ],
      ),
    );
  }
}

class _StatItem extends StatelessWidget {
  final String label;
  final String value;
  final IconData icon;
  final Color color;
  const _StatItem({required this.label, required this.value, required this.icon, required this.color});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Icon(icon, size: 20, color: color),
        const SizedBox(height: 4),
        Text(value, style: DesignSystem.h2.copyWith(fontSize: 18)),
        Text(label, style: DesignSystem.bodySmall.copyWith(fontSize: 10)),
      ],
    );
  }
}

class _LearningJourneyMap extends StatefulWidget {
  final Color color;
  final String subject;
  final int classLevel;
  const _LearningJourneyMap({required this.color, required this.subject, required this.classLevel});

  @override
  State<_LearningJourneyMap> createState() => _LearningJourneyMapState();
}

class _LearningJourneyMapState extends State<_LearningJourneyMap> {
  ConceptNode? _firstConcept;

  @override
  void initState() {
    super.initState();
    _loadFirstConcept();
  }

  Future<void> _loadFirstConcept() async {
    final chapters = await sl<FrameworkRepository>().getChapters(widget.classLevel, widget.subject);
    if (chapters.isNotEmpty) {
      final node = await sl<FrameworkRepository>().getConceptNode(chapters.first['id']);
      if (mounted) setState(() => _firstConcept = node);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: BoxDecoration(
        gradient: LinearGradient(colors: [widget.color.withValues(alpha: 0.8), widget.color]),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
        boxShadow: DesignSystem.shadowMd,
      ),
      child: Row(
        children: [
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('LEARNING JOURNEY', style: DesignSystem.label.copyWith(color: Colors.white.withValues(alpha: 0.8))),
                const SizedBox(height: 4),
                Text('Visual Roadmap', style: DesignSystem.h2.copyWith(color: Colors.white, fontSize: 18)),
                const SizedBox(height: 4),
                Text('Track your progress through all chapters', style: DesignSystem.bodySmall.copyWith(color: Colors.white.withValues(alpha: 0.9))),
              ],
            ),
          ),
          ElevatedButton(
            onPressed: _firstConcept == null ? null : () {
              Navigator.push(context, MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: _firstConcept!)));
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: Colors.white,
              foregroundColor: widget.color,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(DesignSystem.radiusMd)),
              elevation: 0,
            ),
            child: const Text('View Map'),
          ),
        ],
      ),
    );
  }
}

class _CommandCenter extends StatelessWidget {
  final Color color;
  final String subject;
  final int classLevel;
  const _CommandCenter({required this.color, required this.subject, required this.classLevel});

  @override
  Widget build(BuildContext context) {
    final actions = [
      {'label': 'Practice', 'icon': Icons.edit_document, 'color': Colors.blue},
      {'label': 'Quiz', 'icon': Icons.quiz_rounded, 'color': Colors.orange},
      {'label': 'Revision', 'icon': Icons.auto_mode_rounded, 'color': Colors.purple},
      {'label': 'Flashcards', 'icon': Icons.style_rounded, 'color': Colors.pink},
      {'label': 'Mind Maps', 'icon': Icons.hub_rounded, 'color': Colors.teal},
      {'label': 'Homework', 'icon': Icons.assignment_rounded, 'color': Colors.amber},
      {'label': 'AI Tutor', 'icon': Icons.smart_toy_rounded, 'color': Colors.indigo},
      {'label': 'Question Centre', 'icon': Icons.help_center_rounded, 'color': Colors.red},
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 4,
        mainAxisSpacing: 16,
        crossAxisSpacing: 16,
        childAspectRatio: 0.8,
      ),
      itemCount: actions.length,
      itemBuilder: (context, index) {
        final a = actions[index];
        return _ActionIcon(
          label: a['label'] as String,
          icon: a['icon'] as IconData,
          color: a['color'] as Color,
          onTap: () {
            if (a['label'] == 'Question Centre' || a['label'] == 'Practice') {
              Navigator.push(context, MaterialPageRoute(builder: (_) => QuestionCenterScreen(classLevel: classLevel, subject: subject)));
            } else if (a['label'] == 'Flashcards') {
              Navigator.push(context, MaterialPageRoute(builder: (_) => FlashcardsScreen(subject: subject)));
            } else if (a['label'] == 'Mind Maps') {
              Navigator.push(context, MaterialPageRoute(builder: (_) => MindMapScreen(
                topic: subject,
                branches: const ['Concepts', 'Formulas', 'Theorems', 'Real-world Applications', 'Practice Questions'],
              )));
            } else if (a['label'] == 'AI Tutor') {
              // Navigation to AI Tutor tab is usually handled via bottom nav,
              // but we can push the standalone chat screen here too.
            }
          },
        );
      },
    );
  }
}

class _ActionIcon extends StatelessWidget {
  final String label;
  final IconData icon;
  final Color color;
  final VoidCallback? onTap;
  const _ActionIcon({required this.label, required this.icon, required this.color, this.onTap});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: color.withValues(alpha: 0.1),
              borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
            ),
            child: Icon(icon, color: color, size: 24),
          ),
          const SizedBox(height: 6),
          Text(
            label,
            textAlign: TextAlign.center,
            style: DesignSystem.bodySmall.copyWith(fontSize: 10, fontWeight: FontWeight.bold),
          ),
        ],
      ),
    );
  }
}

class _ChapterList extends StatelessWidget {
  final Future<List<Map<String, dynamic>>> chaptersFuture;
  final String subject;
  final Color color;
  const _ChapterList({required this.chaptersFuture, required this.subject, required this.color});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<Map<String, dynamic>>>(
      future: chaptersFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const SliverToBoxAdapter(child: Center(child: Padding(
            padding: EdgeInsets.all(32.0),
            child: CircularProgressIndicator(),
          )));
        }
        if (!snapshot.hasData || snapshot.data!.isEmpty) {
          return const SliverToBoxAdapter(child: Center(child: Text('No chapters found.')));
        }
        final chapters = snapshot.data!;
        return SliverPadding(
          padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingMd),
          sliver: SliverList(
            delegate: SliverChildBuilderDelegate(
              (context, index) => _ChapterCard(chapter: chapters[index], index: index, color: color, subject: subject),
              childCount: chapters.length,
            ),
          ),
        );
      },
    );
  }
}

class _ChapterCard extends StatelessWidget {
  final Map<String, dynamic> chapter;
  final int index;
  final Color color;
  final String subject;
  const _ChapterCard({required this.chapter, required this.index, required this.color, required this.subject});

  @override
  Widget build(BuildContext context) {
    final mastery = (index % 5 + 1) * 0.2;
    return Container(
      margin: const EdgeInsets.only(bottom: DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: InkWell(
        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => ChapterDashboardScreen(chapterId: chapter['id'], subject: subject))),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
        child: Padding(
          padding: const EdgeInsets.all(DesignSystem.spacingMd),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                    decoration: BoxDecoration(color: color.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(4)),
                    child: Text('CHAPTER ${index + 1}', style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 10)),
                  ),
                  const Spacer(),
                  if (mastery >= 0.8)
                    const Icon(Icons.verified, color: Colors.green, size: 16),
                ],
              ),
              const SizedBox(height: DesignSystem.spacingSm),
              Text(chapter['title'], style: DesignSystem.title.copyWith(fontSize: 16)),
              const SizedBox(height: DesignSystem.spacingMd),
              Row(
                children: [
                  _Detail(Icons.layers_outlined, '${(chapter['topics'] as List).length} Topics'),
                  const SizedBox(width: DesignSystem.spacingMd),
                  _Detail(Icons.schedule, '45-60m'),
                  const Spacer(),
                  Column(
                    crossAxisAlignment: CrossAxisAlignment.end,
                    children: [
                      Text('${(mastery * 100).toInt()}% Mastered', style: DesignSystem.bodySmall.copyWith(fontSize: 10, color: color, fontWeight: FontWeight.bold)),
                      const SizedBox(height: 4),
                      SizedBox(
                        width: 80,
                        child: LinearProgressIndicator(value: mastery, color: color, backgroundColor: color.withValues(alpha: 0.1), minHeight: 4),
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _Detail extends StatelessWidget {
  final IconData icon;
  final String label;
  const _Detail(this.icon, this.label);

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 14, color: DesignSystem.textTertiary),
        const SizedBox(width: 4),
        Text(label, style: DesignSystem.bodySmall.copyWith(fontSize: 11, color: DesignSystem.textTertiary)),
      ],
    );
  }
}

