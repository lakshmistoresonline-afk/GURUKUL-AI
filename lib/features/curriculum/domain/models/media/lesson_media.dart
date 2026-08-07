class LessonMedia {
  final String lessonId;
  final String chapterId;
  final String subject;
  final String title;
  final String? animationAsset;
  final String? videoAsset;
  final String? audioNarration;
  final String? thumbnail;
  final Duration? duration;
  final String? license;
  final String? source;
  final bool offlineAvailable;

  const LessonMedia({
    required this.lessonId,
    required this.chapterId,
    required this.subject,
    required this.title,
    this.animationAsset,
    this.videoAsset,
    this.audioNarration,
    this.thumbnail,
    this.duration,
    this.license,
    this.source,
    this.offlineAvailable = false,
  });

  Map<String, dynamic> toMap() {
    return {
      'lessonId': lessonId,
      'chapterId': chapterId,
      'subject': subject,
      'title': title,
      'animationAsset': animationAsset,
      'videoAsset': videoAsset,
      'audioNarration': audioNarration,
      'thumbnail': thumbnail,
      'duration': duration?.inSeconds,
      'license': license,
      'source': source,
      'offlineAvailable': offlineAvailable,
    };
  }

  factory LessonMedia.fromMap(Map<String, dynamic> map) {
    return LessonMedia(
      lessonId: map['lessonId'] ?? '',
      chapterId: map['chapterId'] ?? '',
      subject: map['subject'] ?? '',
      title: map['title'] ?? '',
      animationAsset: map['animationAsset'],
      videoAsset: map['videoAsset'],
      audioNarration: map['audioNarration'],
      thumbnail: map['thumbnail'],
      duration: map['duration'] != null ? Duration(seconds: map['duration']) : null,
      license: map['license'],
      source: map['source'],
      offlineAvailable: map['offlineAvailable'] ?? false,
    );
  }
}
