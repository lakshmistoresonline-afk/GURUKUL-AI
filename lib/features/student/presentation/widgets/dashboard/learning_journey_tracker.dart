import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/chapter_dashboard_screen.dart';

class LearningJourneyTracker extends StatelessWidget {
  final int classLevel;
  final Function(int)? onTabChange;
  const LearningJourneyTracker({super.key, required this.classLevel, this.onTabChange});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const Text('LEARNING JOURNEY', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: DesignSystem.textSecondary)),
            TextButton(
              onPressed: () => onTabChange?.call(1),
              child: const Text('View Roadmap', style: TextStyle(fontSize: 12)),
            ),
          ],
        ),
        FutureBuilder<List<Map<String, dynamic>>>(
          future: sl<FrameworkRepository>().getAllChapters(classLevel),
          builder: (context, snapshot) {
            final chapters = snapshot.data ?? [];
            return Container(
              height: 100,
              padding: const EdgeInsets.symmetric(vertical: DesignSystem.spacingMd),
              decoration: BoxDecoration(
                color: DesignSystem.surface,
                borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
                border: Border.all(color: DesignSystem.border),
              ),
              child: ListView.builder(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingMd),
                itemCount: chapters.length,
                itemBuilder: (context, index) {
                  final isCurrent = index == 0;

                  return Row(
                    children: [
                      Column(
                        children: [
                          InkWell(
                            onTap: () {
                              Navigator.push(context, MaterialPageRoute(builder: (_) => ChapterDashboardScreen(chapterId: chapters[index]['id'], subject: chapters[index]['subject'])));
                            },
                            child: Container(
                              width: 40,
                              height: 40,
                              decoration: BoxDecoration(
                                shape: BoxShape.circle,
                                color: isCurrent ? DesignSystem.primary : DesignSystem.background,
                                border: isCurrent ? Border.all(color: DesignSystem.primary.withValues(alpha: 0.3), width: 4) : null,
                              ),
                              child: Icon(
                                isCurrent ? Icons.auto_awesome : Icons.lock_outline,
                                color: isCurrent ? Colors.white : DesignSystem.textTertiary,
                                size: 20,
                              ),
                            ),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Ch ${index + 1}',
                            style: TextStyle(
                              fontSize: 10,
                              fontWeight: isCurrent ? FontWeight.bold : FontWeight.normal,
                              color: isCurrent ? DesignSystem.primary : DesignSystem.textSecondary,
                            ),
                          ),
                        ],
                      ),
                      if (index < chapters.length - 1)
                        Container(
                          width: 40,
                          height: 2,
                          margin: const Offset(0, -20).dy != 0 ? const EdgeInsets.only(bottom: 20) : EdgeInsets.zero,
                          color: DesignSystem.border,
                        ),
                    ],
                  );
                },
              ),
            );
          }
        ),
      ],
    );
  }
}
