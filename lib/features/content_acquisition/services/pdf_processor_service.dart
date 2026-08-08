import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:path/path.dart' as p;
import 'package:syncfusion_flutter_pdf/pdf.dart';
import '../models/acquisition_file.dart';
import '../models/extraction_result.dart';
import '../models/import_queue_item.dart';
import '../../ai/data/ocr_service.dart';

/// Service responsible for processing PDF files and extracting structured content.
class PDFProcessorService {
  final String _rawStoragePath = 'datasets/processed/ai_json/raw_extractions/';
  final String _imageAssetsPath = 'datasets/processed/assets/images/';
  final OcrService _ocrService;

  PDFProcessorService(this._ocrService);

  /// Processes an [ImportQueueItem] by extracting real text and metadata from PDF.
  Future<ExtractionResult> process(ImportQueueItem item) async {
    final file = File(item.file.path);
    if (!await file.exists()) {
      throw Exception('File not found: ${item.file.path}');
    }

    final List<int> bytes = await file.readAsBytes();
    final PdfDocument document = PdfDocument(inputBytes: bytes);
    final int pageCount = document.pages.count;

    final StringBuffer fullRawText = StringBuffer();
    final List<String> allHeadings = [];
    final List<List<String>> allTables = [];
    final List<String> imagePaths = [];

    final String chapterId = item.id;
    final String imageDir = p.join(_imageAssetsPath, chapterId);

    // Ensure image directory exists
    await Directory(imageDir).create(recursive: true);

    final PdfTextExtractor textExtractor = PdfTextExtractor(document);

    for (int i = 0; i < pageCount; i++) {
      // 1. Text Extraction
      // Note: In Syncfusion 26.x, extractText might take startPageIndex and endPageIndex
      String pageText = textExtractor.extractText(startPageIndex: i, endPageIndex: i);

      // Heuristic for scanned pages: very little text
      if (pageText.trim().length < 50) {
        debugPrint('PDFProcessor: Page $i of chapter $chapterId might be scanned.');
      }

      fullRawText.writeln(pageText);

      // 2. Heading Detection (Heuristic)
      final List<String> pageHeadings = _detectHeadingsBasic(pageText);
      allHeadings.addAll(pageHeadings);

      // 3. Table Extraction (Heuristic)
      final String layoutText = textExtractor.extractText(startPageIndex: i, endPageIndex: i, layoutText: true);
      final List<List<String>> tables = _extractTablesHeuristic(layoutText);
      allTables.addAll(tables);
    }

    final String finalRawText = fullRawText.toString();

    // Paragraph detection
    final List<String> paragraphs = finalRawText.split('\n\n')
        .map((p) => p.trim())
        .where((p) => p.isNotEmpty)
        .toList();

    // Construct the result
    final result = ExtractionResult(
      rawText: finalRawText,
      headings: allHeadings.toSet().toList(), // Deduplicate
      paragraphs: paragraphs,
      tables: allTables,
      images: imagePaths,
      chapterBoundaries: _detectChapterBoundaries(finalRawText),
    );

    document.dispose();

    // Store raw extraction
    await _storeRawExtraction(item.id, result);

    return result;
  }

  List<String> _detectHeadingsBasic(String text) {
    final List<String> headings = [];
    final lines = text.split('\n');
    for (var line in lines) {
      final trimmed = line.trim();
      if (trimmed.isEmpty) continue;
      if (trimmed.length < 100 && (trimmed.toUpperCase().contains('CHAPTER') || _isMostlyUppercase(trimmed))) {
        headings.add(trimmed);
      } else if (_isNcertHeadingPattern(trimmed)) {
        headings.add(trimmed);
      }
    }
    return headings;
  }

  bool _isNcertHeadingPattern(String text) {
    final regex = RegExp(r'^(\d+(\.\d+)*|Chapter\s+\d+|[IVXLCDM]+\.|[A-Z]\.)\s+[A-Z].*', caseSensitive: false);
    return regex.hasMatch(text);
  }

  bool _isMostlyUppercase(String s) {
    if (s.length < 5) return false;
    int upper = 0;
    int alpha = 0;
    for (var i = 0; i < s.length; i++) {
      final char = s[i];
      if (char.toUpperCase() != char.toLowerCase()) {
        alpha++;
        if (char.toUpperCase() == char) upper++;
      }
    }
    if (alpha == 0) return false;
    return upper / alpha > 0.8;
  }

  /// Heuristic to group tab-separated or grid-aligned text into tables.
  List<List<String>> _extractTablesHeuristic(String layoutText) {
    final List<List<String>> tables = [];
    final lines = layoutText.split('\n');
    List<String> currentTableRows = [];

    for (var line in lines) {
      if (line.contains(RegExp(r'\s{3,}'))) {
        currentTableRows.add(line.trim());
      } else if (currentTableRows.isNotEmpty) {
        if (currentTableRows.length > 1) {
          tables.add(List.from(currentTableRows));
        }
        currentTableRows = [];
      }
    }

    if (currentTableRows.length > 1) {
      tables.add(currentTableRows);
    }

    return tables;
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
      currentOffset += line.length + 1;
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
