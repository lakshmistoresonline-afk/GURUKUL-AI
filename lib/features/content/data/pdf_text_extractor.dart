import 'dart:io';
import 'package:syncfusion_flutter_pdf/pdf.dart';

class PdfTextExtractor {
  Future<String> extractText(String filePath) async {
    try {
      final File file = File(filePath);
      final List<int> bytes = await file.readAsBytes();
      final PdfDocument document = PdfDocument(inputBytes: bytes);

      String text = PdfTextExtractor().extractTextFromDocument(document);
      document.dispose();
      return text;
    } catch (e) {
      return 'Error extracting text: $e';
    }
  }

  String extractTextFromDocument(PdfDocument document) {
    PdfTextExtractor extractor = PdfTextExtractor();
    // This is a bit recursive in name, but Syncfusion's PdfTextExtractor
    // is a class we use on the document.
    return PdfTextExtractor().extractTextFromDocument(document);
  }
}
