import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class LearningJourneyTracker extends StatelessWidget {
  const LearningJourneyTracker({super.key});

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
              onPressed: () {},
              child: const Text('View Roadmap', style: TextStyle(fontSize: 12)),
            ),
          ],
        ),
        Container(
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
            itemCount: 5,
            itemBuilder: (context, index) {
              final isCompleted = index < 2;
              final isCurrent = index == 2;

              return Row(
                children: [
                  Column(
                    children: [
                      Container(
                        width: 40,
                        height: 40,
                        decoration: BoxDecoration(
                          shape: BoxShape.circle,
                          color: isCompleted ? DesignSystem.accent : (isCurrent ? DesignSystem.primary : DesignSystem.background),
                          border: isCurrent ? Border.all(color: DesignSystem.primary.withOpacity(0.3), width: 4) : null,
                        ),
                        child: Icon(
                          isCompleted ? Icons.check : (isCurrent ? Icons.auto_awesome : Icons.lock_outline),
                          color: isCompleted || isCurrent ? Colors.white : DesignSystem.textTertiary,
                          size: 20,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Step ${index + 1}',
                        style: TextStyle(
                          fontSize: 10,
                          fontWeight: isCurrent ? FontWeight.bold : FontWeight.normal,
                          color: isCurrent ? DesignSystem.primary : DesignSystem.textSecondary,
                        ),
                      ),
                    ],
                  ),
                  if (index < 4)
                    Container(
                      width: 40,
                      height: 2,
                      margin: const EdgeInsets.only(bottom: 20),
                      color: isCompleted ? DesignSystem.accent : DesignSystem.border,
                    ),
                ],
              );
            },
          ),
        ),
      ],
    );
  }
}
