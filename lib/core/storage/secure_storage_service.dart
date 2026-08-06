import 'dart:convert';
import 'package:flutter/foundation.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:hive/hive.dart';

class SecureStorageService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  static const String _hiveKey = 'hive_encryption_key';

  Future<List<int>> getOrCreateHiveKey() async {
    try {
      debugPrint('Reading Hive key from secure storage...');
      final String? key = await _storage.read(key: _hiveKey);

      if (key == null) {
        debugPrint('No key found, generating new one...');
        final List<int> newKey = Hive.generateSecureKey();
        await _storage.write(key: _hiveKey, value: base64UrlEncode(newKey));
        return newKey;
      } else {
        debugPrint('Existing key found.');
        return base64Url.decode(key);
      }
    } catch (e) {
      debugPrint('Error accessing secure storage: $e');
      // Fallback for Web/Development if secure storage is unavailable
      if (kDebugMode) {
        debugPrint('Using fallback non-secure key for development.');
        return List<int>.generate(32, (i) => i);
      }
      rethrow;
    }
  }
}
