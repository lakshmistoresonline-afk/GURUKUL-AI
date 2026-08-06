import 'package:flutter/material.dart';
import '../../domain/models/assignment.dart';
import '../../domain/models/class_report.dart';

class TeacherDashboardScreen extends StatelessWidget {
  final String teacherName;
  final List<Assignment> assignments;
  final ClassReport? classReport;

  const TeacherDashboardScreen({
    super.key,
    required this.teacherName,
    required this.assignments,
    this.classReport,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Teacher Dashboard'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Welcome, $teacherName', style: Theme.of(context).textTheme.headlineSmall),
            const SizedBox(height: 20),
            _buildSectionHeader(context, 'Active Assignments', () {}),
            if (assignments.isEmpty)
              const Center(child: Padding(padding: EdgeInsets.all(16.0), child: Text('No active assignments'))),
            ...assignments.map((a) => _buildAssignmentCard(context, a)),
            const SizedBox(height: 20),
            _buildSectionHeader(context, 'Class Analytics', () {}),
            if (classReport != null) _buildAnalyticsOverview(context, classReport!)
            else const Center(child: Text('Loading analytics...')),
          ],
        ),
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () {},
        label: const Text('New Assignment'),
        icon: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildSectionHeader(BuildContext context, String title, VoidCallback onSeeAll) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Text(title, style: Theme.of(context).textTheme.titleLarge),
        TextButton(onPressed: onSeeAll, child: const Text('See All')),
      ],
    );
  }

  Widget _buildAssignmentCard(BuildContext context, Assignment assignment) {
    return Card(
      margin: const EdgeInsets.symmetric(vertical: 8),
      child: ListTile(
        title: Text(assignment.title),
        subtitle: Text('Due: ${assignment.dueDate.day}/${assignment.dueDate.month}'),
        trailing: const Icon(Icons.chevron_right),
        onTap: () {},
      ),
    );
  }

  Widget _buildAnalyticsOverview(BuildContext context, ClassReport report) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildAnalyticRow('Total Students', '${report.totalStudents}'),
            _buildAnalyticRow('Class Average Mastery', '${(report.averageMastery * 100).toStringAsFixed(1)}%'),
            const SizedBox(height: 12),
            const Text('AI Classroom Insight:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.blueGrey)),
            Text(report.aiInsight, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 12),
            const Text('Struggling Topics:', style: TextStyle(fontWeight: FontWeight.bold)),
            Wrap(
              spacing: 8,
              children: report.strugglingTopics.map((t) => Chip(label: Text(t, style: const TextStyle(fontSize: 10)))).toList(),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAnalyticRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4.0),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }
}
