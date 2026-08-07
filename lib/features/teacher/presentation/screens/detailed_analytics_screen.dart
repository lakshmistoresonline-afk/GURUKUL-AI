import 'package:flutter/material.dart';
import 'package:fl_chart/fl_chart.dart';

class DetailedAnalyticsScreen extends StatelessWidget {
  const DetailedAnalyticsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detailed Class Analytics')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _buildParticipationCard(),
            const SizedBox(height: 24),
            const Text('Mastery Distribution', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildMasteryChart(),
            const SizedBox(height: 24),
            const Text('Topic-wise Difficulty Heatmap', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 16),
            _buildDifficultyHeatmap(),
            const SizedBox(height: 24),
            _buildTopLearnersList(),
          ],
        ),
      ),
    );
  }

  Widget _buildParticipationCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(20),
        child: Column(
          children: [
            const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Active Students', style: TextStyle(color: Colors.grey)),
                Text('38 / 42', style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
              ],
            ),
            const SizedBox(height: 12),
            LinearProgressIndicator(value: 38/42, backgroundColor: Colors.grey.shade100, color: Colors.green),
            const SizedBox(height: 20),
            const Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Text('Avg. Time Spent', style: TextStyle(color: Colors.grey)),
                Text('45 mins/day', style: TextStyle(fontWeight: FontWeight.bold)),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildMasteryChart() {
    return SizedBox(
      height: 200,
      child: PieChart(
        PieChartData(
          sections: [
            PieChartSectionData(value: 40, color: Colors.green, title: 'Mastered', radius: 50, titleStyle: const TextStyle(fontSize: 12, color: Colors.white)),
            PieChartSectionData(value: 30, color: Colors.blue, title: 'Learning', radius: 50, titleStyle: const TextStyle(fontSize: 12, color: Colors.white)),
            PieChartSectionData(value: 20, color: Colors.orange, title: 'Struggling', radius: 50, titleStyle: const TextStyle(fontSize: 12, color: Colors.white)),
            PieChartSectionData(value: 10, color: Colors.red, title: 'Not Started', radius: 50, titleStyle: const TextStyle(fontSize: 12, color: Colors.white)),
          ],
        ),
      ),
    );
  }

  Widget _buildDifficultyHeatmap() {
    final topics = ['Fractions', 'Decimals', 'Geometry', 'Algebra', 'Ratio'];
    final performance = [0.8, 0.6, 0.4, 0.5, 0.9]; // 0 to 1

    return Column(
      children: List.generate(topics.length, (index) {
        final score = performance[index];
        final color = score > 0.7 ? Colors.green : (score > 0.4 ? Colors.orange : Colors.red);
        return Padding(
          padding: const EdgeInsets.only(bottom: 8.0),
          child: Row(
            children: [
              SizedBox(width: 80, child: Text(topics[index], style: const TextStyle(fontSize: 12))),
              Expanded(
                child: Container(
                  height: 24,
                  decoration: BoxDecoration(color: color.withValues(alpha: 0.2), borderRadius: BorderRadius.circular(4)),
                  child: FractionallySizedBox(
                    alignment: Alignment.centerLeft,
                    widthFactor: score,
                    child: Container(decoration: BoxDecoration(color: color, borderRadius: BorderRadius.circular(4))),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Text('${(score * 100).toInt()}%'),
            ],
          ),
        );
      }),
    );
  }

  Widget _buildTopLearnersList() {
    final learners = [
      {'name': 'Rahul Sharma', 'xp': '4500', 'rank': '1'},
      {'name': 'Ananya Iyer', 'xp': '4200', 'rank': '2'},
      {'name': 'Siddharth V', 'xp': '3900', 'rank': '3'},
    ];

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Top Performing Students', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        ...learners.map((l) => ListTile(
          leading: CircleAvatar(child: Text(l['rank']!)),
          title: Text(l['name']!),
          trailing: Text('${l['xp']} XP', style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.blue)),
        )),
      ],
    );
  }
}
