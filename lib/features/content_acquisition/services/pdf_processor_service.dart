import 'dart:convert';
import 'dart:io';
import 'package:path/path.dart' as p;
import 'package:syncfusion_flutter_pdf/pdf.dart';
import '../models/acquisition_file.dart';
import '../models/extraction_result.dart';
import '../models/import_queue_item.dart';

/// Service responsible for processing PDF files and extracting structured content.
class PDFProcessorService {
  final String _rawStoragePath = 'datasets/processed/ai_json/raw_extractions/';

  /// Processes an [ImportQueueItem] by extracting real text and metadata from PDF.
  Future<ExtractionResult> process(ImportQueueItem item) async {
    final file = File(item.file.path);
    if (!await file.exists()) {
      throw Exception('File not found: ${item.file.path}');
    }

    final List<int> bytes = await file.readAsBytes();
    final PdfDocument document = PdfDocument(inputBytes: bytes);
    final PdfTextExtractor extractor = PdfTextExtractor(document);

    final String rawText = extractor.extractText();
    // final int pageCount = document.pages.count;

    // Headings detection (simple heuristic for now: uppercase lines or specific patterns)
    final List<String> headings = _detectHeadings(rawText);

    // Paragraph detection
    final List<String> paragraphs = rawText.split('\n\n').where((p) => p.trim().isNotEmpty).toList();

    // Construct the result
    final result = ExtractionResult(
      rawText: rawText,
      headings: headings,
      paragraphs: paragraphs,
      tables: [], // Advanced table extraction needed
      images: [], // Advanced image extraction needed
      chapterBoundaries: _detectChapterBoundaries(rawText),
    );

    document.dispose();

    // Store raw extraction
    await _storeRawExtraction(item.id, result);

    return result;
  }

  List<String> _detectHeadings(String text) {
    final List<String> headings = [];
    final lines = text.split('\n');
    for (var line in lines) {
      final trimmed = line.trim();
      if (trimmed.isEmpty) continue;
      if (trimmed.length < 100 && (trimmed.toUpperCase().contains('CHAPTER') || _isMostlyUppercase(trimmed))) {
        headings.add(trimmed);
      }
    }
    return headings;
  }

  bool _isMostlyUppercase(String s) {
    if (s.length < 5) return false;
    int upper = 0;
    for (var i = 0; i < s.length; i++) {
      if (s[i].toUpperCase() == s[i] && s[i].toLowerCase() != s[i]) upper++;
    }
    return upper / s.length > 0.8;
  }

  /// Detects chapter boundaries based on character offsets where "Chapter" appears.
  List<int> _detectChapterBoundaries(String text) {
    final List<int> boundaries = [];
    final lines = text.split('\n');
    int currentOffset = 0;

    for (var line in lines) {
      if (line.toUpperCase().contains('CHAPTER')) {
        boundaries.add(currentOffset);
      }
      currentOffset += line.length + 1; // +1 for the newline character
    }

    if (boundaries.isEmpty || boundaries.first != 0) {
      boundaries.insert(0, 0);
    }

    return boundaries;
  }

  /// Stores the raw extraction data as a JSON file for future reference.
  Future<void> _storeRawExtraction(String id, ExtractionResult result) async {
    try {
      final directory = Directory(_rawStoragePath);
      if (!await directory.exists()) {
        await directory.create(recursive: true);
      }

      final file = File(p.join(_rawStoragePath, '$id.json'));
      final jsonContent = jsonEncode(result.toJson());
      await file.writeAsString(jsonContent);
    } catch (e) {
      stderr.writeln('Failed to store raw extraction for $id: $e');
    }
  }
}
