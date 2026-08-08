import 'package:hive/hive.dart';
import 'package:uuid/uuid.dart';
import '../models/import_status.dart';
import '../models/import_queue_item.dart';
import '../models/acquisition_file.dart';

class ContentAcquisitionRepository {
  static const String _boxName = 'acquisition_queue';
  final _uuid = const Uuid();

  /// Returns the Hive box for the acquisition queue.
  /// Assumes the box is already opened.
  Box get _box => Hive.box(_boxName);

  /// Adds a new file to the acquisition queue.
  Future<void> addToQueue(AcquisitionFile file) async {
    final item = ImportQueueItem(
      id: _uuid.v4(),
      file: file,
      status: ImportStatus.queued,
      progress: 0.0,
      timestamp: DateTime.now(),
      processingStage: 'Queued',
    );
    await _box.put(item.id, item.toJson());
  }

  /// Updates the status of a specific item in the queue.
  Future<void> updateStatus(String id, ImportStatus status, {String? error}) async {
    final data = _box.get(id);
    if (data != null) {
      final item = ImportQueueItem.fromJson(Map<String, dynamic>.from(data));
      final newItem = ImportQueueItem(
        id: item.id,
        file: item.file,
        status: status,
        progress: item.progress,
        errorMessage: error ?? item.errorMessage,
        timestamp: item.timestamp,
        processingStage: item.processingStage,
      );
      await _box.put(id, newItem.toJson());
    }
  }

  /// Updates the progress and optionally the stage of a specific item.
  Future<void> updateProgress(String id, double progress, {String? stage}) async {
    final data = _box.get(id);
    if (data != null) {
      final item = ImportQueueItem.fromJson(Map<String, dynamic>.from(data));
      final newItem = ImportQueueItem(
        id: item.id,
        file: item.file,
        status: item.status,
        progress: progress,
        errorMessage: item.errorMessage,
        timestamp: item.timestamp,
        processingStage: stage ?? item.processingStage,
      );
      await _box.put(id, newItem.toJson());
    }
  }

  /// Retrieves all items with a [ImportStatus.failed] status.
  List<ImportQueueItem> getErrorItems() {
    return _box.values
        .map((e) => ImportQueueItem.fromJson(Map<String, dynamic>.from(e)))
        .where((item) => item.status == ImportStatus.failed)
        .toList();
  }

  /// Retrieves all items that are currently pending (Queued, Processing, or Retry).
  List<ImportQueueItem> getPendingItems() {
    const pendingStatuses = [
      ImportStatus.queued,
      ImportStatus.processing,
      ImportStatus.retry,
    ];
    return _box.values
        .map((e) => ImportQueueItem.fromJson(Map<String, dynamic>.from(e)))
        .where((item) => pendingStatuses.contains(item.status))
        .toList();
  }

  /// Retrieves all items with a [ImportStatus.completed] status.
  List<ImportQueueItem> getCompletedItems() {
    return _box.values
        .map((e) => ImportQueueItem.fromJson(Map<String, dynamic>.from(e)))
        .where((item) => item.status == ImportStatus.completed)
        .toList();
  }

  /// Clears all items from the acquisition queue.
  Future<void> clearQueue() async {
    await _box.clear();
  }

  /// Returns a stream of the entire queue for real-time updates.
  Stream<List<ImportQueueItem>> watchQueue() {
    return _box.watch().map((_) => getAllItems());
  }

  /// Retrieves all items in the queue, sorted by timestamp (newest first).
  List<ImportQueueItem> getAllItems() {
    return _box.values
        .map((e) => ImportQueueItem.fromJson(Map<String, dynamic>.from(e)))
        .toList()
      ..sort((a, b) => b.timestamp.compareTo(a.timestamp));
  }
}
