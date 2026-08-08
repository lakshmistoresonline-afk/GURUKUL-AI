import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class AiRecommendationSection extends StatelessWidget {
  final Function(int)? onTabChange;
  const AiRecommendationSection({super.key, this.onTabChange});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            const Icon(Icons.auto_awesome, color: DesignSystem.secondary, size: 20),
            const SizedBox(width: DesignSystem.spacingSm),
            Text('AI PERSONALIZED INSIGHTS', style: DesignSystem.labelSmall.copyWith(color: DesignSystem.secondary)),
          ],
        ),
        const SizedBox(height: DesignSystem.spacingMd),
        SizedBox(
          height: 160,
          child: ListView(
            scrollDirection: Axis.horizontal,
            clipBehavior: Clip.none,
            children: [
              _buildRecommendationCard(
                'AI Teacher Says',
                'Welcome! Let\'s start by exploring "The Fish Tale" in Mathematics.',
                Icons.emoji_events_rounded,
                DesignSystem.secondary,
                'View Stats',
                () => onTabChange?.call(3)
              ),
              _buildRecommendationCard(
                'Personalized Tip',
                'Flashcards are a great way to remember "Super Senses" in EVS.',
                Icons.trending_up_rounded,
                DesignSystem.orange,
                'Start Practice',
                () => onTabChange?.call(1)
              ),
              _buildRecommendationCard(
                'Learning Goal',
                'Try to complete the first chapter of every subject this week.',
                Icons.stars_rounded,
                DesignSystem.accent,
                'Take Challenge',
                () => onTabChange?.call(1)
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildRecommendationCard(String title, String subtitle, IconData icon, Color color, String action, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      child: Container(
        width: 260,
        margin: const EdgeInsets.only(right: DesignSystem.spacingMd),
        padding: const EdgeInsets.all(DesignSystem.spacingMd),
        decoration: BoxDecoration(
          color: DesignSystem.surface,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
          border: Border.all(color: color.withValues(alpha: 0.2)),
          boxShadow: [
            BoxShadow(
              color: color.withValues(alpha: 0.05),
              blurRadius: 10,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Icon(icon, color: color, size: 20),
                const SizedBox(width: DesignSystem.spacingSm),
                Text(title, style: TextStyle(color: color, fontWeight: FontWeight.bold, fontSize: 12)),
              ],
            ),
            const SizedBox(height: DesignSystem.spacingSm),
            Expanded(
              child: Text(
                subtitle,
                style: DesignSystem.bodyMedium.copyWith(fontSize: 13, height: 1.3),
                maxLines: 3,
                overflow: TextOverflow.ellipsis,
              ),
            ),
            const SizedBox(height: DesignSystem.spacingSm),
            Text(
              action,
              style: TextStyle(color: color, fontWeight: FontWeight.w700, fontSize: 12),
            ),
          ],
        ),
      ),
    );
  }
}
