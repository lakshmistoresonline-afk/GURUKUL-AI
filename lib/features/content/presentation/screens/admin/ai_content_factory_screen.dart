import 'package:flutter/material.dart';
import '../../../../../core/di/injection.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';
import 'package:project_gurukul_ai/features/content/data/ai_batch_factory_service.dart';

class AiContentFactoryScreen extends StatefulWidget {
  const AiContentFactoryScreen({super.key});

  @override
  State<AiContentFactoryScreen> createState() => _AiContentFactoryScreenState();
}

class _AiContentFactoryScreenState extends State<AiContentFactoryScreen> {
  final _service = sl<AiBatchFactoryService>();
  String _selectedScope = 'class_05';
  bool _regenerate = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: const Text('AI Content Factory'),
        elevation: 0,
      ),
      body: StreamBuilder<BatchJobProgress>(
        stream: _service.progressStream,
        initialData: _service.currentJob,
        builder: (context, snapshot) {
          final job = snapshot.data;

          return ListView(
            padding: const EdgeInsets.all(DesignSystem.spacingMd),
            children: [
              if (job != null && job.status != BatchJobStatus.idle)
                _buildProgressCard(job)
              else
                _buildConfigurationCard(),

              const SizedBox(height: DesignSystem.spacingLg),
              _buildPhaseCard(),

              const SizedBox(height: DesignSystem.spacingLg),
              _buildStatusReport(),
            ],
          );
        },
      ),
    );
  }

  Widget _buildConfigurationCard() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(DesignSystem.spacingMd),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Batch Generation Configuration', style: DesignSystem.title),
            const SizedBox(height: DesignSystem.spacingMd),
            DropdownButtonFormField<String>(
              value: _selectedScope,
              decoration: const InputDecoration(labelText: 'Generation Scope', border: OutlineInputBorder()),
              items: const [
                DropdownMenuItem(value: 'class_05', child: Text('Entire Class 5')),
                DropdownMenuItem(value: 'class_06', child: Text('Entire Class 6')),
                DropdownMenuItem(value: 'm5_math', child: Text('Class 5 Mathematics')),
                DropdownMenuItem(value: 's6_science', child: Text('Class 6 Science')),
              ],
              onChanged: (v) => setState(() => _selectedScope = v!),
            ),
            const SizedBox(height: DesignSystem.spacingMd),
            SwitchListTile(
              title: const Text('Regenerate Existing Content'),
              subtitle: const Text('Overwrite chapters that are already AI enriched'),
              value: _regenerate,
              onChanged: (v) => setState(() => _regenerate = v),
            ),
            const SizedBox(height: DesignSystem.spacingLg),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton.icon(
                onPressed: () => _service.startBatchGeneration(scope: _selectedScope, regenerate: _regenerate),
                icon: const Icon(Icons.rocket_launch),
                label: const Text('Start Production Run'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: DesignSystem.primary,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.all(16),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildProgressCard(BatchJobProgress job) {
    return Card(
      color: DesignSystem.primary.withValues(alpha: 0.05),
      child: Padding(
        padding: const EdgeInsets.all(DesignSystem.spacingMd),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.sync, color: DesignSystem.primary),
                const SizedBox(width: 8),
                Expanded(child: Text(job.title, style: DesignSystem.title)),
                _statusChip(job.status),
              ],
            ),
            const SizedBox(height: DesignSystem.spacingMd),
            LinearProgressIndicator(
              value: job.percentage,
              backgroundColor: Colors.grey.shade200,
              minHeight: 10,
              borderRadius: BorderRadius.circular(5),
            ),
            const SizedBox(height: 8),
            Text('${(job.percentage * 100).round()}% Complete (${job.completedChapters}/${job.totalChapters} Chapters)'),
            const SizedBox(height: 16),
            Text('Current: ${job.currentChapter}', style: const TextStyle(fontWeight: FontWeight.bold)),
            const Divider(height: 32),
            const Text('Production Logs', style: TextStyle(fontSize: 12, fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Container(
              height: 150,
              width: double.infinity,
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(color: Colors.black.withValues(alpha: 0.8), borderRadius: BorderRadius.circular(8)),
              child: ListView.builder(
                itemCount: job.logs.length,
                itemBuilder: (context, index) => Text(
                  job.logs[index],
                  style: const TextStyle(color: Colors.greenAccent, fontSize: 10, fontFamily: 'monospace'),
                ),
              ),
            ),
            const SizedBox(height: 16),
            if (job.status == BatchJobStatus.running)
              OutlinedButton.icon(
                onPressed: () => _service.pauseJob(),
                icon: const Icon(Icons.pause),
                label: const Text('Pause Production'),
              )
            else if (job.status == BatchJobStatus.completed)
              ElevatedButton.icon(
                onPressed: () => setState(() => _service.startBatchGeneration(scope: _selectedScope)), // Reset
                icon: const Icon(Icons.check),
                label: const Text('New Production Run'),
              ),
          ],
        ),
      ),
    );
  }

  Widget _buildPhaseCard() {
    return Card(
      child: Column(
        children: [
          ListTile(
            leading: const CircleAvatar(backgroundColor: Colors.blue, child: Text('A', style: TextStyle(color: Colors.white))),
            title: const Text('Phase A: Class 5 Mathematics'),
            subtitle: const Text('14 Chapters • Priority: High'),
            trailing: const Icon(Icons.check_circle, color: Colors.green),
          ),
          const Divider(height: 0),
          ListTile(
            leading: const CircleAvatar(backgroundColor: Colors.grey, child: Text('B', style: TextStyle(color: Colors.white))),
            title: const Text('Phase B: Class 5 EVS'),
            subtitle: const Text('22 Chapters • Waiting'),
            onTap: () => setState(() => _selectedScope = 'class_05_evs'),
          ),
          const Divider(height: 0),
          ListTile(
            leading: const CircleAvatar(backgroundColor: Colors.grey, child: Text('C', style: TextStyle(color: Colors.white))),
            title: const Text('Phase C: Class 5 English'),
            subtitle: const Text('10 Chapters • Waiting'),
          ),
        ],
      ),
    );
  }

  Widget _buildStatusReport() {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Content Readiness Matrix', style: DesignSystem.title),
          const SizedBox(height: 16),
          _readinessRow('Lessons', 141, 25),
          _readinessRow('Quizzes', 141, 25),
          _readinessRow('Flashcards', 141, 25),
          _readinessRow('Animations', 141, 10),
          _readinessRow('Videos', 141, 0),
        ],
      ),
    );
  }

  Widget _readinessRow(String label, int total, int current) {
    final perc = current / total;
    return Padding(
      padding: const EdgeInsets.only(bottom: 12.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(label, style: DesignSystem.bodyMedium),
              Text('$current/$total', style: DesignSystem.bodySmall),
            ],
          ),
          const SizedBox(height: 4),
          LinearProgressIndicator(value: perc, backgroundColor: Colors.grey.shade100, color: perc > 0.8 ? Colors.green : Colors.blue),
        ],
      ),
    );
  }

  Widget _statusChip(BatchJobStatus status) {
    Color color = Colors.grey;
    if (status == BatchJobStatus.running) color = Colors.blue;
    if (status == BatchJobStatus.completed) color = Colors.green;
    if (status == BatchJobStatus.failed) color = Colors.red;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(color: color.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(4), border: Border.all(color: color)),
      child: Text(status.name.toUpperCase(), style: TextStyle(color: color, fontSize: 10, fontWeight: FontWeight.bold)),
    );
  }
}
