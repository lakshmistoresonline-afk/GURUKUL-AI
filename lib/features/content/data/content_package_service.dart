import 'dart:io';
import 'package:archive/archive.dart';
import 'package:path_provider/path_provider.dart';

class ContentPackageService {
  Future<void> extractAndLoad(String zipPath) async {
    final bytes = await File(zipPath).readAsBytes();
    final archive = ZipDecoder().decodeBytes(bytes);

    final dir = await getApplicationDocumentsDirectory();
    final outDir = Directory('${dir.path}/extracted_content');

    if (!await outDir.exists()) await outDir.create();

    for (final file in archive) {
      final filename = file.name;
      if (file.isFile) {
        final data = file.content as List<int>;
        File('${outDir.path}/$filename')
          ..createSync(recursive: true)
          ..writeAsBytesSync(data);
      } else {
        Directory('${outDir.path}/$filename').create(recursive: true);
      }
    }
  }
}
