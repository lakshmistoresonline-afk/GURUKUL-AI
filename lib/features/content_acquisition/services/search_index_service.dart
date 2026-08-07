import 'dart:convert';
import 'dart:io';
import '../../curriculum/domain/models/concept_node.dart';

/// Service responsible for generating and maintaining the search index.
class SearchIndexService {
  final String indexPath;

  SearchIndexService({
    this.indexPath = 'D:/GURUKUL-AI/datasets/processed/search_index/search_index.json',
  });

  /// Generates the search index from a list of enriched [ConceptNode].
  Future<void> buildIndex(List<ConceptNode> nodes) async {
    final List<Map<String, dynamic>> indexEntries = [];

    for (final node in nodes) {
      indexEntries.add({
        'id': node.id,
        'class': node.classLevel,
        'subject': node.subject,
        'chapter': node.chapter,
        'topic': node.topic,
        'keywords': node.keyTakeaways,
        'content_preview': _generatePreview(node),
        'status': node.status,
      });
    }

    final indexFile = File(indexPath);
    await indexFile.create(recursive: true);
    await indexFile.writeAsString(const JsonEncoder.withIndent('  ').convert({
      'updated_at': DateTime.now().toIso8601String(),
      'total_indexed': indexEntries.length,
      'entries': indexEntries,
    }));
  }

  String _generatePreview(ConceptNode node) {
    final text = '${node.introduction} ${node.teacherExplanation}';
    return text.length > 500 ? text.substring(0, 500) : text;
  }
}
