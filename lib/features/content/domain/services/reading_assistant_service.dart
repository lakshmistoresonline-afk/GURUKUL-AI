import 'package:flutter_tts/flutter_tts.dart';

class ReadingAssistantService {
  final FlutterTts _tts = FlutterTts();
  bool _isPlaying = false;

  Future<void> speak(String text, String language) async {
    await _tts.setLanguage(language == 'hi' ? 'hi-IN' : 'en-IN');
    await _tts.setPitch(1.0);
    await _tts.setSpeechRate(0.5);

    _isPlaying = true;
    await _tts.speak(text);
  }

  Future<void> stop() async {
    await _tts.stop();
    _isPlaying = false;
  }

  bool get isPlaying => _isPlaying;

  void setHandlers({
    required Function(String text, int start, int end, String word) onProgress,
  }) {
    _tts.setProgressHandler((text, start, end, word) {
      onProgress(text, start, end, word);
    });

    _tts.setCompletionHandler(() {
      _isPlaying = false;
    });
  }
}
