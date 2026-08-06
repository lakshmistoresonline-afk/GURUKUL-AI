import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:hive/hive.dart';

class SecureStorageService {
  final FlutterSecureStorage _storage = const FlutterSecureStorage();
  static const String _hiveKey = 'hive_encryption_key';

  Future<List<int>> getOrCreateHiveKey() async {
    final String? key = await _storage.read(key: _hiveKey);
    if (key == null) {
      final List<int> newKey = Hive.generateSecureKey();
      await _storage.write(key: _hiveKey, value: base64UrlEncode(newKey));
      return newKey;
    } else {
      return base64Url.decode(key);
    }
  }
}
