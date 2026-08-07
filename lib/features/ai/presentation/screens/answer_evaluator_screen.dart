import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import '../../../../core/di/injection.dart';
import '../../data/ai_tutor_service.dart';
import '../../data/ocr_service.dart';

class AnswerEvaluatorScreen extends StatefulWidget {
  const AnswerEvaluatorScreen({super.key});

  @override
  State<AnswerEvaluatorScreen> createState() => _AnswerEvaluatorScreenState();
}

class _AnswerEvaluatorScreenState extends State<AnswerEvaluatorScreen> {
  final ImagePicker _picker = ImagePicker();
  bool _isProcessing = false;
  String? _ocrText;
  Map<String, dynamic>? _evaluation;

  Future<void> _pickImage(ImageSource source) async {
    final XFile? image = await _picker.pickImage(source: source);
    if (image == null) return;

    setState(() {
      _isProcessing = true;
      _evaluation = null;
    });

    try {
      final ocrText = await sl<OcrService>().recognizeText(image.path);
      setState(() => _ocrText = ocrText);

      // In a real flow, you'd have the question and model answer
      final evaluation = await sl<AiTutorService>().evaluateAnswer(
        question: "Explain the Water Cycle.",
        studentAnswer: ocrText,
        modelAnswer: "The water cycle is the continuous movement of water within the Earth and atmosphere. It involves processes like evaporation, condensation, and precipitation.",
      );

      setState(() {
        _evaluation = evaluation;
        _isProcessing = false;
      });
    } catch (e) {
      setState(() => _isProcessing = false);
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('AI Answer Evaluator')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            _buildUploadSection(),
            const SizedBox(height: 32),
            if (_isProcessing)
              const Center(child: CircularProgressIndicator())
            else if (_evaluation != null)
              _buildResultSection()
            else if (_ocrText != null)
               _buildOcrPreview(),
          ],
        ),
      ),
    );
  }

  Widget _buildUploadSection() {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(24),
        child: Column(
          children: [
            const Icon(Icons.camera_alt, size: 48, color: Colors.blue),
            const SizedBox(height: 16),
            const Text('Upload your Handwritten Answer', style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
            const SizedBox(height: 24),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                FilledButton.icon(
                  onPressed: () => _pickImage(ImageSource.camera),
                  icon: const Icon(Icons.photo_camera),
                  label: const Text('Camera'),
                ),
                const SizedBox(width: 12),
                OutlinedButton.icon(
                  onPressed: () => _pickImage(ImageSource.gallery),
                  icon: const Icon(Icons.photo_library),
                  label: const Text('Gallery'),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildOcrPreview() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text('Recognized Text:', style: TextStyle(fontWeight: FontWeight.bold)),
        const SizedBox(height: 8),
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(color: Colors.grey.shade100, borderRadius: BorderRadius.circular(8)),
          child: Text(_ocrText!),
        ),
      ],
    );
  }

  Widget _buildResultSection() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Divider(height: 48),
        const Text('AI Evaluation', style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold)),
        const SizedBox(height: 16),
        Container(
          padding: const EdgeInsets.all(20),
          decoration: BoxDecoration(color: Colors.green.shade50, borderRadius: BorderRadius.circular(16)),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Score: 4.5 / 5', style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold, color: Colors.green)),
              const SizedBox(height: 12),
              Text(_evaluation?['rawResponse'] ?? 'Excellent attempt! Your explanation covers the main points well.', style: const TextStyle(fontSize: 15)),
            ],
          ),
        ),
        const SizedBox(height: 24),
        _buildFeedbackItem(Icons.check_circle, 'Strong Points', 'Clear definition, used correct terms like evaporation.'),
        _buildFeedbackItem(Icons.tips_and_updates, 'Suggestions', 'Try to mention "transpiration" from plants for extra marks.'),
      ],
    );
  }

  Widget _buildFeedbackItem(IconData icon, String title, String content) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, size: 20, color: Colors.blue),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(title, style: const TextStyle(fontWeight: FontWeight.bold)),
                Text(content, style: const TextStyle(color: Colors.black54)),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
