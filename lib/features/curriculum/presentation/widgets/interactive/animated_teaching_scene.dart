import 'package:flutter/material.dart';
import 'package:lottie/lottie.dart';

class AnimatedTeachingScene extends StatelessWidget {
  final String assetPath;
  final String caption;
  final String? audioPath;

  const AnimatedTeachingScene({
    super.key,
    required this.assetPath,
    required this.caption,
    this.audioPath,
  });

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;

    return Column(
      children: [
        Expanded(
          child: Center(
            child: assetPath.endsWith('.json')
                ? Lottie.asset(
                    assetPath,
                    repeat: true,
                    errorBuilder: (context, error, stackTrace) {
                      return Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(Icons.movie_filter_outlined,
                              size: 80, color: colorScheme.primary.withValues(alpha: 0.2)),
                          const SizedBox(height: 16),
                          const Text(
                            'Visualizing Concept...',
                            style: TextStyle(color: Colors.grey, fontStyle: FontStyle.italic),
                          ),
                        ],
                      );
                    },
                  )
                : Icon(Icons.animation, size: 100, color: colorScheme.primary),
          ),
        ),
        Container(
          padding: const EdgeInsets.all(16),
          margin: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white,
            borderRadius: BorderRadius.circular(16),
            boxShadow: [
              BoxShadow(
                color: Colors.black.withValues(alpha: 0.05),
                blurRadius: 10,
                offset: const Offset(0, 4),
              ),
            ],
          ),
          child: Text(
            caption,
            textAlign: TextAlign.center,
            style: const TextStyle(
              fontSize: 16,
              fontWeight: FontWeight.w500,
              height: 1.5,
            ),
          ),
        ),
      ],
    );
  }
}
