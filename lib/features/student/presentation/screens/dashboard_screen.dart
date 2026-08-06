import 'dart:async';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/di/injection.dart';
import '../../../../core/notifications/notification_service.dart';
import '../../../curriculum/data/framework_repository.dart';
import '../../../gamification/presentation/widgets/xp_bar.dart';
import '../../../gamification/data/gamification_repository.dart';
import '../../../gamification/domain/models/achievement.dart';
import '../../../auth/presentation/bloc/auth_bloc.dart';
import 'chapter_list_screen.dart';
import 'progress_dashboard_screen.dart';

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

    // Listen to Auth State
    final authState = context.read<AuthBloc>().state;
    if (authState is AuthAuthenticated) {
      _currentUserId = authState.user.uid;
      _initUserFeatures(_currentUserId!);
    }
  }

  void _initUserFeatures(String userId) {
    _gamificationStream = sl<GamificationRepository>().watchUserStats(userId);

    // Listen for foreground notifications
    _notificationSubscription = sl<NotificationService>().messageStream.listen((message) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(message.notification?.title ?? 'New notification from Gurukul AI'),
            behavior: SnackBarBehavior.floating,
            action: SnackBarAction(
              label: 'View',
              onPressed: () {
                // Handle notification navigation
              },
            ),
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
        appBar: AppBar(
          title: Text(_currentIndex == 0 ? 'Gurukul AI - Class ${widget.classLevel}' : 'My Progress'),
          actions: [
            IconButton(onPressed: () {}, icon: const Icon(Icons.person_outline)),
          ],
        ),
        body: _buildBody(),
        bottomNavigationBar: BottomNavigationBar(
          currentIndex: _currentIndex,
          onTap: (index) => setState(() => _currentIndex = index),
          items: const [
            BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
            BottomNavigationBarItem(icon: Icon(Icons.bar_chart), label: 'Progress'),
          ],
        ),
        floatingActionButton: _currentIndex == 0 ? FloatingActionButton.extended(
          onPressed: () {},
          label: const Text('Ask Gurukul AI'),
          icon: const Icon(Icons.auto_awesome),
        ) : null,
      ),
    );
  }

  Widget _buildBody() {
    if (_currentIndex == 1) {
      return ProgressDashboardScreen(studentId: _currentUserId ?? 'mock_student_id');
    }

    return Column(
      children: [
        _buildHeader(),
        Expanded(
          child: FutureBuilder<List<String>>(
            future: _subjectsFuture,
            builder: (context, snapshot) {
              if (snapshot.connectionState == ConnectionState.waiting) {
                return const Center(child: CircularProgressIndicator());
              }
              final subjects = snapshot.data ?? [];
              return GridView.builder(
                padding: const EdgeInsets.all(16),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 2,
                  crossAxisSpacing: 16,
                  mainAxisSpacing: 16,
                  childAspectRatio: 1.2,
                ),
                itemCount: subjects.length,
                itemBuilder: (context, index) {
                  final subject = subjects[index];
                  return _SubjectCard(subject: subject, classLevel: widget.classLevel);
                },
              );
            },
          ),
        ),
      ],
    );
  }

  Widget _buildHeader() {
    if (_gamificationStream == null) return const SizedBox.shrink();
    return StreamBuilder<UserGamification>(
      stream: _gamificationStream!,
      builder: (context, snapshot) {
        if (!snapshot.hasData) return const SizedBox.shrink();
        final stats = snapshot.data!;
        return Container(
          padding: const EdgeInsets.all(16),
          color: Theme.of(context).primaryColor.withOpacity(0.1),
          child: Row(
            children: [
              CircleAvatar(
                backgroundColor: Theme.of(context).primaryColor,
                child: Text('Lvl ${stats.level}', style: const TextStyle(color: Colors.white, fontSize: 12)),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: XpBar(currentXp: stats.currentXp % 1000, maxXp: 1000),
              ),
              const SizedBox(width: 16),
              Column(
                children: [
                  const Icon(Icons.fireplace, color: Colors.orange),
                  Text('${stats.currentStreak} days', style: const TextStyle(fontSize: 10)),
                ],
              )
            ],
          ),
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
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: () {
          Navigator.push(
            context,
            MaterialPageRoute(
              builder: (context) => ChapterListScreen(
                classLevel: classLevel,
                subject: subject,
              ),
            ),
          );
        },
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(_getIconForSubject(subject), size: 40, color: Theme.of(context).primaryColor),
              const SizedBox(height: 12),
              Text(subject, style: Theme.of(context).textTheme.titleMedium),
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
      default: return Icons.school;
    }
  }
}
