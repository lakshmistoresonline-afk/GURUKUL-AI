import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class GamificationStatsRow extends StatelessWidget {
  final int xp;
  final int coins;
  final int certificates;

  const GamificationStatsRow({
    super.key,
    this.xp = 0,
    this.coins = 0,
    this.certificates = 0,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: DesignSystem.spacingMd),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceAround,
        children: [
          _buildStatItem(Icons.bolt_rounded, '$xp XP', Colors.amber),
          _buildDivider(),
          _buildStatItem(Icons.monetization_on_rounded, '$coins Coins', DesignSystem.orange),
          _buildDivider(),
          _buildStatItem(Icons.verified_rounded, '$certificates Badges', DesignSystem.primary),
        ],
      ),
    );
  }

  Widget _buildDivider() {
    return Container(
      height: 24,
      width: 1,
      color: DesignSystem.border,
    );
  }

  Widget _buildStatItem(IconData icon, String label, Color color) {
    return Row(
      children: [
        Icon(icon, color: color, size: 20),
        const SizedBox(width: DesignSystem.spacingXs),
        Text(
          label,
          style: DesignSystem.titleLarge.copyWith(fontSize: 14),
        ),
      ],
    );
  }
}
