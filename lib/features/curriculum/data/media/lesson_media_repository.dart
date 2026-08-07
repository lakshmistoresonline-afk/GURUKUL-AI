import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import '../../domain/models/media/lesson_media.dart';
import 'package:path/path.dart' as p;

class LessonMediaRepository {
  final String _root = 'D:/GURUKUL-AI/content_repository';

  Future<LessonMedia?> getMediaForChapter(String chapterId) async {
    // 1. Determine path (similar logic to FrameworkRepository)
    // For simplicity, search in the repository
    final curriculumDir = Directory(p.join(_root, 'curriculum'));
    if (!await curriculumDir.exists()) return null;

    final suffix = chapterId.split('_').last;

    try {
      final allFiles = curriculumDir.listSync(recursive: true);
      for (var entity in allFiles) {
        if (entity is Directory && p.basename(entity.path) == 'chapter_$suffix') {
          final mediaFile = File(p.join(entity.path, 'media.json'));
          if (await mediaFile.exists()) {
            final data = jsonDecode(await mediaFile.readAsString());
            if (data['lessonId'] != null) {
              return LessonMedia(
                lessonId: data['lessonId'],
                chapterId: chapterId,
                subject: data['subject'] ?? '',
                title: data['title'] ?? '',
                animationAsset: data['animationAsset'],
                videoAsset: data['videoAsset'],
                thumbnail: data['thumbnail'],
                audioNarration: data['audioNarration'],
                duration: data['duration'] != null ? Duration(minutes: data['duration']) : const Duration(minutes: 5),
                license: data['license'],
                source: data['source'],
              );
            }
          }
        }
      }
    } catch (e) {
      debugPrint('LessonMediaRepository: Error loading media for $chapterId: $e');
    }

    return null;
  }

  /// Generates a fallback lesson media if specific assets are missing.
  LessonMedia generateFallbackMedia(String chapterId, String subject, String title) {
    return LessonMedia(
      lessonId: '${chapterId}_fallback',
      chapterId: chapterId,
      subject: subject,
      title: title,
    );
  }
}
