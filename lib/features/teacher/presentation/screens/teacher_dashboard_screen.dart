import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import 'detailed_analytics_screen.dart';

class TeacherDashboardScreen extends StatelessWidget {
  const TeacherDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Teacher Dashboard')),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              _buildClassOverview(),
              const SizedBox(height: 32),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text('Subject Performance', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  TextButton(
                    onPressed: () => Navigator.push(context, MaterialPageRoute(builder: (_) => const DetailedAnalyticsScreen())),
                    child: const Text('View Reports'),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              _buildPerformanceChart(),
              const SizedBox(height: 32),
              const Text('Recent Assignments', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
              const SizedBox(height: 16),
              _buildAssignmentsList(),
            ],
          ),
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        label: const Text('Create Assignment'),
        icon: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildClassOverview() {
    return Row(
      children: [
        _buildSummaryBox('Class 6A', 'Grade', Colors.blue),
        const SizedBox(width: 12),
        _buildSummaryBox('42', 'Students', Colors.green),
        const SizedBox(width: 12),
        _buildSummaryBox('84%', 'Avg. Mastery', Colors.orange),
      ],
    );
  }

  Widget _buildSummaryBox(String value, String label, Color color) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(color: color.withOpacity(0.12), borderRadius: BorderRadius.circular(16)),
        child: Column(
          children: [
            Text(value, style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold, color: color)),
            Text(label, style: TextStyle(fontSize: 10, color: color.withOpacity(0.8))),
          ],
        ),
      ),
    );
  }

  Widget _buildPerformanceChart() {
    return SizedBox(
      height: 200,
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
      {'title': 'Science: Living Organisms', 'submitted': '38/42'},
      {'title': 'Math: Ratio & Proportion', 'submitted': '25/42'},
    ];
    return Column(
      children: list.map((a) => Card(
        margin: const EdgeInsets.only(bottom: 12),
        child: ListTile(
          title: Text(a['title']!),
          subtitle: Text('Submitted: ${a['submitted']}'),
          trailing: const Icon(Icons.analytics_outlined),
        ),
      )).toList(),
    );
  }
}
