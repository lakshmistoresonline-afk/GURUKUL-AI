import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class DailyChallengeCard extends StatelessWidget {
  const DailyChallengeCard({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingLg),
      decoration: BoxDecoration(
        gradient: const LinearGradient(
          colors: [Color(0xFFFB923C), Color(0xFFF97316)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
        boxShadow: DesignSystem.shadowMd,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              const Icon(Icons.bolt, color: Colors.white, size: 24),
              const SizedBox(width: DesignSystem.spacingSm),
              Expanded(
                child: Text(
                  'DAILY CHALLENGE',
                  style: DesignSystem.labelSmall.copyWith(color: Colors.white70),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: DesignSystem.spacingSm),
              const Text('12h left', style: TextStyle(color: Colors.white60, fontSize: 11)),
            ],
          ),
          const SizedBox(height: DesignSystem.spacingMd),
          Text(
            'Mental Math Marathon',
            style: DesignSystem.headlineLarge.copyWith(color: Colors.white, fontSize: 22),
          ),
          const SizedBox(height: DesignSystem.spacingSm),
          const Text(
            'Solve 10 problems in 2 minutes to earn 100 XP and 50 Coins!',
            style: TextStyle(color: Colors.white70, fontSize: 14),
          ),
          const SizedBox(height: DesignSystem.spacingLg),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () {},
              style: ElevatedButton.styleFrom(
                backgroundColor: Colors.white,
                foregroundColor: const Color(0xFFF97316),
                shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(DesignSystem.radiusMd)),
              ),
              child: const Text('Start Challenge'),
            ),
          ),
        ],
      ),
    );
  }
}
