import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/learning_journey_screen.dart';
import 'package:project_gurukul_ai/features/gamification/domain/services/daily_challenge_service.dart';

class DailyChallengeCard extends StatelessWidget {
  const DailyChallengeCard({super.key});

  @override
  Widget build(BuildContext context) {
    final challenge = sl<DailyChallengeService>().getTodaysChallenge();

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
            challenge.title,
            style: DesignSystem.headlineLarge.copyWith(color: Colors.white, fontSize: 22),
          ),
          const SizedBox(height: DesignSystem.spacingSm),
          Text(
            challenge.description,
            style: const TextStyle(color: Colors.white70, fontSize: 14),
          ),
          const SizedBox(height: DesignSystem.spacingLg),
          SizedBox(
            width: double.infinity,
            child: ElevatedButton(
              onPressed: () async {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Loading ${challenge.title}...')),
                );

                // Map challenge type to subject
                String subject = 'Mathematics';
                if (challenge.type == 'english') subject = 'English';
                if (challenge.type == 'evs') subject = 'EVS';
                if (challenge.type == 'hindi') subject = 'Hindi';

                final chapters = await sl<FrameworkRepository>().getChapters(5, subject);
                if (chapters.isNotEmpty && chapters.first['id'] != null && context.mounted) {
                   final node = await sl<FrameworkRepository>().getConceptNode(chapters.first['id'].toString());
                   if (node != null && context.mounted) {
                      Navigator.push(context, MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: node)));
                   }
                }
              },
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
