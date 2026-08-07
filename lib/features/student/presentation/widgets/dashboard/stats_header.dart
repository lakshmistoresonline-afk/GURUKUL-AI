import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class StatsHeader extends StatelessWidget {
  const StatsHeader({super.key});

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceAround,
      children: [
        _buildStat(Icons.local_fire_department, '7', 'Days', Colors.orange),
        _buildStat(Icons.stars, '1.2k', 'XP', Colors.blue),
        _buildStat(Icons.monetization_on, '450', 'Coins', Colors.amber),
        _buildStat(Icons.military_tech, 'Lvl 5', 'Rank', Colors.purple),
      ],
    );
  }

  Widget _buildStat(IconData icon, String value, String label, Color color) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(DesignSystem.spacingSm),
          decoration: BoxDecoration(
            color: color.withOpacity(0.1),
            shape: BoxShape.circle,
          ),
          child: Icon(icon, color: color, size: 24),
        ),
        const SizedBox(height: DesignSystem.spacingXs),
        Text(value, style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16)),
        Text(label, style: const TextStyle(fontSize: 10, color: Colors.grey)),
      ],
    );
  }
}
