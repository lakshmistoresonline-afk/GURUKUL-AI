import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:fl_chart/fl_chart.dart';
import 'detailed_analytics_screen.dart';

class TeacherDashboardScreen extends StatelessWidget {
  const TeacherDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: Text('Teacher Dashboard', style: DesignSystem.h2),
        backgroundColor: DesignSystem.background,
        actions: [
          IconButton(onPressed: () {}, icon: const Icon(Icons.group_add_outlined)),
        ],
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DesignSystem.spacingMd),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildClassOverview(),
            const SizedBox(height: DesignSystem.spacingLg),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('SUBJECT PERFORMANCE', style: DesignSystem.label),
                TextButton(
                  onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const DetailedAnalyticsScreen())),
                  child: const Text('View Detailed Reports'),
                ),
              ],
            ),
            const SizedBox(height: DesignSystem.spacingSm),
            _buildPerformanceChart(),
            const SizedBox(height: DesignSystem.spacingLg),
            Text('PENDING ASSIGNMENTS', style: DesignSystem.label),
            const SizedBox(height: DesignSystem.spacingMd),
            _buildAssignmentsList(),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        label: const Text('Create Assignment'),
        icon: const Icon(Icons.add),
        backgroundColor: DesignSystem.primary,
        foregroundColor: Colors.white,
      ),
    );
  }

  Widget _buildClassOverview() {
    return Row(
      children: [
        _summaryBox('Grade 5A', '42 Students', DesignSystem.primary),
        const SizedBox(width: DesignSystem.spacingMd),
        _summaryBox('84%', 'Avg. Mastery', DesignSystem.accent),
      ],
    );
  }

  Widget _summaryBox(String value, String label, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(DesignSystem.spacingMd),
        decoration: DesignSystem.cardDecoration,
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(value, style: DesignSystem.h2.copyWith(color: color, fontSize: 22)),
            Text(label, style: DesignSystem.bodySmall),
          ],
        ),
      ),
    );
  }

  Widget _buildPerformanceChart() {
    return Container(
      height: 200,
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: BarChart(
        BarChartData(
          titlesData: const FlTitlesData(show: false),
          borderData: FlBorderData(show: false),
          barGroups: [
            BarChartGroupData(x: 0, barRods: [BarChartRodData(toY: 8, color: Colors.blue)]),
            BarChartGroupData(x: 1, barRods: [BarChartRodData(toY: 6, color: Colors.green)]),
            BarChartGroupData(x: 2, barRods: [BarChartRodData(toY: 9, color: Colors.purple)]),
            BarChartGroupData(x: 3, barRods: [BarChartRodData(toY: 7, color: Colors.orange)]),
          ],
        ),
      ),
    );
  }

  Widget _buildAssignmentsList() {
    final list = [
      {'title': 'Math: Fractions Homework', 'status': '28/42 Submitted'},
      {'title': 'Science: Plant Diagram', 'status': '15/42 Submitted'},
    ];
    return Column(
      children: list.map((a) => Container(
        margin: const EdgeInsets.only(bottom: DesignSystem.spacingSm),
        decoration: DesignSystem.cardDecoration,
        child: ListTile(
          title: Text(a['title']!, style: const TextStyle(fontWeight: FontWeight.bold)),
          subtitle: Text(a['status']!),
          trailing: const Icon(Icons.chevron_right),
        ),
      )).toList(),
    );
  }
}
