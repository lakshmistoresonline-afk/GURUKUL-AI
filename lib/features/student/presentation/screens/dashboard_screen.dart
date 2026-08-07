import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/core/notifications/notification_service.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/gamification/data/gamification_repository.dart';
import 'package:project_gurukul_ai/features/gamification/domain/models/achievement.dart';
import 'package:project_gurukul_ai/features/auth/presentation/bloc/auth_bloc.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/subject_dashboard_screen.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/progress_dashboard_screen.dart';
import 'package:project_gurukul_ai/core/theme/theme_service.dart';
import 'package:project_gurukul_ai/features/ai/presentation/screens/ai_tutor_chat_screen.dart';
import 'package:project_gurukul_ai/features/planner/presentation/widgets/pomodoro_timer.dart';
import 'package:project_gurukul_ai/features/planner/presentation/widgets/exam_countdown.dart';
import 'package:project_gurukul_ai/features/questions/presentation/screens/question_center_screen.dart';
import 'package:project_gurukul_ai/features/simulations/presentation/screens/virtual_lab_screen.dart';
import 'package:project_gurukul_ai/features/planner/presentation/screens/study_planner_screen.dart';
import 'package:project_gurukul_ai/features/notebook/presentation/screens/notebook_screen.dart';
import 'package:project_gurukul_ai/features/teacher/presentation/screens/teacher_dashboard_screen.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/discussion_forum_screen.dart';
import 'package:project_gurukul_ai/core/utils/qr_scanner_service.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/global_search_screen.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/framework_selection_screen.dart';
import 'package:project_gurukul_ai/features/content/presentation/screens/ai_lesson_creator_screen.dart';
import 'package:project_gurukul_ai/features/content/presentation/screens/content_store_screen.dart';
import 'package:project_gurukul_ai/core/telemetry/telemetry_service.dart';

class DashboardScreen extends StatefulWidget {
  final int classLevel;
  const DashboardScreen({super.key, required this.classLevel});

  @override
  State<DashboardScreen> createState() => _DashboardScreenState();
}

class _DashboardScreenState extends State<DashboardScreen> {
  late Future<List<String>> _subjectsFuture;
  Stream<UserGamification>? _gamificationStream;
  StreamSubscription? _notificationSubscription;
  String? _currentUserId;
  int _currentIndex = 0;

  @override
  void initState() {
    super.initState();
    _subjectsFuture = sl<FrameworkRepository>().getSubjects(widget.classLevel);

    final authState = context.read<AuthBloc>().state;
    if (authState is AuthAuthenticated) {
      _currentUserId = authState.user.uid;
      _initUserFeatures(_currentUserId!);
    }
  }

  void _initUserFeatures(String userId) {
    _gamificationStream = sl<GamificationRepository>().watchUserStats(userId);

    _notificationSubscription = sl<NotificationService>().messageStream.listen((message) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message.notification?.title ?? 'New notification from Gurukul AI'),
            behavior: SnackBarBehavior.floating,
          ),
        );
      }
    });
  }

  @override
  void dispose() {
    _notificationSubscription?.cancel();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return BlocListener<AuthBloc, AuthState>(
      listener: (context, state) {
        if (state is AuthAuthenticated) {
          setState(() {
            _currentUserId = state.user.uid;
            _initUserFeatures(_currentUserId!);
          });
        }
      },
      child: Scaffold(
        body: SafeArea(child: _buildBody()),
        bottomNavigationBar: NavigationBar(
          selectedIndex: _currentIndex,
          onDestinationSelected: (index) {
             setState(() => _currentIndex = index);
             sl<TelemetryService>().logImpression(pageId: 'nav_$index', type: 'TAB');
          },
          destinations: const [
            NavigationDestination(icon: Icon(Icons.home_outlined), selectedIcon: Icon(Icons.home), label: 'Home'),
            NavigationDestination(icon: Icon(Icons.auto_stories_outlined), selectedIcon: Icon(Icons.auto_stories), label: 'Subjects'),
            NavigationDestination(icon: Icon(Icons.track_changes_outlined), selectedIcon: Icon(Icons.track_changes), label: 'Practice'),
            NavigationDestination(icon: Icon(Icons.smart_toy_outlined), selectedIcon: Icon(Icons.smart_toy), label: 'AI Tutor'),
            NavigationDestination(icon: Icon(Icons.person_outline), selectedIcon: Icon(Icons.person), label: 'Profile'),
          ],
        ),
      ),
    );
  }

  Widget _buildBody() {
    switch (_currentIndex) {
      case 0: return _buildHomeDashboard();
      case 1: return _buildSubjectsGrid();
      case 2: return const VirtualLabScreen();
      case 3: return const AiTutorChatScreen();
      case 4: return _buildProfileScreen();
      default: return _buildHomeDashboard();
    }
  }

  Widget _buildHomeDashboard() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildTopGreeting(),
          const SizedBox(height: 24),
          _buildStatsRow(),
          const SizedBox(height: 24),
          ExamCountdown(examName: 'Final Term Exam', examDate: DateTime(2026, 3, 15)),
          const SizedBox(height: 24),
          const PomodoroTimer(),
          const SizedBox(height: 24),
          _buildQuickAccess(),
          const SizedBox(height: 24),
          _buildContinueLearningCard(),
          const SizedBox(height: 24),
          _buildTodaysPlan(),
          const SizedBox(height: 24),
          _buildAiRecommendation(),
        ],
      ),
    );
  }

  Widget _buildTopGreeting() {
    final hour = DateTime.now().hour;
    String greeting = 'Good Morning';
    if (hour >= 12 && hour < 17) greeting = 'Good Afternoon';
    if (hour >= 17) greeting = 'Good Evening';

    return Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('$greeting, Student!', style: Theme.of(context).textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold, color: Colors.blue.shade900)),
              Text('Ready to learn something new today?', style: Theme.of(context).textTheme.bodyMedium?.copyWith(color: Colors.grey.shade600)),
            ],
          ),
        ),
        IconButton(
          onPressed: () {
            sl<TelemetryService>().logInteract(id: 'search', type: 'BUTTON', pageId: 'home');
            Navigator.push(context, MaterialPageRoute(builder: (_) => GlobalSearchScreen(classLevel: widget.classLevel)));
          },
          icon: const Icon(Icons.search, size: 28, color: Colors.blue),
        ),
        IconButton(
          onPressed: () async {
            sl<TelemetryService>().logInteract(id: 'qr_scanner', type: 'BUTTON', pageId: 'home');
            final code = await sl<QrScannerService>().scanFromImage();
            if (code != null && mounted) {
               ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('QR Scanned: $code')));
            }
          },
          icon: const Icon(Icons.qr_code_scanner, size: 28, color: Colors.blue),
        ),
        const SizedBox(width: 8),
        const CircleAvatar(radius: 28, backgroundImage: NetworkImage('https://api.dicebear.com/7.x/avataaars/png?seed=Felix')),
      ],
    );
  }

  Widget _buildStatsRow() {
    return StreamBuilder<UserGamification>(
      stream: _gamificationStream,
      builder: (context, snapshot) {
        final stats = snapshot.data;
        return Row(
          children: [
            _buildStatItem(Icons.local_fire_department, '${stats?.currentStreak ?? 0}', 'Streak', Colors.orange),
            _buildStatItem(Icons.stars, '${stats?.currentXp ?? 0}', 'XP', Colors.blue),
            _buildStatItem(Icons.military_tech, 'Lvl ${stats?.level ?? 1}', 'Level', Colors.purple),
            _buildStatItem(Icons.monetization_on, '120', 'Coins', Colors.amber),
          ],
        );
      },
    );
  }

  Widget _buildStatItem(IconData icon, String value, String label, Color color) {
    return Expanded(
      child: Column(
        children: [
          Icon(icon, color: color, size: 28),
          const SizedBox(height: 4),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
          Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
        ],
      ),
    );
  }

  Widget _buildQuickAccess() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        _quickAccessBtn('Planner', Icons.calendar_today, Colors.indigo, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const StudyPlannerScreen()))),
        _quickAccessBtn('Creator', Icons.auto_awesome, Colors.pink, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const AiLessonCreatorScreen()))),
        _quickAccessBtn('Store', Icons.local_mall, Colors.orange, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ContentStoreScreen()))),
        _quickAccessBtn('Teacher', Icons.admin_panel_settings, Colors.blueGrey, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const TeacherDashboardScreen()))),
      ],
    );
  }

  Widget _quickAccessBtn(String label, IconData icon, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: () {
        sl<TelemetryService>().logInteract(id: label.toLowerCase(), type: 'QUICK_ACCESS', pageId: 'home');
        onTap();
      },
      child: Column(
        children: [
          Container(padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: color.withOpacity(0.12), shape: BoxShape.circle), child: Icon(icon, color: color, size: 24)),
          const SizedBox(height: 8),
          Text(label, style: const TextStyle(fontSize: 11, fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  Widget _buildContinueLearningCard() {
    return Card(
      color: Colors.blue.shade50,
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('CONTINUE LEARNING', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold, color: Colors.blue)),
            const SizedBox(height: 12),
            const Text('The Fish Tale', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
            const Text('Topic: Large Numbers', style: TextStyle(color: Colors.black54)),
            const SizedBox(height: 16),
            const LinearProgressIndicator(value: 0.6, backgroundColor: Colors.white, valueColor: AlwaysStoppedAnimation(Colors.blue)),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                const Text('Est. 15 mins remaining', style: TextStyle(fontSize: 12, color: Colors.grey)),
                FilledButton.icon(
                  onPressed: () {
                    sl<TelemetryService>().logInteract(id: 'resume_learning', type: 'BUTTON', pageId: 'home');
                  },
                  icon: const Icon(Icons.play_arrow),
                  label: const Text('Resume'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildTodaysPlan() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text("Today's Plan", style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        _buildPlanItem(Icons.calculate, 'Math: Practice Decimals', '10 Questions', Colors.blue),
        _buildPlanItem(Icons.science, 'Science: Super Senses', 'Revision', Colors.green),
      ],
    );
  }

  Widget _buildPlanItem(IconData icon, String title, String subtitle, Color color) {
    return ListTile(
      contentPadding: EdgeInsets.zero,
      leading: CircleAvatar(backgroundColor: color.withOpacity(0.12), child: Icon(icon, color: color)),
      title: Text(title, style: const TextStyle(fontWeight: FontWeight.w600)),
      subtitle: Text(subtitle),
      trailing: const Icon(Icons.chevron_right),
    );
  }

  Widget _buildAiRecommendation() {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(color: Colors.purple.shade50, borderRadius: BorderRadius.circular(16), border: Border.all(color: Colors.purple.shade100)),
      child: const Row(
        children: [
          Icon(Icons.auto_awesome, color: Colors.purple),
          SizedBox(width: 12),
          Expanded(child: Text('Gurukul AI: "You are doing great in Math! Let\'s try a quick quiz on Fractions today?"', style: TextStyle(fontStyle: FontStyle.italic, color: Colors.purple))),
        ],
      ),
    );
  }

  Widget _buildSubjectsGrid() {
    return FutureBuilder<List<String>>(
      future: _subjectsFuture,
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) return const Center(child: CircularProgressIndicator());
        final subjects = snapshot.data ?? [];
        return GridView.builder(
          padding: const EdgeInsets.all(20),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(crossAxisCount: 2, crossAxisSpacing: 16, mainAxisSpacing: 16, childAspectRatio: 0.85),
          itemCount: subjects.length,
          itemBuilder: (context, index) => _SubjectCard(subject: subjects[index], classLevel: widget.classLevel),
        );
      },
    );
  }

  Widget _buildProfileScreen() {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(20),
      child: Column(
        children: [
          const CircleAvatar(radius: 50, backgroundImage: NetworkImage('https://api.dicebear.com/7.x/avataaars/png?seed=Felix')),
          const SizedBox(height: 16),
          const Text('Gurukul Student', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold)),
          const Text('Class 6 • Member since 2024', style: TextStyle(color: Colors.grey)),
          const SizedBox(height: 32),
          _buildProfileStats(),
          const SizedBox(height: 32),
          _buildBadgeSection(),
          const SizedBox(height: 32),
          _buildSettingsSection(),
        ],
      ),
    );
  }

  Widget _buildProfileStats() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          children: [
            _buildStatItem(Icons.timer, '12h', 'Study Time', Colors.blue),
            _buildStatItem(Icons.check_circle, '45', 'Lessons', Colors.green),
            _buildStatItem(Icons.emoji_events, '12', 'Badges', Colors.amber),
          ],
        ),
      ),
    );
  }

  Widget _buildBadgeSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Recent Badges', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        Row(
          children: [
            _buildBadgeIcon(Icons.auto_awesome, 'Quick Learner', Colors.purple),
            _buildBadgeIcon(Icons.local_fire_department, '7 Day Streak', Colors.orange),
            _buildBadgeIcon(Icons.calculate, 'Math Whiz', Colors.blue),
          ],
        ),
      ],
    );
  }

  Widget _buildBadgeIcon(IconData icon, String label, Color color) {
    return Expanded(
      child: Column(
        children: [
          Container(padding: const EdgeInsets.all(12), decoration: BoxDecoration(color: color.withOpacity(0.12), shape: BoxShape.circle), child: Icon(icon, color: color, size: 28)),
          const SizedBox(height: 8),
          Text(label, style: const TextStyle(fontSize: 10), textAlign: TextAlign.center),
        ],
      ),
    );
  }

  Widget _buildSettingsSection() {
    return Column(
      children: [
        _buildSettingsTile(Icons.school, 'Board/Grade/Medium', const Icon(Icons.chevron_right), onTap: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const FrameworkSelectionScreen()))),
        _buildSettingsTile(Icons.dark_mode, 'Dark Mode', Switch(value: false, onChanged: (v) {})),
        _buildSettingsTile(Icons.language, 'Language', const Text('English (India)', style: TextStyle(color: Colors.blue))),
        _buildSettingsTile(Icons.notifications, 'Notifications', const Icon(Icons.chevron_right)),
        _buildSettingsTile(Icons.logout, 'Logout', const Icon(Icons.chevron_right), color: Colors.red),
      ],
    );
  }

  Widget _buildSettingsTile(IconData icon, String label, Widget trailing, {Color? color, VoidCallback? onTap}) {
    return ListTile(onTap: onTap, leading: Icon(icon, color: color ?? Colors.grey.shade700), title: Text(label, style: TextStyle(color: color)), trailing: trailing, contentPadding: EdgeInsets.zero);
  }
}

class _SubjectCard extends StatelessWidget {
  final String subject;
  final int classLevel;
  const _SubjectCard({required this.subject, required this.classLevel});

  @override
  Widget build(BuildContext context) {
    final themeService = sl<ThemeService>();
    final color = themeService.getSubjectColor(subject);
    return Card(
      child: InkWell(
        borderRadius: BorderRadius.circular(20),
        onTap: () {
          sl<TelemetryService>().logInteract(id: 'select_subject_$subject', type: 'CARD', pageId: 'subjects_grid');
          Navigator.push(context, MaterialPageRoute(builder: (context) => SubjectDashboardScreen(classLevel: classLevel, subject: subject)));
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Align(alignment: Alignment.centerRight, child: Icon(_getIconForSubject(subject), size: 32, color: color)),
              const Spacer(),
              Text(subject, style: Theme.of(context).textTheme.titleLarge?.copyWith(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Text('12 Chapters', style: TextStyle(fontSize: 12, color: Colors.grey.shade600)),
              const SizedBox(height: 12),
              ClipRRect(borderRadius: BorderRadius.circular(10), child: LinearProgressIndicator(value: 0.4, backgroundColor: color.withOpacity(0.12), valueColor: AlwaysStoppedAnimation(color), minHeight: 6)),
              const SizedBox(height: 8),
              Row(mainAxisAlignment: MainAxisAlignment.spaceBetween, children: [Text('40% Mastery', style: TextStyle(fontSize: 10, color: color, fontWeight: FontWeight.bold)), const Icon(Icons.arrow_forward_ios, size: 12, color: Colors.grey)]),
            ],
          ),
        ),
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
