import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/features/content/data/pdf_text_extractor_service.dart';
import 'package:project_gurukul_ai/features/content/data/ai_content_factory.dart';
import 'package:project_gurukul_ai/core/di/injection.dart';
import 'package:file_picker/file_picker.dart';

class ImportWizardScreen extends StatefulWidget {
  const ImportWizardScreen({super.key});

  @override
  State<ImportWizardScreen> createState() => _ImportWizardScreenState();
}

class _ImportWizardScreenState extends State<ImportWizardScreen> {
  int _currentStep = 0;
  String? _filePath;
  String? _fileName;
  bool _isProcessing = false;
  String _status = 'Select a PDF to begin.';

  Future<void> _pickFile() async {
    final result = await FilePicker.platform.pickFiles(
      type: FileType.custom,
      allowedExtensions: ['pdf', 'docx', 'txt'],
    );

    if (result != null && result.files.single.path != null) {
      setState(() {
        _filePath = result.files.single.path;
        _fileName = result.files.single.name;
        _currentStep = 1;
      });
    }
  }

  Future<void> _startProcessing() async {
    setState(() {
      _isProcessing = true;
      _status = 'Extracting and analyzing...';
    });

    try {
      // Logic from Phase 47
      final text = await PdfTextExtractorService().extractText(_filePath!);
      final factory = sl<AiContentFactory>();
      final lesson = await factory.createLessonFromText(
        text: text,
        subject: 'General',
        classLevel: 6,
        chapterTitle: _fileName!.replaceAll('.pdf', ''),
      );

      if (lesson != null) {
        setState(() {
          _isProcessing = false;
          _currentStep = 2;
          _status = 'Successfully generated structured lesson!';
        });
      } else {
        throw Exception('AI failed to parse content.');
      }
    } catch (e) {
      setState(() {
        _isProcessing = false;
        _status = 'Error: $e';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Curriculum Import Wizard')),
      body: Stepper(
        currentStep: _currentStep,
        onStepContinue: () {
          if (_currentStep == 0) _pickFile();
          if (_currentStep == 1) _startProcessing();
          if (_currentStep == 2) Navigator.pop(context);
        },
        onStepCancel: () {
          if (_currentStep > 0) setState(() => _currentStep--);
        },
        steps: [
          Step(
            title: const Text('Upload Document'),
            content: Column(
              children: [
                const Icon(Icons.upload_file, size: 64, color: Colors.blue),
                const SizedBox(height: 16),
                const Text('Select an NCERT textbook chapter PDF or Word document.'),
                if (_fileName != null)
                   Padding(
                     padding: const EdgeInsets.only(top: 8.0),
                     child: Text('Selected: $_fileName', style: const TextStyle(fontWeight: FontWeight.bold)),
                   ),
              ],
            ),
            isActive: _currentStep >= 0,
          ),
          Step(
            title: const Text('AI Analysis'),
            content: Column(
              children: [
                if (_isProcessing)
                  const CircularProgressIndicator()
                else
                  const Icon(Icons.psychology, size: 64, color: Colors.purple),
                const SizedBox(height: 16),
                Text(_status),
              ],
            ),
            isActive: _currentStep >= 1,
          ),
          Step(
            title: const Text('Review & Publish'),
            content: Column(
              children: [
                const Icon(Icons.verified, size: 64, color: Colors.green),
                const SizedBox(height: 16),
                const Text('Content is ready for Studio review.'),
                TextButton(onPressed: () {}, child: const Text('Preview in Content Studio')),
              ],
            ),
            isActive: _currentStep >= 2,
          ),
        ],
      ),
    );
  }
}
