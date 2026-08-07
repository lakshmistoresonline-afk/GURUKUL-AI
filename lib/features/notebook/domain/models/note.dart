class Note {
  final String id;
  final String userId;
  final String? chapterId;
  final String? topicId;
  final String title;
  final String content; // Markdown content
  final DateTime createdAt;
  final DateTime updatedAt;
  final List<String> tags;
  final String? aiSummary;

  Note({
    required this.id,
    required this.userId,
    this.chapterId,
    this.topicId,
    required this.title,
    required this.content,
    required this.createdAt,
    required this.updatedAt,
    this.tags = const [],
    this.aiSummary,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'userId': userId,
      'chapterId': chapterId,
      'topicId': topicId,
      'title': title,
      'content': content,
      'createdAt': createdAt.toIso8601String(),
      'updatedAt': updatedAt.toIso8601String(),
      'tags': tags,
      'aiSummary': aiSummary,
    };
  }
}
