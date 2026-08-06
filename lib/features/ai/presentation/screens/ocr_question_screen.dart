import 'dart:io';
import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/di/injection.dart';
import '../../data/ocr_service.dart';
import '../../data/ai_tutor_service.dart';
import '../../../curriculum/domain/models/concept_node.dart';
import '../../../curriculum/domain/models/mastery.dart';
import 'ai_tutor_chat_screen.dart';

class OcrQuestionScreen extends StatefulWidget {
  final ConceptNode? currentConcept; // Optional, AI can try to identify
  final Mastery? currentMastery;

  const OcrQuestionScreen({super.key, this.currentConcept, this.currentMastery});

  @override
  State<OcrQuestionScreen> createState() => _OcrQuestionScreenState();
}

class _OcrQuestionScreenState extends State<OcrQuestionScreen> {
  final ImagePicker _picker = ImagePicker();
  String? _imagePath;
  String _recognizedText = "";
  bool _isProcessing = false;

  Future<void> _pickImage(ImageSource source) async {
    final XFile? image = await _picker.pickImage(source: source);
    if (image != null) {
      setState(() {
        _imagePath = image.path;
        _isProcessing = true;
      });

      final text = await sl<OcrService>().recognizeText(image.path);

      setState(() {
        _recognizedText = text;
        _isProcessing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Scan Question')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            if (_imagePath != null)
              Container(
                height: 200,
                width: double.infinity,
                decoration: BoxDecoration(
                  border: Border.all(color: Colors.grey),
                  image: DecorationImage(
                    image: FileImage(File(_imagePath!)),
                    fit: BoxFit.cover,
                  ),
                ),
              )
            else
              Container(
                height: 200,
                width: double.infinity,
                color: Colors.grey[200],
                child: const Icon(Icons.camera_alt, size: 50, color: Colors.grey),
              ),
            const SizedBox(height: 20),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                ElevatedButton.icon(
                  onPressed: () => _pickImage(ImageSource.camera),
                  icon: const Icon(Icons.camera),
                  label: const Text('Camera'),
                ),
                ElevatedButton.icon(
                  onPressed: () => _pickImage(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library),
                  label: const Text('Gallery'),
                ),
              ],
            ),
            const SizedBox(height: 20),
            if (_isProcessing)
              const CircularProgressIndicator()
            else if (_recognizedText.isNotEmpty)
              Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Text('Recognized Text:', style: TextStyle(fontWeight: FontWeight.bold)),
                  const SizedBox(height: 8),
                  TextFormField(
                    initialValue: _recognizedText,
                    maxLines: 5,
                    decoration: const InputDecoration(border: OutlineInputBorder()),
                    onChanged: (val) => _recognizedText = val,
                  ),
                  const SizedBox(height: 20),
                  ElevatedButton(
                    onPressed: () {
                      // Navigate to AI Tutor with this text
                      if (widget.currentConcept != null && widget.currentMastery != null) {
                         Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => AiTutorChatScreen(
                              concept: widget.currentConcept!,
                              mastery: widget.currentMastery!,
                              initialQuery: _recognizedText,
                            ),
                          ),
                        );
                      } else {
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(content: Text('Please select a topic first.')),
                        );
                      }
                    },
                    style: ElevatedButton.styleFrom(
                      minimumSize: const Size(double.infinity, 50),
                      backgroundColor: Colors.deepPurple,
                      foregroundColor: Colors.white,
                    ),
                    child: const Text('Ask Gurukul AI about this'),
                  ),
                ],
              ),
          ],
        ),
      ),
    );
  }
}
