import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';
import '../../../../core/di/injection.dart';
import '../../../curriculum/data/mastery_repository.dart';
import '../../../curriculum/domain/models/mastery.dart';
import '../../../curriculum/domain/models/concept_node.dart';

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
    final colorScheme = Theme.of(context).colorScheme;

    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      appBar: AppBar(
        title: const Text('Learning Insights'),
        backgroundColor: Colors.transparent,
      ),
      body: FutureBuilder<List<Mastery>>(
        future: _masteryFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          final data = snapshot.data ?? [];

          return SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                _buildSummaryCards(),
                const SizedBox(height: 24),
                const Text('Learning Curve', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                _buildLearningCurveChart(),
                const SizedBox(height: 24),
                const Text('Mastery by Status', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                const SizedBox(height: 16),
                _buildOverviewChart(data),
                const SizedBox(height: 24),
                _buildTopicAnalysis(data),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildSummaryCards() {
    return Row(
      children: [
        _buildSmallStatCard('Study Time', '2.5 hrs', Icons.timer, Colors.blue),
        const SizedBox(width: 12),
        _buildSmallStatCard('Avg Accuracy', '84%', Icons.gps_fixed, Colors.green),
      ],
    );
  }

  Widget _buildSmallStatCard(String label, String value, IconData icon, Color color) {
    return Expanded(
      child: Card(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Icon(icon, color: color, size: 20),
              const SizedBox(height: 12),
              Text(value, style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
              Text(label, style: const TextStyle(fontSize: 12, color: Colors.grey)),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLearningCurveChart() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: SizedBox(
          height: 180,
          child: LineChart(
            LineChartData(
              gridData: const FlGridData(show: false),
              titlesData: const FlTitlesData(show: false),
              borderData: FlBorderData(show: false),
              lineBarsData: [
                LineChartBarData(
                  spots: const [
                    FlSpot(0, 30),
                    FlSpot(1, 45),
                    FlSpot(2, 40),
                    FlSpot(3, 65),
                    FlSpot(4, 72),
                    FlSpot(5, 84),
                  ],
                  isCurved: true,
                  color: Colors.blue,
                  barWidth: 4,
                  belowBarData: BarAreaData(
                    show: true,
                    color: Colors.blue.withOpacity(0.1),
                  ),
                  dotData: const FlDotData(show: false),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildOverviewChart(List<Mastery> data) {
    if (data.isEmpty) {
      return const Card(
        child: Padding(
          padding: EdgeInsets.all(20),
          child: Center(child: Text('No data yet')),
        ),
      );
    }

    final mastered = data.where((m) => m.status == LearningStatus.mastered).length;
    final inProgress = data.where((m) => m.status == LearningStatus.inProgress).length;
    final needsRevision = data.where((m) => m.status == LearningStatus.needsRevision).length;

    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Row(
          children: [
            SizedBox(
              height: 120,
              width: 120,
              child: PieChart(
                PieChartData(
                  sections: [
                    PieChartSectionData(value: mastered.toDouble(), color: Colors.green, radius: 15, showTitle: false),
                    PieChartSectionData(value: inProgress.toDouble(), color: Colors.blue, radius: 15, showTitle: false),
                    PieChartSectionData(value: needsRevision.toDouble(), color: Colors.orange, radius: 15, showTitle: false),
                  ],
                ),
              ),
            ),
            const SizedBox(width: 24),
            Expanded(
              child: Column(
                children: [
                  _buildLegendItem('Mastered', Colors.green),
                  _buildLegendItem('In Progress', Colors.blue),
                  _buildLegendItem('Revision', Colors.orange),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLegendItem(String label, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Container(width: 12, height: 12, decoration: BoxDecoration(color: color, shape: BoxShape.circle)),
          const SizedBox(width: 8),
          Text(label, style: const TextStyle(fontSize: 12)),
        ],
      ),
    );
  }

  Widget _buildTopicAnalysis(List<Mastery> data) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Strong Areas', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...data.take(2).map((m) => _buildTopicTile(m, true)),
        const SizedBox(height: 20),
        const Text('Needs Focus', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 12),
        ...data.skip(2).take(2).map((m) => _buildTopicTile(m, false)),
      ],
    );
  }

  Widget _buildTopicTile(Mastery m, bool isStrong) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: ListTile(
        leading: CircleAvatar(
          backgroundColor: (isStrong ? Colors.green : Colors.orange).withOpacity(0.1),
          child: Icon(isStrong ? Icons.trending_up : Icons.trending_down, color: isStrong ? Colors.green : Colors.orange),
        ),
        title: Text('Concept: ${m.conceptId}'),
        subtitle: Text('Mastery: ${(m.masteryScore * 100).toStringAsFixed(0)}%'),
        trailing: const Icon(Icons.chevron_right),
      ),
    );
  }
}
