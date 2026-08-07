import 'dart:async';
import 'package:flutter/foundation.dart';
import 'package:cloud_firestore/cloud_firestore.dart';
import 'telemetry_service.dart';

class TelemetrySyncWorker {
  final TelemetryService _telemetryService;
  final FirebaseFirestore _firestore;
  Timer? _timer;

  TelemetrySyncWorker(this._telemetryService, this._firestore);

  void start() {
    // Sync every 5 minutes
    _timer = Timer.periodic(const Duration(minutes: 5), (_) => sync());
    debugPrint('Telemetry Sync Worker Started');
  }

  Future<void> sync() async {
    final events = await _telemetryService.getQueuedEvents();
    if (events.isEmpty) return;

    try {
      debugPrint('Syncing ${events.length} telemetry events...');
      final batch = _firestore.batch();
      final collection = _firestore.collection('telemetry');

      for (var eventJson in events) {
        final docRef = collection.doc();
        batch.set(docRef, {'payload': eventJson, 'syncedAt': FieldValue.serverTimestamp()});
      }

      await batch.commit();
      await _telemetryService.clearQueue();
      debugPrint('Telemetry sync successful.');
    } catch (e) {
      debugPrint('Telemetry sync failed: $e');
    }
  }

  void stop() {
    _timer?.cancel();
  }
}
