import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class CommandCenterGrid extends StatelessWidget {
  const CommandCenterGrid({super.key});

  @override
  Widget build(BuildContext context) {
    final actions = [
      _ActionData(Icons.smart_toy_rounded, 'AI Tutor', Colors.indigo),
      _ActionData(Icons.menu_book_rounded, 'Reading', Colors.blue),
      _ActionData(Icons.help_center_rounded, 'Q Centre', Colors.amber),
      _ActionData(Icons.style_rounded, 'Flashcards', Colors.orange),
      _ActionData(Icons.hub_rounded, 'Mind Maps', Colors.purple),
      _ActionData(Icons.assignment_rounded, 'Homework', Colors.pink),
      _ActionData(Icons.bookmarks_rounded, 'Bookmarks', Colors.teal),
      _ActionData(Icons.more_horiz_rounded, 'More', Colors.grey),
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('COMMAND CENTER', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: DesignSystem.textSecondary)),
        const SizedBox(height: DesignSystem.spacingMd),
        LayoutBuilder(
          builder: (context, constraints) {
            final crossAxisCount = constraints.maxWidth > 600 ? 6 : 4;
            return GridView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: crossAxisCount,
                crossAxisSpacing: DesignSystem.spacingMd,
                mainAxisSpacing: DesignSystem.spacingMd,
                childAspectRatio: 0.85,
              ),
              itemCount: actions.length,
              itemBuilder: (context, index) {
                final action = actions[index];
                return _buildActionItem(context, action);
              },
            );
          },
        ),
      ],
    );
  }

  Widget _buildActionItem(BuildContext context, _ActionData action) {
    return InkWell(
      onTap: () {},
      borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
      child: Column(
        children: [
          Expanded(
            child: Container(
              width: double.infinity,
              decoration: BoxDecoration(
                color: DesignSystem.surface,
                borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
                border: Border.all(color: DesignSystem.border),
                boxShadow: [
                  BoxShadow(
                    color: action.color.withValues(alpha: 0.1),
                    blurRadius: 10,
                    offset: const Offset(0, 4),
                  ),
                ],
              ),
              child: Icon(action.icon, color: action.color, size: 28),
            ),
          ),
          const SizedBox(height: DesignSystem.spacingSm),
          Text(
            action.label,
            style: const TextStyle(fontSize: 11, fontWeight: FontWeight.w600),
            textAlign: TextAlign.center,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}

class _ActionData {
  final IconData icon;
  final String label;
  final Color color;

  _ActionData(this.icon, this.label, this.color);
}
