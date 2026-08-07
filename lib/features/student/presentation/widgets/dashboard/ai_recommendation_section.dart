import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class AiRecommendationSection extends StatelessWidget {
  const AiRecommendationSection({super.key});

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
                'Your speed in Geometry has improved by 20% this week! Keep it up.',
                Icons.emoji_events_rounded,
                DesignSystem.secondary,
                'View Stats',
              ),
              _buildRecommendationCard(
                'Weak Concept',
                'Fractions: Addition of unlike denominators needs practice.',
                Icons.trending_down_rounded,
                DesignSystem.orange,
                'Start Practice',
              ),
              _buildRecommendationCard(
                'Strong Concept',
                'You are a Master of "Photosynthesis"! Help a peer today.',
                Icons.trending_up_rounded,
                DesignSystem.accent,
                'Take Challenge',
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildRecommendationCard(String title, String subtitle, IconData icon, Color color, String action) {
    return Container(
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
    );
  }
}
