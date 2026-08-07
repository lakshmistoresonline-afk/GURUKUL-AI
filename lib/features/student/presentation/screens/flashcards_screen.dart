import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class FlashcardsScreen extends StatelessWidget {
  final String subject;
  final String? chapterId;

  const FlashcardsScreen({super.key, required this.subject, this.chapterId});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: DesignSystem.background,
      appBar: AppBar(
        title: const Text('Smart Flashcards'),
        backgroundColor: DesignSystem.background,
        elevation: 0,
      ),
      body: Column(
        children: [
          const SizedBox(height: DesignSystem.spacingLg),
          _buildFlashcardView(),
          const SizedBox(height: DesignSystem.spacingXl),
          _buildControls(),
          const Spacer(),
          _buildStats(),
          const SizedBox(height: DesignSystem.spacingXl),
        ],
      ),
    );
  }

  Widget _buildFlashcardView() {
    return Center(
      child: Container(
        width: 300,
        height: 400,
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(DesignSystem.radiusLg),
          boxShadow: DesignSystem.shadowLg,
          border: Border.all(color: DesignSystem.primary.withValues(alpha: 0.2)),
        ),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Icon(Icons.style_rounded, color: DesignSystem.primary, size: 64),
            const SizedBox(height: DesignSystem.spacingLg),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingLg),
              child: Text(
                'What is the fundamental unit of life?',
                textAlign: TextAlign.center,
                style: DesignSystem.h2.copyWith(fontSize: 22),
              ),
            ),
            const SizedBox(height: DesignSystem.spacingXl),
            Text('TAP TO REVEAL', style: DesignSystem.label.copyWith(color: DesignSystem.primary)),
          ],
        ),
      ),
    );
  }

  Widget _buildControls() {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        _buildActionButton(Icons.close, Colors.red, 'Hard'),
        const SizedBox(width: DesignSystem.spacingLg),
        _buildActionButton(Icons.sentiment_neutral, Colors.orange, 'Okay'),
        const SizedBox(width: DesignSystem.spacingLg),
        _buildActionButton(Icons.check, Colors.green, 'Easy'),
      ],
    );
  }

  Widget _buildActionButton(IconData icon, Color color, String label) {
    return Column(
      children: [
        CircleAvatar(
          radius: 30,
          backgroundColor: color.withValues(alpha: 0.1),
          child: Icon(icon, color: color, size: 30),
        ),
        const SizedBox(height: 8),
        Text(label, style: DesignSystem.label.copyWith(color: color)),
      ],
    );
  }

  Widget _buildStats() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: DesignSystem.spacingXl),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          _StatInfo('Mastered', '12', Colors.green),
          _StatInfo('To Review', '45', Colors.orange),
          _StatInfo('New', '103', Colors.blue),
        ],
      ),
    );
  }

  Widget _StatInfo(String label, String value, Color color) {
    return Column(
      children: [
        Text(value, style: DesignSystem.h2.copyWith(color: color)),
        Text(label, style: DesignSystem.bodySmall),
      ],
    );
  }
}
