import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/theme/design_system.dart';
import '../controllers/acquisition_bloc.dart';
import '../models/import_status.dart';
import '../models/validation_report.dart';

/// A dashboard for managing content acquisition from external repositories.
/// Displays high-level stats, available files, and the current import queue.
class AcquisitionDashboardScreen extends StatelessWidget {
  const AcquisitionDashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<AcquisitionBloc, AcquisitionState>(
      builder: (context, state) {
        return Scaffold(
          backgroundColor: DesignSystem.background,
          appBar: AppBar(
            title: const Text('Acquisition Dashboard', style: DesignSystem.titleLarge),
            backgroundColor: DesignSystem.surface,
            elevation: 0,
            actions: [
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
            child: SingleChildScrollView(
              physics: const AlwaysScrollableScrollPhysics(),
              padding: const EdgeInsets.all(DesignSystem.spacingMd),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  _buildStatsSection(state),
                  if (state.lastValidationReport != null) ...[
                    const SizedBox(height: DesignSystem.spacingLg),
                    _buildValidationSummary(state.lastValidationReport!),
                  ],
                  const SizedBox(height: DesignSystem.spacingLg),
                  _buildSectionHeader('Scanned Files', 'NCERT Source Repository'),
                  const SizedBox(height: DesignSystem.spacingMd),
                  _buildScannedFilesList(context, state),
                  const SizedBox(height: DesignSystem.spacingLg),
                  _buildSectionHeader('Import Queue', 'Real-time Processing Status'),
                  const SizedBox(height: DesignSystem.spacingMd),
                  _buildQueueList(state),
                  // Bottom padding for FAB
                  const SizedBox(height: 80),
                ],
              ),
            ),
          ),
          floatingActionButton: FloatingActionButton.extended(
            onPressed: state.isProcessing || state.queue.every((i) => i.status == ImportStatus.completed)
                ? null
                : () => context.read<AcquisitionBloc>().add(ProcessQueue()),
            backgroundColor: state.isProcessing ? DesignSystem.textTertiary : DesignSystem.primary,
            icon: state.isProcessing
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(color: Colors.white, strokeWidth: 2),
                  )
                : const Icon(Icons.play_circle_filled, color: Colors.white),
            label: Text(
              state.isProcessing ? 'Processing Queue...' : 'Start Processing',
              style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
            ),
          ),
        );
      },
    );
  }

  Widget _buildSectionHeader(String title, String subtitle) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(title, style: DesignSystem.headlineMedium),
        Text(subtitle, style: DesignSystem.bodySmall),
      ],
    );
  }

  Widget _buildStatsSection(AcquisitionState state) {
    final total = state.queue.length;
    final pending = state.queue.where((i) => i.status == ImportStatus.queued).length;
    final processed = state.queue.where((i) => i.status == ImportStatus.completed).length;
    final failed = state.queue.where((i) => i.status == ImportStatus.failed).length;

    return Row(
      children: [
        Expanded(child: _buildStatCard('Total', total.toString(), DesignSystem.primary)),
        const SizedBox(width: DesignSystem.spacingSm),
        Expanded(child: _buildStatCard('Pending', pending.toString(), DesignSystem.orange)),
        const SizedBox(width: DesignSystem.spacingSm),
        Expanded(child: _buildStatCard('Done', processed.toString(), DesignSystem.accent)),
        const SizedBox(width: DesignSystem.spacingSm),
        Expanded(child: _buildStatCard('Failed', failed.toString(), DesignSystem.pink)),
      ],
    );
  }

  Widget _buildStatCard(String label, String value, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(vertical: DesignSystem.spacingMd),
      decoration: DesignSystem.cardDecoration,
      child: Column(
        children: [
          Text(value, style: DesignSystem.headlineLarge.copyWith(color: color, fontSize: 24)),
          Text(label, style: DesignSystem.labelSmall),
        ],
      ),
    );
  }

  Widget _buildValidationSummary(ValidationReport report) {
    return Container(
      padding: const EdgeInsets.all(DesignSystem.spacingMd),
      decoration: BoxDecoration(
        color: report.statistics['errors']! > 0 ? DesignSystem.pink.withValues(alpha: 0.1) : DesignSystem.accent.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(DesignSystem.radiusMd),
        border: Border.all(color: report.statistics['errors']! > 0 ? DesignSystem.pink.withValues(alpha: 0.3) : DesignSystem.accent.withValues(alpha: 0.3)),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(
                report.statistics['errors']! > 0 ? Icons.error_outline : Icons.check_circle_outline,
                color: report.statistics['errors']! > 0 ? DesignSystem.pink : DesignSystem.accent,
              ),
              const SizedBox(width: 8),
              Text(
                'Validation Report',
                style: DesignSystem.titleMedium.copyWith(color: report.statistics['errors']! > 0 ? DesignSystem.pink : DesignSystem.accent),
              ),
            ],
          ),
          const SizedBox(height: 8),
          Text(
            '${report.statistics['errors']} Errors • ${report.statistics['warnings']} Warnings detected.',
            style: DesignSystem.bodySmall,
          ),
          if (report.issues.isNotEmpty) ...[
            const SizedBox(height: 12),
            ...report.issues.take(3).map((i) => Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text('• ${i.message}', style: const TextStyle(fontSize: 11, color: DesignSystem.textSecondary), maxLines: 1, overflow: TextOverflow.ellipsis),
            )),
          ],
        ],
      ),
    );
  }

  Widget _buildScannedFilesList(BuildContext context, AcquisitionState state) {
    if (state.isScanning) {
      return const Center(
        child: Padding(
          padding: EdgeInsets.all(DesignSystem.spacingLg),
          child: CircularProgressIndicator(color: DesignSystem.primary),
        ),
      );
    }

    if (state.scannedFiles.isEmpty) {
      return _buildEmptyState('No files found. Tap refresh to scan NCERT repository.');
    }

    return ListView.separated(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: state.scannedFiles.length,
      separatorBuilder: (_, __) => const SizedBox(height: DesignSystem.spacingSm),
      itemBuilder: (context, index) {
        final file = state.scannedFiles[index];
        final isQueued = state.queue.any((item) => item.file.path == file.path);

        return Container(
          decoration: DesignSystem.cardDecoration,
          child: ListTile(
            leading: Container(
              padding: const EdgeInsets.all(DesignSystem.spacingSm),
              decoration: BoxDecoration(
                color: DesignSystem.primaryLight,
                borderRadius: BorderRadius.circular(DesignSystem.radiusSm),
              ),
              child: const Icon(Icons.picture_as_pdf, color: DesignSystem.primary),
            ),
            title: Text(file.name, style: DesignSystem.titleLarge.copyWith(fontSize: 16)),
            subtitle: Text(
              'Class ${file.classLevel} • ${file.subject} • Chapter ${file.chapterIndex}',
              style: DesignSystem.bodySmall,
            ),
            trailing: isQueued
                ? const Icon(Icons.check_circle, color: DesignSystem.accent)
                : TextButton(
                    onPressed: () => context.read<AcquisitionBloc>().add(AddToQueue(file)),
                    style: TextButton.styleFrom(
                      foregroundColor: DesignSystem.primary,
                      textStyle: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    child: const Text('Add to Queue'),
                  ),
          ),
        );
      },
    );
  }

  Widget _buildQueueList(AcquisitionState state) {
    if (state.queue.isEmpty) {
      return _buildEmptyState('Import queue is currently empty.');
    }

    return ListView.separated(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: state.queue.length,
      separatorBuilder: (_, __) => const SizedBox(height: DesignSystem.spacingSm),
      itemBuilder: (context, index) {
        final item = state.queue[index];
        final color = _getStatusColor(item.status);

        return Container(
          decoration: DesignSystem.cardDecoration,
          padding: const EdgeInsets.all(DesignSystem.spacingMd),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(item.file.name, style: DesignSystem.titleLarge.copyWith(fontSize: 16)),
                        Text(
                          item.processingStage.isEmpty ? 'Waiting...' : item.processingStage,
                          style: DesignSystem.bodySmall.copyWith(color: DesignSystem.textSecondary),
                        ),
                      ],
                    ),
                  ),
                  _buildStatusChip(item.status),
                ],
              ),
              const SizedBox(height: DesignSystem.spacingMd),
              Stack(
                children: [
                  Container(
                    height: 8,
                    width: double.infinity,
                    decoration: BoxDecoration(
                      color: DesignSystem.border,
                      borderRadius: BorderRadius.circular(DesignSystem.radiusSm),
                    ),
                  ),
                  AnimatedContainer(
                    duration: const Duration(milliseconds: 300),
                    height: 8,
                    width: (MediaQuery.of(context).size.width - (DesignSystem.spacingMd * 4)) * item.progress,
                    decoration: BoxDecoration(
                      color: color,
                      borderRadius: BorderRadius.circular(DesignSystem.radiusSm),
                    ),
                  ),
                ],
              ),
              if (item.errorMessage != null && item.errorMessage!.isNotEmpty) ...[
                const SizedBox(height: DesignSystem.spacingSm),
                Text(
                  'Error: ${item.errorMessage}',
                  style: DesignSystem.bodySmall.copyWith(color: DesignSystem.pink, fontWeight: FontWeight.bold),
                ),
              ],
            ],
          ),
        );
      },
    );
  }

  Widget _buildStatusChip(ImportStatus status) {
    final color = _getStatusColor(status);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.1),
        borderRadius: BorderRadius.circular(DesignSystem.radiusSm),
        border: Border.all(color: color.withValues(alpha: 0.5)),
      ),
      child: Text(
        status.name.toUpperCase(),
        style: DesignSystem.labelSmall.copyWith(color: color, fontSize: 10),
      ),
    );
  }

  Color _getStatusColor(ImportStatus status) {
    switch (status) {
      case ImportStatus.queued: return DesignSystem.orange;
      case ImportStatus.processing: return DesignSystem.primary;
      case ImportStatus.completed: return DesignSystem.accent;
      case ImportStatus.failed: return DesignSystem.pink;
      case ImportStatus.retry: return DesignSystem.secondary;
      case ImportStatus.cancelled: return DesignSystem.textTertiary;
    }
  }

  Widget _buildEmptyState(String message) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: DesignSystem.spacingLg),
        child: Column(
          children: [
            Icon(Icons.cloud_download_outlined, size: 48, color: DesignSystem.textTertiary.withValues(alpha: 0.3)),
            const SizedBox(height: DesignSystem.spacingSm),
            Text(
              message,
              style: DesignSystem.bodyMedium.copyWith(color: DesignSystem.textTertiary),
              textAlign: TextAlign.center,
            ),
          ],
        ),
      ),
    );
  }
}
