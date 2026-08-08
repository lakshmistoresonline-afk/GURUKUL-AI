import 'package:hive_flutter/hive_flutter.dart';

class LocalStorageService {
  static const String _metadataBox = 'metadata';
  static const String _contentBox = 'content_cache';

  Future<void> init(List<int> encryptionKey) async {
    final cipher = HiveAesCipher(encryptionKey);
    await Hive.openBox(_metadataBox, encryptionCipher: cipher);
    await Hive.openBox(_contentBox, encryptionCipher: cipher);
  }

  // Generic Save/Get with TTL support
  Future<void> save(String key, dynamic value, {Duration? ttl}) async {
    final box = Hive.box(_metadataBox);
    final data = {
      'value': value,
      'expiry': ttl != null ? DateTime.now().add(ttl).millisecondsSinceEpoch : null,
    };
    await box.put(key, data);
  }

  dynamic get(String key) {
    final box = Hive.box(_metadataBox);
    final data = box.get(key);
    if (data == null) return null;

    if (data is Map && data.containsKey('value') && data.containsKey('expiry')) {
      if (data['expiry'] != null) {
        final expiry = DateTime.fromMillisecondsSinceEpoch(data['expiry'] as int);
        if (DateTime.now().isAfter(expiry)) {
          box.delete(key);
          return null;
        }
      }
      return data['value'];
    }
    return data;
  }

  // Content Caching
  Future<void> cacheContent(String id, Map<String, dynamic> data) async {
    final box = Hive.box(_contentBox);
    await box.put(id, data);
  }

  Map<String, dynamic>? getCachedContent(String id) {
    final box = Hive.box(_contentBox);
    final data = box.get(id);
    return data != null ? Map<String, dynamic>.from(data) : null;
  }

  Future<void> clearAll() async {
    await Hive.box(_metadataBox).clear();
    await Hive.box(_contentBox).clear();
  }
}
