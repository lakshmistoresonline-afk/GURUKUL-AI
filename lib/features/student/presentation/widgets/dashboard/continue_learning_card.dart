import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:project_gurukul_ai/features/curriculum/data/framework_repository.dart';
import 'package:project_gurukul_ai/features/curriculum/presentation/screens/learning_journey_screen.dart';

class ContinueLearningCard extends StatelessWidget {
  const ContinueLearningCard({super.key});

  Future<void> _handleContinue(BuildContext context) async {
    // In a real app, fetch last accessed from local storage
    // For now, fetch first chapter of Class 5 Mathematics as fallback
    final chapters = await sl<FrameworkRepository>().getChapters(5, 'Mathematics');
    if (chapters.isNotEmpty) {
      final node = await sl<FrameworkRepository>().getConceptNode(chapters.first['id']);
      if (node != null && context.mounted) {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: node)),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      decoration: BoxDecoration(
        gradient: LinearGradient(
          colors: [DesignSystem.primary, DesignSystem.primary.withBlue(255)],
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
        ),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
        boxShadow: [
          BoxShadow(
            color: DesignSystem.primary.withValues(alpha: 0.3),
            blurRadius: 15,
            offset: const Offset(0, 8),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: () => _handleContinue(context),
          borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
          child: Stack(
            children: [
              Positioned(
                right: -20,
                top: -20,
                child: Icon(Icons.auto_stories, size: 120, color: Colors.white.withValues(alpha: 0.1)),
              ),
              Padding(
                padding: const EdgeInsets.all(DesignSystem.spacingLg),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                          decoration: BoxDecoration(
                            color: Colors.white.withValues(alpha: 0.2),
                            borderRadius: BorderRadius.circular(DesignSystem.radiusSm),
                          ),
                          child: const Text(
                            'CONTINUE LEARNING',
                            style: TextStyle(color: Colors.white, fontSize: 10, fontWeight: FontWeight.bold, letterSpacing: 0.5),
                          ),
                        ),
                        const Spacer(),
                        const Icon(Icons.more_horiz, color: Colors.white70),
                      ],
                    ),
                    const SizedBox(height: DesignSystem.spacingLg),
                    Text(
                      'The Fish Tale',
                      style: DesignSystem.h2.copyWith(color: Colors.white, fontSize: 24),
                    ),
                    const Text(
                      'Chapter 1 • Mathematics',
                      style: TextStyle(color: Colors.white70, fontSize: 14),
                    ),
                    const SizedBox(height: DesignSystem.spacingLg),
                    Row(
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              const Row(
                                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                children: [
                                  Text('65% Mastery', style: TextStyle(color: Colors.white, fontSize: 12, fontWeight: FontWeight.w600)),
                                  Text('12 mins left', style: TextStyle(color: Colors.white70, fontSize: 12)),
                                ],
                              ),
                              const SizedBox(height: 8),
                              ClipRRect(
                                borderRadius: BorderRadius.circular(10),
                                child: LinearProgressIndicator(
                                  value: 0.65,
                                  backgroundColor: Colors.white.withValues(alpha: 0.1),
                                  valueColor: const AlwaysStoppedAnimation<Color>(DesignSystem.accent),
                                  minHeight: 8,
                                ),
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: DesignSystem.spacingLg),
                        Container(
                          decoration: const BoxDecoration(
                            color: Colors.white,
                            shape: BoxShape.circle,
                          ),
                          child: const Padding(
                            padding: EdgeInsets.all(8.0),
                            child: Icon(Icons.play_arrow_rounded, color: DesignSystem.primary, size: 32),
                          ),
                        ),
                      ],
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
