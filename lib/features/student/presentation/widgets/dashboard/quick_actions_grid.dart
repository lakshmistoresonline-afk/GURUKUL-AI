import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/features/content/presentation/screens/content_store_screen.dart';
import 'package:project_gurukul_ai/features/questions/presentation/screens/question_center_screen.dart';
import 'package:project_gurukul_ai/features/notebook/presentation/screens/notebook_screen.dart';
import 'package:project_gurukul_ai/features/teacher/presentation/screens/teacher_dashboard_screen.dart';
import 'package:project_gurukul_ai/features/content/presentation/screens/admin/content_studio_screen.dart';

class QuickActionsGrid extends StatelessWidget {
  const QuickActionsGrid({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('QUICK ACTIONS', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 13, color: DesignSystem.textSecondary)),
        const SizedBox(height: DesignSystem.spacingMd),
        GridView.count(
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisCount: 4,
          crossAxisSpacing: DesignSystem.spacingMd,
          mainAxisSpacing: DesignSystem.spacingMd,
          children: [
            _buildActionItem(context, Icons.help_center_outlined, 'Q Centre', Colors.amber, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const QuestionCenterScreen(classLevel: 5, subject: 'Mathematics')))),
            _buildActionItem(context, Icons.edit_note, 'Notebook', Colors.indigo, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const NotebookScreen()))),
            _buildActionItem(context, Icons.local_mall_outlined, 'Store', Colors.orange, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ContentStoreScreen()))),
            _buildActionItem(context, Icons.admin_panel_settings_outlined, 'Studio', Colors.pink, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const ContentStudioScreen()))),
            _buildActionItem(context, Icons.school_outlined, 'Teacher', Colors.blueGrey, () => Navigator.push(context, MaterialPageRoute(builder: (_) => const TeacherDashboardScreen()))),
            _buildActionItem(context, Icons.videogame_asset_outlined, 'Games', Colors.green, () {}),
            _buildActionItem(context, Icons.auto_awesome, 'Lab', Colors.deepPurple, () {}),
            _buildActionItem(context, Icons.settings_outlined, 'Settings', Colors.grey, () {}),
          ],
        ),
      ],
    );
  }

  Widget _buildActionItem(BuildContext context, IconData icon, String label, Color color, VoidCallback onTap) {
    return InkWell(
      onTap: onTap,
      child: Column(
        children: [
          Container(
            width: 50,
            height: 50,
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
            ),
            child: Icon(icon, color: color, size: 24),
          ),
          const SizedBox(height: DesignSystem.spacingXs),
          Text(
            label,
            style: const TextStyle(fontSize: 10, fontWeight: FontWeight.bold),
            textAlign: TextAlign.center,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }
}
