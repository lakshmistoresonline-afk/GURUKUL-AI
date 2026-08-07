import 'acquisition_file.dart';
import 'import_status.dart';

class ImportQueueItem {
  final String id;
  final AcquisitionFile file;
  final ImportStatus status;
  final double progress;
  final String? errorMessage;
  final DateTime timestamp;
  final String processingStage;

  ImportQueueItem({
    required this.id,
    required this.file,
    required this.status,
    required this.progress,
    this.errorMessage,
    required this.timestamp,
    required this.processingStage,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'file': file.toJson(),
      'status': status.name,
      'progress': progress,
      'errorMessage': errorMessage,
      'timestamp': timestamp.toIso8601String(),
      'processingStage': processingStage,
    };
  }

  factory ImportQueueItem.fromJson(Map<String, dynamic> json) {
    return ImportQueueItem(
      id: json['id'] as String,
      file: AcquisitionFile.fromJson(json['file'] as Map<String, dynamic>),
      status: ImportStatus.values.byName(json['status'] as String),
      progress: (json['progress'] as num).toDouble(),
      errorMessage: json['errorMessage'] as String?,
      timestamp: DateTime.parse(json['timestamp'] as String),
      processingStage: json['processingStage'] as String,
    );
  }
}
