import 'package:google_mlkit_text_recognition/google_mlkit_text_recognition.dart';

class OcrService {
  final TextRecognizer _textRecognizer = TextRecognizer(script: TextRecognitionScript.latin);

  Future<String> recognizeText(String imagePath) async {
    final inputImage = InputImage.fromFilePath(imagePath);
    final RecognizedText recognizedText = await _textRecognizer.processImage(inputImage);

    String text = recognizedText.text;

    // Simple post-processing: remove extra newlines and trim
    text = text.replaceAll('\n', ' ').trim();

    return text;
  }

  void dispose() {
    _textRecognizer.close();
  }
}
