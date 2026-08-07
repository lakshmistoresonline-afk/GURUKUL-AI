import 'package:flutter/material.dart';
import 'package:project_gurukul_ai/core/theme/design_system.dart';

class FillBlanksActivity extends StatefulWidget {
  final String sentence; // Example: "The ____ rises in the ____."
  final List<String> correctAnswers; // ["Sun", "East"]
  final List<String> distractors; // ["Moon", "West"]
  final Function(bool) onComplete;

  const FillBlanksActivity({
    super.key,
    required this.sentence,
    required this.correctAnswers,
    required this.distractors,
    required this.onComplete,
  });

  @override
  State<FillBlanksActivity> createState() => _FillBlanksActivityState();
}

class _FillBlanksActivityState extends State<FillBlanksActivity> {
  late List<String?> _userAnswers;
  late List<String> _options;

  @override
  void initState() {
    super.initState();
    _userAnswers = List.filled(widget.correctAnswers.length, null);
    _options = [...widget.correctAnswers, ...widget.distractors]..shuffle();
  }

  @override
  Widget build(BuildContext context) {
    List<String> parts = widget.sentence.split('____');

    return Column(
      children: [
        Wrap(
          crossAxisAlignment: WrapCrossAlignment.center,
          children: List.generate(parts.length + _userAnswers.length, (index) {
            if (index % 2 == 0) {
              return Text(parts[index ~/ 2], style: const TextStyle(fontSize: 18));
            } else {
              int blankIndex = index ~/ 2;
              return DragTarget<String>(
                onAccept: (data) => setState(() => _userAnswers[blankIndex] = data),
                builder: (context, candidateData, rejectedData) => Container(
                  width: 80,
                  height: 30,
                  margin: const EdgeInsets.symmetric(horizontal: 8),
                  decoration: BoxDecoration(
                    border: Border(bottom: BorderSide(color: DesignSystem.primary, width: 2)),
                    color: _userAnswers[blankIndex] != null ? DesignSystem.primary.withOpacity(0.1) : Colors.transparent,
                  ),
                  child: Center(child: Text(_userAnswers[blankIndex] ?? '', style: const TextStyle(fontWeight: FontWeight.bold))),
                ),
              );
            }
          }),
        ),
        const SizedBox(height: 48),
        Wrap(
          spacing: 12,
          runSpacing: 12,
          children: _options.map((opt) => Draggable<String>(
            data: opt,
            feedback: _buildOption(opt, true),
            childWhenDragging: Opacity(opacity: 0.3, child: _buildOption(opt, false)),
            child: _buildOption(opt, false),
          )).toList(),
        ),
        const Spacer(),
        FilledButton(
          onPressed: _userAnswers.contains(null) ? null : () {
            bool allCorrect = true;
            for(int i=0; i<_userAnswers.length; i++) {
              if (_userAnswers[i] != widget.correctAnswers[i]) allCorrect = false;
            }
            widget.onComplete(allCorrect);
          },
          child: const Text('Check Answers'),
        ),
      ],
    );
  }

  Widget _buildOption(String text, bool isFeedback) {
    return Material(
      color: Colors.transparent,
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: BoxDecoration(
          color: DesignSystem.surface,
          borderRadius: BorderRadius.circular(20),
          border: Border.all(color: Colors.grey.shade300),
          boxShadow: isFeedback ? DesignSystem.shadowMd : null,
        ),
        child: Text(text, style: const TextStyle(fontWeight: FontWeight.w500)),
      ),
    );
  }
}
