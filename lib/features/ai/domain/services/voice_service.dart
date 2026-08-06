import 'package:speech_to_text/speech_to_text.dart';
import 'package:flutter_tts/flutter_tts.dart';

class VoiceService {
  final SpeechToText _stt = SpeechToText();
  final FlutterTts _tts = FlutterTts();

  Future<bool> init() async {
    bool hasStt = await _stt.initialize();
    await _tts.setLanguage("en-IN");
    await _tts.setSpeechRate(0.5);
    return hasStt;
  }

  Future<void> startListening(Function(String) onResult) async {
    await _stt.listen(onResult: (res) => onResult(res.recognizedWords));
  }

  Future<void> stopListening() async {
    await _stt.stop();
  }

  Future<void> speak(String text) async {
    await _tts.speak(text);
  }

  Future<void> stopSpeaking() async {
    await _tts.stop();
  }
}
