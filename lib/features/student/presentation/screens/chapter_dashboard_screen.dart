import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/curriculum/domain/models/concept_node.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/learning_journey_screen.dart';

import 'package:project_gurukul_ai/features/questions/presentation/screens/question_center_screen.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/flashcards_screen.dart';
import 'package:project_gurukul_ai/features/ai/presentation/screens/ai_tutor_chat_screen.dart';

class ChapterDashboardScreen extends StatefulWidget {
  final String chapterId;
  final String subject;

  const ChapterDashboardScreen({
    super.key,
    required this.chapterId,
    required this.subject,
  });

  @override
  State<ChapterDashboardScreen> createState() => _ChapterDashboardScreenState();
}

class _ChapterDashboardScreenState extends State<ChapterDashboardScreen> with SingleTickerProviderStateMixin {
  ConceptNode? _concept;
  bool _isLoading = true;
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 4, vsync: this);
    _loadData();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  Future<void> _loadData() async {
    final concept = await sl<FrameworkRepository>().getConceptNode(widget.chapterId);
    if (mounted) {
      setState(() {
        _concept = concept;
        _isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final color = sl<ThemeService>().getSubjectColor(widget.subject);

    if (_isLoading) return const Scaffold(body: Center(child: CircularProgressIndicator()));
    if (_concept == null) return const Scaffold(body: Center(child: Text('Chapter content not found.')));

    return Scaffold(
      backgroundColor: DesignSystem.background,
      body: NestedScrollView(
        headerSliverBuilder: (context, innerBoxIsScrolled) => [
          _ChapterAppBar(concept: _concept!, color: color),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.all(DesignSystem.spacingMd),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _ChapterMetaInfo(concept: _concept!, color: color),
                  const SizedBox(height: DesignSystem.spacingLg),
                  _ProgressCard(concept: _concept!, color: color),
                  const SizedBox(height: DesignSystem.spacingLg),
                  Text('LEARNING MODULES', style: DesignSystem.label),
                ],
              ),
            ),
          ),
          SliverPersistentHeader(
            pinned: true,
            delegate: _SliverTabDelegate(
              TabBar(
                controller: _tabController,
                labelColor: color,
                unselectedLabelColor: DesignSystem.textTertiary,
                indicatorColor: color,
                tabs: const [
                  Tab(text: 'Topics'),
                  Tab(text: 'Animations'),
                  Tab(text: 'Videos'),
                  Tab(text: 'Interactive'),
                ],
              ),
            ),
          ),
        ],
        body: TabBarView(
          controller: _tabController,
          children: [
            _TopicsTab(concept: _concept!, color: color),
            _ContentListTab(type: 'Animations', concept: _concept!, color: color),
            _ContentListTab(type: 'Videos', concept: _concept!, color: color),
            _ContentListTab(type: 'Interactive', concept: _concept!, color: color),
          ],
        ),
      ),
      bottomNavigationBar: _ResourcesBottomPanel(concept: _concept!, color: color, subject: widget.subject),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.push(context, MaterialPageRoute(builder: (_) => AiTutorChatScreen(concept: _concept)));
        },
        backgroundColor: Colors.indigo,
        child: const Icon(Icons.smart_toy, color: Colors.white),
      ),
    );
  }
}

class _ChapterAppBar extends StatelessWidget {
  final ConceptNode concept;
  final Color color;
  const _ChapterAppBar({required this.concept, required this.color});

  @override
  Widget build(BuildContext context) {
    return SliverAppBar.large(
      pinned: true,
      backgroundColor: color,
      foregroundColor: Colors.white,
      expandedHeight: 180,
      flexibleSpace: FlexibleSpaceBar(
        titlePadding: const EdgeInsets.only(left: 16, bottom: 16),
        title: Text(concept.chapter ?? 'Chapter Detail', style: DesignSystem.h2.copyWith(color: Colors.white, fontSize: 18)),
        background: Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              colors: [color, color.withValues(alpha: 0.7)],
              begin: Alignment.bottomLeft,
              end: Alignment.topRight,
            ),
          ),
          child: Stack(
            children: [
              Positioned(
                right: -20,
                bottom: -20,
                child: Opacity(
                  opacity: 0.1,
                  child: Icon(Icons.menu_book, size: 200, color: Colors.white),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}

class _ChapterMetaInfo extends StatelessWidget {
  final ConceptNode concept;
  final Color color;
  const _ChapterMetaInfo({required this.concept, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              _MetaItem(Icons.schedule, '${concept.estStudyTime.inMinutes} mins', color),
              const SizedBox(width: DesignSystem.spacingMd),
              _MetaItem(Icons.trending_up, concept.difficulty.name.toUpperCase(), color),
              const SizedBox(width: DesignSystem.spacingMd),
              _MetaItem(Icons.auto_awesome, 'HOTS Incl.', color),
            ],
          ),
          const SizedBox(height: DesignSystem.spacingMd),
          Text('Overview', style: DesignSystem.title.copyWith(fontSize: 16)),
          const SizedBox(height: 4),
          Text(concept.introduction ?? '', style: DesignSystem.bodySmall),
          const SizedBox(height: DesignSystem.spacingMd),
          Text('Objectives', style: DesignSystem.title.copyWith(fontSize: 14)),
          const SizedBox(height: 4),
          ...concept.learningObjectives.take(3).map((o) => Padding(
            padding: const EdgeInsets.only(bottom: 2.0),
            child: Row(
              children: [
                Icon(Icons.check, size: 12, color: color),
                const SizedBox(width: 8),
                Expanded(child: Text(o, style: DesignSystem.bodySmall.copyWith(fontSize: 11))),
              ],
            ),
          )),
        ],
      ),
    );
  }
}

class _MetaItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  const _MetaItem(this.icon, this.label, this.color);

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Icon(icon, size: 16, color: color),
        const SizedBox(width: 4),
        Text(label, style: DesignSystem.label.copyWith(fontSize: 10, color: DesignSystem.textSecondary)),
      ],
    );
  }
}

class _ProgressCard extends StatelessWidget {
  final ConceptNode concept;
  final Color color;
  const _ProgressCard({required this.concept, required this.color});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
        border: Border.all(color: color.withValues(alpha: 0.2)),
      ),
      child: Row(
        children: [
          CircularProgressIndicator(
            value: 0.35,
            strokeWidth: 6,
            backgroundColor: color.withValues(alpha: 0.1),
            valueColor: AlwaysStoppedAnimation(color),
          ),
          const SizedBox(width: DesignSystem.spacingMd),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text('Chapter Mastery', style: DesignSystem.title.copyWith(fontSize: 14)),
                Text('Complete all modules to unlock assessment', style: DesignSystem.bodySmall.copyWith(fontSize: 11)),
              ],
            ),
          ),
          Text('35%', style: DesignSystem.h2.copyWith(color: color, fontSize: 20)),
        ],
      ),
    );
  }
}

class _TopicsTab extends StatelessWidget {
  final ConceptNode concept;
  final Color color;
  const _TopicsTab({required this.concept, required this.color});

  @override
  Widget build(BuildContext context) {
    final topics = concept.learningObjectives.isNotEmpty
      ? concept.learningObjectives
      : ['Introduction to ${concept.topic}', 'Key Concepts', 'Real-world Applications', 'Practice and Summary'];

    return ListView.builder(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      itemCount: topics.length,
      itemBuilder: (context, index) {
        return Container(
          margin: const EdgeInsets.only(bottom: DesignSystem.spacingSm),
          child: Material(
            color: DesignSystem.surface,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
              side: const BorderSide(color: DesignSystem.border),
            ),
            shadowColor: Colors.black.withValues(alpha: 0.05),
            elevation: 1,
            clipBehavior: Clip.antiAlias,
            child: ListTile(
              leading: CircleAvatar(
                backgroundColor: color.withValues(alpha: 0.1),
                child: Text('${index + 1}', style: TextStyle(color: color, fontWeight: FontWeight.bold)),
              ),
              title: Text(topics[index], style: const TextStyle(fontWeight: FontWeight.bold)),
              subtitle: const Text('Interactive module', style: TextStyle(fontSize: 12)),
              trailing: const Icon(Icons.play_circle_outline, color: DesignSystem.textTertiary),
              onTap: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: concept)));
              },
            ),
          ),
        );
      },
    );
  }
}

class _ContentListTab extends StatelessWidget {
  final String type;
  final ConceptNode concept;
  final Color color;
  const _ContentListTab({required this.type, required this.concept, required this.color});

  @override
  Widget build(BuildContext context) {
    List<Map<String, String>> items = [];
    if (type == 'Animations') {
      if (concept.animatedLessonAsset.isNotEmpty) {
        items.add({'title': 'Concept Animation: ${concept.chapter}', 'duration': '2:45'});
      }
      items.add({'title': 'Understanding $type Summary', 'duration': '1:30'});
    } else if (type == 'Videos') {
      if (concept.videoUrl != null && concept.videoUrl!.isNotEmpty) {
        items.add({'title': 'Teacher Lesson: ${concept.chapter}', 'duration': '10:20'});
      }
      items.add({'title': 'Topic $type Overview', 'duration': '5:00'});
    } else {
      items = [
        {'title': 'Interactive $type 1', 'duration': '5:30'},
        {'title': 'Discovery $type', 'duration': '8:15'},
      ];
    }

    return ListView.builder(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      itemCount: items.length,
      itemBuilder: (context, index) {
        return Container(
          margin: const EdgeInsets.only(bottom: DesignSystem.spacingSm),
          child: Material(
            color: DesignSystem.surface,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
              side: const BorderSide(color: DesignSystem.border),
            ),
            shadowColor: Colors.black.withValues(alpha: 0.05),
            elevation: 1,
            clipBehavior: Clip.antiAlias,
            child: ListTile(
              leading: Icon(_getIcon(type), color: color),
              title: Text(items[index]['title']!),
              subtitle: Text('Duration: ${items[index]['duration']}'),
              trailing: const Icon(Icons.arrow_forward_ios, size: 14),
              onTap: () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: concept)));
              },
            ),
          ),
        );
      },
    );
  }

  IconData _getIcon(String type) {
    if (type == 'Animations') return Icons.movie_outlined;
    if (type == 'Videos') return Icons.video_library_outlined;
    return Icons.science_outlined;
  }
}

class _ResourcesBottomPanel extends StatelessWidget {
  final ConceptNode concept;
  final Color color;
  final String subject;
  const _ResourcesBottomPanel({required this.concept, required this.color, required this.subject});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: BoxDecoration(
        color: DesignSystem.surface,
        boxShadow: [BoxShadow(color: Colors.black.withValues(alpha: 0.05), blurRadius: 10, offset: const Offset(0, -2))],
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('CHAPTER RESOURCES', style: DesignSystem.label),
          const SizedBox(height: DesignSystem.spacingMd),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _ResourceBtn('Practice', Icons.edit_note, Colors.blue, () {
                 Navigator.push(context, MaterialPageRoute(builder: (_) => QuestionCenterScreen(classLevel: concept.classLevel, subject: subject)));
              }),
              _ResourceBtn('Quiz', Icons.quiz_outlined, Colors.orange, () {
                 Navigator.push(context, MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: concept)));
              }),
              _ResourceBtn('Flashcards', Icons.style_outlined, Colors.pink, () {
                Navigator.push(context, MaterialPageRoute(builder: (_) => FlashcardsScreen(subject: subject, chapterId: concept.id)));
              }),
              _ResourceBtn('Revision', Icons.history, Colors.purple, () {}),
            ],
          ),
        ],
      ),
    );
  }
}

class _ResourceBtn extends StatelessWidget {
  final String label;
  final IconData icon;
  final Color color;
  final VoidCallback onTap;
  const _ResourceBtn(this.label, this.icon, this.color, this.onTap);

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
      child: Column(
        children: [
          Container(
            padding: const EdgeInsets.all(10),
            decoration: BoxDecoration(color: color.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(DesignSystem.radiusMd)),
            child: Icon(icon, color: color, size: 20),
          ),
          const SizedBox(height: 4),
          Text(label, style: DesignSystem.bodySmall.copyWith(fontSize: 10, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}

class _SliverTabDelegate extends SliverPersistentHeaderDelegate {
  final TabBar tabBar;
  _SliverTabDelegate(this.tabBar);

  @override
  double get minExtent => tabBar.preferredSize.height;
  @override
  double get maxExtent => tabBar.preferredSize.height;

  @override
  Widget build(BuildContext context, double shrinkOffset, bool overlapsContent) {
    return Container(
      color: DesignSystem.background,
      child: tabBar,
    );
  }

  @override
  bool shouldRebuild(_SliverTabDelegate oldDelegate) => false;
}
