import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/student/presentation/widgets/dashboard/premium_header.dart';
import 'package:project_gurukul_ai/features/student/presentation/widgets/dashboard/gamification_stats_row.dart';
import 'package:project_gurukul_ai/features/student/presentation/widgets/dashboard/continue_learning_card.dart';
import 'package:project_gurukul_ai/features/student/presentation/widgets/dashboard/ai_recommendation_section.dart';
import 'package:project_gurukul_ai/features/student/presentation/widgets/dashboard/command_center_grid.dart';
import 'package:project_gurukul_ai/features/student/presentation/widgets/dashboard/learning_journey_tracker.dart';
import 'package:project_gurukul_ai/features/student/presentation/widgets/dashboard/daily_challenge_card.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/subject_dashboard_screen.dart';
import 'package:project_gurukul_ai/features/ai/presentation/screens/ai_tutor_chat_screen.dart';
import 'package:project_gurukul_ai/core/telemetry/telemetry_service.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/progress_dashboard_screen.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';

class DashboardScreen extends StatefulWidget {
  final int classLevel;
  const DashboardScreen({super.key, required this.classLevel});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  int _currentIndex = 0;
  String? _currentUserId;
  String _studentName = 'Scholar';

  @override
  void initState() {
    super.initState();
    final authState = context.read<AuthBloc>().state;
    if (authState is AuthAuthenticated) {
      _currentUserId = authState.user.uid;
      _studentName = authState.user.name;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      body: IndexedStack(
        index: _currentIndex,
        children: [
          _HomeTab(studentName: _studentName),
          _MyLearningTab(classLevel: widget.classLevel),
          const AiTutorChatScreen(),
          ProgressDashboardScreen(studentId: _currentUserId ?? 'guest'),
          const _ProfileTab(),
        ],
      ),
      bottomNavigationBar: _DashboardBottomNav(
        currentIndex: _currentIndex,
        onTap: (index) {
          setState(() => _currentIndex = index);
          sl<TelemetryService>().logImpression(pageId: 'tab_$index', type: 'NAV_TAB');
        },
      ),
    );
  }
}

class _HomeTab extends StatelessWidget {
  final String studentName;
  const _HomeTab({required this.studentName});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: LayoutBuilder(
        builder: (context, constraints) {
          final isTablet = constraints.maxWidth > 600;

          return CustomScrollView(
            physics: const BouncingScrollPhysics(),
            slivers: [
              SliverToBoxAdapter(
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingMd),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      PremiumHeader(studentName: studentName),
                      const GamificationStatsRow(),
                      const SizedBox(height: DesignSystem.spacingMd),

                      if (isTablet)
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Expanded(flex: 3, child: ContinueLearningCard()),
                            const SizedBox(width: DesignSystem.spacingLg),
                            const Expanded(flex: 2, child: DailyChallengeCard()),
                          ],
                        )
                      else ...[
                        const ContinueLearningCard(),
                        const SizedBox(height: DesignSystem.spacingLg),
                        const DailyChallengeCard(),
                      ],

                      const SizedBox(height: DesignSystem.spacingXl),
                      const AiRecommendationSection(),

                      const SizedBox(height: DesignSystem.spacingXl),
                      const LearningJourneyTracker(),

                      const SizedBox(height: DesignSystem.spacingXl),
                      const CommandCenterGrid(),

                      const SizedBox(height: 120), // Bottom padding for nav
                    ],
                  ),
                ),
              ),
            ],
          );
        },
      ),
    );
  }
}

class _MyLearningTab extends StatelessWidget {
  final int classLevel;
  const _MyLearningTab({required this.classLevel});

  @override
  Widget build(BuildContext context) {
    return FutureBuilder<List<String>>(
      future: sl<FrameworkRepository>().getSubjects(classLevel),
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const Center(child: CircularProgressIndicator());
        final subjects = snapshot.data!;
        return CustomScrollView(
          slivers: [
            SliverAppBar.large(
              title: Text('My Learning', style: DesignSystem.h2),
              backgroundColor: DesignSystem.background,
            ),
            SliverPadding(
              padding: const EdgeInsets.all(DesignSystem.spacingMd),
              sliver: SliverGrid(
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: DesignSystem.spacingMd,
                  mainAxisSpacing: DesignSystem.spacingMd,
                  childAspectRatio: 0.85,
                ),
                delegate: SliverChildBuilderDelegate(
                  (context, index) => _SubjectCard(subject: subjects[index], classLevel: classLevel),
                  childCount: subjects.length,
                ),
              ),
            ),
            const SliverToBoxAdapter(child: SizedBox(height: 100)),
          ],
        );
      },
    );
  }
}

class _SubjectCard extends StatelessWidget {
  final String subject;
  final int classLevel;
  const _SubjectCard({required this.subject, required this.classLevel});

  @override
  Widget build(BuildContext context) {
    final color = sl<ThemeService>().getSubjectColor(subject);
    return Card(
      child: InkWell(
        onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => SubjectDashboardScreen(classLevel: classLevel, subject: subject))),
        child: Padding(
          padding: const EdgeInsets.all(DesignSystem.spacingMd),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(_getIcon(subject), color: color, size: 32),
              const Spacer(),
              Text(subject, style: DesignSystem.title.copyWith(fontSize: 16)),
              const SizedBox(height: DesignSystem.spacingXs),
              const Text('12 Chapters', style: TextStyle(fontSize: 12, color: DesignSystem.textTertiary)),
              const SizedBox(height: DesignSystem.spacingSm),
              ClipRRect(
                borderRadius: BorderRadius.circular(2),
                child: LinearProgressIndicator(value: 0.4, color: color, backgroundColor: color.withValues(alpha: 0.1), minHeight: 4),
              ),
            ],
          ),
        ),
      ),
    );
  }

  IconData _getIcon(String subject) {
    switch (subject.toLowerCase()) {
      case 'mathematics': return Icons.calculate_outlined;
      case 'science': return Icons.science_outlined;
      case 'evs': return Icons.nature_people_outlined;
      case 'english': return Icons.translate_outlined;
      case 'hindi': return Icons.history_edu_outlined;
      default: return Icons.book_outlined;
    }
  }
}

class _DashboardBottomNav extends StatelessWidget {
  final int currentIndex;
  final ValueChanged<int> onTap;
  const _DashboardBottomNav({required this.currentIndex, required this.onTap});

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        color: DesignSystem.surface,
        border: const Border(top: BorderSide(color: DesignSystem.border)),
      ),
      child: NavigationBar(
        selectedIndex: currentIndex,
        onDestinationSelected: onTap,
        backgroundColor: Colors.transparent,
        indicatorColor: DesignSystem.primaryLight,
        destinations: const [
          NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home, color: DesignSystem.primary), label: 'Home'),
          NavigationDestination(icon: Icon(Icons.auto_stories_outlined), selectedIcon: Icon(Icons.auto_stories, color: DesignSystem.primary), label: 'Learning'),
          NavigationDestination(icon: Icon(Icons.smart_toy_outlined), selectedIcon: Icon(Icons.smart_toy, color: DesignSystem.primary), label: 'Tutor'),
          NavigationDestination(icon: Icon(Icons.analytics_outlined), selectedIcon: Icon(Icons.analytics, color: DesignSystem.primary), label: 'Progress'),
          NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person, color: DesignSystem.primary), label: 'Profile'),
        ],
      ),
    );
  }
}

class _ProfileTab extends StatelessWidget {
  const _ProfileTab();
  @override
  Widget build(BuildContext context) {
    return const Center(child: Text('Profile Screen - Implementation in Progress'));
  }
}
