import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../../core/di/injection.dart';
import '../../../curriculum/data/mastery_repository.dart';
import '../../../curriculum/domain/models/mastery.dart';

class ProgressDashboardScreen extends StatefulWidget {
  final String studentId;
  const ProgressDashboardScreen({super.key, required this.studentId});

  @override
  State<ProgressDashboardScreen> createState() => _ProgressDashboardScreenState();
}

class _ProgressDashboardScreenState extends State<ProgressDashboardScreen> {
  late Future<List<Mastery>> _masteryFuture;

  @override
  void initState() {
    super.initState();
    _masteryFuture = sl<MasteryRepository>().getStudentMastery(widget.studentId);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('My Learning Progress')),
      body: FutureBuilder<List<Mastery>>(
        future: _masteryFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final data = snapshot.data ?? [];
          if (data.isEmpty) {
            return const Center(child: Text('No progress data yet. Keep learning!'));
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                _buildOverviewChart(data),
                const SizedBox(height: 30),
                _buildSubjectBreakdown(data),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildOverviewChart(List<Mastery> data) {
    final mastered = data.where((m) => m.status == LearningStatus.mastered).length;
    final inProgress = data.where((m) => m.status == LearningStatus.inProgress).length;
    final needsRevision = data.where((m) => m.status == LearningStatus.needsRevision).length;

    return SizedBox(
      height: 200,
      child: PieChart(
        PieChartData(
          sections: [
            PieChartSectionData(value: mastered.toDouble(), color: Colors.green, title: 'Mastered'),
            PieChartSectionData(value: inProgress.toDouble(), color: Colors.blue, title: 'In Progress'),
            PieChartSectionData(value: needsRevision.toDouble(), color: Colors.orange, title: 'Revision'),
          ],
        ),
      ),
    );
  }

  Widget _buildSubjectBreakdown(List<Mastery> data) {
    // Basic implementation: show list of mastered concepts
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Mastered Concepts', style: Theme.of(context).textTheme.titleLarge),
        const SizedBox(height: 10),
        ...data.where((m) => m.status == LearningStatus.mastered).map((m) => ListTile(
          leading: const Icon(Icons.check_circle, color: Colors.green),
          title: Text('Concept ID: ${m.conceptId}'),
          subtitle: Text('Mastery: ${(m.masteryScore * 100).toStringAsFixed(0)}%'),
        )),
      ],
    );
  }
}
