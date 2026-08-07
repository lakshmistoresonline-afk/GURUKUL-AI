import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:fl_chart/fl_chart.dart';

class ParentDashboardScreen extends StatelessWidget {
  const ParentDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: Text('Parent Insight', style: DesignSystem.h2),
        backgroundColor: DesignSystem.background,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(DesignSystem.spacingMd),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildChildSelector(),
            const SizedBox(height: DesignSystem.spacingLg),
            _buildDailyProgressCard(),
            const SizedBox(height: DesignSystem.spacingLg),
            Text('LEARNING GAPS', style: DesignSystem.label),
            const SizedBox(height: DesignSystem.spacingMd),
            _buildLearningGaps(),
            const SizedBox(height: DesignSystem.spacingLg),
            _buildStudySuggestions(),
          ],
        ),
      ),
    );
  }

  Widget _buildChildSelector() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: Row(
        children: [
          const CircleAvatar(
            radius: 24,
            backgroundImage: NetworkImage('https://api.dicebear.com/7.x/avataaars/png?seed=Felix'),
          ),
          const SizedBox(width: DesignSystem.spacingMd),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Felix Sharma', style: DesignSystem.title),
              Text('Class 5 • Section A', style: DesignSystem.bodySmall),
            ],
          ),
          const Spacer(),
          const Icon(Icons.keyboard_arrow_down, color: DesignSystem.textTertiary),
        ],
      ),
    );
  }

  Widget _buildDailyProgressCard() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('STUDY TIME THIS WEEK', style: DesignSystem.label),
          const SizedBox(height: DesignSystem.spacingLg),
          SizedBox(
            height: 150,
            child: BarChart(
              BarChartData(
                gridData: const FlGridData(show: false),
                titlesData: const FlTitlesData(show: false),
                borderData: FlBorderData(show: false),
                barGroups: [
                  BarChartGroupData(x: 0, barRods: [BarChartRodData(toY: 2, color: DesignSystem.primary)]),
                  BarChartGroupData(x: 1, barRods: [BarChartRodData(toY: 3, color: DesignSystem.primary)]),
                  BarChartGroupData(x: 2, barRods: [BarChartRodData(toY: 1.5, color: DesignSystem.primary)]),
                  BarChartGroupData(x: 3, barRods: [BarChartRodData(toY: 4, color: DesignSystem.primary)]),
                  BarChartGroupData(x: 4, barRods: [BarChartRodData(toY: 2.5, color: DesignSystem.primary)]),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildLearningGaps() {
    return Column(
      children: [
        _gapItem('Fractions', 'Struggling with Division', Colors.red),
        _gapItem('Science', 'Needs Revision: Digestive System', Colors.orange),
      ],
    );
  }

  Widget _gapItem(String subject, String issue, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: DesignSystem.spacingSm),
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: Row(
        children: [
          Icon(Icons.warning_amber_rounded, color: color),
          const SizedBox(width: DesignSystem.spacingMd),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(subject, style: DesignSystem.title.copyWith(fontSize: 14)),
              Text(issue, style: DesignSystem.bodySmall),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildStudySuggestions() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingLg),
      decoration: BoxDecoration(
        color: DesignSystem.primary.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Icon(Icons.auto_awesome, color: DesignSystem.primary),
          const SizedBox(height: DesignSystem.spacingMd),
          Text('AI SUGGESTION', style: DesignSystem.label.copyWith(color: DesignSystem.primary)),
          const SizedBox(height: DesignSystem.spacingSm),
          Text(
            'Felix is finding "Fractions" difficult. Spend 15 minutes tonight doing a hands-on pizza cutting activity to help him visualize the concept.',
            style: DesignSystem.bodySmall.copyWith(color: DesignSystem.textPrimary, fontWeight: FontWeight.w500),
          ),
        ],
      ),
    );
  }
}
