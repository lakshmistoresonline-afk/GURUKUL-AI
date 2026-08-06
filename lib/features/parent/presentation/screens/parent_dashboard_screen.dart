import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../domain/models/student_report.dart';
import '../../domain/services/report_service.dart';
import '../../../curriculum/data/mastery_repository.dart';
import '../../../ai/data/ai_insight_service.dart';

class ParentDashboardScreen extends StatefulWidget {
  final List<String> childrenIds;

  const ParentDashboardScreen({super.key, required this.childrenIds});

  @override
  State<ParentDashboardScreen> createState() => _ParentDashboardScreenState();
}

class _ParentDashboardScreenState extends State<ParentDashboardScreen> {
  late Future<List<StudentReport>> _reportsFuture;

  @override
  void initState() {
    super.initState();
    _reportsFuture = _loadReports();
  }

  Future<List<StudentReport>> _loadReports() async {
    final reportService = sl<ReportService>();
    final masteryRepo = sl<MasteryRepository>();
    final insightService = sl<AiInsightService>();

    List<StudentReport> reports = [];
    for (var id in widget.childrenIds) {
      final masteryData = await masteryRepo.getStudentMastery(id);

      // We generate a temp report to get stats, then get AI summary
      final baseReport = await reportService.generateStudentReport(
        studentId: id,
        studentName: "Student $id", // In real app, fetch from UserProfile
        masteryData: masteryData,
        aiSummary: "Generating summary...",
      );

      final aiSummary = await insightService.generateParentSummary(baseReport);

      reports.add(await reportService.generateStudentReport(
        studentId: id,
        studentName: "Student $id",
        masteryData: masteryData,
        aiSummary: aiSummary,
      ));
    }
    return reports;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Parent Dashboard'),
        actions: [
          IconButton(
            onPressed: () => setState(() { _reportsFuture = _loadReports(); }),
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: FutureBuilder<List<StudentReport>>(
        future: _reportsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          final reports = snapshot.data ?? [];
          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: reports.length,
            itemBuilder: (context, index) {
              final report = reports[index];
              return _ReportCard(report: report);
            },
          );
        },
      ),
    );
  }
}

class _ReportCard extends StatelessWidget {
  final StudentReport report;
  const _ReportCard({required this.report});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 16),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              report.studentName,
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const Divider(),
            _buildStatRow(context, 'Average Mastery', '${(report.averageMastery * 100).toStringAsFixed(0)}%'),
            _buildStatRow(context, 'Study Time', '${report.totalStudyTimeMinutes} mins'),
            const SizedBox(height: 12),
            Text('Gurukul AI Insight:', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.deepPurple)),
            Text(report.aiSummary, style: Theme.of(context).textTheme.bodyMedium),
            const SizedBox(height: 16),
            _buildAreaTags(context, 'Strong Areas', report.strongAreas, Colors.green[100]!),
            _buildAreaTags(context, 'Areas to Improve', report.weakAreas, Colors.orange[100]!),
          ],
        ),
      ),
    );
  }

  Widget _buildStatRow(BuildContext context, String label, String value) {
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

  Widget _buildAreaTags(BuildContext context, String label, List<String> areas, Color color) {
    if (areas.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(label, style: Theme.of(context).textTheme.titleSmall),
        const SizedBox(height: 4),
        Wrap(
          spacing: 8,
          children: areas.map((area) => Chip(
            label: Text(area, style: const TextStyle(fontSize: 12)),
            backgroundColor: color,
          )).toList(),
        ),
        const SizedBox(height: 12),
      ],
    );
  }
}
