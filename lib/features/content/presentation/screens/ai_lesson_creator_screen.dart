import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import '../../../../core/di/injection.dart';
import '../../data/pdf_text_extractor_service.dart';
import '../../data/ai_content_factory.dart';
import '../../../curriculum/presentation/screens/learning_journey_screen.dart';

class AiLessonCreatorScreen extends StatefulWidget {
  const AiLessonCreatorScreen({super.key});

  @override
  State<AiLessonCreatorScreen> createState() => _AiLessonCreatorScreenState();
}

class _AiLessonCreatorScreenState extends State<AiLessonCreatorScreen> {
  bool _isProcessing = false;
  String _status = 'Select a PDF textbook chapter to generate an AI lesson.';
  double _progress = 0;

  Future<void> _pickAndProcess() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf'],
    );

    if (result == null || result.files.single.path == null) return;

    setState(() {
      _isProcessing = true;
      _status = 'Extracting text from PDF...';
      _progress = 0.2;
    });

    try {
      final text = await PdfTextExtractorService().extractText(result.files.single.path!);

      setState(() {
        _status = 'Analyzing with Gemini AI...';
        _progress = 0.5;
      });

      final factory = sl<AiContentFactory>();
      final lesson = await factory.createLessonFromText(
        text: text,
        subject: 'Science', // Example
        classLevel: 6,
        chapterTitle: result.files.single.name.replaceAll('.pdf', ''),
      );

      if (lesson != null && mounted) {
        setState(() {
          _status = 'Lesson Generated Successfully!';
          _progress = 1.0;
          _isProcessing = false;
        });

        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('AI Lesson Ready!')),
        );

        Navigator.push(
          context,
          MaterialPageRoute(builder: (_) => LearningJourneyScreen(concept: lesson)),
        );
      } else {
        setState(() {
          _status = 'Failed to generate lesson. Please try again.';
          _isProcessing = false;
        });
      }
    } catch (e) {
      setState(() {
        _status = 'Error: $e';
        _isProcessing = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Lesson Creator')),
      body: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.auto_awesome, size: 80, color: Colors.blue),
            const SizedBox(height: 32),
            const Text(
              'PDF to Interactive Lesson',
              style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 16),
            Text(
              _status,
              textAlign: TextAlign.center,
              style: TextStyle(color: Colors.grey.shade600),
            ),
            const SizedBox(height: 48),
            if (_isProcessing)
              Column(
                children: [
                  LinearProgressIndicator(value: _progress),
                  const SizedBox(height: 16),
                  const Text('Processing... This may take a minute.'),
                ],
              )
            else
              ElevatedButton.icon(
                onPressed: _pickAndProcess,
                icon: const Icon(Icons.upload_file),
                label: const Text('Upload PDF Chapter'),
                style: ElevatedButton.styleFrom(
                  padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
                  textStyle: const TextStyle(fontSize: 18),
                ),
              ),
            const SizedBox(height: 24),
            const Text(
              'Supported: NCERT/CBSE Textbooks (English/Hindi)',
              style: TextStyle(fontSize: 12, color: Colors.grey),
            ),
          ],
        ),
      ),
    );
  }
}
