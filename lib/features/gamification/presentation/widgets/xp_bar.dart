import 'package:flutter/material.dart';

class XpBar extends StatelessWidget {
  final int currentXp;
  final int maxXp;

  const XpBar({super.key, required this.currentXp, required this.maxXp});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        LinearProgressIndicator(
          value: currentXp / maxXp,
          backgroundColor: Colors.grey[300],
          valueColor: const AlwaysStoppedAnimation<Color>(Colors.amber),
        ),
        const SizedBox(height: 4),
        Text('$currentXp / $maxXp XP', style: Theme.of(context).textTheme.bodySmall),
      ],
    );
  }
}
