import 'dart:convert';
import 'dart:math';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';
import 'package:sqflite/sqflite.dart';
import '../../../core/database/sqlite_service.dart';
import '../../../core/ai/ai_provider.dart';
import '../../curriculum/domain/models/concept_node.dart';

/// Service responsible for managing the hybrid search index (FTS5 + Semantic).
class SearchEngineService {
  final SqliteService _db;
  final AIProvider _ai;

  SearchEngineService(this._db, this._ai);

  /// Builds or updates the search index for a list of [ConceptNode].
  /// Generates both FTS5 keyword index and semantic embeddings.
  Future<void> buildIndex(List<ConceptNode> nodes) async {
    final db = await _db.database;
    final batch = db.batch();

    for (final node in nodes) {
      // 1. Keyword Index (FTS5)
      batch.insert(
        'search_index',
        {
          'node_id': node.id,
          'title': node.chapter,
          'subject': node.subject,
          'class_level': node.classLevel.toString(),
          'content': '${node.topic} ${node.introduction} ${node.teacherExplanation}',
          'keywords': node.keyTakeaways.join(', '),
        },
        conflictAlgorithm: ConflictAlgorithm.replace,
      );

      // 2. Semantic Index (Embeddings)
      final textToEmbed = '${node.chapter} ${node.topic} ${node.introduction}';
      final vector = await _ai.generateEmbeddings(textToEmbed);

      if (vector.isNotEmpty) {
        final float32List = Float32List.fromList(vector);
        batch.insert(
          'embeddings',
          {
            'node_id': node.id,
            'vector': float32List.buffer.asUint8List(),
            'metadata': jsonEncode({
              'title': node.chapter,
              'subject': node.subject,
              'class_level': node.classLevel,
            }),
          },
          conflictAlgorithm: ConflictAlgorithm.replace,
        );
      }
    }

    await batch.commit(noResult: true);
    debugPrint('Search Engine: Indexed ${nodes.length} nodes with hybrid search support.');
  }

  /// Performs a hybrid search across keyword and semantic indices.
  Future<List<Map<String, dynamic>>> search(String query, {int? classLevel, String? subject}) async {
    final db = await _db.database;

    // 1. Keyword Search
    String ftsSql = 'SELECT *, 1.0 as score FROM search_index WHERE search_index MATCH ?';
    List<dynamic> ftsArgs = [query];

    if (classLevel != null) {
      ftsSql += ' AND class_level = ?';
      ftsArgs.add(classLevel.toString());
    }
    if (subject != null) {
      ftsSql += ' AND subject = ?';
      ftsArgs.add(subject);
    }

    final ftsResults = await db.rawQuery(ftsSql, ftsArgs);

    // 2. Semantic Search
    final queryVector = await _ai.generateEmbeddings(query);
    List<Map<String, dynamic>> semanticResults = [];

    if (queryVector.isNotEmpty) {
      final allEmbeddings = await db.query('embeddings');
      for (final row in allEmbeddings) {
        final blob = row['vector'] as Uint8List;
        final vector = blob.buffer.asFloat32List();

        final similarity = _cosineSimilarity(queryVector, vector);
        if (similarity > 0.7) { // Threshold
           final metadata = jsonDecode(row['metadata'] as String);
           // Filter by class/subject if provided
           if (classLevel != null && metadata['class_level'] != classLevel) continue;
           if (subject != null && metadata['subject'] != subject) continue;

           semanticResults.add({
             'node_id': row['node_id'],
             'title': metadata['title'],
             'subject': metadata['subject'],
             'class_level': metadata['class_level'].toString(),
             'score': similarity,
             'source': 'semantic'
           });
        }
      }
    }

    // 3. Hybrid Ranking (Simple merger)
    final Map<String, Map<String, dynamic>> hybridMap = {};

    for (final r in ftsResults) {
      final id = r['node_id'].toString();
      hybridMap[id] = Map<String, dynamic>.from(r);
    }

    for (final r in semanticResults) {
      final id = r['node_id'].toString();
      if (hybridMap.containsKey(id)) {
        // Boost score if found in both
        hybridMap[id]!['score'] = (hybridMap[id]!['score'] as double) + (r['score'] as double);
      } else {
        hybridMap[id] = r;
      }
    }

    final sortedResults = hybridMap.values.toList()
      ..sort((a, b) => (b['score'] as num).compareTo(a['score'] as num));

    return sortedResults;
  }

  double _cosineSimilarity(List<double> v1, Float32List v2) {
    double dotProduct = 0;
    double normA = 0;
    double normB = 0;
    for (int i = 0; i < v1.length; i++) {
      dotProduct += v1[i] * v2[i];
      normA += v1[i] * v1[i];
      normB += v2[i] * v2[i];
    }
    if (normA == 0 || normB == 0) return 0;
    return dotProduct / (sqrt(normA) * sqrt(normB));
  }
}
