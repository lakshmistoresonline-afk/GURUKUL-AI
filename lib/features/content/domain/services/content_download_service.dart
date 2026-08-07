import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import '../../../../core/storage/local_storage_service.dart';

class ContentDownloadService {
  final LocalStorageService _storage;

  ContentDownloadService(this._storage);

  Future<File?> downloadContent(String url, String contentId) async {
    try {
      final response = await http.get(Uri.parse(url));
      final dir = await getApplicationDocumentsDirectory();
      final file = File('${dir.path}/content_$contentId.pdf');

      await file.writeAsBytes(response.bodyBytes);

      // Mark as downloaded
      await _storage.save('downloaded_$contentId', file.path);

      return file;
    } catch (e) {
      debugPrint('Download error: $e');
      return null;
    }
  }

  bool isDownloaded(String contentId) {
    return _storage.get('downloaded_$contentId') != null;
  }

  String? getLocalPath(String contentId) {
    return _storage.get('downloaded_$contentId');
  }
}
