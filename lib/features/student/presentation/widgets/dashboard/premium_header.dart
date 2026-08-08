import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class PremiumHeader extends StatelessWidget {
  final String studentName;
  final int level;
  final double dailyGoalProgress;

  const PremiumHeader({
    super.key,
    this.studentName = 'Scholar',
    this.level = 12,
    this.dailyGoalProgress = 0.75,
  });

  @override
  Widget build(BuildContext context) {
    final String greeting = _getGreeting();

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingMd, vertical: DesignSystem.spacingLg),
      child: Row(
        children: [
          Stack(
            alignment: Alignment.bottomRight,
            children: [
              Container(
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  border: Border.all(color: DesignSystem.primary.withValues(alpha: 0.2), width: 3),
                ),
                child: const CircleAvatar(
                  radius: 35,
                  backgroundImage: NetworkImage('https://api.dicebear.com/7.x/avataaars/png?seed=Gurukul'),
                ),
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
                decoration: BoxDecoration(
                  color: DesignSystem.orange,
                  borderRadius: BorderRadius.circular(10),
                  border: Border.all(color: Colors.white, width: 1.5),
                ),
                child: Text(
                  'Lvl $level',
                  style: const TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold),
                ),
              ),
            ],
          ),
          const SizedBox(width: DesignSystem.spacingMd),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  '$greeting,',
                  style: DesignSystem.bodyMedium.copyWith(color: DesignSystem.textSecondary),
                ),
                Text(
                  studentName,
                  style: DesignSystem.h2.copyWith(fontSize: 24, height: 1.1),
                ),
              ],
            ),
          ),
          _DailyGoalRing(progress: dailyGoalProgress),
        ],
      ),
    );
  }

  String _getGreeting() {
    final hour = DateTime.now().hour;
    if (hour < 12) return 'Good Morning';
    if (hour < 17) return 'Good Afternoon';
    return 'Good Evening';
  }
}

class _DailyGoalRing extends StatelessWidget {
  final double progress;

  const _DailyGoalRing({required this.progress});

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: () {
         ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('You are on track! Keep learning to hit your goal.')),
        );
      },
      child: Column(
        children: [
          Stack(
            alignment: Alignment.center,
            children: [
              SizedBox(
                width: 55,
                height: 55,
                child: CircularProgressIndicator(
                  value: progress,
                  strokeWidth: 6,
                  backgroundColor: DesignSystem.primary.withValues(alpha: 0.1),
                  valueColor: const AlwaysStoppedAnimation<Color>(DesignSystem.accent),
                  strokeCap: StrokeCap.round,
                ),
              ),
              Text(
                '${(progress * 100).toInt()}%',
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 12),
              ),
            ],
          ),
          const SizedBox(height: 4),
          const Text('Daily Goal', style: TextStyle(fontSize: 10, fontWeight: FontWeight.w600)),
        ],
      ),
    );
  }
}
