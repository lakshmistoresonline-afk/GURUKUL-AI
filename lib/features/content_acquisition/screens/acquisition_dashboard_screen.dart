import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/theme/design_system.dart';
import '../../../core/config/app_config.dart';
import '../controllers/acquisition_bloc.dart';
import '../models/import_status.dart';
import '../models/validation_report.dart';
import 'package:file_picker/file_picker.dart';
import 'dart:io';
import 'package:path/path.dart' as p;

/// A production-grade dashboard for managing content acquisition and AI enrichment.
class AcquisitionDashboardScreen extends StatelessWidget {
  const AcquisitionDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AcquisitionBloc, AcquisitionState>(
      builder: (context, state) {
        return Scaffold(
          backgroundColor: DesignSystem.background,
          appBar: AppBar(
            title: const Text('Acquisition Dash', style: DesignSystem.titleLarge),
            backgroundColor: DesignSystem.surface,
            elevation: 0,
            actions: [
               IconButton(
                icon: const Icon(Icons.upload_file, color: DesignSystem.primary),
                tooltip: 'Upload Manual PDF',
                onPressed: () => _showUploadDialog(context),
              ),
              IconButton(
                icon: const Icon(Icons.bug_report_outlined, color: DesignSystem.pink),
                tooltip: 'Run Validation',
                onPressed: () => context.read<AcquisitionBloc>().add(RunValidation()),
              ),
              IconButton(
                icon: const Icon(Icons.refresh, color: DesignSystem.primary),
                tooltip: 'Scan Repository',
                onPressed: () => context.read<AcquisitionBloc>().add(StartScan()),
              ),
            ],
          ),
          body: RefreshIndicator(
            onRefresh: () async {
              context.read<AcquisitionBloc>().add(StartScan());
              context.read<AcquisitionBloc>().add(LoadQueue());
            },
            child: CustomScrollView(
              slivers: [
                SliverPadding(
                  padding: const EdgeInsets.all(DesignSystem.spacingMd),
                  sliver: SliverToBoxAdapter(child: _buildStatsSection(state)),
                ),
                if (state.lastValidationReport != null)
                  SliverPadding(
                    padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingMd),
                    sliver: SliverToBoxAdapter(child: _buildValidationSummary(state.lastValidationReport!)),
                  ),
                SliverPadding(
                  padding: const EdgeInsets.all(DesignSystem.spacingMd),
                  sliver: SliverToBoxAdapter(child: _buildSectionHeader('Import Queue', 'Real-time Processing Status')),
                ),
                _buildQueueSliver(state),
                SliverPadding(
                  padding: const EdgeInsets.all(DesignSystem.spacingMd),
                  sliver: SliverToBoxAdapter(child: _buildSectionHeader('Source Files', 'Available NCERT Material')),
                ),
                _buildScannedFilesSliver(context, state),
                const SliverToBoxAdapter(child: SizedBox(height: 100)),
              ],
            ),
          ),
          floatingActionButton: FloatingActionButton.extended(
            onPressed: state.isProcessing || state.queue.every((i) => i.status == ImportStatus.completed)
                ? null
                : () => context.read<AcquisitionBloc>().add(ProcessQueue()),
            backgroundColor: state.isProcessing ? DesignSystem.textTertiary : DesignSystem.primary,
            icon: state.isProcessing
                ? const SizedBox(width: 20, height: 20, child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2))
                : const Icon(Icons.play_circle_filled, color: Colors.white),
            label: Text(state.isProcessing ? 'Enriching...' : 'Start Batch Enrichment', style: const TextStyle(color: Colors.white)),
          ),
        );
      },
    );
  }

  Widget _buildSectionHeader(String title, String subtitle) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: DesignSystem.headlineMedium.copyWith(fontSize: 20)),
        Text(subtitle, style: DesignSystem.bodySmall),
      ],
    );
  }

  Widget _buildStatsSection(AcquisitionState state) {
    final total = state.queue.length;
    final processed = state.queue.where((i) => i.status == ImportStatus.completed).length;
    final failed = state.queue.where((i) => i.status == ImportStatus.failed).length;

    String speedText = '0/m';
    if (state.isProcessing && state.processingStartTime != null) {
      final diff = DateTime.now().difference(state.processingStartTime!).inMinutes;
      if (diff > 0) {
        speedText = '${(processed / diff).toStringAsFixed(1)}/m';
      }
    }

    return Column(
      children: [
        _buildSystemHealthCard(speedText),
        const SizedBox(height: DesignSystem.spacingMd),
        Row(
          children: [
            Expanded(child: _buildStatCard('TOTAL', total.toString(), DesignSystem.primary)),
            const SizedBox(width: DesignSystem.spacingSm),
            Expanded(child: _buildStatCard('ENRICHED', processed.toString(), DesignSystem.accent)),
            const SizedBox(width: DesignSystem.spacingSm),
            Expanded(child: _buildStatCard('FAILED', failed.toString(), DesignSystem.pink)),
          ],
        ),
      ],
    );
  }

  Widget _buildSystemHealthCard(String speed) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: DesignSystem.border),
      ),
      child: Row(
        children: [
          const Icon(Icons.hub_outlined, color: DesignSystem.primary),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const Text('AI ENGINE STATUS', style: TextStyle(fontSize: 10, fontWeight: FontWeight.bold, color: DesignSystem.textSecondary)),
                Text(
                  AppConfig.useLocalAi ? 'Local (Ollama @ 11434)' : 'Cloud (Gemini API)',
                  style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                ),
                if (speed != '0/m')
                   Text('Processing Speed: $speed', style: const TextStyle(fontSize: 10, color: Colors.blue)),
              ],
            ),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(4)),
            child: const Text('ONLINE', style: TextStyle(color: Colors.green, fontSize: 10, fontWeight: FontWeight.bold)),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 16),
      decoration: DesignSystem.cardDecoration,
      child: Column(
        children: [
          Text(value, style: DesignSystem.headlineLarge.copyWith(color: color, fontSize: 22)),
          Text(label, style: DesignSystem.labelSmall.copyWith(fontSize: 9)),
        ],
      ),
    );
  }

  Widget _buildValidationSummary(ValidationReport report) {
    final hasErrors = report.statistics['errors']! > 0;
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: BoxDecoration(
        color: hasErrors ? DesignSystem.pink.withValues(alpha: 0.05) : DesignSystem.accent.withValues(alpha: 0.05),
        borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
        border: Border.all(color: hasErrors ? DesignSystem.pink.withValues(alpha: 0.2) : DesignSystem.accent.withValues(alpha: 0.2)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(hasErrors ? Icons.warning_amber : Icons.check_circle, color: hasErrors ? DesignSystem.pink : DesignSystem.accent, size: 20),
              const SizedBox(width: 8),
              Text('Integrity Report', style: DesignSystem.titleMedium.copyWith(color: hasErrors ? DesignSystem.pink : DesignSystem.accent)),
            ],
          ),
          const SizedBox(height: 4),
          Text('${report.statistics['errors']} Errors • ${report.statistics['warnings']} Warnings detected in dataset.', style: DesignSystem.bodySmall),
        ],
      ),
    );
  }

  Widget _buildQueueSliver(AcquisitionState state) {
    if (state.queue.isEmpty) {
       return const SliverToBoxAdapter(child: Center(child: Padding(
         padding: EdgeInsets.all(32.0),
         child: Text('Queue is empty'),
       )));
    }
    return SliverPadding(
      padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingMd),
      sliver: SliverList(
        delegate: SliverChildBuilderDelegate(
          (context, index) {
            final item = state.queue[index];
            final color = _getStatusColor(item.status);
            return Card(
              margin: const EdgeInsets.only(bottom: 8),
              child: ListTile(
                title: Text(item.file.name, style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold)),
                subtitle: LinearProgressIndicator(value: item.progress, color: color, backgroundColor: color.withValues(alpha: 0.1)),
                trailing: _buildStatusChip(item.status),
              ),
            );
          },
          childCount: state.queue.length,
        ),
      ),
    );
  }

  Widget _buildScannedFilesSliver(BuildContext context, AcquisitionState state) {
    return SliverPadding(
      padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingMd),
      sliver: SliverList(
        delegate: SliverChildBuilderDelegate(
          (context, index) {
            final file = state.scannedFiles[index];
            final isQueued = state.queue.any((item) => item.file.path == file.path);
            return Container(
              margin: const EdgeInsets.only(bottom: 8),
              decoration: DesignSystem.cardDecoration,
              child: ListTile(
                dense: true,
                title: Text(file.name, style: const TextStyle(fontWeight: FontWeight.bold)),
                subtitle: Text('Class ${file.classLevel} • ${file.subject}'),
                trailing: isQueued
                  ? const Icon(Icons.check_circle, color: DesignSystem.accent, size: 20)
                  : IconButton(
                      icon: const Icon(Icons.add_circle_outline, color: DesignSystem.primary),
                      onPressed: () => context.read<AcquisitionBloc>().add(AddToQueue(file)),
                    ),
              ),
            );
          },
          childCount: state.scannedFiles.length,
        ),
      ),
    );
  }

  Widget _buildStatusChip(ImportStatus status) {
    final color = _getStatusColor(status);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 2),
      decoration: BoxDecoration(color: color.withValues(alpha: 0.1), borderRadius: BorderRadius.circular(4)),
      child: Text(status.name.toUpperCase(), style: TextStyle(color: color, fontSize: 9, fontWeight: FontWeight.bold)),
    );
  }

  Color _getStatusColor(ImportStatus status) {
    switch (status) {
      case ImportStatus.queued: return DesignSystem.orange;
      case ImportStatus.processing: return DesignSystem.primary;
      case ImportStatus.completed: return DesignSystem.accent;
      case ImportStatus.failed: return DesignSystem.pink;
      default: return DesignSystem.textTertiary;
    }
  }

  void _showUploadDialog(BuildContext context) {
    int selectedClass = 5;
    String selectedSubject = 'Mathematics';

    showDialog(
      context: context,
      builder: (dialogContext) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('Upload PDF'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              DropdownButtonFormField<int>(
                value: selectedClass,
                decoration: const InputDecoration(labelText: 'Class'),
                items: [5, 6].map((l) => DropdownMenuItem(value: l, child: Text('Class $l'))).toList(),
                onChanged: (v) => setDialogState(() => selectedClass = v!),
              ),
              const SizedBox(height: 12),
              DropdownButtonFormField<String>(
                value: selectedSubject,
                decoration: const InputDecoration(labelText: 'Subject'),
                items: ['Mathematics', 'Science', 'EVS', 'English', 'Hindi'].map((s) => DropdownMenuItem(value: s, child: Text(s))).toList(),
                onChanged: (v) => setDialogState(() => selectedSubject = v!),
              ),
            ],
          ),
          actions: [
            TextButton(onPressed: () => Navigator.pop(dialogContext), child: const Text('Cancel')),
            ElevatedButton(
              onPressed: () async {
                final result = await FilePicker.platform.pickFiles(type: FileType.custom, allowedExtensions: ['pdf']);
                if (result != null && result.files.single.path != null) {
                  final path = result.files.single.path!;
                  final name = result.files.single.name;
                  final classDir = 'class_${selectedClass.toString().padLeft(2, '0')}';
                  final destDir = Directory('D:/GURUKUL-AI/datasets/ncert_source/$classDir/${selectedSubject.toLowerCase()}');
                  if (!await destDir.exists()) await destDir.create(recursive: true);
                  await File(path).copy(p.join(destDir.path, name));
                  if (context.mounted) {
                    context.read<AcquisitionBloc>().add(StartScan());
                    Navigator.pop(dialogContext);
                  }
                }
              },
              child: const Text('Select & Upload'),
            ),
          ],
        ),
      ),
    );
  }
}
