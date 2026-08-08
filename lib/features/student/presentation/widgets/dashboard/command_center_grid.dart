import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

import 'package:project_gurukul_ai/features/questions/presentation/screens/question_center_screen.dart';
import 'package:project_gurukul_ai/features/notebook/presentation/screens/notebook_screen.dart';
import 'package:project_gurukul_ai/features/ai/presentation/screens/ai_tutor_chat_screen.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/flashcards_screen.dart';
import 'package:project_gurukul_ai/features/student/presentation/screens/homework_screen.dart';

class CommandCenterGrid extends StatelessWidget {
  final int classLevel;
  final Function(int)? onTabChange;
  const CommandCenterGrid({super.key, required this.classLevel, this.onTabChange});

  @override
  Widget build(BuildContext context) {
    final actions = [
      _ActionData(Icons.smart_toy_rounded, 'AI Tutor', Colors.indigo, () => onTabChange?.call(2)),
      _ActionData(Icons.menu_book_rounded, 'Reading', Colors.blue, () => onTabChange?.call(1)),
      _ActionData(Icons.help_center_rounded, 'Q Centre', Colors.amber, () => Navigator.push(context, MaterialPageRoute(builder: (_) => QuestionCenterScreen(classLevel: classLevel, subject: 'Mathematics')))),
      _ActionData(Icons.style_rounded, 'Flashcards', Colors.orange, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const FlashcardsScreen(subject: 'Mathematics')))),
      _ActionData(Icons.hub_rounded, 'Mind Maps', Colors.purple, () {}),
      _ActionData(Icons.assignment_rounded, 'Homework', Colors.pink, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const HomeworkScreen()))),
      _ActionData(Icons.edit_note, 'Notebook', Colors.teal, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const NotebookScreen()))),
      _ActionData(Icons.more_horiz_rounded, 'More', Colors.grey, () => onTabChange?.call(4)),
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
      onTap: action.onTap,
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
  final VoidCallback onTap;

  _ActionData(this.icon, this.label, this.color, this.onTap);
}
