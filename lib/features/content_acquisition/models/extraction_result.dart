class ExtractionResult {
  final String rawText;
  final List<String> headings;
  final List<String> paragraphs;
  final List<List<String>> tables;
  final List<String> images; // paths
  final List<int> chapterBoundaries;

  ExtractionResult({
    required this.rawText,
    required this.headings,
    required this.paragraphs,
    required this.tables,
    required this.images,
    required this.chapterBoundaries,
  });

  Map<String, dynamic> toJson() {
    return {
      'rawText': rawText,
      'headings': headings,
      'paragraphs': paragraphs,
      'tables': tables,
      'images': images,
      'chapterBoundaries': chapterBoundaries,
    };
  }

  factory ExtractionResult.fromJson(Map<String, dynamic> json) {
    return ExtractionResult(
      rawText: json['rawText'] as String,
      headings: List<String>.from(json['headings'] as List),
      paragraphs: List<String>.from(json['paragraphs'] as List),
      tables: (json['tables'] as List)
          .map((table) => List<String>.from(table as List))
          .toList(),
      images: List<String>.from(json['images'] as List),
      chapterBoundaries: List<int>.from(json['chapterBoundaries'] as List),
    );
  }
}
