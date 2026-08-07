import 'dart:convert';
import 'package:logger/logger.dart';
import 'package:uuid/uuid.dart';
import '../storage/local_storage_service.dart';

class TelemetryService {
  final Logger _logger;
  final LocalStorageService _storage;
  final _uuid = const Uuid();
  static const String _telemetryQueueKey = 'telemetry_queue';

  TelemetryService(this._logger, this._storage);

  Future<void> logEvent({
    required String eid,
    required Map<String, dynamic> edata,
    Map<String, dynamic>? context,
    Map<String, dynamic>? actor,
  }) async {
    final event = {
      'eid': eid,
      'ets': DateTime.now().millisecondsSinceEpoch,
      'ver': '3.0',
      'mid': _uuid.v4(),
      'actor': actor ?? {'id': 'anonymous', 'type': 'User'},
      'context': context ?? {'env': 'app', 'pdata': {'id': 'gurukul.ai', 'ver': '1.0'}},
      'edata': edata,
    };

    final eventJson = jsonEncode(event);
    _logger.i('Telemetry Event: $eventJson');

    // Queue for sync
    await _queueEvent(eventJson);
  }

  Future<void> _queueEvent(String eventJson) async {
    List<String> queue = List<String>.from(_storage.get(_telemetryQueueKey) ?? []);
    queue.add(eventJson);
    await _storage.save(_telemetryQueueKey, queue);
  }

  Future<List<String>> getQueuedEvents() async {
    return List<String>.from(_storage.get(_telemetryQueueKey) ?? []);
  }

  Future<void> clearQueue() async {
    await _storage.save(_telemetryQueueKey, []);
  }

  void logImpression({required String pageId, required String type}) {
    logEvent(eid: 'IMPRESSION', edata: {'pageid': pageId, 'type': type});
  }

  void logInteract({required String id, required String type, required String pageId}) {
    logEvent(eid: 'INTERACT', edata: {'id': id, 'type': type, 'pageid': pageId});
  }

  void logStart({required String type, required String id, Map<String, dynamic>? cdata}) {
    logEvent(eid: 'START', edata: {'type': type, 'id': id, 'cdata': cdata});
  }

  void logEnd({required String type, required String id, Map<String, dynamic>? summary}) {
    logEvent(eid: 'END', edata: {'type': type, 'id': id, 'summary': summary});
  }

  void logAssess({
    required String item,
    required String pass,
    required double score,
    required int reslength,
    required List<Map<String, dynamic>> res,
  }) {
    logEvent(eid: 'ASSESS', edata: {
      'item': item,
      'pass': pass,
      'score': score,
      'reslength': reslength,
      'res': res,
    });
  }
}
