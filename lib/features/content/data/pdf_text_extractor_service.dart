import 'dart:io';
import 'package:syncfusion_flutter_pdf/pdf.dart';

class PdfTextExtractorService {
  Future<String> extractText(String filePath) async {
    try {
      final File file = File(filePath);
      final List<int> bytes = await file.readAsBytes();
      final PdfDocument document = PdfDocument(inputBytes: bytes);

      // Use Syncfusion's extractor
      final String text = PdfTextExtractor(document).extractText();

      document.dispose();
      return text;
    } catch (e) {
      return 'Error extracting text: $e';
    }
  }
}
